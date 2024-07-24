"""This file deals with versioning and updating the game's elements."""


class Version:
    def __init__(self, major: int, minor: int, patch: int, prerelease: str = ""):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.pre = prerelease

    def __repr__(self):
        return f"Version(major={self.major}, minor={self.minor}, patch={self.patch}, prerelease={self.pre})"

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
        if string[0] == "v":
            string = string[1:]
        temp = string.split("+", 1)[0].split("-", 1)
        temp = list(map(int, temp[0].split("."))) + temp[1:]
        return Version(*temp)

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


# + class Updater coming soon
