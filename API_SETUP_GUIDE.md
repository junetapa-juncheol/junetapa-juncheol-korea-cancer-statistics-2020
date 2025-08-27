# 🔑 공공데이터포털 API 설정 가이드

## 1단계: 공공데이터포털 회원가입 및 API 신청

### 회원가입
1. **공공데이터포털 접속**: https://www.data.go.kr
2. **회원가입** 클릭 후 개인정보 입력
3. **이메일 인증** 완료

### API 신청
1. **데이터 검색**: "국립암센터" 또는 "암발생통계" 검색
2. **추천 API**:
   - 국립암센터_전립선암_라이브러리_환자수
   - 국립암센터_폐암 라이브러리 환자수  
   - 국립암센터_췌장암_라이브러리_환자수

3. **각 API 신청 과정**:
   - API 상세페이지 이동
   - **"활용신청"** 버튼 클릭
   - **개발계정 신청** (일 10,000건 제한)
   - **활용목적**: "개인 포트폴리오 프로젝트 - 한국 암 통계 분석"
   - **상세기능정보** 작성

## 2단계: API 키 발급 확인

### 발급 확인 방법
1. **마이페이지** → **데이터활용** → **오픈API**
2. **개발계정** 탭에서 신청 현황 확인
3. **승인 완료 시** → **인증키** 복사

### 일반적인 승인 시간
- **즉시 승인**: 대부분의 API
- **1-2일**: 일부 승인 검토가 필요한 API

## 3단계: 환경변수 설정

### .env 파일 생성
```bash
# 프로젝트 루트에 .env 파일 생성
cp .env.example .env
```

### API 키 입력
```env
# .env 파일 내용
CANCER_API_KEY=your_actual_api_key_here
NCC_API_KEY=your_ncc_api_key_here
```

⚠️ **주의사항**: 
- API 키는 절대 GitHub에 업로드하지 마세요
- .env 파일은 .gitignore에 포함되어 있습니다

## 4단계: API 연동 테스트

### 테스트 실행
```bash
python main.py
```

### 성공 시 메시지
```
Using real API data...
✅ prostate data collected successfully  
✅ lung data collected successfully
✅ pancreatic data collected successfully
```

### 실패 시 메시지
```
Using sample data (API key not configured)...
⚠️ API request failed for prostate: 401
🔄 API data collection failed, falling back to sample data...
```

## 5단계: 문제 해결

### 일반적인 오류
1. **401 Unauthorized**: API 키 오류
   - API 키가 정확한지 확인
   - 따옴표 없이 키만 입력했는지 확인

2. **403 Forbidden**: 트래픽 초과
   - 일일 10,000건 제한 초과
   - 내일 다시 시도하거나 운영계정 신청

3. **404 Not Found**: 엔드포인트 오류
   - API 주소가 변경되었을 수 있음
   - 공식 문서에서 최신 주소 확인

### 도움말 리소스
- **공공데이터포털 고객센터**: 1577-3069
- **국립암센터 문의**: 031-920-0760~2
- **API 문서**: 각 API 상세페이지에서 확인

## 6단계: 운영계정 신청 (선택사항)

### 더 많은 데이터가 필요한 경우
1. **활용사례** 등록
2. **운영계정** 신청
3. **트래픽 제한 해제** (API별 상이)

---

## ✅ API 설정 체크리스트

- [ ] 공공데이터포털 회원가입 완료
- [ ] 국립암센터 관련 API 3개 이상 신청
- [ ] API 키 발급 확인
- [ ] .env 파일에 API 키 설정
- [ ] python main.py 실행하여 API 연동 테스트
- [ ] 실제 데이터 수집 성공 확인

**모든 단계 완료 후 실제 공공데이터를 활용한 분석이 가능합니다!** 🎉