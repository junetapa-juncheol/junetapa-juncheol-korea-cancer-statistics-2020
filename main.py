#!/usr/bin/env python3
"""
한국 암 발생 통계 분석 프로젝트 (2020년)
메인 실행 스크립트
"""

import os
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python path에 추가
project_root = Path(__file__).parent
sys.path.append(str(project_root / 'src'))

from data_collector import CancerDataCollector
from data_analyzer import CancerDataAnalyzer
from visualizer import CancerDataVisualizer

def print_banner():
    """배너 출력"""
    banner = """
    ============================================================
                                                             
        Korean Cancer Statistics Analysis Project (2020)           
                                                             
      Cancer Type | Gender | Age Group | Regional Analysis        
                                                             
    ============================================================
    """
    print(banner)

def check_dependencies():
    """필요한 패키지 확인"""
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'plotly', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    
    return True

def check_api_key():
    """API 키 확인"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # dotenv가 없어도 계속 진행
        pass
    
    api_key = os.getenv('CANCER_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("Warning: API key not configured.")
        print("1. Copy .env.example to .env")
        print("2. Get API key from data.go.kr and add to .env file")
        print("3. Running with sample data for now")
        return False
    
    return True

def main():
    """메인 실행 함수"""
    print_banner()
    
    # 의존성 확인
    if not check_dependencies():
        return
    
    # API 키 확인 (없어도 샘플 데이터로 실행)
    api_key_available = check_api_key()
    if not api_key_available:
        print("Running with sample data...\n")
    
    try:
        # 1단계: 데이터 수집
        print("=" * 60)
        print("Step 1: Data Collection")
        print("=" * 60)
        collector = CancerDataCollector()
        collector.save_data()
        
        # 2단계: 데이터 분석
        print("\n" + "=" * 60)
        print("Step 2: Data Analysis")
        print("=" * 60)
        analyzer = CancerDataAnalyzer()
        if analyzer.load_data():
            report = analyzer.generate_summary_report()
            
            # 분석 결과 요약 출력
            print("\nAnalysis Summary:")
            print(f"  - Total cancer cases: {report['분석_개요']['총_암_발생_건수']:,}")
            print(f"  - Male ratio: {report['성별_분석']['남성_비율']}")
            print(f"  - Female ratio: {report['성별_분석']['여성_비율']}")
            print(f"  - Top cancer type: {report['상위_암종']['1위']}")
        
        # 3단계: 시각화
        print("\n" + "=" * 60)
        print("Step 3: Visualization")
        print("=" * 60)
        visualizer = CancerDataVisualizer()
        visualizer.generate_all_charts()
        
        # 완료 메시지
        print("\n" + "=" * 60)
        print("Analysis Complete!")
        print("=" * 60)
        print("Generated files:")
        print("  Data: data/ folder")
        print("  Charts: charts/ folder") 
        print("  Reports: reports/ folder")
        print("  Dashboard: charts/interactive_dashboard.html")
        
        print("\nNext steps:")
        print("  1. Open charts/interactive_dashboard.html in browser")
        print("  2. Check analysis reports in reports/ folder")
        print("  3. Modify src/ code if needed and re-run")
        
        if not api_key_available:
            print("\nTo use real public data:")
            print("  1. Register at https://www.data.go.kr")
            print("  2. Apply for National Cancer Center API")
            print("  3. Set API key in .env file")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Please report issues to GitHub Issues if problem persists")

if __name__ == "__main__":
    main()