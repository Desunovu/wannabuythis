import abc
from random import random


class ActivationCodeGenerator(abc.ABC):
    @abc.abstractmethod
    def create_code(self) -> str:
        pass


class RandomActivationCodeGenerator(ActivationCodeGenerator):
    def create_code(self) -> str:
        return str(10000000 + int(1000000000 * random()))
