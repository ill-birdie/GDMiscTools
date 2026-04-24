from functools import cached_property
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import lineStyles


class Chokepoints:
    def __init__(self, attempts: dict[int, int]) -> None:
        death_percents = {percent: 0 for percent in range(1, 101)}
        death_percents.update(attempts)

        # Avoids division-by-zero errors when calculating the regression equation
        if 0 in death_percents:
            death_percents.pop(0)

        self._x = np.arange(1, 101, 1)
        self._y = np.array(list(death_percents.values()))
        fit = np.polyfit(np.log(self._x), self._y, deg=1)

        # Regression equation is a*ln(x) + b
        self._a_fit, self._b_fit = fit[1], fit[0]

    @cached_property
    def fit(self) -> str:
        return f"{round(self._a_fit, 3)} + {round(self._b_fit, 3)}ln(x)"

    def expected(self, percent) -> float:
        return self._a_fit + self._b_fit*np.log(percent)

    @cached_property
    def expected_y(self):
        return [max(0.0, self.expected(percent)) for percent in range(1, 101)]

    def graph(self) -> None:
        plt.plot(self._x, self._y, color="orange")
        plt.plot(self._x, self.expected_y, color="blue", ls="--", alpha=0.7)
        plt.show()