from abc import ABCMeta, abstractmethod

from matplotlib import axes


class Plotter(metaclass=ABCMeta):
    @abstractmethod
    def plot(self, ax: axes.Axes) -> None:
        raise NotImplementedError
