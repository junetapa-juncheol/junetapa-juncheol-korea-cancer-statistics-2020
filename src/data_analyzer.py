import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

class CancerDataAnalyzer:
    def __init__(self):
        self.data_dir = Path('data')
        self.charts_dir = Path('charts')
        self.reports_dir = Path('reports')
        
        # 디렉토리 생성
        self.charts_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        
    def load_data(self):
        """데이터 로드"""
        print("Loading data...")
        
        try:
            self.cancer_data = pd.read_csv(self.data_dir / 'cancer_by_type_gender.csv')
            self.age_data = pd.read_csv(self.data_dir / 'cancer_by_age.csv')
            self.regional_data = pd.read_csv(self.data_dir / 'cancer_by_region.csv')
            print("Data loading completed!")
        except FileNotFoundError:
            print("Data files not found. Please run data_collector.py first.")
            return False
        return True
    
    def analyze_gender_distribution(self):
        """성별 암 발생 분포 분석"""
        print("Analyzing gender distribution...")
        
        # 성별 총 발생 수 계산
        total_male = self.cancer_data['남성'].sum()
        total_female = self.cancer_data['여성'].sum()
        
        gender_stats = {
            '남성': total_male,
            '여성': total_female,
            '남성_비율': total_male / (total_male + total_female) * 100,
            '여성_비율': total_female / (total_male + total_female) * 100
        }
        
        return gender_stats
    
    def analyze_top_cancers(self, top_n=10):
        """상위 암종 분석"""
        print(f"Analyzing top {top_n} cancer types...")
        
        # 총 발생 수 기준 정렬
        top_cancers = self.cancer_data.nlargest(top_n, '총계')
        
        return top_cancers
    
    def analyze_age_distribution(self):
        """연령별 분포 분석"""
        print("Analyzing age distribution...")
        
        # 연령대별 비율 계산
        total_cases = self.age_data['발생수'].sum()
        self.age_data['비율'] = (self.age_data['발생수'] / total_cases * 100).round(2)
        
        # 고위험 연령대 식별 (발생수 상위 3개)
        high_risk_ages = self.age_data.nlargest(3, '발생수')
        
        return {
            'total_cases': total_cases,
            'high_risk_ages': high_risk_ages,
            'age_distribution': self.age_data
        }
    
    def analyze_regional_distribution(self):
        """지역별 분포 분석"""
        print("Analyzing regional distribution...")
        
        # 인구 대비 발생률 계산을 위한 예시 인구 데이터
        population_data = {
            '서울특별시': 9720846,
            '부산광역시': 3378016,
            '대구광역시': 2401110,
            '인천광역시': 2947217,
            '광주광역시': 1441970,
            '대전광역시': 1454679,
            '울산광역시': 1124459,
            '세종특별자치시': 355831,
            '경기도': 13379311,
            '강원도': 1518500,
            '충청북도': 1595460,
            '충청남도': 2123692,
            '전라북도': 1792476,
            '전라남도': 1838353,
            '경상북도': 2625961,
            '경상남도': 3309918,
            '제주특별자치도': 672948
        }
        
        # 인구 10만명당 발생률 계산
        self.regional_data['인구'] = self.regional_data['지역'].map(population_data)
        self.regional_data['인구10만명당발생률'] = (self.regional_data['발생수'] / self.regional_data['인구'] * 100000).round(2)
        
        # 발생률 상위 지역
        high_incidence_regions = self.regional_data.nlargest(5, '인구10만명당발생률')
        
        return {
            'high_incidence_regions': high_incidence_regions,
            'regional_stats': self.regional_data
        }
    
    def generate_summary_report(self):
        """종합 분석 보고서 생성"""
        print("Generating summary report...")
        
        # 각종 분석 수행
        gender_stats = self.analyze_gender_distribution()
        top_cancers = self.analyze_top_cancers()
        age_analysis = self.analyze_age_distribution()
        regional_analysis = self.analyze_regional_distribution()
        
        # 보고서 생성
        report = {
            "분석_개요": {
                "분석_연도": "2020년",
                "총_암_발생_건수": int(self.cancer_data['총계'].sum()),
                "분석_암종_수": len(self.cancer_data),
                "분석_지역_수": len(self.regional_data)
            },
            "성별_분석": {
                "남성_발생_건수": int(gender_stats['남성']),
                "여성_발생_건수": int(gender_stats['여성']),
                "남성_비율": f"{gender_stats['남성_비율']:.1f}%",
                "여성_비율": f"{gender_stats['여성_비율']:.1f}%"
            },
            "상위_암종": {
                "1위": f"{top_cancers.iloc[0]['암종']} ({top_cancers.iloc[0]['총계']:,}건)",
                "2위": f"{top_cancers.iloc[1]['암종']} ({top_cancers.iloc[1]['총계']:,}건)",
                "3위": f"{top_cancers.iloc[2]['암종']} ({top_cancers.iloc[2]['총계']:,}건)"
            },
            "연령대_분석": {
                "총_발생_건수": int(age_analysis['total_cases']),
                "최고_위험_연령대": age_analysis['high_risk_ages'].iloc[0]['연령대'],
                "최고_위험_연령대_발생수": f"{age_analysis['high_risk_ages'].iloc[0]['발생수']:,}건"
            },
            "지역별_분석": {
                "최고_발생률_지역": regional_analysis['high_incidence_regions'].iloc[0]['지역'],
                "최고_발생률": f"{regional_analysis['high_incidence_regions'].iloc[0]['인구10만명당발생률']}명/10만명"
            }
        }
        
        # JSON 형태로 저장
        with open(self.reports_dir / 'cancer_analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 텍스트 보고서 생성
        report_text = f"""
# 2020년 한국 암 발생 통계 분석 보고서

## 📊 분석 개요
- 분석 연도: 2020년
- 총 암 발생 건수: {report['분석_개요']['총_암_발생_건수']:,}건
- 분석 암종 수: {report['분석_개요']['분석_암종_수']}개
- 분석 지역 수: {report['분석_개요']['분석_지역_수']}개

## 🚻 성별 분석
- 남성 발생 건수: {report['성별_분석']['남성_발생_건수']:,}건 ({report['성별_분석']['남성_비율']})
- 여성 발생 건수: {report['성별_분석']['여성_발생_건수']:,}건 ({report['성별_분석']['여성_비율']})

## 🏆 상위 암종 (발생 건수 기준)
1. {report['상위_암종']['1위']}
2. {report['상위_암종']['2위']}  
3. {report['상위_암종']['3위']}

## 📈 연령대별 분석
- 최고 위험 연령대: {report['연령대_분석']['최고_위험_연령대']}
- 해당 연령대 발생 건수: {report['연령대_분석']['최고_위험_연령대_발생수']}

## 🗺️ 지역별 분석  
- 인구 대비 최고 발생률 지역: {report['지역별_분석']['최고_발생률_지역']}
- 발생률: {report['지역별_분석']['최고_발생률']}

---
*본 보고서는 2020년 공공데이터를 기반으로 작성되었습니다.*
"""
        
        with open(self.reports_dir / 'cancer_analysis_summary.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print("Analysis report generated successfully!")
        return report

if __name__ == "__main__":
    analyzer = CancerDataAnalyzer()
    if analyzer.load_data():
        analyzer.generate_summary_report()