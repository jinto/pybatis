"""
테스트용 픽스처들

README.md 예시에 맞는 UserRepository 등을 포함합니다.
"""

from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    """사용자 모델"""

    id: int
    name: str
    email: str
    is_active: bool


class UserRepository:
    """README.md 예시의 UserRepository"""

    def __init__(self, db):
        self.db = db

    async def count_active(self, active: bool) -> int:
        """
        활성 사용자 수를 반환합니다.
        """
        sql = "SELECT COUNT(*) FROM users WHERE is_active = :active"
        # fetch_val: 단일 스칼라 값을 바로 리턴
        return await self.db.fetch_val(sql, params={"active": active})

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        주어진 ID의 사용자 한 명을 User 모델로 반환합니다.
        """
        sql = "SELECT id, name, email, is_active FROM users WHERE id = :user_id"
        row = await self.db.fetch_one(sql, params={"user_id": user_id})
        return User(**row) if row else None

    async def get_users_by_activity(self, active_status: bool) -> List[User]:
        """
        활성 상태에 따라 사용자 목록을 User 모델 리스트로 반환합니다.
        """
        sql = (
            "SELECT id, name, email, is_active FROM users "
            "WHERE is_active = :active_status"
        )
        rows = await self.db.fetch_all(sql, params={"active_status": active_status})
        return [User(**r) for r in rows]
