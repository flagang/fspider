import contextvars
from typing import TypeVar, Generic, Dict

T = TypeVar('T')


class ContextManager(Generic[T]):
    def __init__(self, name):
        self.cxtvar = contextvars.ContextVar(name)

    def get(self) -> T:
        return self.cxtvar.get()

    def set(self, value: T):
        self.cxtvar.set(value)


spider = ContextManager('spider')
crawler = ContextManager('crawler')
settings = ContextManager('settings')
