#!/bin/bash

# pyBatis 테스트 자동화 스크립트

set -e  # 오류 발생 시 스크립트 중단

echo "🧪 pyBatis 테스트 자동화 시작..."

echo "📦 1. 코드 포맷팅 검사 (black)..."
black --check src tests

echo "📋 2. Import 정렬 검사 (isort)..."
isort --check-only src tests

echo "🔍 3. 코드 품질 검사 (flake8)..."
flake8 src tests --max-line-length=88 --extend-ignore=E203,W503

echo "🔬 4. 타입 체크 (mypy)..."
mypy src

echo "🧪 5. 테스트 실행 (pytest)..."
pytest --cov=pybatis --cov-report=term-missing --cov-report=html

echo "✅ 모든 검사가 완료되었습니다!"
echo "📊 HTML 커버리지 리포트: htmlcov/index.html"