"""
PyBatis 메인 클래스

README.md에서 제시한 API를 구현합니다.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class PyBatis:
    """
    pyBatis의 메인 클래스

    DSN을 통해 데이터베이스에 연결하고,
    fetch_val, fetch_one, fetch_all, execute 메서드를 제공합니다.
    """

    def __init__(self, dsn: Optional[str] = None):
        """
        PyBatis 인스턴스를 초기화합니다.

        Args:
            dsn: 데이터베이스 연결 문자열 (예: "postgresql://user:pass@localhost:5432/mydb")
        """
        self.dsn = dsn
        self._connection = None

    async def connect(self) -> None:
        """
        데이터베이스에 연결합니다.
        실제 구현에서는 DSN을 파싱하여 적절한 드라이버로 연결합니다.
        """
        if self.dsn is None:
            raise ValueError("DSN이 설정되지 않았습니다.")

        # 실제 구현에서는 DSN을 파싱하여 적절한 데이터베이스 드라이버 사용
        # 예: asyncpg, aiomysql, aiosqlite 등
        logger.info(f"데이터베이스 연결 중: {self.dsn}")

        # 현재는 NotImplementedError를 발생시킵니다.
        # 실제 구현 시에는 각 데이터베이스 드라이버에 맞는 연결 로직을 구현합니다.
        raise NotImplementedError(
            "실제 데이터베이스 연결은 구체적인 드라이버 구현에서 제공됩니다."
        )

    async def fetch_val(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        단일 스칼라 값을 반환합니다.

        Args:
            sql: 실행할 SQL 문
            params: SQL 파라미터

        Returns:
            단일 스칼라 값 (예: COUNT, MAX, MIN 등의 결과)
        """
        if self._connection is None:
            raise RuntimeError("데이터베이스에 연결되지 않았습니다.")

        logger.debug(f"SQL 실행 (fetch_val): {sql}, params: {params}")
        # 테스트에서는 _connection이 주입되므로 실제로 실행됩니다
        return await self._connection.fetchval(sql, params)

    async def fetch_one(
        self, sql: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        하나의 레코드를 반환합니다.

        Args:
            sql: 실행할 SQL 문
            params: SQL 파라미터

        Returns:
            레코드 딕셔너리 또는 None
        """
        if self._connection is None:
            raise RuntimeError("데이터베이스에 연결되지 않았습니다.")

        logger.debug(f"SQL 실행 (fetch_one): {sql}, params: {params}")
        # 테스트에서는 _connection이 주입되므로 실제로 실행됩니다
        row = await self._connection.fetchrow(sql, params)
        return dict(row) if row else None

    async def fetch_all(
        self, sql: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        모든 레코드를 반환합니다.

        Args:
            sql: 실행할 SQL 문
            params: SQL 파라미터

        Returns:
            레코드 딕셔너리들의 리스트
        """
        if self._connection is None:
            raise RuntimeError("데이터베이스에 연결되지 않았습니다.")

        logger.debug(f"SQL 실행 (fetch_all): {sql}, params: {params}")
        # 테스트에서는 _connection이 주입되므로 실제로 실행됩니다
        rows = await self._connection.fetch(sql, params)
        return [dict(row) for row in rows]

    async def execute(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        SQL 문을 실행합니다 (INSERT, UPDATE, DELETE).

        Args:
            sql: 실행할 SQL 문
            params: SQL 파라미터

        Returns:
            영향받은 행의 수 또는 기타 실행 결과
        """
        if self._connection is None:
            raise RuntimeError("데이터베이스에 연결되지 않았습니다.")

        logger.debug(f"SQL 실행 (execute): {sql}, params: {params}")
        # 테스트에서는 _connection이 주입되므로 실제로 실행됩니다
        return await self._connection.execute(sql, params)

    async def close(self) -> None:
        """
        데이터베이스 연결을 닫습니다.
        """
        if self._connection:
            # 테스트에서는 _connection이 주입되므로 실제로 실행됩니다
            await self._connection.close()
            self._connection = None
            logger.info("데이터베이스 연결이 닫혔습니다.")

    async def __aenter__(self) -> "PyBatis":
        """비동기 컨텍스트 매니저 진입"""
        if self.dsn and self._connection is None:
            await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """비동기 컨텍스트 매니저 종료"""
        await self.close()
