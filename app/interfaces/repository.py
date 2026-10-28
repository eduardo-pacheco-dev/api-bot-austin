from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Any

T = TypeVar("T")
CreateSchema = TypeVar("CreateSchema")
UpdateSchema = TypeVar("UpdateSchema")


class BaseRepository(ABC, Generic[T, CreateSchema, UpdateSchema]):
    @abstractmethod
    def create(self, obj_in: CreateSchema) -> T:
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        **filters: Any,
    ) -> tuple[list[T], int]:
        pass

    @abstractmethod
    def update(self, id: int, obj_in: UpdateSchema) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
