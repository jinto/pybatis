# ✅ pyBatis 개발 TODO

## 📁 1. 프로젝트 초기화 ✅

- [x] `uv`를 사용하여 프로젝트 디렉토리 생성
  - `uv venv`로 가상환경 생성 ✅
  - `uv pip install --editable .`로 로컬 패키지 설치 ✅
- [x] `pyproject.toml` 파일 생성 및 설정 ✅
  - 패키지 메타데이터 작성 ✅
  - 의존성 목록 작성 ✅
  - Python 3.11 이상 요구사항 설정 ✅
- [x] 디렉토리 구조 설정 ✅

  ```bash
  pybatis/
  ├── pyproject.toml          ✅
  ├── README.md               ✅
  ├── src/
  │   └── pybatis/
  │       ├── __init__.py     ✅
  │       ├── pybatis.py      ✅
  │       ├── sql_loader.py   ✅
  │       └── fastapi.py      ✅
  └── tests/
      ├── __init__.py         ✅
      ├── test_pybatis.py     ✅
      ├── test_sql_loader.py  ✅
      ├── test_sqlite_integration.py ✅
      ├── test_fastapi_integration.py ✅
      └── fixtures.py         ✅

## 🧪 2. 테스트 환경 구성 (TDD 기반) ✅

- [x] pytest 설치 및 설정 ✅
  - pytest.ini 또는 pyproject.toml에 테스트 설정 추가 ✅
  - tests/ 디렉토리에 초기 테스트 파일 생성 ✅
  - coverage 도구 설치 및 설정 ✅
- [x] 개발 도구 설정 ✅
  - black을 사용한 코드 포맷팅 ✅
  - isort를 사용한 import 정렬 ✅
  - flake8을 사용한 코드 품질 검사 ✅
  - mypy를 사용한 타입 체크 ✅
- [x] 테스트 자동화 스크립트 작성 ✅
  - scripts/test.sh 생성 ✅
  - 84% 커버리지 달성 ✅

## 🧱 3. 기본 기능 구현 (MVP) ✅

### 🎯 **핵심 API 구현** ✅
- [x] PyBatis 메인 클래스 구현 ✅
  - DSN 기반 초기화 ✅
  - fetch_val, fetch_one, fetch_all, execute 메서드 ✅
  - 비동기 컨텍스트 매니저 지원 ✅
  - 트랜잭션 컨텍스트 매니저 지원 ✅
- [x] Pydantic 모델과의 연동 ✅
  - 쿼리 결과를 Pydantic 모델로 매핑 ✅
  - Repository 패턴 구현 ✅
- [x] 테스트 작성 및 검증 ✅
  - 62개 테스트 모두 통과 ✅
  - MockConnection을 통한 단위 테스트 ✅

### 🔄 **확장 기능 구현** ✅
- [x] SQL 파일 로딩 기능 ✅
  - .sql 파일에서 SQL 문 로드 ✅
  - 이름 기반 SQL 추출 지원 (-- name=sql_name) ✅
  - PyBatis 통합 (set_sql_loader_dir, load_sql 메서드) ✅
  - 15개 테스트 모두 통과 ✅
- [x] SQLite 통합 ✅
  - aiosqlite (SQLite) 지원 ✅
  - DSN 파싱 및 연결 관리 ✅
  - 실제 데이터베이스 통합 테스트 12개 통과 ✅
  - SQL 로더와 SQLite 통합 테스트 ✅
  - Repository 패턴과 SQLite 통합 테스트 ✅
  - 스키마 기반 boolean 자동 변환 ✅
    - PRAGMA table_info를 사용한 스키마 정보 캐싱 ✅
    - BOOLEAN 타입 컬럼 자동 감지 및 변환 ✅
    - SQL에서 테이블명 자동 추출 ✅
    - 5개 추가 테스트 통과 ✅
- [x] FastAPI 의존성 주입 통합 ✅
  - PyBatisManager 클래스 구현 ✅
  - create_pybatis_dependency() 함수 구현 ✅
  - get_pybatis() 기본 의존성 함수 구현 ✅
  - transaction_context() 트랜잭션 컨텍스트 매니저 구현 ✅
  - 애플리케이션 생명주기 관리 함수들 구현 ✅
  - 17개 FastAPI 통합 테스트 모두 통과 ✅
  - samples/fastapi_example.py 예제 코드 작성 ✅

## 🧪 4. 고급 기능 및 최적화
- [x] 연결 풀링 가이드 문서화 ✅
  - 애플리케이션 레벨에서 풀링 관리하는 것이 적절하다고 결정 ✅
  - 각 데이터베이스 드라이버의 풀링 기능 활용 권장 ✅
  - 예제 코드 및 모범 사례 문서 작성 필요
- [x] 쿼리 로깅 및 모니터링 ✅
  - 쿼리 로깅 기능 구현 (enable_query_logging, disable_query_logging) ✅
  - 쿼리 모니터링 기능 구현 (enable_query_monitoring, get_query_stats) ✅
  - 실행 시간 측정 및 느린 쿼리 감지 ✅
  - 트랜잭션 로깅 지원 ✅
  - 13개 로깅/모니터링 테스트 모두 통과 ✅
- [x] 테스트 커버리지 85% 달성 ✅ (84% → 85% 향상)

## 📦 5. 배포 준비
- [x] pyproject.toml에 배포 정보 추가 ✅
 - 버전, 설명, 작성자, 라이선스 등 ✅
- [x] README.md 작성 ✅
 - 프로젝트 소개, 설치 방법, 사용 예시 등 ✅
- [ ] LICENSE 파일 추가
- [ ] PyPI 배포 테스트
 - uv publish 또는 twine을 사용한 배포