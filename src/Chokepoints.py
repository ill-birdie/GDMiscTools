import numpy as np
import matplotlib as plt

from Attempts import Attempts


class Chokepoints:
    def __init__(self, attempts: dict[int, int]) -> None:
        # Overwrites TypeError: expected non-empty vector for x
        assert attempts, "No attempts given"

        # Avoids division by zero when calculating the log regression
        attempts.pop(0)

        # Converts the attempts into numpy array local variables x and y
        x, y = np.array(list(attempts.keys())), np.array(list(attempts.values()))
        fit = np.polyfit(np.log(x), y, 1)
        self._a_fit, self._b_fit = fit[1], fit[0]

    @property
    def fit(self) -> str:
        return f"{round(self._a_fit, 3)} + {round(self._b_fit, 3)}ln(x)"

    def expected(self, percent) -> float:
        return self._a_fit + self._b_fit*np.log(percent)