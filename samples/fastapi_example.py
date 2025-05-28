"""
FastAPI와 pyBatis 통합 예제

이 예제는 pyBatis를 FastAPI와 함께 사용하는 방법을 보여줍니다.
주요 기능:
- 의존성 주입을 통한 PyBatis 인스턴스 관리
- Repository 패턴 구현
- 트랜잭션 관리
- 애플리케이션 생명주기 관리
"""

import os
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

# pyBatis 모듈 import
from pybatis import PyBatis
from pybatis.fastapi import (
    PyBatisManager,
    create_pybatis_dependency,
    transaction_context,
)


# Pydantic 모델 정의
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    is_active: bool = True

    class Config:
        # ORM 모드 활성화 (dict에서 직접 생성 가능)
        from_attributes = True


class UserInput(BaseModel):
    """사용자 입력용 모델 (생성/업데이트 공통)"""
    name: str
    email: str
    is_active: bool = True


# Repository 패턴 구현
class UserRepository:
    """사용자 관련 데이터베이스 작업을 담당하는 Repository"""

    def __init__(self, pybatis: PyBatis):
        self.pybatis = pybatis

    async def create_user(self, user_data: UserInput) -> User:
        """새 사용자 생성"""
        user_id = await self.pybatis.execute(
            """
            INSERT INTO users (name, email, is_active)
            VALUES (:name, :email, :is_active)
            """,
            {
                "name": user_data.name,
                "email": user_data.email,
                "is_active": user_data.is_active
            }
        )

        # 생성된 사용자 정보 반환
        user_dict = await self.pybatis.fetch_one(
            "SELECT * FROM users WHERE id = :id",
            {"id": user_id}
        )

        return User(**user_dict)

    @query("SELECT * FROM users WHERE id = :id")
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """ID로 사용자 조회"""
        user_dict = await self.pybatis.fetch_one(
            "SELECT * FROM users WHERE id = :id",
            {"id": user_id}
        )

        return User(**user_dict) if user_dict else None

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """사용자 목록 조회"""
        users_data = await self.pybatis.fetch_all(
            """
            SELECT * FROM users
            ORDER BY id
            LIMIT :limit OFFSET :skip
            """,
            {"skip": skip, "limit": limit}
        )

        return [User(**user_dict) for user_dict in users_data]

    async def update_user(self, user_id: int, user_update: UserInput) -> Optional[User]:
        """사용자 정보 업데이트"""
        affected_rows = await self.pybatis.execute(
            """
            UPDATE users
            SET name = :name, email = :email, is_active = :is_active
            WHERE id = :id
            """,
            {
                "id": user_id,
                "name": user_update.name,
                "email": user_update.email,
                "is_active": user_update.is_active
            }
        )

        if affected_rows == 0:
            return None

        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id: int) -> bool:
        """사용자 삭제"""
        affected_rows = await self.pybatis.execute(
            "DELETE FROM users WHERE id = :id",
            {"id": user_id}
        )

        return affected_rows > 0

    async def get_active_users_count(self) -> int:
        """활성 사용자 수 조회"""
        count = await self.pybatis.fetch_val(
            "SELECT COUNT(*) FROM users WHERE is_active = :is_active",
            {"is_active": True}
        )

        return count


# PyBatis 매니저 설정 및 의존성 함수 생성
manager = PyBatisManager(dsn="sqlite:///example.db")
get_pybatis = create_pybatis_dependency(manager)


async def get_user_repository(
    pybatis: PyBatis = Depends(get_pybatis)
) -> UserRepository:
    """Repository 의존성 함수"""
    return UserRepository(pybatis)


# 애플리케이션 생명주기 관리
@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 리소스 관리"""
    # 시작 시: 데이터베이스 테이블 생성
    async with manager.get_pybatis() as pybatis:
        await pybatis.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)

    yield

    # 종료 시: 리소스 정리
    await manager.close()


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="pyBatis FastAPI 예제",
    description="pyBatis와 FastAPI 통합 예제 애플리케이션",
    version="1.0.0",
    lifespan=lifespan
)


# API 엔드포인트 정의
@app.post("/users/", response_model=User)
async def create_user(
    user_data: UserInput,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """새 사용자 생성"""
    # 생성 시 필수 필드 검증
    if not user_data.name or not user_data.email:
        raise HTTPException(
            status_code=400,
            detail="name과 email은 필수 필드입니다"
        )

    try:
        return await user_repo.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """사용자 조회"""
    user = await user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user


@app.get("/users/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """사용자 목록 조회"""
    return await user_repo.get_users(skip=skip, limit=limit)


@app.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserInput,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """사용자 정보 업데이트"""
    user = await user_repo.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user


@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """사용자 삭제"""
    success = await user_repo.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return {"message": "사용자가 삭제되었습니다"}


@app.get("/users/stats/active-count")
async def get_active_users_count(
    user_repo: UserRepository = Depends(get_user_repository)
):
    """활성 사용자 수 조회"""
    count = await user_repo.get_active_users_count()
    return {"active_users_count": count}


# 트랜잭션 사용 예제
@app.post("/users/batch/", response_model=List[User])
async def create_users_batch(
    users_data: List[UserInput],
    pybatis: PyBatis = Depends(get_pybatis)
):
    """여러 사용자를 트랜잭션으로 일괄 생성"""
    # 모든 사용자 데이터의 필수 필드 검증
    for i, user_data in enumerate(users_data):
        if not user_data.name or not user_data.email:
            raise HTTPException(
                status_code=400,
                detail=f"사용자 {i+1}번: name과 email은 필수 필드입니다"
            )

    created_users = []

    try:
        async with transaction_context(pybatis) as tx:
            user_repo = UserRepository(tx)

            for user_data in users_data:
                user = await user_repo.create_user(user_data)
                created_users.append(user)

            # 모든 사용자가 성공적으로 생성되면 커밋
            return created_users

    except Exception as e:
        # 오류 발생 시 자동으로 롤백됨
        raise HTTPException(
            status_code=400,
            detail=f"사용자 일괄 생성 중 오류 발생: {str(e)}"
        )


# 헬스 체크 엔드포인트
@app.get("/health")
async def health_check(pybatis: PyBatis = Depends(get_pybatis)):
    """애플리케이션 상태 확인"""
    try:
        # 간단한 쿼리로 데이터베이스 연결 확인
        result = await pybatis.fetch_val("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "test_query_result": result
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn

    # 개발 서버 실행
    uvicorn.run(
        "fastapi_example:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )