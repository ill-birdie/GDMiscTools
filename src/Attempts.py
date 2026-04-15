from pathlib import Path


class Attempts:
    def __init__(self, level_name=None) -> None:
        self._curr_dir = Path.home() / "IdeaProjects" / "GeometryDash" / "src"
        self._name = level_name

        # Helper functions insert data into from_zero and runs
        self._from_zero = {}
        self.parse_from_zero()
        self._runs = {}
        self.parse_runs()
        self._total = self._from_zero | self._runs

        # These variables cache the amount of attempts in from_zero, runs, and the two combined
        self._from_zero_count = sum(self._from_zero.values())
        self._runs_count = sum(self._runs.values())
        self._total_count = self._from_zero_count + self._runs_count

    def __str__(self) -> str:
        return f"AttemptHelper object {f"for level {self._name}" if self._name is not None else f"with {self._total_count} attempts"}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def from_zero(self) -> dict[int, int]:
        return self._from_zero

    @property
    def runs(self) -> dict[tuple, int]:
        return self._runs

    @property
    def total(self) -> dict[int | tuple, int]:
        return self._total

    @property
    def from_zero_count(self) -> int:
        return self._from_zero_count

    @property
    def runs_count(self) -> int:
        return self._runs_count

    @property
    def total_count(self) -> int:
        return self._total_count


    def parse_from_zero(self) -> None:
        """
        Function goes line-by-line through "FromZero.txt" to add entries into self._from_zero
        :return: None
        """
        path = self._curr_dir / "FromZero.txt"
        if not path.exists():
            print(f'File not found: "{path.name}"')
            return

        with open(path, mode="r") as file:
            for line in file:
                if "%" in line:
                    # The format of each line is "{percent}% x{num_deaths}" (ex. 5% x10)
                    # Removes the space and the "%" in line
                    line = line.strip().replace("%", " ").replace(" ", "")

                    # String now in the format "{percent}x{num_deaths}" (ex. 5x10)
                    # Splits line across "x" into a list of integers
                    line = [int(n) for n in line.split("x")]
                    percent, num_deaths = line[0], line[1]

                    # Inserts data in the format "{percent}: {num_deaths}" (ex. {5: 10})
                    self._from_zero[percent] = num_deaths


    def parse_runs(self) -> None:
        """
        Function goes line-by-line through "Runs.txt" to add entries into self._runs
        :return: None
        """
        path = self._curr_dir / "Runs.txt"
        if not path.exists():
            print(f'File not found: "{path.name}"')
            return

        with open(path, mode="r") as file:
            for line in file:
                if "-" in line:
                    # The format of each line is "{run_start}% - {run_end}% x{num_deaths}" (ex. 5% - 25% x10)
                    # Removes the "-", the "x", and all instances of spaces, in line
                    line = line.strip().replace("x", " ").replace("-", " ").replace(" ", "")

                    # String now in the format "{run_start}%{run_end}%{num_deaths}" (ex. 5%25%10)
                    # Splits line across instances of "%" into a list of integers
                    line = [int(n) for n in line.split("%")]
                    run_start, run_end, num_deaths = line[0], line[1], line[2]

                    # Inserts data in the format "{({run_start}, {run_end}): {num_deaths})}" (ex. {(5, 25): 10})
                    self._runs[(run_start, run_end)] = num_deaths