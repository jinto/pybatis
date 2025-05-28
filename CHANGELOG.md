# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-XX

### Added
- 🚀 **핵심 기능**
  - PyBatis 메인 클래스 구현 (DSN 기반 초기화)
  - `fetch_val`, `fetch_one`, `fetch_all`, `execute` 메서드
  - 비동기 컨텍스트 매니저 지원
  - 트랜잭션 컨텍스트 매니저 지원

- 🎯 **Pydantic 통합**
  - 쿼리 결과를 Pydantic 모델로 자동 매핑
  - Repository 패턴 구현 지원

- 📁 **SQL 파일 로더**
  - .sql 파일에서 SQL 문 로드
  - 이름 기반 SQL 추출 지원 (`-- name=sql_name`)

- 🔄 **데이터베이스 지원**
  - SQLite 통합 (aiosqlite)
  - PostgreSQL 지원 준비 (asyncpg)
  - MySQL 지원 준비 (aiomysql)
  - 스키마 기반 boolean 자동 변환

- 🚀 **FastAPI 통합**
  - PyBatisManager 클래스
  - 의존성 주입 지원 (`create_pybatis_dependency`)
  - 애플리케이션 생명주기 관리
  - 트랜잭션 컨텍스트 매니저

- 📊 **쿼리 모니터링**
  - 쿼리 로깅 기능 (`enable_query_logging`)
  - 쿼리 모니터링 및 통계 수집 (`enable_query_monitoring`)
  - 실행 시간 측정 및 느린 쿼리 감지
  - 트랜잭션 로깅 지원

- 🧪 **테스트 및 품질**
  - 75개 테스트 케이스 (85% 커버리지)
  - TDD 방식으로 개발
  - MockConnection을 통한 단위 테스트
  - 실제 데이터베이스 통합 테스트

### Technical Details
- Python 3.11+ 지원
- FastAPI 0.104.0+ 호환
- Pydantic 2.0.0+ 지원
- 비동기 I/O 기반 고성능
- SOLID 원칙 및 Clean Architecture 준수

[Unreleased]: https://github.com/pybatis/pybatis/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/pybatis/pybatis/releases/tag/v0.1.0