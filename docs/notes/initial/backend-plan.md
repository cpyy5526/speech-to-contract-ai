# 백엔드 주차별 계획

## 주요 역할

- API 설계 및 구현
- 데이터 흐름 및 백엔드 시스템 설계
- 배포 및 운영 환경 구축

## 사용 기술

- FastAPI: 백엔드 프레임워크
    - 경량화된 Python 프레임워크. 빠르고 효율적
    - OpenAI API 및 STT 연동에 용이할 것으로 기대
- OpenAI Whisper API: STT(Speech-to-Text)
    - 기업 측에서 지원하는 OpenAI API에 포함
    - 다국어 지원
- SQLite/PostgreSQL: 데이터 저장 및 관리
    - SQLite: 초기에는 간단한 DB 구축
    - PostgreSQL: DB 확장. AWS 배포 고려
- AWS 및 Docker: 배포 서비스, 기업 측 세부 확인 필요

## 주차별 계획

<aside>

### **1주차 (3.17-3.23)**

</aside>

- 백엔드 세부 요구사항 문서화 및 피드백
- 역할 범위 및 세부 계획 검토

<aside>

### **2주차 (3.24-3.30)**

</aside>

- FastAPI 기반 API 설계 초안 작성
- 데이터 흐름 및 저장 방식 초안 작성
- Whisper API 테스트

<aside>

### **3주차 (3.31-4.6)**

</aside>

- FastAPI 기반 백엔드 API 개발 시작
- Whisper API 연동 테스트
- 데이터 저장 및 로그 기록 설계

<aside>

### **4주차 (4.7-4.13)**

</aside>

- API 성능 개선(Whisper 호출 최적화)
- 프롬프트 엔지니어링 팀과의 API 연동 논의

<aside>

### **5주차 (4.14-4.20)**

</aside>

- API 엔드포인트 문서화
- ChatGPT API 연동 구현

<aside>

### **6주차 (4.21-4.27)**

</aside>

- 프론트엔드 연동 논의 및 테스트
- 백엔드 API 테스트 및 디버깅

<aside>

### **7주차 (4.28-5.4)**

</aside>

- 계약서 저장 및 PDF 변환 기능 추가
- 백엔드 API 안정화 및 성능 최적화

<aside>

### **8주차 (5.5-5.11)**

</aside>

- 배포 인프라 설정 및 운영 환경 구축
- Docker 기반 컨테이너 배포

<aside>

### **9주차 (5.12-5.18)**

</aside>

- 배포 및 성능 개선 작업
- 최종 서비스 점검 및 사용자 테스트

<aside>

### **10주차 (5.19-5.25)**

</aside>

- 구현 사항 최종 정리 및 문서화
- 결과보고서 작성 준비