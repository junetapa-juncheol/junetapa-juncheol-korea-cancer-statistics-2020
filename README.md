# 🏥 한국 암 발생 통계 분석 (2020년)

2020년 한국인 암 발생 현황을 분석하는 **비영리 포트폴리오** 프로젝트입니다.

## 📄 데이터 출처 및 저작권
- **데이터 제공**: 국립암센터 국가암정보센터 (https://www.cancer.go.kr)
- **저작권**: 국립암센터 (National Cancer Center Korea)
- **이용허락**: 저작자표시-비영리-변경금지
- **프로젝트 목적**: 포트폴리오 및 학습용 (완전 비영리)

> ⚠️ **중요**: 본 프로젝트는 **상업적 이용을 금지**하며, **포트폴리오 및 학습 목적**으로만 사용됩니다.

## 📊 분석 내용
- **암종별 발생률**: 주요 24개 암종 분석
- **성별 통계**: 남성/여성별 암 발생 패턴
- **연령대별 분석**: 연령층에 따른 암 발생 동향
- **지역별 현황**: 시도별 암 발생 분포

## 🛠️ 기술 스택
- **Python 3.8+**
- **pandas**: 데이터 처리
- **matplotlib, seaborn**: 데이터 시각화
- **plotly**: 인터랙티브 차트
- **requests**: API 데이터 수집

## 🚀 실행 방법

### 1. 환경 설정
```bash
pip install -r requirements.txt
```

### 2. API 키 설정
`.env` 파일을 생성하고 공공데이터포털 API 키를 입력하세요:
```
CANCER_API_KEY=your_api_key_here
```

### 3. 데이터 수집 및 분석
```bash
python data_collector.py  # 데이터 수집
python data_analyzer.py   # 데이터 분석
python visualizer.py      # 시각화 생성
```

## 📈 결과물

### 🎯 **인터랙티브 대시보드 (메인 결과물)**
**👉 [실시간 3D 인터랙티브 대시보드 보기](https://htmlpreview.github.io/?https://github.com/junetapa-juncheol/junetapa-juncheol-korea-cancer-statistics-2020/blob/main/charts/interactive_dashboard.html)**

### 📁 **파일 구조**
- **`charts/`**: 생성된 차트 이미지 및 인터랙티브 대시보드
  - [`interactive_dashboard.html`](charts/interactive_dashboard.html) - 메인 3D 대시보드
  - [`cancer_by_type.png`](charts/cancer_by_type.png) - 암종별 발생 현황
  - [`gender_distribution.png`](charts/gender_distribution.png) - 성별 분포
  - [`age_distribution.png`](charts/age_distribution.png) - 연령별 분포
  - [`regional_distribution.png`](charts/regional_distribution.png) - 지역별 분포
- **`data/`**: 수집된 원본 데이터 (CSV 파일)
  - [`cancer_by_type_gender.csv`](data/cancer_by_type_gender.csv) - 암종별 성별 데이터
  - [`cancer_by_age.csv`](data/cancer_by_age.csv) - 연령별 데이터
  - [`cancer_by_region.csv`](data/cancer_by_region.csv) - 지역별 데이터
- **`reports/`**: 분석 보고서
  - [`cancer_analysis_summary.txt`](reports/cancer_analysis_summary.txt) - 분석 요약
  - [`cancer_analysis_report.json`](reports/cancer_analysis_report.json) - 상세 분석 데이터

## 📋 데이터 출처
- 공공데이터포털 (data.go.kr)
- 국립암센터 암발생통계
- 국가통계포털 (KOSIS)

## ⚠️ 주의사항 및 라이센스 준수
- **목적**: 학습 및 포트폴리오 목적으로만 제작 (완전 비영리)
- **의료적 사용 금지**: 실제 의료 진단이나 치료에 사용 절대 금지
- **상업적 이용 금지**: 판매, 영리 목적 사용 엄격히 금지
- **데이터 변경 금지**: 원본 데이터 수정 없이 그대로 활용
- **출처 표시**: 모든 사용 시 국립암센터 출처 명시 필수
- **API 키 보안**: 개인 정보이므로 공유 금지

### 저작권 고지
본 프로젝트는 국립암센터의 **저작자표시-비영리-변경금지** 조건을 엄격히 준수합니다. 
자세한 내용은 [LICENSE.md](LICENSE.md)를 참조하세요.