from pathlib import Path
from collections import defaultdict


class Attempts:
    def __init__(self, level_name=None) -> None:
        self._curr_dir = Path.home() / "IdeaProjects" / "GeometryDash" / "src"
        self._name = level_name
        self._from_zero = {}
        self._runs = {}
        self.parse_from_zero()
        self.parse_runs()
        self._total = self._from_zero | self._runs
        self._from_zero_count = sum(self._from_zero.values())
        self._runs_count = sum(self._runs.values())
        self._total_count = self._from_zero_count + self._runs_count

    def __str__(self) -> str:
        return f"AttemptHelper object for level: {self._name}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def total(self) -> defaultdict[int, int]:
        return self._total

    @property
    def from_zero(self) -> dict:
        return self._from_zero

    @property
    def runs(self) -> dict:
        return self._runs

    @property
    def total_count(self) -> int:
        return self._total_count

    @property
    def from_zero_count(self) -> int:
        return self._from_zero_count

    @property
    def runs_count(self) -> int:
        return self._runs_count


    def parse_from_zero(self) -> None:
        path = self._curr_dir / "FromZero.txt"
        if not path.exists():
            print(f'File not found: "{path.name}"')
            return

        with open(path, mode="r") as file:
            for line in file:
                if "%" in line:
                    line = line.strip().replace("%", " ").replace(" ", "").split("x")
                    line = [int(n) for n in line]
                    percent, num_deaths = line[0], line[1]
                    self._from_zero[percent] = num_deaths

    def parse_runs(self) -> None:
        path = self._curr_dir / "Runs.txt"
        if not path.exists():
            print(f'File not found: "{path.name}"')
            return

        with open(path, mode="r") as file:
            for line in file:
                if "-" in line:
                    line = line.strip().replace("x", " ").replace("-", " ")
                    line = line.replace(" ", "").split("%")
                    line = [int(n) for n in line]
                    run_start, run_end, num_deaths = line[0], line[1], line[2]
                    self._runs[(run_start, run_end)] = num_deaths