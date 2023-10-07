from enum import Enum
from typing import Optional, Callable, Self

class OptionState(Enum):
    SOME = "Some"
    NONE = "None"

class Option[T]:
    def __init__(self, state: OptionState, value: Optional[T]):
        self.state = state
        self.value = value

        if state == OptionState.NONE and self.value is not None:
            raise Exception(f"Could not have None state but an actual value {self.value}")

    def is_some(self) -> bool:
        return self.state == OptionState.SOME

    def is_none(self) -> bool:
        return not self.is_some()

    def match(
        self,
        some_func: Callable[[T], any],
        none_func: Callable[None, any]

    ):
        if self.state == OptionState.SOME:
            return some_func(self.value)
        else:
            return none_func()

    def unwrap(self) -> T:

        # Safety check
        if self.is_none():
            raise Exception("Tried to unwrap a None value")

        return self.value

    def __repr__(self) -> str:
        if self.state == OptionState.NONE:
            return "NONE"
        else:
            return f"Some({self.value})"

    def some[T](value: T) -> Self:
        return Option(state = OptionState.SOME, value = value)

    def none() -> Self:
        return Option(state = OptionState.NONE, value = None)

    def __eq__(self, other: Self) -> bool:

        if self.state != other.state:
            return False

        if self.value != other.value:
            return False

        return True





