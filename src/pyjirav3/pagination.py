from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any, Callable, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class Paginator(Iterator[T]):
  """Sync iterator that auto-paginates through Jira API results.

  Yields individual items from paginated responses.
  """

  def __init__(
    self,
    fetch_page: Callable[[int, int], tuple[list[T], int]],
    *,
    page_size: int = 50,
  ) -> None:
    self._fetch_page = fetch_page
    self._page_size = page_size
    self._start_at = 0
    self._total: int | None = None
    self._buffer: list[T] = []
    self._buffer_index = 0
    self._exhausted = False

  def __iter__(self) -> Paginator[T]:
    return self

  def __next__(self) -> T:
    if self._buffer_index < len(self._buffer):
      item = self._buffer[self._buffer_index]
      self._buffer_index += 1
      return item

    if self._exhausted:
      raise StopIteration

    self._buffer, total = self._fetch_page(self._start_at, self._page_size)
    self._total = total
    self._buffer_index = 0
    self._start_at += len(self._buffer)

    if not self._buffer or self._start_at >= total:
      self._exhausted = True

    if not self._buffer:
      raise StopIteration

    item = self._buffer[self._buffer_index]
    self._buffer_index += 1
    return item


class AsyncPaginator(AsyncIterator[T]):
  """Async iterator that auto-paginates through Jira API results.

  Yields individual items from paginated responses.
  """

  def __init__(
    self,
    fetch_page: Callable[[int, int], Any],  # async callable
    *,
    page_size: int = 50,
  ) -> None:
    self._fetch_page = fetch_page
    self._page_size = page_size
    self._start_at = 0
    self._total: int | None = None
    self._buffer: list[T] = []
    self._buffer_index = 0
    self._exhausted = False

  def __aiter__(self) -> AsyncPaginator[T]:
    return self

  async def __anext__(self) -> T:
    if self._buffer_index < len(self._buffer):
      item = self._buffer[self._buffer_index]
      self._buffer_index += 1
      return item

    if self._exhausted:
      raise StopAsyncIteration

    self._buffer, total = await self._fetch_page(self._start_at, self._page_size)
    self._total = total
    self._buffer_index = 0
    self._start_at += len(self._buffer)

    if not self._buffer or self._start_at >= total:
      self._exhausted = True

    if not self._buffer:
      raise StopAsyncIteration

    item = self._buffer[self._buffer_index]
    self._buffer_index += 1
    return item
