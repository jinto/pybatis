"""
pyBatis Core Module

이 모듈은 pyBatis의 핵심 기능을 제공합니다:
- SQL 매퍼 클래스
- SQL 실행을 위한 세션 관리
- SQL 정의를 위한 데코레이터들
"""

import logging
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

from fastapi import Depends
from pydantic import BaseModel

# 타입 힌트를 위한 제네릭 타입 변수
T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)


class SqlSession(ABC):
    """SQL 세션을 관리하는 추상 클래스"""

    @abstractmethod
    async def execute(
        self, sql: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """SQL을 실행합니다."""
        pass

    @abstractmethod
    async def fetch_one(
        self, sql: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """하나의 레코드를 조회합니다."""
        pass

    @abstractmethod
    async def fetch_all(
        self, sql: str, parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """모든 레코드를 조회합니다."""
        pass

    @abstractmethod
    async def commit(self) -> None:
        """트랜잭션을 커밋합니다."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """트랜잭션을 롤백합니다."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """세션을 닫습니다."""
        pass


class PyBatisMapper:
    """pyBatis의 메인 매퍼 클래스"""

    def __init__(self, session: SqlSession):
        self.session = session

    async def select_one(
        self,
        sql: str,
        parameters: Optional[Dict[str, Any]] = None,
        result_type: Optional[Type[T]] = None,
    ) -> Union[Optional[T], Optional[Dict[str, Any]]]:
        """하나의 레코드를 조회하고 지정된 타입으로 변환합니다."""
        row = await self.session.fetch_one(sql, parameters)
        if row is None:
            return None

        if result_type is not None:
            return result_type(**row)
        return row

    async def select_list(
        self,
        sql: str,
        parameters: Optional[Dict[str, Any]] = None,
        result_type: Optional[Type[T]] = None,
    ) -> Union[List[T], List[Dict[str, Any]]]:
        """여러 레코드를 조회하고 지정된 타입의 리스트로 변환합니다."""
        rows = await self.session.fetch_all(sql, parameters)

        if result_type is not None:
            return [result_type(**row) for row in rows]
        return rows

    async def insert(
        self, sql: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """INSERT 문을 실행합니다."""
        return await self.session.execute(sql, parameters)

    async def update(
        self, sql: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """UPDATE 문을 실행합니다."""
        return await self.session.execute(sql, parameters)

    async def delete(
        self, sql: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """DELETE 문을 실행합니다."""
        return await self.session.execute(sql, parameters)


def sql_query(sql: str, result_type: Optional[Type[T]] = None) -> Callable[..., Any]:
    """SQL 쿼리를 정의하는 데코레이터 (SELECT용)"""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 첫 번째 인수가 PyBatisMapper 인스턴스인지 확인
            if args and isinstance(args[0], PyBatisMapper):
                mapper = args[0]
                # 함수의 인수들을 파라미터로 사용
                parameters = kwargs if kwargs else None

                if "List" in str(func.__annotations__.get("return", "")):
                    return await mapper.select_list(sql, parameters, result_type)
                else:
                    return await mapper.select_one(sql, parameters, result_type)
            else:
                raise ValueError("첫 번째 인수는 PyBatisMapper 인스턴스여야 합니다.")

        # 원본 SQL을 함수에 저장
        setattr(wrapper, "_sql", sql)
        setattr(wrapper, "_result_type", result_type)
        return wrapper

    return decorator


def sql_update(sql: str) -> Callable[..., Any]:
    """SQL 업데이트 문을 정의하는 데코레이터 (INSERT/UPDATE/DELETE용)"""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if args and isinstance(args[0], PyBatisMapper):
                mapper = args[0]
                parameters = kwargs if kwargs else None
                return await mapper.update(sql, parameters)
            else:
                raise ValueError("첫 번째 인수는 PyBatisMapper 인스턴스여야 합니다.")

        setattr(wrapper, "_sql", sql)
        return wrapper

    return decorator


def sql_select(sql: str, result_type: Optional[Type[T]] = None) -> Callable[..., Any]:
    """SQL SELECT 문을 정의하는 데코레이터 (sql_query의 별칭)"""
    return sql_query(sql, result_type)


# FastAPI 의존성 주입을 위한 헬퍼 함수들
async def get_sql_session() -> SqlSession:
    """SQL 세션을 반환하는 의존성 함수"""
    # 실제 구현에서는 데이터베이스 연결 풀에서 세션을 가져옵니다.
    # 이는 구체적인 데이터베이스 구현에 따라 달라집니다.
    raise NotImplementedError(
        "이 함수는 구체적인 데이터베이스 구현에서 오버라이드되어야 합니다."
    )


def get_mapper(session: SqlSession = Depends(get_sql_session)) -> PyBatisMapper:
    """PyBatisMapper 인스턴스를 반환하는 의존성 함수"""
    return PyBatisMapper(session)
