"""
pyBatis Core 모듈의 테스트

이 파일은 pyBatis의 핵심 기능들을 테스트합니다.
"""

import pytest
from typing import List, Optional
from pydantic import BaseModel

from pybatis.core import PyBatisMapper, SqlSession, sql_query, sql_update, sql_select


class MockUser(BaseModel):
    """테스트용 사용자 모델"""
    id: int
    name: str
    email: str


class MockSqlSession(SqlSession):
    """테스트용 SQL 세션 구현"""

    def __init__(self):
        self.executed_sql = []
        self.executed_parameters = []
        self.mock_data = {}

    async def execute(self, sql: str, parameters: Optional[dict] = None) -> int:
        """SQL 실행을 모킹합니다."""
        self.executed_sql.append(sql)
        self.executed_parameters.append(parameters)
        return 1  # 영향받은 행 수

    async def fetch_one(self, sql: str, parameters: Optional[dict] = None) -> Optional[dict]:
        """하나의 레코드 조회를 모킹합니다."""
        self.executed_sql.append(sql)
        self.executed_parameters.append(parameters)

        # 모킹된 사용자 데이터 반환
        if "SELECT" in sql and "users" in sql:
            return {"id": 1, "name": "테스트사용자", "email": "test@example.com"}
        return None

    async def fetch_all(self, sql: str, parameters: Optional[dict] = None) -> List[dict]:
        """모든 레코드 조회를 모킹합니다."""
        self.executed_sql.append(sql)
        self.executed_parameters.append(parameters)

        # 모킹된 사용자 리스트 반환
        if "SELECT" in sql and "users" in sql:
            return [
                {"id": 1, "name": "사용자1", "email": "user1@example.com"},
                {"id": 2, "name": "사용자2", "email": "user2@example.com"},
            ]
        return []

    async def commit(self) -> None:
        """커밋을 모킹합니다."""
        pass

    async def rollback(self) -> None:
        """롤백을 모킹합니다."""
        pass

    async def close(self) -> None:
        """세션 닫기를 모킹합니다."""
        pass


class TestPyBatisMapper:
    """PyBatisMapper 클래스의 테스트"""

    @pytest.fixture
    def session(self):
        """테스트용 세션 픽스처"""
        return MockSqlSession()

    @pytest.fixture
    def mapper(self, session):
        """테스트용 매퍼 픽스처"""
        return PyBatisMapper(session)

    @pytest.mark.asyncio
    async def test_select_one_without_type(self, mapper, session):
        """타입 없이 하나의 레코드 조회 테스트"""
        sql = "SELECT * FROM users WHERE id = :id"
        result = await mapper.select_one(sql, {"id": 1})

        assert result is not None
        assert result["id"] == 1
        assert result["name"] == "테스트사용자"
        assert sql in session.executed_sql

    @pytest.mark.asyncio
    async def test_select_one_with_type(self, mapper, session):
        """타입 지정하여 하나의 레코드 조회 테스트"""
        sql = "SELECT * FROM users WHERE id = :id"
        result = await mapper.select_one(sql, {"id": 1}, MockUser)

        assert isinstance(result, MockUser)
        assert result.id == 1
        assert result.name == "테스트사용자"
        assert result.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_select_list_without_type(self, mapper, session):
        """타입 없이 여러 레코드 조회 테스트"""
        sql = "SELECT * FROM users"
        result = await mapper.select_list(sql)

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    @pytest.mark.asyncio
    async def test_select_list_with_type(self, mapper, session):
        """타입 지정하여 여러 레코드 조회 테스트"""
        sql = "SELECT * FROM users"
        result = await mapper.select_list(sql, None, MockUser)

        assert len(result) == 2
        assert all(isinstance(user, MockUser) for user in result)
        assert result[0].id == 1
        assert result[1].id == 2

    @pytest.mark.asyncio
    async def test_insert(self, mapper, session):
        """INSERT 테스트"""
        sql = "INSERT INTO users (name, email) VALUES (:name, :email)"
        parameters = {"name": "새사용자", "email": "new@example.com"}

        result = await mapper.insert(sql, parameters)

        assert result == 1
        assert sql in session.executed_sql
        assert parameters in session.executed_parameters

    @pytest.mark.asyncio
    async def test_update(self, mapper, session):
        """UPDATE 테스트"""
        sql = "UPDATE users SET name = :name WHERE id = :id"
        parameters = {"name": "수정된이름", "id": 1}

        result = await mapper.update(sql, parameters)

        assert result == 1
        assert sql in session.executed_sql
        assert parameters in session.executed_parameters

    @pytest.mark.asyncio
    async def test_delete(self, mapper, session):
        """DELETE 테스트"""
        sql = "DELETE FROM users WHERE id = :id"
        parameters = {"id": 1}

        result = await mapper.delete(sql, parameters)

        assert result == 1
        assert sql in session.executed_sql
        assert parameters in session.executed_parameters


class TestDecorators:
    """데코레이터 함수들의 테스트"""

    @pytest.fixture
    def session(self):
        """테스트용 세션 픽스처"""
        return MockSqlSession()

    @pytest.fixture
    def mapper(self, session):
        """테스트용 매퍼 픽스처"""
        return PyBatisMapper(session)

    @pytest.mark.asyncio
    async def test_sql_query_decorator(self, mapper):
        """sql_query 데코레이터 테스트"""

        @sql_query("SELECT * FROM users WHERE id = :id", MockUser)
        async def get_user_by_id(mapper_instance, id: int) -> Optional[MockUser]:
            pass

        result = await get_user_by_id(mapper, id=1)

        assert isinstance(result, MockUser)
        assert result.id == 1
        assert hasattr(get_user_by_id, '_sql')
        assert get_user_by_id._sql == "SELECT * FROM users WHERE id = :id"

    @pytest.mark.asyncio
    async def test_sql_update_decorator(self, mapper):
        """sql_update 데코레이터 테스트"""

        @sql_update("INSERT INTO users (name, email) VALUES (:name, :email)")
        async def create_user(mapper_instance, name: str, email: str) -> int:
            pass

        result = await create_user(mapper, name="테스트", email="test@example.com")

        assert result == 1
        assert hasattr(create_user, '_sql')

    @pytest.mark.asyncio
    async def test_sql_select_decorator(self, mapper):
        """sql_select 데코레이터 테스트 (sql_query의 별칭)"""

        @sql_select("SELECT * FROM users", MockUser)
        async def get_all_users(mapper_instance) -> List[MockUser]:
            pass

        result = await get_all_users(mapper)

        assert len(result) == 2
        assert all(isinstance(user, MockUser) for user in result)
        assert hasattr(get_all_users, '_sql')


class TestIntegration:
    """통합 테스트"""

    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """전체 워크플로우 테스트"""
        session = MockSqlSession()
        mapper = PyBatisMapper(session)

        # 사용자 생성
        await mapper.insert(
            "INSERT INTO users (name, email) VALUES (:name, :email)",
            {"name": "통합테스트", "email": "integration@example.com"}
        )

        # 사용자 조회
        user = await mapper.select_one(
            "SELECT * FROM users WHERE id = :id",
            {"id": 1},
            MockUser
        )

        # 사용자 목록 조회
        users = await mapper.select_list(
            "SELECT * FROM users",
            None,
            MockUser
        )

        assert isinstance(user, MockUser)
        assert len(users) == 2
        assert len(session.executed_sql) == 3