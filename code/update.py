"""This file deals with versioning and updating the game's elements."""

import os
import shutil
import requests
from tempfile import mkdtemp
from code.functions import set_seq_length


class Version:
    def __init__(self, major: int, minor: int, patch: int, prerelease: str = ""):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.pre = prerelease

    def __repr__(self):
        return f"Version(major={self.major}, minor={self.minor}, patch={self.patch}, prerelease={self.pre})" \
            if self.pre else f"Version(major={self.major}, minor={self.minor}, patch={self.patch})"

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}" + (f"-{self.pre}" if self.pre else "")

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch and self.pre == other.pre

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch
        if not self.pre:
            return False
        if not other.pre:
            return True
        return self.pre < other.pre

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __iter__(self):
        return iter((self.major, self.minor, self.patch, self.pre) if self.pre else (self.major, self.minor, self.patch))

    @classmethod
    def from_str(cls, string: str):
        """Converts a string that looks like 'v1.0.3-beta' into a Version object.
        If the version has '+...' in it, it will be ignored.
        The 'v' at the beginning of the version is not mandatory and will be ignored."""
        string = string.lower()  # "V1.3-Beta+Win" -> "v1.3-beta+win"
        if string[0] == "v":
            string = string[1:]  # "v1.3-beta+win" -> "1.3-beta+win"
        temp = string.split("+", 1)[0].split("-", 1)  # "1.3-beta+win" -> ["1.3", "beta"]
        return cls(*set_seq_length(map(int, temp[0].split(".")), 0, 3),  # "1.3" -> [1, 3, 0]
                   prerelease=temp[1] if len(temp) > 1 else "")

    def shorten_str(self, level: int) -> str:
        """Shortens the version to the specified level as such:
        1: v1.0.3-beta -> v1
        2: v1.0.3-beta -> v1.0
        3: v1.0.3-beta -> v1.0.3
        Any other: v1.0.3-beta -> v1.0.3-beta"""
        if level == 1:
            return f"v{self.major}.{self.minor}.{self.patch}"
        if level == 2:
            return f"v{self.major}.{self.minor}"
        if level == 3:
            return f"v{self.major}"
        return str(self)


class Updater:
    """Class that handles the version checking and updating of the game."""

    def __init__(self, current_version: Version):
        self.current = current_version
        self.latest = None
        self.temp_dir = None

    def check_updates(self, accept_prerelease: bool = False) -> bool:
        """Checks for updates in the releases on the game's GitHub repository.
        Returns True if one is available, or False if no update has been found or if the check failed."""
        response = requests.get(self.URL)
        if response.ok:
            data = [el for el in response.json() if Version.from_str(el["tag_name"]) > self.current]
            if not accept_prerelease:
                data = [el for el in data if not el["prerelease"]]
            if data:
                self.latest = data[0]
                return True
        return False

    def install_update(self) -> bool:
        """Installs the latest update available.
        Returns True if the update has been successfully installed, and False otherwise."""
        if self.latest is None and not self.check_updates():
            return False
        self.temp_dir = mkdtemp()
        self.__download_pkg()
        self.__replace_files()
        shutil.rmtree(self.temp_dir)
        self.temp_dir = None
        return True

    def __download_pkg(self) -> int:
        """Downloads the update package to the temporary folder. Returns the downloaded package's size."""
        if self.temp_dir is None:
            raise ValueError("the temporary directory has not been created.")
        with open(self.temp_dir + "/update.zip", "wb") as file:
            size = file.write(requests.get(self.latest["zipball_url"], allow_redirects=True).content)
        shutil.unpack_archive(self.temp_dir + "/update.zip", self.temp_dir)
        return size

    def __replace_files(self, game_dir: str = os.getcwd()):
        if self.temp_dir is None:
            raise ValueError("the temporary directory has not been created.")
        """Completely removes the current game files."""
        for el in os.listdir(game_dir):
            if os.path.isfile(el):
                os.remove(el)
            else:
                shutil.rmtree(el)
        commit = os.listdir(self.temp_dir)[0]
        for el in os.listdir(f"{self.temp_dir}/{commit}"):
            shutil.move(f"{self.temp_dir}/{commit}/{el}", f"{game_dir}/{el}")

    URL = "https://api.github.com/repos/Eraldorure/the-last-space-fighter/releases"


if __name__ == '__main__':
    updater = Updater(Version.from_str("v0.0.1"))
    if updater.check_updates():
        print(f"Release {updater.latest['tag_name']} is available.")
    elif updater.check_updates(True):
        print(f"Pre-release {updater.latest['tag_name']} is available.")
    else:
        print("No update available.")
