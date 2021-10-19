from typing import TypeVar, AsyncIterator, Tuple

T = TypeVar('T')


async def aenumerate(asequence: AsyncIterator[T], start: int = 0) -> AsyncIterator[Tuple[int, T]]:
    n = start
    async for elem in asequence:
        yield n, elem
        n += 1
