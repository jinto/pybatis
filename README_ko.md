# 🐍 pyBatis Neo

**FastAPI를 위한 MyBatis 스타일의 SQL 매퍼 - 현대적이고 Pythonic한 구현**

[![PyPI version](https://badge.fury.io/py/pybatis-neo.svg)](https://badge.fury.io/py/pybatis-neo)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English README](README.md) | [문서](https://pybatis-neo.readthedocs.io) | [PyPI](https://pypi.org/project/pybatis-neo/)

pyBatis Neo는 FastAPI 백엔드 개발자를 위한 오픈소스 SQL 매퍼 라이브러리입니다. Java의 MyBatis에서 영감을 받아, XML 없이도 SQL을 명시적으로 작성하고, 비즈니스 로직과 분리하여 관리할 수 있도록 설계되었습니다.

## ✨ 주요 특징

- 🚀 **FastAPI 완벽 통합**: FastAPI의 의존성 주입 시스템과 자연스럽게 통합
- 🔄 **비동기 지원**: async/await를 활용한 고성능 비동기 SQL 실행
- 🎯 **Pydantic 모델 매핑**: SQL 쿼리 결과를 자동으로 Pydantic 모델로 변환
- 🐍 **Pythonic한 구성**: XML 대신 데코레이터와 함수 주석을 활용
- 🔒 **SQL 인젝션 방지**: 안전한 파라미터 바인딩
- 🧪 **테스트 친화적**: 모킹 및 의존성 주입을 통한 쉬운 테스트
- 📊 **쿼리 모니터링**: 실행 시간 측정 및 성능 모니터링
- 📁 **SQL 파일 로더**: 외부 .sql 파일에서 SQL 문 로드

## 📋 요구사항

- **Python 3.11 이상**
- FastAPI 0.104.0 이상
- Pydantic 2.0.0 이상

## 📦 설치

```bash
pip install pybatis-neo
```

### 데이터베이스 드라이버 설치

```bash
# PostgreSQL
pip install pybatis-neo[postgres]

# MySQL
pip install pybatis-neo[mysql]

# SQLite
pip install pybatis-neo[sqlite]

# 모든 드라이버
pip install pybatis-neo[all]
```

## 🚀 빠른 시작

### 1. 모델 정의

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
```

### 2. Repository 클래스 생성

```python
from typing import Optional, List
from pybatis import PyBatis
from .models import User

class UserRepository:
    def __init__(self, db: PyBatis):
        self.db = db

    async def create_user(self, name: str, email: str, is_active: bool = True) -> int:
        """새 사용자 생성"""
        sql = """
        INSERT INTO users (name, email, is_active)
        VALUES (:name, :email, :is_active)
        """
        return await self.db.execute(sql, params={
            "name": name,
            "email": email,
            "is_active": is_active
        })

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """ID로 사용자 조회"""
        sql = "SELECT id, name, email, is_active FROM users WHERE id = :user_id"
        row = await self.db.fetch_one(sql, params={"user_id": user_id})
        return User(**row) if row else None

    async def get_users_by_activity(self, active_status: bool) -> List[User]:
        """활성 상태에 따라 사용자 목록 조회"""
        sql = "SELECT id, name, email, is_active FROM users WHERE is_active = :active_status"
        rows = await self.db.fetch_all(sql, params={"active_status": active_status})
        return [User(**row) for row in rows]

    async def count_active(self, active: bool) -> int:
        """활성 사용자 수 조회"""
        sql = "SELECT COUNT(*) FROM users WHERE is_active = :active"
        return await self.db.fetch_val(sql, params={"active": active})
```

### 3. FastAPI와 통합 (기본)

```python
from fastapi import FastAPI, HTTPException
from pybatis import PyBatis

app = FastAPI()

# 간단한 사용법
@app.on_event("startup")
async def startup():
    global db
    db = PyBatis(dsn="sqlite:///example.db")
    await db.connect()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    repo = UserRepository(db)
    user = await repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### 4. FastAPI와 통합 (고급 - 의존성 주입)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from pybatis import PyBatis
from pybatis.fastapi import PyBatisManager, create_pybatis_dependency

# PyBatis 매니저 설정
manager = PyBatisManager(dsn="sqlite:///example.db")
get_pybatis = create_pybatis_dependency(manager)

# Repository 의존성 함수
async def get_user_repository(pybatis: PyBatis = Depends(get_pybatis)) -> UserRepository:
    return UserRepository(pybatis)

# 애플리케이션 생명주기 관리
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시: 테이블 생성
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

app = FastAPI(lifespan=lifespan)

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    user_repo: UserRepository = Depends(get_user_repository)
):
    user = await user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/active-count")
async def active_users_count(
    user_repo: UserRepository = Depends(get_user_repository)
):
    count = await user_repo.count_active(active=True)
    return {"active_user_count": count}
```

## 🔧 고급 기능

### 쿼리 로깅 및 모니터링

```python
import logging

# 쿼리 로깅 활성화
db.enable_query_logging(level=logging.INFO)

# 쿼리 모니터링 활성화
db.enable_query_monitoring()

# 느린 쿼리 임계값 설정 (1초)
db.set_slow_query_threshold(1.0)

# 통계 조회
stats = db.get_query_stats()
print(f"총 쿼리 수: {stats['total_queries']}")
print(f"평균 실행 시간: {stats['average_execution_time']:.4f}초")
```

### 트랜잭션 관리

```python
# 트랜잭션 컨텍스트 매니저 사용
async with db.transaction() as tx:
    await tx.execute("INSERT INTO users (name) VALUES (:name)", {"name": "사용자1"})
    await tx.execute("INSERT INTO profiles (user_id) VALUES (:user_id)", {"user_id": 1})
    # 자동 커밋 (예외 발생 시 자동 롤백)
```

### SQL 파일 로더

```python
# SQL 디렉토리 설정
db.set_sql_loader_dir("sql/")

# SQL 파일에서 로드
sql = db.load_sql("users.sql", "get_active_users")
users = await db.fetch_all(sql, {"active": True})
```

## 🏗️ 아키텍처

pyBatis Neo는 다음과 같은 핵심 컴포넌트로 구성됩니다:

- **PyBatis**: 핵심 SQL 실행기 클래스
- **Repository Pattern**: 도메인별 데이터 액세스 로직 캡슐화
- **DSN 연결**: 데이터베이스 연결 문자열 기반 초기화
- **비동기 지원**: async/await를 활용한 고성능 SQL 실행
- **FastAPI 통합**: 의존성 주입 및 생명주기 관리

## 🧪 개발 환경 설정

프로젝트를 로컬에서 개발하려면:

```bash
# 저장소 클론
git clone https://github.com/jinto/pybatis.git
cd pybatis

# 가상환경 생성 (uv 사용)
uv venv
source .venv/bin/activate

# 개발 의존성 설치
uv pip install -e ".[dev]"

# 테스트 실행
uv run pytest

# 코드 포맷팅
black src tests
isort src tests

# 타입 체크
mypy src

# 샘플 코드 실행
python samples/demo_sqlite_pydantic.py
python samples/fastapi_example.py
```

## 📊 테스트

```bash
# 모든 테스트 실행
uv run pytest

# 커버리지 포함 테스트
uv run pytest --cov=pybatis --cov-report=html

# 특정 테스트 파일 실행
uv run pytest tests/test_pybatis.py
```

## 📚 샘플 코드

`samples/` 디렉토리에서 다양한 사용 예제를 확인할 수 있습니다:

- `demo_sqlite_pydantic.py`: SQLite와 Pydantic 모델 연동 데모
- `fastapi_example.py`: FastAPI 완전 통합 예제

## 🤝 기여하기

pyBatis Neo는 오픈소스 프로젝트입니다. 기여를 환영합니다!

1. 이슈를 확인하거나 새로운 이슈를 생성하세요
2. 피처 브랜치를 생성하세요 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성하세요

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🔗 링크

- [문서](https://pybatis-neo.readthedocs.io)
- [GitHub 저장소](https://github.com/jinto/pybatis)
- [이슈 트래커](https://github.com/jinto/pybatis/issues)
- [PyPI](https://pypi.org/project/pybatis-neo/)
- [변경 이력](CHANGELOG.md)

---

**pyBatis Neo와 함께 FastAPI에서 깔끔하고 유지보수하기 쉬운 SQL 코드를 작성해보세요! 🚀**