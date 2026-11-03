import abc
import secrets


class VerificationCodeGenerator(abc.ABC):
    @abc.abstractmethod
    def create_code(self) -> str:
        pass


class RandomVerificationCodeGenerator(VerificationCodeGenerator):
    length: int = 8

    def create_code(self) -> str:
        # Generate a random zero-padded numeric verification code of the specified length
        return f"{secrets.randbelow(10**self.length):0{self.length}d}"
