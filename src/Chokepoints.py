import numpy as np
import matplotlib.pyplot as plt


class Chokepoints:
    def __init__(self, attempts: dict[int, int]) -> None:
        # Avoids division by zero when calculating for the weight of each percent
        if not attempts:
            raise TypeError("No attempts listed")

        self._pass_rates = {}
        self._avg_pass_rate = 0.0
        death_total = sum(attempts.values())
        reached = death_total
        for percent, deaths in attempts.items():
            passed = reached - deaths
            pass_rate = (passed / reached) * 100
            weight = deaths / death_total
            self._avg_pass_rate += pass_rate*weight
            self._pass_rates[percent] = pass_rate
            reached = passed

    @property
    def pass_rates(self) -> dict[int, tuple]:
        return self._pass_rates

    @property
    def avg_pass_rate(self) -> float:
        return self._avg_pass_rate