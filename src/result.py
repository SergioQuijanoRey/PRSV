from enum import Enum
from option import Option
from typing import Optional, Callable, Self, List

class ResultState(Enum):
    OK = "Ok"
    ERROR = "Error"

class Result[TOK, TERR]:
    def __init__(self, state: ResultState, ok_value: Option[TOK], err_value: Option[TERR]):
        self.state = state
        self.ok_value = ok_value
        self.err_value = err_value

        self.__validate()

    def __validate(self):

        if self.state == ResultState.OK:
            if self.ok_value.is_none():
                raise Exception("Result is ok but has no ok value")
            if self.err_value.is_some():
                raise Exception("Result is ok but has err value")

        if self.state == ResultState.ERROR:
            if self.ok_value.is_some():
                raise Exception("Result is err but has ok value")
            if self.err_value.is_none():
                raise Exception("Result is err but has no err value")



    def ok(value: TOK) -> Self:
        return Result(
            state = ResultState.OK,
            ok_value = Option.some(value),
            err_value = Option.none()
        )

    def err(err: TERR) -> Self:
        return Result(
            state = ResultState.ERROR,
            ok_value = Option.none(),
            err_value = Option.some(err),
        )


    def match(self, ok_func: Callable[TOK, ...], err_func: Callable[TERR, ...]):
        if self.state == ResultState.OK:
            return ok_func(self.ok_value.unwrap())
        return err_func(self.err_value.unwrap())

    def __repr__(self) -> str:
        if self.state == ResultState.OK:
            return f"Ok({self.ok_value.unwrap()})"

        return f"Error({self.err_value.unwrap()})"

    def __eq__(self, other: Self) -> bool:

        if self.state != other.state:
            return False

        if self.ok_value != other.ok_value:
            return False

        if self.err_value != other.err_value:
            return False

        return True

