import numpy as np
import matplotlib.pyplot as plt

class Chokepoints:
    def __init__(self, attempts: dict[int, int]) -> None:
        # Avoids division by zero when calculating the log regression
        if 0 in attempts:
            attempts.pop(0)

        # TODO: all x values from 1 to 100 should be included, not just the one where deaths took place
        try:
            self._x, self._y = np.array(list(attempts.keys())), np.array(list(attempts.values()))
            fit = np.polyfit(np.log(self._x), self._y, 1)
        except ValueError:
            raise TypeError("Attempt data must be purely runs from zero. Maybe the wrong data was inserted?")
        except TypeError:
            raise TypeError("Attempt data must contain at least one death entry.")

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