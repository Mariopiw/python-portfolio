from abc import ABC, abstractmethod
from harness.models import AttackCase, TargetResponse

class TargetAdapter(ABC):
    @abstractmethod
    def prepare_case(self, case: AttackCase) -> None:
        ...

    @abstractmethod
    def execute(self, case: AttackCase) -> TargetResponse:
        ...
