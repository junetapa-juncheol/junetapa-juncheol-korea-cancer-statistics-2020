import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 스타일 설정
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class CancerDataVisualizer:
    def __init__(self):
        self.data_dir = Path('data')
        self.charts_dir = Path('charts')
        
        # 차트 디렉토리 생성
        self.charts_dir.mkdir(exist_ok=True)
        
    def load_data(self):
        """데이터 로드"""
        try:
            self.cancer_data = pd.read_csv(self.data_dir / 'cancer_by_type_gender.csv')
            self.age_data = pd.read_csv(self.data_dir / 'cancer_by_age.csv')
            self.regional_data = pd.read_csv(self.data_dir / 'cancer_by_region.csv')
            return True
        except FileNotFoundError:
            print("Data files not found.")
            return False
    
    def create_cancer_type_chart(self):
        """암종별 발생 현황 차트"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # 1. 총 발생 건수 차트
        top_cancers = self.cancer_data.nlargest(8, '총계')
        bars1 = ax1.bar(range(len(top_cancers)), top_cancers['총계'], 
                       color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
                             '#FFEAA7', '#DDA0DD', '#98D8E8', '#F7DC6F'])
        ax1.set_title('주요 암종별 발생 건수 (2020년)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('암종')
        ax1.set_ylabel('발생 건수')
        ax1.set_xticks(range(len(top_cancers)))
        ax1.set_xticklabels(top_cancers['암종'], rotation=45, ha='right')
        
        # 값 표시
        for i, bar in enumerate(bars1):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 500,
                    f'{int(height):,}', ha='center', va='bottom', fontsize=10)
        
        # 2. 성별 비교 차트
        x = range(len(top_cancers))
        width = 0.35
        bars2 = ax2.bar([i - width/2 for i in x], top_cancers['남성'], 
                       width, label='남성', color='#4A90E2')
        bars3 = ax2.bar([i + width/2 for i in x], top_cancers['여성'], 
                       width, label='여성', color='#E24A90')
        
        ax2.set_title('암종별 성별 발생 현황', fontsize=14, fontweight='bold')
        ax2.set_xlabel('암종')
        ax2.set_ylabel('발생 건수')
        ax2.set_xticks(x)
        ax2.set_xticklabels(top_cancers['암종'], rotation=45, ha='right')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(self.charts_dir / 'cancer_by_type.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_gender_distribution_chart(self):
        """성별 분포 파이 차트"""
        total_male = self.cancer_data['남성'].sum()
        total_female = self.cancer_data['여성'].sum()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sizes = [total_male, total_female]
        labels = ['남성', '여성']
        colors = ['#4A90E2', '#E24A90']
        explode = (0.05, 0.05)
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                         autopct='%1.1f%%', startangle=90, 
                                         explode=explode, shadow=True)
        
        # 텍스트 스타일링
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        for text in texts:
            text.set_fontsize(14)
            text.set_fontweight('bold')
        
        ax.set_title('2020년 암 발생 성별 분포', fontsize=16, fontweight='bold', pad=20)
        
        # 범례 추가
        ax.legend(wedges, [f'{label}: {size:,}명' for label, size in zip(labels, sizes)],
                 loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.savefig(self.charts_dir / 'gender_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_age_distribution_chart(self):
        """연령별 분포 차트"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 1. 연령별 발생 건수 바 차트
        colors = plt.cm.viridis(range(len(self.age_data)))
        bars = ax1.bar(self.age_data['연령대'], self.age_data['발생수'], color=colors)
        ax1.set_title('연령대별 암 발생 건수', fontsize=14, fontweight='bold')
        ax1.set_xlabel('연령대')
        ax1.set_ylabel('발생 건수')
        ax1.tick_params(axis='x', rotation=45)
        
        # 값 표시
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 200,
                    f'{int(height):,}', ha='center', va='bottom', fontsize=9)
        
        # 2. 연령별 누적 차트
        cumulative = self.age_data['발생수'].cumsum()
        ax2.plot(self.age_data['연령대'], cumulative, marker='o', linewidth=3, 
                markersize=8, color='#FF6B6B')
        ax2.fill_between(self.age_data['연령대'], cumulative, alpha=0.3, color='#FF6B6B')
        ax2.set_title('연령대별 누적 발생 건수', fontsize=14, fontweight='bold')
        ax2.set_xlabel('연령대')
        ax2.set_ylabel('누적 발생 건수')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.charts_dir / 'age_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_regional_map_chart(self):
        """지역별 발생 현황 차트"""
        # 인구 데이터 추가
        population_data = {
            '서울특별시': 9720846, '부산광역시': 3378016, '대구광역시': 2401110,
            '인천광역시': 2947217, '광주광역시': 1441970, '대전광역시': 1454679,
            '울산광역시': 1124459, '세종특별자치시': 355831, '경기도': 13379311,
            '강원도': 1518500, '충청북도': 1595460, '충청남도': 2123692,
            '전라북도': 1792476, '전라남도': 1838353, '경상북도': 2625961,
            '경상남도': 3309918, '제주특별자치도': 672948
        }
        
        self.regional_data['인구'] = self.regional_data['지역'].map(population_data)
        self.regional_data['인구10만명당발생률'] = (self.regional_data['발생수'] / 
                                                    self.regional_data['인구'] * 100000).round(1)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
        
        # 1. 지역별 총 발생 건수
        sorted_data = self.regional_data.sort_values('발생수', ascending=True)
        bars1 = ax1.barh(sorted_data['지역'], sorted_data['발생수'], 
                        color='lightcoral')
        ax1.set_title('지역별 암 발생 건수', fontsize=14, fontweight='bold')
        ax1.set_xlabel('발생 건수')
        
        # 2. 인구 10만명당 발생률
        sorted_rate = self.regional_data.sort_values('인구10만명당발생률', ascending=True)
        bars2 = ax2.barh(sorted_rate['지역'], sorted_rate['인구10만명당발생률'], 
                        color='lightblue')
        ax2.set_title('지역별 인구 10만명당 암 발생률', fontsize=14, fontweight='bold')
        ax2.set_xlabel('인구 10만명당 발생률')
        
        plt.tight_layout()
        plt.savefig(self.charts_dir / 'regional_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_interactive_dashboard(self):
        """인터랙티브 대시보드 생성"""
        # Plotly를 사용한 인터랙티브 차트
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('암종별 성별 발생 현황', '성별 분포', '연령별 분포', '지역별 발생률'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # 1. 암종별 성별 발생 현황 (3D 그라데이션 효과)
        top_cancers = self.cancer_data.nlargest(8, '총계')
        fig.add_trace(
            go.Bar(x=top_cancers['암종'], y=top_cancers['남성'],
                  name='남성', 
                  marker=dict(
                      color='#4A90E2',
                      line=dict(color='#2563EB', width=2),
                      pattern_shape="/",  # 패턴 추가
                      opacity=0.9
                  ),
                  text=top_cancers['남성'],
                  textposition='outside',
                  textfont=dict(size=10, color='#2563EB')),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(x=top_cancers['암종'], y=top_cancers['여성'],
                  name='여성',
                  marker=dict(
                      color='#E24A90',
                      line=dict(color='#BE185D', width=2),
                      pattern_shape="\\",  # 패턴 추가
                      opacity=0.9
                  ),
                  text=top_cancers['여성'],
                  textposition='outside',
                  textfont=dict(size=10, color='#BE185D')),
            row=1, col=1
        )
        
        # 2. 성별 분포 (3D 파이차트 효과)
        total_male = self.cancer_data['남성'].sum()
        total_female = self.cancer_data['여성'].sum()
        fig.add_trace(
            go.Pie(labels=['남성', '여성'], 
                  values=[total_male, total_female],
                  name="성별 분포", 
                  marker=dict(
                      colors=['#4A90E2', '#E24A90'],
                      line=dict(color='#FFFFFF', width=3)
                  ),
                  textfont=dict(size=12, color='white'),
                  textinfo='label+percent+value',
                  hole=0.3,  # 도넛 형태로 입체감
                  pull=[0.1, 0.1]),  # 조각 분리 효과
            row=1, col=2
        )
        
        # 3. 연령별 분포 (그라데이션 효과)
        fig.add_trace(
            go.Bar(x=self.age_data['연령대'], y=self.age_data['발생수'],
                  name='연령별',
                  marker=dict(
                      color=self.age_data['발생수'],
                      colorscale='Viridis',  # 그라데이션 컬러스케일
                      line=dict(color='#333333', width=1),
                      opacity=0.8
                  ),
                  text=self.age_data['발생수'],
                  textposition='outside',
                  textfont=dict(size=10)),
            row=2, col=1
        )
        
        # 4. 지역별 상위 10개 (그라데이션 효과)
        top_regions = self.regional_data.nlargest(10, '발생수')
        fig.add_trace(
            go.Bar(x=top_regions['지역'], y=top_regions['발생수'],
                  name='지역별',
                  marker=dict(
                      color=top_regions['발생수'],
                      colorscale='Blues',  # 파란색 그라데이션
                      line=dict(color='#1E3A8A', width=1),
                      opacity=0.85
                  ),
                  text=top_regions['발생수'],
                  textposition='outside',
                  textfont=dict(size=10)),
            row=2, col=2
        )
        
        # 레이아웃 업데이트 (3D 및 입체감 효과)
        fig.update_layout(
            height=900, 
            showlegend=True,
            title_text="2020년 한국 암 발생 통계 대시보드",
            title_font=dict(size=20, color='#1f2937'),
            plot_bgcolor='rgba(248,250,252,0.8)',
            paper_bgcolor='rgba(255,255,255,0.95)',
            annotations=[
                dict(
                    text="<b>📄 데이터 출처 및 저작권</b><br>" +
                         "• <b>국립암센터 국가암정보센터</b>: www.cancer.go.kr<br>" +
                         "• 중앙암등록본부 (국립암센터): ncc.re.kr<br>" +
                         "• KOSIS 국가통계포털: kosis.kr<br>" +
                         "• 공공데이터포털: data.go.kr<br>" +
                         "• e-나라지표: index.go.kr<br>" +
                         "<br><b>⚠️ 이용 조건</b><br>" +
                         "• 저작자표시-비영리-변경금지<br>" +
                         "• 포트폴리오/학습 목적만 허용<br>" +
                         "• 상업적 이용 절대 금지<br>" +
                         "<i>© 국립암센터 - 비영리 포트폴리오 프로젝트</i>",
                    xref="paper", yref="paper",
                    x=0.98, y=0.25, xanchor="right", yanchor="bottom",
                    showarrow=False,
                    font=dict(size=10, color="gray"),
                    bgcolor="rgba(255,255,255,0.95)",
                    bordercolor="rgba(209,213,219,1)",
                    borderwidth=2,
                    borderpad=8
                )
            ]
        )
        
        # 각 서브플롯에 그림자 효과 추가
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(235,236,240,0.6)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(235,236,240,0.6)')
        
        # 범례 스타일링
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(209,213,219,1)",
                borderwidth=1
            )
        )
        
        # HTML 파일로 저장
        fig.write_html(str(self.charts_dir / 'interactive_dashboard.html'))
        
    def generate_all_charts(self):
        """모든 차트 생성"""
        print("Starting chart generation...")
        
        if not self.load_data():
            return
        
        print("Creating cancer type charts...")
        self.create_cancer_type_chart()
        
        print("Creating gender distribution pie chart...")
        self.create_gender_distribution_chart()
        
        print("Creating age distribution charts...")
        self.create_age_distribution_chart()
        
        print("Creating regional distribution charts...")
        self.create_regional_map_chart()
        
        print("Creating interactive dashboard...")
        self.create_interactive_dashboard()
        
        print("All charts generated successfully!")
        print("Generated files:")
        print("  - charts/cancer_by_type.png")
        print("  - charts/gender_distribution.png")
        print("  - charts/age_distribution.png")
        print("  - charts/regional_distribution.png")
        print("  - charts/interactive_dashboard.html")

if __name__ == "__main__":
    visualizer = CancerDataVisualizer()
    visualizer.generate_all_charts()