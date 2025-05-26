#!/usr/bin/env python3
"""
SQLite와 Pydantic 모델 연동 데모

실제 SQLite 데이터베이스를 사용하여 pyBatis의 Pydantic 모델 연동을 시연합니다.
"""

import asyncio
import tempfile
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel

from pybatis import PyBatis


class User(BaseModel):
    """사용자 Pydantic 모델"""
    id: int
    name: str
    email: str
    is_active: bool


class UserRepository:
    """사용자 Repository 클래스"""

    def __init__(self, db: PyBatis):
        self.db = db

    def _convert_row_to_user_data(self, row: dict) -> dict:
        """SQLite의 boolean integer를 Python boolean으로 변환"""
        if row is None:
            return None

        user_data = dict(row)
        if "is_active" in user_data:
            user_data["is_active"] = bool(user_data["is_active"])
        return user_data

    async def create_user(self, name: str, email: str, is_active: bool = True) -> int:
        """새 사용자 생성"""
        sql = """
        INSERT INTO users (name, email, is_active)
        VALUES (:name, :email, :is_active)
        """
        result = await self.db.execute(sql, params={
            "name": name,
            "email": email,
            "is_active": is_active
        })
        return result  # SQLite에서는 lastrowid 반환

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """ID로 사용자 조회"""
        sql = "SELECT id, name, email, is_active FROM users WHERE id = :user_id"
        row = await self.db.fetch_one(sql, params={"user_id": user_id})

        if row is None:
            return None

        user_data = self._convert_row_to_user_data(row)
        return User(**user_data)

    async def get_all_users(self) -> List[User]:
        """모든 사용자 조회"""
        sql = "SELECT id, name, email, is_active FROM users ORDER BY id"
        rows = await self.db.fetch_all(sql)

        users = []
        for row in rows:
            user_data = self._convert_row_to_user_data(row)
            users.append(User(**user_data))

        return users

    async def get_active_users(self) -> List[User]:
        """활성 사용자만 조회"""
        sql = "SELECT id, name, email, is_active FROM users WHERE is_active = :active ORDER BY id"
        rows = await self.db.fetch_all(sql, params={"active": True})

        users = []
        for row in rows:
            user_data = self._convert_row_to_user_data(row)
            users.append(User(**user_data))

        return users

    async def count_users(self) -> int:
        """전체 사용자 수"""
        return await self.db.fetch_val("SELECT COUNT(*) FROM users")

    async def update_user_status(self, user_id: int, is_active: bool) -> bool:
        """사용자 활성 상태 업데이트"""
        sql = "UPDATE users SET is_active = :is_active WHERE id = :user_id"
        result = await self.db.execute(sql, params={
            "user_id": user_id,
            "is_active": is_active
        })
        return result > 0  # 영향받은 행이 있으면 True


async def main():
    """메인 데모 함수"""
    print("🚀 pyBatis SQLite + Pydantic 모델 연동 데모")
    print("=" * 50)

    # 임시 SQLite 데이터베이스 생성
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        db_path = temp_file.name

    dsn = f"sqlite:///{db_path}"

    try:
        # PyBatis 인스턴스 생성 및 연결
        async with PyBatis(dsn=dsn) as db:
            print(f"📁 임시 데이터베이스: {db_path}")

            # 테이블 생성
            await db.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            print("✅ users 테이블 생성 완료")

            # Repository 인스턴스 생성
            repo = UserRepository(db)

            # 1. 사용자 생성
            print("\n📝 사용자 생성:")
            user1_id = await repo.create_user("김철수", "kim@example.com", True)
            user2_id = await repo.create_user("이영희", "lee@example.com", True)
            user3_id = await repo.create_user("박민수", "park@example.com", False)

            print(f"   - 김철수 (ID: {user1_id})")
            print(f"   - 이영희 (ID: {user2_id})")
            print(f"   - 박민수 (ID: {user3_id}) - 비활성")

            # 2. 단일 사용자 조회 (Pydantic 모델로 반환)
            print("\n🔍 단일 사용자 조회:")
            user = await repo.get_user_by_id(1)
            if user:
                print(f"   - User 객체: {user}")
                print(f"   - 타입: {type(user)}")
                print(f"   - 이름: {user.name}")
                print(f"   - 이메일: {user.email}")
                print(f"   - 활성 상태: {user.is_active}")

            # 3. 모든 사용자 조회 (Pydantic 모델 리스트로 반환)
            print("\n📋 모든 사용자 조회:")
            all_users = await repo.get_all_users()
            for user in all_users:
                status = "활성" if user.is_active else "비활성"
                print(f"   - {user.name} ({user.email}) - {status}")

            # 4. 활성 사용자만 조회
            print("\n✅ 활성 사용자만 조회:")
            active_users = await repo.get_active_users()
            for user in active_users:
                print(f"   - {user.name} ({user.email})")

            # 5. 사용자 수 조회
            total_count = await repo.count_users()
            print(f"\n📊 전체 사용자 수: {total_count}")

            # 6. 사용자 상태 업데이트
            print("\n🔄 박민수 활성화:")
            updated = await repo.update_user_status(3, True)
            if updated:
                print("   - 상태 업데이트 성공")

                # 업데이트 후 다시 조회
                updated_user = await repo.get_user_by_id(3)
                if updated_user:
                    status = "활성" if updated_user.is_active else "비활성"
                    print(f"   - 업데이트된 상태: {updated_user.name} - {status}")

            # 7. 최종 활성 사용자 목록
            print("\n🎉 최종 활성 사용자 목록:")
            final_active_users = await repo.get_active_users()
            for user in final_active_users:
                print(f"   - {user.name} ({user.email})")

            print(f"\n✨ 총 {len(final_active_users)}명의 활성 사용자")

    finally:
        # 임시 파일 정리
        Path(db_path).unlink(missing_ok=True)
        print(f"\n🗑️  임시 데이터베이스 파일 삭제: {db_path}")

    print("\n🎊 데모 완료!")


if __name__ == "__main__":
    asyncio.run(main())