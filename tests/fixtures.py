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

    def _convert_row_to_user_data(self, row: dict) -> dict:
        """
        데이터베이스 행을 User 모델에 맞는 데이터로 변환합니다.
        SQLite에서 boolean이 integer로 저장되는 문제를 해결합니다.
        """
        if row is None:
            return None

        user_data = dict(row)
        # SQLite에서 boolean은 integer로 저장되므로 변환
        if "is_active" in user_data:
            user_data["is_active"] = bool(user_data["is_active"])
        return user_data

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

        if row is None:
            return None

        user_data = self._convert_row_to_user_data(row)
        return User(**user_data)

    async def get_users_by_activity(self, active_status: bool) -> List[User]:
        """
        활성 상태에 따라 사용자 목록을 User 모델 리스트로 반환합니다.
        """
        sql = (
            "SELECT id, name, email, is_active FROM users "
            "WHERE is_active = :active_status"
        )
        rows = await self.db.fetch_all(sql, params={"active_status": active_status})

        users = []
        for row in rows:
            user_data = self._convert_row_to_user_data(row)
            users.append(User(**user_data))

        return users
