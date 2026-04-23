from functools import cached_property
from pathlib import Path


class Attempts:
    def __init__(self, level_name=None) -> None:
        self._curr_dir = Path.home() / "IdeaProjects" / "GeometryDash" / "src"
        self.name = level_name

        self._from_zero = {}
        self._runs = {}
        from_zero_path = self._curr_dir / "FromZero.txt"
        runs_path = self._curr_dir / "Runs.txt"
        self.iter_file(from_zero_path, is_run=False)
        self.iter_file(runs_path, is_run=True)

    def __str__(self) -> str:
        return f"AttemptHelper object {f"for level {self.name}" if self.name is not None else f"with {self.total_count} attempts"}"

    @property
    def name(self) -> str:
        return self.name

    @name.setter
    def name(self, new_name) -> None:
        self.name_ = new_name

    @property
    def from_zero(self) -> dict[int, int]:
        return self._from_zero

    @property
    def runs(self) -> dict[tuple, int]:
        return self._runs

    @cached_property
    def total(self) -> dict[int | tuple, int]:
        return self._from_zero | self._runs

    @cached_property
    def from_zero_count(self) -> int:
        return sum(self._from_zero.values())

    @cached_property
    def runs_count(self) -> int:
        return sum(self._runs.values())

    @cached_property
    def total_count(self) -> int:
        return self.from_zero_count + self.runs_count

    def iter_file(self, path: Path, is_run: bool) -> None:
        if not path.exists():
            raise FileNotFoundError(f"File not found at {path}")

        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if is_run:
                    if "-" in line:
                        # The format of each line is "{run_start}% - {run_end}% x{num_deaths}" (ex. 5% - 25% x10)
                        line = line.replace("x", " ").replace("-", " ").replace(" ", "")

                        # String now in the format "{run_start}%{run_end}%{num_deaths}" (ex. 5%25%10)
                        line = [int(n) for n in line.split("%")]
                        run_start, run_end, num_deaths = line[0], line[1], line[2]

                        # Inserts data in the format "{({run_start}, {run_end}): {num_deaths})}" (ex. {(5, 25): 10})
                        self._runs[(run_start, run_end)] = num_deaths
                else:
                    if "%" in line:
                        # The format of each line is "{percent}% x{num_deaths}" (ex. 5% x10)
                        line = line.replace("%", " ").replace(" ", "")

                        # String now in the format "{percent}x{num_deaths}" (ex. 5x10)
                        line = [int(n) for n in line.split("x")]
                        percent, num_deaths = line[0], line[1]

                        # Inserts data in the format "{percent}: {num_deaths}" (ex. {5: 10})
                        self._from_zero[percent] = num_deaths