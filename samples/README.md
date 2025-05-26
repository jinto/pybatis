# 📚 pyBatis 샘플 코드

이 디렉토리에는 pyBatis의 다양한 기능을 시연하는 샘플 코드들이 포함되어 있습니다.

## 🗂️ 샘플 목록

### 1. `demo_sqlite_pydantic.py`
**SQLite와 Pydantic 모델 연동 데모**

이 샘플은 pyBatis를 사용하여 SQLite 데이터베이스와 Pydantic 모델을 연동하는 방법을 보여줍니다.

#### 주요 기능:
- SQLite 데이터베이스 연결 및 테이블 생성
- Pydantic 모델 정의 및 사용
- Repository 패턴 구현
- CRUD 작업 (생성, 조회, 업데이트, 삭제)
- 비동기 컨텍스트 매니저 사용
- SQLite boolean 타입 자동 변환

#### 실행 방법:
```bash
# 프로젝트 루트에서 실행
python samples/demo_sqlite_pydantic.py
```

#### 예상 출력:
```
🚀 pyBatis SQLite + Pydantic 모델 연동 데모
==================================================
📁 임시 데이터베이스: /tmp/tmpXXXXXX.db
✅ users 테이블 생성 완료

📝 사용자 생성:
   - 김철수 (ID: 1)
   - 이영희 (ID: 2)
   - 박민수 (ID: 3) - 비활성

🔍 단일 사용자 조회:
   - User 객체: id=1 name='김철수' email='kim@example.com' is_active=True
   - 타입: <class '__main__.User'>
   ...

🎊 데모 완료!
```

#### 학습 포인트:
1. **DSN 연결**: `sqlite:///path/to/db.sqlite` 형식의 DSN 사용
2. **Pydantic 모델**: 타입 안전한 데이터 모델 정의
3. **Repository 패턴**: 데이터 액세스 로직 분리
4. **비동기 처리**: `async/await` 패턴 사용
5. **타입 변환**: SQLite의 boolean integer를 Python boolean으로 자동 변환

## 🚀 실행 전 준비사항

모든 샘플을 실행하기 전에 다음 의존성이 설치되어 있는지 확인하세요:

```bash
# 개발 환경 설치
uv pip install -e ".[dev,sqlite]"

# 또는 기본 설치 + SQLite 지원
pip install -e ".[sqlite]"
```

## 📖 추가 리소스

- [pyBatis 메인 README](../README.md)
- [API 문서](../src/pybatis/)
- [테스트 코드](../tests/)

## 🤝 기여하기

새로운 샘플 코드나 기존 샘플의 개선사항이 있다면 언제든지 기여해주세요!

1. 새로운 샘플 파일 생성
2. 이 README.md에 설명 추가
3. 테스트 코드 작성 (선택사항)
4. Pull Request 제출