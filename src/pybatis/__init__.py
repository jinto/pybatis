"""
pyBatis - FastAPI를 위한 MyBatis 스타일의 SQL 매퍼

이 라이브러리는 FastAPI 백엔드 개발자를 위한 SQL 매퍼로,
Java의 MyBatis에서 영감을 받아 Pythonic한 방식으로 구현되었습니다.
"""

from .pybatis import PyBatis

__version__ = "0.1.0"
__author__ = "pyBatis Contributors"

__all__ = [
    "PyBatis",
]
