import abc
import secrets


class ActivationCodeGenerator(abc.ABC):
    @abc.abstractmethod
    def create_code(self) -> str:
        pass


class RandomActivationCodeGenerator(ActivationCodeGenerator):
    length: int = 8

    def create_code(self) -> str:
        # Generate a random zero-padded numeric activation code of the specified length
        return f"{secrets.randbelow(10**self.length):0{self.length}d}"
