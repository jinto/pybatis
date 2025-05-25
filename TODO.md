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
  │       └── core.py         ✅
  └── tests/
      ├── __init__.py         ✅
      └── test_core.py        ✅

## 🧪 2. 테스트 환경 구성 (TDD 기반)

- [ ] pytest 설치 및 설정
 - pytest.ini 또는 pyproject.toml에 테스트 설정 추가
 - tests/ 디렉토리에 초기 테스트 파일 생성
 - coverage 도구 설치 및 설정

## 🧱 3. 최소 기능 구현 (MVP)
- [ ] SQL 매핑 기능 구현
- [ ] SQL 파일 로딩 기능
- [ ] SQL 실행 기능
- [ ] Pydantic 모델과의 연동
- [ ] 쿼리 결과를 Pydantic 모델로 매핑
- [ ] FastAPI와의 통합
- [ ] 의존성 주입을 통한 세션 관리

## 🧪 4. 테스트 작성 및 검증
- [ ] 각 기능에 대한 단위 테스트 작성
- [ ] 테스트 커버리지 90% 이상 달성
- [ ] 테스트 자동화 스크립트 작성

## 📦 5. 배포 준비
- [ ] pyproject.toml에 배포 정보 추가
 - 버전, 설명, 작성자, 라이선스 등
- [ ] README.md 작성
 - 프로젝트 소개, 설치 방법, 사용 예시 등
- [ ] LICENSE 파일 추가
- [ ]  PyPI 배포 테스트
 - uv publish 또는 twine을 사용한 배포