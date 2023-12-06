from typing import Any


class Path:
    def __init__(self, directories: tuple[str, ...] = tuple()) -> None:
        self.directories = directories

    def __contains__(self, item: Any) -> bool:
        if not isinstance(item, Path):
            return NotImplemented
        return item.path in self.path

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Path):
            return NotImplemented
        return self.path == other.path

    @property
    def path(self) -> str:
        return "/".join(self.directories)

    @property
    def name(self) -> str:
        return self.directories[-1] if self.directories else ""

    @property
    def root(self) -> str:
        return self.directories[0] if self.directories else ""

    def parent(self) -> 'Path':
        return Path(self.directories[:-1])

    def child(self, directory_name: str) -> 'Path':
        return Path((*self.directories, directory_name))


class File:
    def __init__(self, name: str, path: Path, size: int) -> None:
        self.name = name
        self.path = path
        self.size = size  # bits

    def __str__(self) -> str:
        return f"File({self.full_path}, {self.size} bits)"

    @property
    def full_path(self) -> str:
        return self.path.child(self.name).path


class Directory:
    def __init__(self, path: Path) -> None:
        self.directories: list[Directory] = []
        self.files: list[File] = []
        self.path = path

    def __str__(self) -> str:
        return f"Directory({self.path.name})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Directory):
            return NotImplemented
        return (
            self.directories == other.directories
            and self.files == other.files
            and self.path == other.path)

    @property
    def name(self) -> str:
        return self.path.name

    def print_directory(self, prefix: str = "") -> None:
        print(prefix + self.name)
        for directory in self.directories:
            directory.print_directory(prefix + "  ")
        for file in self.files:
            print("  " + prefix + file.name)

    def directory_size(self) -> int:
        bits = 0
        for directory in self.directories:
            bits += directory.directory_size()
        for file in self.files:
            bits += file.size
        return bits

    def iterative_size(self) -> int:
        bits = self.directory_size()
        for directory in self.directories:
            bits += directory.directory_size()
        return bits

    def add_file(self, name: str, path: Path, size: int) -> None:
        if not path.directories:
            self.files.append(File(name, self.path, size))
            return

        for directory in self.directories:
            if directory.name == path.root:
                directory.add_file(name, Path(path.directories[1:]), size)
                return
        raise RuntimeError("Could not create file.")

    def add_directory(self, name: str, path: Path) -> None:
        if not path.directories:
            self.directories.append(Directory(self.path.child(name)))
            return

        for directory in self.directories:
            if directory.name == path.root:
                directory.add_directory(name, Path(path.directories[1:]))
                return
        raise RuntimeError("Could not create directory.")

    def get_directories_by_max_size(self, max_size: int) -> list['Directory']:
        small_directories: list[Directory] = [self] if self.directory_size() <= max_size else []
        for directory in self.directories:
            small_directories += directory.get_directories_by_max_size(max_size)
        return small_directories

    def get_directories_by_min_size(self, min_size: int) -> list['Directory']:
        if self.directory_size() < min_size:
            return []

        directories: list[Directory] = [self]
        for directory in self.directories:
            directories += directory.get_directories_by_min_size(min_size)
        return directories


def advent7() -> None:
    with open("inputs/2022/day7.txt", "r") as file:
        commands = file.readlines()

    filesystem = Directory(Path())
    current_path = Path()
    for command in commands:
        if "$ cd" in command:
            _, _, argument = command.strip().split(" ")
            if argument == "..":
                current_path = current_path.parent()
            elif argument == "/":
                current_path = Path()
            else:
                current_path = current_path.child(argument)
        elif "$ ls" in command:
            continue
        else:
            if "dir" in command:
                _, dir_name = command.strip().split(" ")
                filesystem.add_directory(dir_name, current_path)
            else:
                size, filename = command.strip().split(" ")
                filesystem.add_file(filename, current_path, int(size))

    # part 1
    small_dirs = filesystem.get_directories_by_max_size(100000)
    print(sum(x.directory_size() for x in small_dirs))

    # part 2
    total_space = 70000000
    min_space_needed = 30000000
    minimal_size_to_delete = min_space_needed - (total_space - filesystem.directory_size())
    big_dirs = filesystem.get_directories_by_min_size(minimal_size_to_delete)
    print(min(x.directory_size() for x in big_dirs))


if __name__ == "__main__":
    advent7()
