from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, update, delete
from sqlalchemy.orm import InstrumentedAttribute

from app.domain.repositories.base_repository import BaseRepository
from app.infrastructure.persistence.sqlalchemy.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

class SQLAlchemyBaseRepository(BaseRepository[ModelType], Generic[ModelType]):
    """通用仓储SQLAlchemy实现"""

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, entity: ModelType) -> ModelType:
        """创建实体"""
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        """根据ID获取实体"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """获取所有实体"""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def filter_by(self, **kwargs) -> List[ModelType]:
        """根据条件过滤实体"""
        filters = []
        for key, value in kwargs.items():
            field_name, *modifiers = key.split("__")
            column = getattr(self.model, field_name, None)
            if not column:
                continue

            if not modifiers:
                filters.append(column == value)
            elif modifiers[0] == "like":
                filters.append(column.like(f"%{value}%"))
            elif modifiers[0] == "in":
                filters.append(column.in_(value))
            elif modifiers[0] == "isnull":
                if value:
                    filters.append(column.is_(None))
                else:
                    filters.append(column.is_not(None))
            elif modifiers[0] == "gte":
                filters.append(column >= value)
            elif modifiers[0] == "lte":
                filters.append(column <= value)

        result = await self.session.execute(
            select(self.model).where(and_(*filters))
        )
        return list(result.scalars().all())

    async def update(self, id: str, **updates) -> Optional[ModelType]:
        """更新实体"""
        # 使用update语句更新
        stmt = update(self.model).where(self.model.id == id).values(**updates)
        await self.session.execute(stmt)
        await self.session.commit()
        
        # 返回更新后的实体
        return await self.get_by_id(id)

    async def delete(self, id: str) -> bool:
        """删除实体"""
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def count(self) -> int:
        """统计数量"""
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()