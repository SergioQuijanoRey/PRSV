from result import Result
from typing import List

def return_first_user(usr_list: List[int]) -> Result[int, str]:
    if len(usr_list) == 0:
        return Result.err("List is empty so we cannot do a search")

    return Result.ok(usr_list[0])

def test_ok_chaining():
    usr_list = [2, 3, 4]

    x = return_first_user(usr_list).match(
        ok_func = lambda value: Result.ok(value * value),
        err_func = lambda err_value: Result.err(f"Failed to to do the search, reason was:\n {err_value}")
    ).match(
        ok_func = lambda value: Result.ok(value + 3),
        err_func = lambda err_value: Result.err(f"Failed to to do the increment, reason was:\n {err_value}")
    )

    assert x == Result.ok(7)

def test_err_chaining():
    usr_list = []

    x = return_first_user(usr_list).match(
        ok_func = lambda value: Result.ok(value * value),
        err_func = lambda err_value: Result.err(f"Failed to to do the search, reason was:\n{err_value}")
    ).match(
        ok_func = lambda value: Result.ok(value + 3),
        err_func = lambda err_value: Result.err(f"Failed to to do the increment, reason was:\n{err_value}")
    )

    print(x)

    expected_err_msg =  "Failed to to do the increment, reason was:\n"
    expected_err_msg += "Failed to to do the search, reason was:\n"
    expected_err_msg += "List is empty so we cannot do a search"
    assert x == Result.err(expected_err_msg)

