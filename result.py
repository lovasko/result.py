from typing import TypeVar
from typing import Generic
from typing import GenericMeta
from typing import Callable

# Declare type variables for success and failure types.
S = TypeVar('S')
F = TypeVar('F')

# Declare type variable 
R = TypeVar('R')


# Result of a computation that represents success.
class Success(Generic[S]):
    def show(self):
        print(str(self.value))
    
    def __init__(self, value: S):
        self.value = value

    def __add__(self, other):
        return other

# Result of a computation that represents failure.
class Failure(Generic[F]):
    def show(self):
        print(str(self.value))

    def __init__(self, value: F):
        self.value = value

    def __add__(self, other):
        return self

# Metaclass for the result type.
class ResultMeta(GenericMeta):
    pass

class Result(Generic[S, F], metaclass=ResultMeta):
    Success = Success
    Failure = Failure

def failure_rshift(self, func: Callable[[S], Result[S, F]]):
    return self

def success_rshift(self, func: Callable[[S], Result[S, F]]):
    return func(self.value)


Failure.__rshift__ = failure_rshift
Success.__rshift__ = success_rshift
Failure.and_then   = failure_rshift
Success.and_then   = success_rshift

def triple(val: int) -> Result[int, str]:
    if val > 100:
        return Result.Failure('over 100!')
    else:
        return Result.Success(val * 3)


def validate_input(name: str) -> Result[None, str]:
    if name in ["hello", "world"]:
        return Result.Success(None)
    else:
        return Result.Failure(name + ' is not a valid input!')


def query_jobs():
    succ = Result.Success(4)
    fail = Result.Failure('nooo')


    r1 = succ >> triple >> triple
    r2 = fail >> triple >> triple
    r3 = validate_input("mnah") + r1
#    r3.conclude(inform_user, log_error_to_elastic)

    r1.show()
    r2.show()
    r3.show()


query_jobs()
