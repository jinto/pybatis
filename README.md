# 🐍 pyBatis

**FastAPI를 위한 MyBatis 스타일의 SQL 매퍼**

pyBatis는 FastAPI 백엔드 개발자를 위한 오픈소스 SQL 매퍼 라이브러리입니다. Java의 MyBatis에서 영감을 받아, XML 없이도 SQL을 명시적으로 작성하고, 비즈니스 로직과 분리하여 관리할 수 있도록 설계되었습니다.

## ✨ 주요 특징

- 🚀 **FastAPI 완벽 통합**: FastAPI의 의존성 주입 시스템과 자연스럽게 통합
- 🔄 **비동기 지원**: async/await를 활용한 고성능 비동기 SQL 실행
- 🎯 **Pydantic 모델 매핑**: SQL 쿼리 결과를 자동으로 Pydantic 모델로 변환
- 🐍 **Pythonic한 구성**: XML 대신 데코레이터와 함수 주석을 활용
- 🔒 **SQL 인젝션 방지**: 안전한 파라미터 바인딩
- 🧪 **테스트 친화적**: 모킹 및 의존성 주입을 통한 쉬운 테스트

## 📋 요구사항

- **Python 3.11 이상**
- FastAPI 0.104.0 이상
- Pydantic 2.0.0 이상

## 📦 설치

```bash
pip install pybatis
```

### 데이터베이스 드라이버 설치

```bash
# PostgreSQL
pip install pybatis[postgres]

# MySQL
pip install pybatis[mysql]

# SQLite
pip install pybatis[sqlite]

# 모든 드라이버
pip install pybatis[all]
```

## 🚀 빠른 시작

### 1. 모델 정의

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
```

### 2. 매퍼 클래스 생성

```python
# db.py
from typing import Optional, List
from pybatis import PyBatis  # pyBatis의 핵심 DB 실행기
from .models import User

class UserRepository:
    def __init__(self, db: PyBatis):
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
        sql = "SELECT id, name, email, is_active FROM users WHERE is_active = :active_status"
        rows = await self.db.fetch_all(sql, params={"active_status": active_status})
        return [User(**r) for r in rows]
```

### 3. FastAPI와 통합

```python
from typing import List
from fastapi import FastAPI, HTTPException
from pybatis import PyBatis
from .db import UserRepository
from .models import User

app = FastAPI()
db = PyBatis(dsn="postgresql://user:pass@localhost:5432/mydb")
user_repo = UserRepository(db)

@app.get("/users/active-count")
async def active_users_count():
    count = await user_repo.count_active(active=True)
    return {"active_user_count": count}

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = await user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=List[User])
async def read_users_by_activity(active: bool = True):
    return await user_repo.get_users_by_activity(active)

@app.get("/users/all", response_model=List[User])
async def read_all_users():
    active = await user_repo.get_users_by_activity(True)
    inactive = await user_repo.get_users_by_activity(False)
    return active + inactive
```

## 🏗️ 아키텍처

pyBatis는 다음과 같은 핵심 컴포넌트로 구성됩니다:

- **PyBatis**: 핵심 SQL 실행기 클래스
- **Repository Pattern**: 도메인별 데이터 액세스 로직 캡슐화
- **DSN 연결**: 데이터베이스 연결 문자열 기반 초기화
- **비동기 지원**: async/await를 활용한 고성능 SQL 실행

## 🧪 개발 환경 설정

프로젝트를 로컬에서 개발하려면:

```bash
# 저장소 클론
git clone https://github.com/pybatis/pybatis.git
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
```

## 📊 테스트

```bash
# 모든 테스트 실행
uv run pytest

# 커버리지 포함 테스트
uv run pytest --cov=pybatis --cov-report=html

# 특정 테스트 파일 실행
uv run pytest tests/test_core.py
```

## 🤝 기여하기

pyBatis는 오픈소스 프로젝트입니다. 기여를 환영합니다!

1. 이슈를 확인하거나 새로운 이슈를 생성하세요
2. 피처 브랜치를 생성하세요 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성하세요

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🔗 링크

- [문서](https://pybatis.readthedocs.io)
- [GitHub 저장소](https://github.com/pybatis/pybatis)
- [이슈 트래커](https://github.com/pybatis/pybatis/issues)
- [PyPI](https://pypi.org/project/pybatis/)

---

**pyBatis와 함께 FastAPI에서 깔끔하고 유지보수하기 쉬운 SQL 코드를 작성해보세요! 🚀**