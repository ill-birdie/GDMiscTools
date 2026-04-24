import numpy as np
import matplotlib.pyplot as plt

class Chokepoints:
    def __init__(self, attempts: dict[int, int]) -> None:
        death_percents = {percent: 0 for percent in range(1, 101)}
        death_percents.update(attempts)

        # Avoids division-by-zero errors when calculating the regression equation
        if 0 in death_percents:
            death_percents.pop(0)

        self._x, self._y = np.arange(1, 101, 1), np.array(list(death_percents.values()))
        fit = np.polyfit(np.log(self._x), self._y, deg=1)

        # Regression equation is a*ln(x) + b
        self._a_fit, self._b_fit = fit[1], fit[0]

    @property
    def fit(self) -> str:
        return f"{round(self._a_fit, 3)} + {round(self._b_fit, 3)}ln(x)"

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def expected(self, percent) -> float:
        return self._a_fit + self._b_fit*np.log(percent)

    def graph(self) -> None:
        plt.plot(self._x, self._y)
        expected_x = np.arange(1, 101, 1)
        expected_y = [max(0.0, self.expected(n)) for n in np.arange(1, 101, 1)]
        plt.plot(expected_x, expected_y)
        plt.show()