from fastapi import APIRouter, HTTPException
from app.models.stock_data import StockAnalysis, StockInfo, SupplyDemand, SupplyDemandPeriod, Performance, InvestmentPoint, NewsItem, AnalystOpinion, SectorNews, InvestmentMetrics
from typing import Dict

router = APIRouter()

# 시연용 목 데이터
MOCK_DATA: Dict[str, StockAnalysis] = {
    "005930": StockAnalysis(
        stock_info=StockInfo(
            code="005930",
            name="삼성전자",
            current_price=101700,
            change_rate=-1.74,
            change_price=-1800,
            volume=5335381,
            ai_summary="[긍정] 삼성전자는 최근 6건의 긍정 뉴스가 보도되며 HBM 개발 강화와 AI 팩토리 혁신에 집중하는 매우 강한 긍정적 흐름을 보이고 있습니다.\n\n📈 핵심 긍정 요인 (6건):\n삼성전자가 DS부문을 재편하여 HBM 전담 개발조직을 확대하고 메모리·낸드 조직을 통합했습니다. 디지털트윈센터를 신설하고 엔비디아 GPU 5만 장을 도입하여 공정·설비·소재를 가상환경에서 시뮬레이션하는 AI 기반 팩토리 구축에 착수했습니다. 스마트팩토리 TF를 신설하여 실시간 데이터 분석과 예측 유지보수로 생산 효율성을 극대화하고 있습니다. SK텔레콤과 차세대 6G AI-RAN 공동 개발 MOU를 체결했으며, AI·로봇·반도체 중심으로 161명을 임원 승진시키고 2인 CEO체제를 복귀하여 AI 연구를 강화했습니다. 2028년까지 국내에 450조원을 투자하고 평택 P5 팹을 가동할 계획입니다.\n\n💰 수급 분석:\n하루 기준으로 외국인이 3,093억원, 기관이 4,552억원을 순매수하며 강한 동반 매수세를 보이고 있습니다. 최근 1개월간 외국인이 6,435억원을 지속 순매수하며 AI 반도체에 대한 기대감을 반영하고 있습니다.\n\n🎯 증권가 컨센서스:\n평균 목표가는 148,333원으로 현재가 대비 약 46% 상승 여력이 있습니다. KB증권 160,000원, 한국투자증권 150,000원, BNK증권 135,000원(상향)으로 모든 증권사가 매수 의견을 제시하며 강력한 Buy 컨센서스를 형성하고 있습니다."
        ),
        news_summary="""<div class="news-item positive">
<div class="news-header">📈 11/27 DS부문 재편, HBM 개발 조직 강화 및 디지털트윈센터 신설 <span class="news-importance">★★★★★</span></div>
<div class="news-content">삼성전자 DS부문이 메모리 개발과 낸드 조직을 통합하고 HBM 전담 개발조직을 확대했습니다. 또한 '디지털트윈센터'를 신설하여 엔비디아 GPU 5만 장을 도입하고, 공정·설비·소재 등을 가상환경에서 시뮬레이션하는 AI 기반 팩토리 구축에 착수했습니다. 이번 조직개편은 AI 반도체 수요 급증에 선제 대응하기 위한 전략적 움직임으로, HBM 경쟁력 강화와 제조 혁신을 동시에 추진하는 핵심 과제입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/27 스마트팩토리 TF 신설, 제조 AI 혁신 본격화 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">삼성전자는 스마트팩토리 TF를 신설하고 앞으로 수년간 제조 공정 전반에 AI를 도입할 계획입니다. 실시간 데이터 분석과 예측 유지보수로 생산 효율성을 극대화하며 반도체 제조 혁신을 가속화할 전망입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/26 삼성전자·SK텔레콤, 6G AI-RAN 공동 개발 MOU <span class="news-importance">★★★★☆</span></div>
<div class="news-content">두 회사가 차세대 6G 통신을 위해 AI 기반 라디오액세스네트워크 기술을 공동 개발하기로 합의했습니다. 채널 추정, 분산 MIMO, AI 스케줄러 등 핵심 기술을 개발하며 6G 시대를 선도할 전망입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/25 2026년 정기 임원 승진… AI·로봇·반도체 중심 161명 승진 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">삼성전자는 부사장 51명, 상무 93명, 펠로우 1명, 마스터 16명을 승진시키며 젊은 리더 발탁과 AI·로봇·반도체 분야 역량 강화를 강조했습니다. 미래 기술 경쟁력을 높이기 위한 인사로 평가받고 있습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/21 사장단 인사 및 2인 CEO체제 복귀 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">삼성전자가 2026년 사장단 인사를 실시해 신임 사장을 선임하고 기존 임원을 재배치했습니다. AI 및 차세대 기기 연구를 강화하고 사업부 간 협력을 위한 투 CEO체제를 복원했습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/16 국내 5년간 450조 원 투자 발표 <span class="news-importance">★★★★★</span></div>
<div class="news-content">삼성그룹이 2028년까지 반도체·AI 데이터센터 등 국내 연구개발과 생산시설에 450조 원을 투자하고 평택 P5 팹을 2028년부터 가동한다는 계획을 밝혔습니다. 국내 반도체 산업 경쟁력 강화의 핵심 동력이 될 전망입니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: DS부문 재편으로 HBM 개발 조직 강화 및 디지털트윈센터 신설, 스마트팩토리 TF 신설, 6G AI-RAN 공동 개발, AI·로봇·반도체 중심 161명 승진, 2인 CEO체제 복귀, 국내 450조원 투자 등 6건의 긍정 뉴스가 보도되며 AI와 HBM에 집중하는 매우 강력한 긍정적 흐름입니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="+3,093억원",
            institution_net="+4,552억원",
            individual_net="-7,864억원",
            summary="외국인과 기관의 동반 매수세가 이어지며 개인 투자자의 차익실현 물량을 흡수하는 모습입니다. HBM3E 양산 소식이 나오며 AI 반도체에 대한 기대감이 반영되고 있습니다.",
            period_data=[
                SupplyDemandPeriod(
                    period="1주일", 
                    foreign_net="+670억원", 
                    institution_net="+10,249억원", 
                    individual_net="-11,666억원",
                    summary="최근 1주일간 기관의 강력한 매수세가 두드러지며 1조원 이상 순매수를 기록했습니다. HBM3E 엔비디아 공급 승인 소식과 갤럭시 S25 사전 예약 호조로 투자 심리가 크게 개선되었습니다. 외국인은 파운드리와 HBM 사업부 성장 기대감으로 670억원 순매수했으며, 기관은 실적 개선 전망에 1조원 이상을 대규모 매수했습니다. 개인은 주가 상승에 따른 차익 실현으로 1.2조원 가량 매도했습니다."
                ),
                SupplyDemandPeriod(
                    period="1개월", 
                    foreign_net="+6,435억원", 
                    institution_net="-11,034억원", 
                    individual_net="+3,227억원",
                    summary="최근 1개월간 외국인의 꾸준한 매수세가 이어지며 6,435억원의 순매수를 기록했습니다. AI 반도체 시장 확대와 메모리 반도체 가격 상승 사이클 진입으로 중장기 성장성에 대한 기대감이 반영되고 있습니다. 기관은 단기 수익 실현으로 1.1조원을 순매도했으며, 개인은 저가 매수 기회로 판단하고 3,227억원을 순매수했습니다."
                )
            ]
        ),
        performance=Performance(
            revenue="326.4조원",
            operating_profit="38.2조원",
            net_profit="37.2조원",
            summary="2025년 연간 실적 컨센서스는 메모리 반도체 부문의 회복과 HBM3E 양산으로 전년 대비 견조한 성장이 예상됩니다. 영업이익은 전년 대비 16.8% 증가한 38.2조원으로 전망되며, HBM과 DDR5 고부가 제품 비중 확대로 수익성이 개선될 것으로 보입니다.",
            revenue_yoy="+8.5%",
            revenue_qoq="N/A",
            operating_profit_yoy="+16.8%",
            operating_profit_qoq="N/A",
            operating_profit_vs_consensus="N/A",
            earnings_surprise="순이익 전년대비 +10.6%"
        ),
        investment_points=InvestmentPoint(
            positive=[
                "HBM3E 엔비디아 공급 승인으로 AI 메모리 시장 진입 본격화",
                "메모리 반도체 업황 회복과 가격 상승세 지속 전망",
                "파운드리 2나노 공정 개발로 기술 경쟁력 강화",
                "갤럭시 AI 탑재로 프리미엄 스마트폰 수요 증가",
                "배당 확대 정책으로 주주환원율 개선 기대"
            ],
            negative=[
                "중국 반도체 규제 강화로 일부 매출 영향 우려",
                "파운드리 사업 수율 개선 지연 시 실적 부담 가능",
                "환율 변동성 확대로 영업이익 변동성 존재",
                "글로벌 경기 둔화 시 IT 수요 감소 리스크"
            ]
        ),
        recent_issues=[
            NewsItem(
                date="2025.11.26",
                title="삼성전자, HBM3E 양산 본격화로 엔비디아 공급량 2배 확대",
                summary="HBM3E 12단 제품 양산 본격화, 엔비디아 월간 공급량 2배 확대로 2026년 HBM 시장 점유율 30% 목표 달성 가속화",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.25",
                title="파운드리 2나노 공정 고객사 확대 발표",
                summary="추가 3개사 선주문 계약 체결, 총 계약 규모 15조원 돌파, 2026년 파운드리 매출 30% 이상 성장 전망",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.24",
                title="4분기 영업이익 10.5조원 전망, 컨센서스 +10% 상회",
                summary="HBM3E 양산 확대로 HBM 비중 22% 확대, DDR5 가격 10% 상승으로 수익성 크게 개선",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.23",
                title="갤럭시 S25 출시, 사전 예약 200만대 돌파",
                summary="온디바이스 AI 기능 강화로 전작 대비 25% 증가, 울트라 모델 예약률 45%로 평균 판매가 상승 기여",
                url="#",
                sentiment="positive"
            )
        ],
        analyst_opinions=[
            AnalystOpinion(
                target_price="160,000원",
                opinion="HBM3E 양산 본격화와 AI 반도체 시장 확대로 실적 모멘텀 강화. 투자의견 매수 유지",
                firm="KB증권",
                trend="neutral"
            ),
            AnalystOpinion(
                target_price="150,000원",
                opinion="메모리 업황 회복세 지속, 파운드리 경쟁력 강화. 투자의견 매수 유지",
                firm="한국투자증권",
                trend="neutral"
            ),
            AnalystOpinion(
                target_price="135,000원",
                opinion="4분기 실적 개선 전망, HBM 비중 확대로 수익성 개선. 목표가 상향",
                firm="BNK증권",
                trend="up"
            )
        ],
        analyst_summary="최근 증권사들의 목표가는 **매우 낙관적인 수준**을 유지하고 있습니다. KB증권은 160,000원으로 가장 높은 목표가를 제시했으며, 한국투자증권 150,000원, BNK증권 135,000원(상향)으로 평가했습니다. 평균 목표가 148,333원은 현재가 대비 **약 50% 상승 여력**이 있으며, 모든 증권사가 '매수' 의견으로 강력한 매수 컨센서스를 보이고 있습니다. HBM3E 양산 본격화와 AI 반도체 모멘텀이 핵심 투자 포인트입니다.",
        sector_name="반도체",
        sector_news=[
            SectorNews(
                date="2025.11.26",
                title="글로벌 반도체 시장, AI 반도체 중심 성장세 가속화",
                summary="2025년 글로벌 반도체 시장 규모는 전년 대비 18% 성장한 6,250억 달러로 상향 조정. AI GPU와 HBM이 주도하며 2026년까지 성장세 지속 전망",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.25",
                title="HBM 수요 폭발 지속, 2026년까지 공급 부족 심화",
                summary="엔비디아, AMD, 구글 등 빅테크의 AI 인프라 투자 확대로 HBM 수요 급증. 공급 부족이 2026년 하반기까지 지속될 것으로 전망되며 가격 상승세 지속",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.24",
                title="미국 반도체 보조금 집행 가속화, 삼성·SK 추가 수혜",
                summary="미국 CHIPS Act 보조금 집행이 가속화되며 삼성 텍사스 공장에 추가 20억 달러 지원 확정. SK 인디애나 공장도 추가 지원 검토 중",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.23",
                title="중국 반도체 굴기, 한국 기업 첨단 공정 격차 유지 전략",
                summary="중국 SMIC 7나노 공정 양산 개시에도 불구하고 한국 반도체 기업들은 2나노 이하 첨단 공정으로 기술 격차를 유지하며 경쟁력 확보",
                sentiment="neutral"
            )
        ],
        investment_metrics=InvestmentMetrics(
            per="21.12배",
            pbr="1.68배",
            roe="8.37%",
            dividend_yield="1.42%",
            market_cap="602.3조원",
            shares_outstanding="59.2억주"
        )
    ),
    "000660": StockAnalysis(
        stock_info=StockInfo(
            code="000660",
            name="SK하이닉스",
            current_price=541000,
            change_rate=-0.55,
            change_price=-3000,
            volume=1163269,
            ai_summary="[긍정] SK하이닉스는 최근 5건의 긍정 뉴스와 2건의 부정 뉴스가 보도되며 HBM 시장 리더십과 기술 혁신을 이어가고 있습니다.\n\n📈 핵심 긍정 요인 (5건):\n세계 최초 48Gbps GDDR7 DRAM을 2026년 국제고체회로학회에서 공개할 예정이며, 기존 28Gbps 대비 속도가 70% 향상되어 그래픽·AI 메모리 시장을 선도할 전망입니다. SK그룹의 3분기 수출 87.8조원 중 SK하이닉스가 65%를 차지하며 HBM 메모리 호황으로 국가 경제에 크게 기여하고 있습니다. AI 랠리 속에서 외국인 투자자가 7일간의 매도세를 멈추고 순매수로 전환하며 주가가 3.63% 상승했습니다. HBM 칩스 스낵을 출시하여 대중에게 브랜드 친숙도를 높이는 마케팅 활동도 펼치고 있습니다.\n\n📉 주요 리스크 (2건):\n2025년 들어 외국인이 SK하이닉스를 9.9조원 순매도하고 삼성전자로 자금을 이동시키고 있습니다. 주가가 고점 대비 12% 하락하며 개인투자자의 절반이 손실을 본 것으로 추정되어 밸류에이션 부담이 제기되고 있습니다.\n\n💰 수급 분석:\n하루 기준으로 외국인이 3,148억원 매도했으나 기관이 2,977억원 매수하며 방어했습니다. 최근 1주일간 외국인이 2.6조원을 대규모 매도했지만 개인과 기관이 합쳐 2.6조원을 순매수하며 받아냈습니다. 최근 1개월간은 외국인이 12.4조원을 매도한 반면 개인이 9.5조원을 매수하며 국내 투자자들의 강력한 매수세가 두드러지고 있습니다.\n\n🎯 증권가 컨센서스:\n평균 목표가는 703,333원으로 현재가 대비 약 30% 상승 여력이 있습니다. 키움증권 730,000원, 한국투자증권 700,000원, iM증권 680,000원(중립)으로 평가되며, 67%가 매수 의견으로 HBM 독점 지위 유지를 전망하고 있습니다."
        ),
        news_summary="""<div class="news-item positive">
<div class="news-header">📈 11/27 AI 랠리 속 외국인 순매수 전환, 주가 3.63% 상승 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">뉴욕 시장에서 AI 및 반도체주가 상승하자 외국인 투자자가 7일간의 매도세를 멈추고 순매수로 전환해 SK하이닉스 주가가 3.63% 상승했습니다. AI 메모리 수요 회복 기대감이 반영되고 있습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/27 외국인, SK하이닉스 9.9조 매도·삼성전자 8.5조 매수 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">2025년 들어 외국인은 SK하이닉스를 9조9000억 원 순매도하고 삼성전자를 8조5000억 원 순매수했습니다. SK하이닉스의 밸류에이션이 높고 삼성전자가 저평가됐다는 판단 때문으로 보입니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/27 "개미 절반 손실"… SK하이닉스 고점 대비 12% 하락 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">SK하이닉스 주가가 일주일 사이 12.3% 하락해 개인투자자의 절반이 손실을 본 것으로 추정되며, 일부 투자자는 저점 매수 기회로 삼아 1조 원 이상을 매수한 것으로 나타났습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/26 세계 최초 48 Gbps GDDR7 DRAM 공개 예정 <span class="news-importance">★★★★★</span></div>
<div class="news-content">SK하이닉스는 2026년 국제고체회로학회(ISSCC)에서 세계 최고 속도의 48 Gbps GDDR7 DRAM을 발표합니다. 기존 28 Gbps 대비 속도가 70% 향상돼 그래픽·AI 메모리 시장을 선도할 전망입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/26 'HBM 칩스' 스낵 출시로 브랜드 친숙도 제고 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">SK하이닉스는 편의점과 협력해 HBM 패키지 모양의 과자 'HBM 칩스'를 출시했습니다. 꿀바나나 맛 스낵으로 반도체를 대중에게 친숙하게 알리는 마케팅 활동입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/25 SK그룹, SK하이닉스 경제 기여 강조 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">SK그룹은 공정위에 제출한 자료에서 SK하이닉스가 국내 수출과 법인세 납부에서 큰 비중을 차지하며 국가 성장엔진이라고 강조했습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/25 SK 그룹 수출 87.8조… HBM 메모리 호황이 견인 <span class="news-importance">★★★★★</span></div>
<div class="news-content">SK그룹의 3분기 수출이 전년 대비 20% 증가한 87조8000억 원에 달했고, SK하이닉스가 65%를 차지했습니다. HBM 메모리 수요가 급증하면서 수출과 세금 납부가 크게 늘었습니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: AI 랠리 속 외국인 순매수 전환, 세계 최초 48 Gbps GDDR7 DRAM 공개 예정, HBM 칩스 스낵 출시, SK그룹 경제 기여 강조, SK 그룹 수출 87.8조원으로 HBM 메모리 호황 견인 등 5건의 긍정 뉴스가 이어집니다. 다만 외국인의 연간 9.9조원 순매도와 주가 12% 하락으로 개인 투자자 손실 등 2건의 부정 요인이 있습니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="-3,148억원",
            institution_net="+2,977억원",
            individual_net="-64억원",
            summary="외국인의 매도세가 나타났으나 기관의 강력한 매수세로 상쇄되고 있습니다. HBM4 개발 순조와 엔비디아 독점 공급 지위 유지로 기관 투자 심리가 매우 긍정적입니다.",
            period_data=[
                SupplyDemandPeriod(
                    period="1주일", 
                    foreign_net="-26,073억원", 
                    institution_net="+11,871억원", 
                    individual_net="+13,752억원",
                    summary="최근 1주일간 외국인의 대규모 매도세가 나타나며 2.6조원을 순매도했습니다. 높은 밸류에이션 부담과 단기 차익 실현 목적의 매도로 보입니다. 반면 기관은 1.2조원, 개인은 1.4조원을 순매수하며 HBM4 샘플이 엔비디아 테스트를 통과한 호재를 긍정적으로 평가했습니다. 국내 투자자들의 저가 매수세가 두드러졌습니다."
                ),
                SupplyDemandPeriod(
                    period="1개월", 
                    foreign_net="-12.43조원", 
                    institution_net="+2.36조원", 
                    individual_net="+9.49조원",
                    summary="최근 1개월간 외국인이 무려 12.43조원을 순매도하며 차익 실현과 포트폴리오 조정을 단행했습니다. 주가가 고점권에 진입하면서 밸류에이션 부담으로 일부 포지션을 청산한 것으로 보입니다. 반면 개인은 9.49조원, 기관은 2.36조원을 순매수하며 AI 메모리 시장의 중장기 성장성과 HBM 독점 지위를 높이 평가했습니다. 국내 투자자들의 강력한 바이코리아 매수세가 두드러졌습니다."
                )
            ]
        ),
        performance=Performance(
            revenue="92.5조원",
            operating_profit="42.3조원",
            net_profit="38.6조원",
            summary="2025년 연간 실적 컨센서스는 HBM 시장 독점과 AI 메모리 수요 폭발로 전년 대비 폭발적인 성장이 예상됩니다. 매출은 39.8% 증가한 92.5조원, 영업이익은 80.3% 증가한 42.3조원으로 전망되며, HBM 매출 비중 확대로 영업이익률이 45% 이상을 기록할 것으로 보입니다.",
            revenue_yoy="+39.8%",
            revenue_qoq="N/A",
            operating_profit_yoy="+80.3%",
            operating_profit_qoq="N/A",
            operating_profit_vs_consensus="N/A",
            earnings_surprise="순이익 전년대비 +94.8%"
        ),
        investment_points=InvestmentPoint(
            positive=[
                "HBM 시장 점유율 50% 이상 유지하며 독점적 지위 확보",
                "엔비디아 H200, GB200 등 차세대 AI GPU용 HBM 독점 공급",
                "2025년 HBM 매출 20조원 이상 전망, 전년 대비 2배 성장",
                "HBM4 개발 선도하며 기술 격차 확대",
                "미국 패키징 공장 가동으로 공급망 안정성 강화"
            ],
            negative=[
                "HBM 가격 인상 여력 제한적, 수익성 정점 논란",
                "삼성전자의 HBM 시장 진입으로 경쟁 심화 우려",
                "AI 투자 사이클 둔화 시 재고 증가 리스크",
                "높은 밸류에이션 부담, 주가 변동성 확대 가능"
            ]
        ),
        recent_issues=[
            NewsItem(
                date="2025.11.26",
                title="HBM4 샘플 엔비디아 테스트 통과, 2026년 상반기 양산 확정",
                summary="차세대 HBM4 제품 엔비디아 품질 테스트 통과, 대역폭 50% 향상으로 AI GPU 성능 혁신 기대",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.25",
                title="미국 인디애나 패키징 공장 가동률 90% 달성",
                summary="첨단 패키징 공장 본격 가동 성공, 미국 AI 공급망 핵심 파트너로 부상",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.24",
                title="4분기 영업이익 7.8조원 전망, 컨센서스 +8.5% 상회",
                summary="HBM3E 출하량 50% 증가와 DDR5 가격 12% 상승으로 실적 모멘텀 강화",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.23",
                title="엔비디아 GB200용 HBM3E 공급량 추가 확대",
                summary="엔비디아 차세대 AI 슈퍼칩용 HBM3E 12단 공급량 추가 확대 계약 체결, 2026년 HBM 매출 22조원 전망",
                url="#",
                sentiment="positive"
            )
        ],
        analyst_opinions=[
            AnalystOpinion(
                target_price="730,000원",
                opinion="HBM4 개발 선도하며 AI 메모리 시장 독점. 투자의견 매수 유지",
                firm="키움증권",
                trend="neutral"
            ),
            AnalystOpinion(
                target_price="700,000원",
                opinion="엔비디아 독점 공급 지위 유지, 2026년 매출 성장 가속화. 투자의견 매수 유지",
                firm="한국투자증권",
                trend="neutral"
            ),
            AnalystOpinion(
                target_price="680,000원",
                opinion="HBM 실적 모멘텀 강력하나 높은 밸류에이션 부담. 투자의견 중립",
                firm="iM증권",
                trend="neutral"
            )
        ],
        analyst_summary="최근 증권사들의 목표가는 **매우 높은 수준**을 유지하고 있습니다. 키움증권이 730,000원으로 가장 높은 목표가를 제시했으며, 한국투자증권 700,000원, iM증권 680,000원으로 평가했습니다. 평균 목표가 703,333원은 현재가 대비 **약 31% 상승 여력**이 있으나, iM증권이 밸류에이션 부담으로 '중립' 의견을 제시하며 일부 신중론도 존재합니다. 67%가 '매수' 의견이며, HBM4 독점과 AI 메모리 시장 성장이 핵심 투자 포인트입니다.",
        sector_name="반도체",
        sector_news=[
            SectorNews(
                date="2025.11.26",
                title="글로벌 반도체 시장, AI 반도체 중심 성장세 가속화",
                summary="2025년 글로벌 반도체 시장 규모는 전년 대비 18% 성장한 6,250억 달러로 상향 조정. AI GPU와 HBM이 주도하며 2026년까지 성장세 지속 전망",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.25",
                title="HBM 수요 폭발 지속, 2026년까지 공급 부족 심화",
                summary="엔비디아, AMD, 구글 등 빅테크의 AI 인프라 투자 확대로 HBM 수요 급증. 공급 부족이 2026년 하반기까지 지속될 것으로 전망되며 가격 상승세 지속",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.24",
                title="미국 반도체 보조금 집행 가속화, 삼성·SK 추가 수혜",
                summary="미국 CHIPS Act 보조금 집행이 가속화되며 삼성 텍사스 공장에 추가 20억 달러 지원 확정. SK 인디애나 공장도 추가 지원 검토 중",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.23",
                title="중국 반도체 굴기, 한국 기업 첨단 공정 격차 유지 전략",
                summary="중국 SMIC 7나노 공정 양산 개시에도 불구하고 한국 반도체 기업들은 2나노 이하 첨단 공정으로 기술 격차를 유지하며 경쟁력 확보",
                sentiment="neutral"
            )
        ],
        investment_metrics=InvestmentMetrics(
            per="11.02배",
            pbr="3.73배",
            roe="43.20%",
            dividend_yield="0.41%",
            market_cap="393.5조원",
            shares_outstanding="7.28억주"
        )
    ),
    "006800": StockAnalysis(
        stock_info=StockInfo(
            code="006800",
            name="미래에셋증권",
            current_price=21950,
            change_rate=-1.13,
            change_price=-250,
            volume=1131881,
            ai_summary="[긍정] 미래에셋증권은 최근 7건의 긍정 뉴스가 보도되며 IB 부문 강세와 새로운 사업 기회 확대로 매우 긍정적인 흐름을 보이고 있습니다.\n\n📈 핵심 긍정 요인 (7건):\n정부가 종합투자계좌(IMA) 사업자로 미래에셋증권을 선정하며 생산적 금융 시장에서 새로운 사업 기회를 확보했습니다. 전문가들은 WM·IB 시너지 확대와 신규 수익원 창출을 긍정적으로 평가하고 있습니다. 외국인이 801만주, 기관이 140만주를 순매수하며 주가가 5.24% 급등했고, 우선주(2우B)도 외국인·기관 매수세로 3% 상승하며 동반 강세를 보였습니다. 여행 플랫폼 마이리얼트립(가입자 1천만명, 연 거래액 2.3조원)이 내년 IPO 대표 주관사로 미래에셋증권을 선정하며 IB 수주가 확대되고 있습니다. 12월 5일 자사주 405만주(383억원)를 소각하기로 결정하여 주주환원 정책을 강화했습니다. 47만명 학생에게 장학금을 지원하고 봉사 프로그램을 운영하며 사회적 가치를 실현하고 있습니다. 은퇴자산 50조원을 돌파하며 AI·디지털 역량을 강조하는 캠페인을 진행했습니다.\n\n💰 수급 분석:\n하루 기준으로 외국인이 8억원 소폭 매도했으나 기관이 85억원 매수하며 기관 매수가 주도하고 있습니다. 최근 1개월간 개인이 2,006억원을 지속 순매수하며 배당 매력(3.11%)과 성장성을 평가하고 있습니다.\n\n🎯 증권가 컨센서스:\n평균 목표가는 27,000원으로 현재가 대비 약 23% 상승 여력이 있습니다. 유안타증권 29,000원, 하나증권 26,000원, 한국투자증권 26,000원(중립)으로 평가되며, 67%가 매수 의견으로 IB·WM 사업의 성장성을 긍정적으로 전망하고 있습니다."
        ),
        news_summary="""<div class="news-item positive">
<div class="news-header">📈 11/28 IMA 사업자 선정, 생산적 금융 시장 진출 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">정부가 '생산적 금융' 육성을 강조하며 종합투자계좌(IMA) 사업자로 미래에셋증권과 한국투자증권을 선정했습니다. IMA는 자기자본 8조원 이상의 종합금융투자사업자만 취급할 수 있으며, 고객 예탁금의 70% 이상을 기업대출·회사채·벤처투자 등에 운용하는 신규 사업입니다. 미래에셋증권의 발행어음 잔고는 8조 4,000억원으로 한도 대비 40% 수준입니다. 전문가들은 새로운 시장 기회와 WM·IB 시너지 확대가 기대된다고 평가합니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/26 외국인 801만주·기관 140만주 순매수, 주가 5% 급등 <span class="news-importance">★★★★★</span></div>
<div class="news-content">외국인이 801만 주, 기관이 140만 주를 순매수해 주가가 5.24% 오른 22,100원에 마감했습니다. 강한 매수세로 증권주 중 가장 높은 상승률을 기록했습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/26 우선주(2우B)도 외국인·기관 매수세… 3% 상승 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">Mirae Asset 2우B 주식에서 외국인 153만 주와 기관 140만 주가 순매수하며 주가가 3.13% 상승했습니다. 보통주와 우선주 모두 강한 매수세를 보였습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/26 마이리얼트립, 미래에셋증권을 상장 주관사로 선정 <span class="news-importance">★★★★★</span></div>
<div class="news-content">여행 플랫폼 마이리얼트립이 내년 IPO를 준비하며 미래에셋증권을 대표 주관사로, 삼성증권을 공동 주관사로 선정했습니다. 가입자 1,000만 명, 연간 거래액 2.3조 원 규모로 성장성이 높습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/25 자사주 3,236,748주 소각 결정… 383억원 규모 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">회사는 12월 5일에 약 323만 주(보통주)와 82만 주(우선주)를 소각해 총 383.36억원 규모의 자사주를 소각할 계획입니다. 주주환원 정책 강화로 평가받고 있습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/24 장학·봉사·청년희망 등 사회공헌 활동 소개 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">미래에셋증권이 47만 명의 학생에게 장학금을 지원하고 봉사활동과 기부 프로그램, 청년희망 프로젝트, 시니어 지원 서비스 등을 펼치고 있다고 소개했습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/23 '빅픽처' 은퇴자산 캠페인 – 자산 배분과 AI 기술 강조 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">은퇴자산 50조 원을 돌파한 미래에셋증권이 글로벌 자산 배분과 AI·디지털 기술 역량을 강조하는 캠페인을 진행했습니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: IMA 사업자 선정으로 새로운 시장 기회 확보, 외국인·기관 대량 순매수로 주가 5% 급등, 우선주도 3% 상승, 마이리얼트립 IPO 주관사 선정, 자사주 383억원 규모 소각, 사회공헌 활동, 은퇴자산 50조원 돌파 캠페인 등 7건의 긍정 뉴스가 보도되며 매우 긍정적인 흐름입니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="-8억원",
            institution_net="+85억원",
            individual_net="-72억원",
            summary="기관의 매수세가 두드러지며 85억원을 순매수했습니다. 외국인과 개인은 일부 차익실현 중입니다. 대형 IPO 주관 수주와 해외주식 거래 확대가 긍정적으로 평가받고 있습니다.",
            period_data=[
                SupplyDemandPeriod(
                    period="1주일", 
                    foreign_net="-238억원", 
                    institution_net="+23억원", 
                    individual_net="+216억원",
                    summary="최근 1주일간 외국인이 238억원을 순매도하며 차익 실현에 나섰습니다. 반면 개인은 216억원을 순매수하며 증시 거래대금 감소에도 불구하고 대형 IPO 수주 호재를 긍정적으로 평가했습니다. 기관도 23억원을 소폭 매수하며 IB 부문 실적 개선 기대감을 반영했습니다."
                ),
                SupplyDemandPeriod(
                    period="1개월", 
                    foreign_net="-2,231억원", 
                    institution_net="+274억원", 
                    individual_net="+2,006억원",
                    summary="최근 1개월간 외국인이 2,231억원을 순매도하며 포지션을 축소했습니다. 증시 거래대금 감소와 수수료 인하 경쟁 심화로 단기 수익성 압박을 우려한 것으로 보입니다. 반면 개인은 2,006억원을 순매수하며 배당 매력과 웰스케어 자산관리 사업 성장을 긍정적으로 평가했습니다. 기관도 274억원을 순매수하며 ROE 16% 이상의 높은 수익성에 주목했습니다."
                )
            ]
        ),
        performance=Performance(
            revenue="25.7조원",
            operating_profit="1.38조원",
            net_profit="1.24조원",
            summary="2025년 연간 실적 컨센서스는 해외주식 거래 증가와 IB 부문 호조로 전년 대비 견조한 성장이 예상됩니다. 매출은 15.6% 증가한 25.7조원, 순이익은 34.5% 증가한 1.24조원으로 전망되며, 웰스케어 자산관리 사업 확대와 디지털 혁신으로 ROE 10% 이상을 유지할 것으로 보입니다.",
            revenue_yoy="+15.6%",
            revenue_qoq="N/A",
            operating_profit_yoy="+16.4%",
            operating_profit_qoq="N/A",
            operating_profit_vs_consensus="N/A",
            earnings_surprise="순이익 전년대비 +34.5%"
        ),
        investment_points=InvestmentPoint(
            positive=[
                "국내 1위 증권사 지위와 글로벌 네트워크 경쟁력",
                "해외주식 거래 플랫폼 강화로 MZ세대 유입 지속",
                "웰스케어 자산관리 서비스 확대로 고액 자산가 확보",
                "디지털 자산 사업 진출로 신성장 동력 확보",
                "안정적인 배당 정책으로 주주환원율 4% 이상 유지"
            ],
            negative=[
                "증시 거래대금 감소 시 브로커리지 수익 타격",
                "금리 변동성 확대 시 IB 실적 불확실성",
                "경쟁 격화로 수수료 인하 압력 지속",
                "규제 강화 리스크 (가상자산, 공매도 등)"
            ]
        ),
        recent_issues=[
            NewsItem(
                date="2025.11.26",
                title="미래에셋증권, 대형 IPO 3건 주관 수주로 IB 부문 실적 호조",
                summary="시가총액 1조원 이상 대형 IPO 3건 대표 주관사 선정, 약 420억원 수수료 수입 예상",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.25",
                title="해외주식 거래량 전월 대비 35% 증가",
                summary="수수료 인하 효과로 해외주식 거래량 급증, 브로커리지 수익 크게 개선",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.24",
                title="웰스케어 자산관리 고객 1.8만명 돌파",
                summary="프리미엄 자산관리 서비스 성장세 지속, 총 관리자산 99조원 달성",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.23",
                title="4분기 순이익 1.6조원 전망, 컨센서스 +12% 상회",
                summary="브로커리지와 IB 부문 동반 성장으로 컨센서스 대비 12% 초과 달성 전망",
                url="#",
                sentiment="positive"
            )
        ],
        analyst_opinions=[
            AnalystOpinion(
                target_price="29,000원",
                opinion="IB 부문 호조와 해외주식 거래 확대로 실적 개선. 투자의견 매수 유지",
                firm="유안타증권",
                trend="neutral"
            ),
            AnalystOpinion(
                target_price="26,000원",
                opinion="웰스케어 자산관리 성장세 지속, 브로커리지 안정적. 투자의견 매수 유지",
                firm="하나증권",
                trend="neutral"
            ),
            AnalystOpinion(
                target_price="26,000원",
                opinion="증시 거래대금 감소 우려, 단기 실적 불확실성. 투자의견 중립",
                firm="한국투자증권",
                trend="neutral"
            )
        ],
        analyst_summary="최근 증권사들의 목표가는 **26,000~29,000원 범위**를 형성하고 있습니다. 유안타증권이 29,000원으로 가장 높은 목표가를 제시했으며, 하나증권과 한국투자증권은 26,000원으로 평가했습니다. 평균 목표가 27,000원은 현재가 대비 **약 23% 상승 여력**이 있으며, 67%가 '매수' 의견입니다. 다만 한국투자증권은 증시 거래대금 감소 우려로 '중립' 의견을 제시하며 단기 실적 불확실성을 경고하고 있습니다. IB 부문 호조와 웰스케어 사업 성장이 핵심 포인트입니다.",
        sector_name="증권",
        sector_news=[
            SectorNews(
                date="2025.11.26",
                title="증권업계, AI 투자 플랫폼 경쟁 가속화",
                summary="미래에셋·삼성·NH투자증권 등 주요 증권사들이 AI 기반 투자 정보 서비스 고객 확보 경쟁 가속. 가입자 수 경쟁 치열",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.25",
                title="증권사 IB 부문 실적 호조 지속, 대형 IPO 대기 증가",
                summary="2025년 하반기 대형 IPO 대기 기업 증가로 증권사 IB 부문 수수료 수입 증가 전망. 2026년 상반기까지 호조 지속 예상",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.24",
                title="자산관리 플랫폼 경쟁, 웰스테크 투자 확대",
                summary="증권사들의 디지털 자산관리 플랫폼 투자 확대. MZ세대 고액 자산가 확보 경쟁 가속화",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.23",
                title="해외주식 거래 수수료 인하 경쟁 심화",
                summary="증권업계 해외주식 수수료 인하 경쟁 가속. 미국 주식 평균 수수료 0.08% 이하로 하락하며 수익성 압박",
                sentiment="negative"
            )
        ],
        investment_metrics=InvestmentMetrics(
            per="13.23배",
            pbr="1.05배",
            roe="10.33%",
            dividend_yield="3.11%",
            market_cap="12.5조원",
            shares_outstanding="5.70억주"
        )
    ),
    "373220": StockAnalysis(
        stock_info=StockInfo(
            code="373220",
            name="LG에너지솔루션",
            current_price=413000,
            change_rate=-5.71,
            change_price=-25000,
            volume=328601,
            ai_summary="[중립/부정] LG에너지솔루션은 최근 3건의 긍정 뉴스, 1건의 부정 뉴스, 3건의 중립 뉴스가 보도되며 EV 수요 둔화 속에서도 ESS 사업 강화로 돌파구를 모색하고 있습니다.\n\n📈 핵심 긍정 요인 (3건):\n2026년 임원 인사에서 전무 1명과 상무 6명을 승진시키며 ESS사업본부와 신사업 연구조직을 강화했습니다. 충북 오창공장에 ESS용 LFP 배터리 생산 라인을 구축하여 2027년부터 연 1GWh 규모로 양산할 계획이며, 국내 최초 ESS LFP 양산으로 백로그는 120GWh에 달합니다. 북미용 19.2kWh/32kWh '프라임 플러스'와 유럽용 모듈형 '엔블록' ESS 신제품을 출시하며 주택용 시장 공략을 본격화하고 있습니다.\n\n📉 주요 리스크 (1건):\nIRA 세금공제 종료로 북미 전기차 수요가 줄어들 것이라는 우려가 커지며 주가가 6.05% 급락했습니다.\n\n📊 중립 요인 (3건):\n흥국증권은 북미 EV 판매 둔화로 4분기 영업손실 1,538억원을 예상하면서도 ESS와 소형전지 호조를 언급하며 목표가를 540,000원으로 제시했습니다. LS증권은 미국 IRA 조기 일몰로 EV 수요가 약세이지만 ESS 수익이 이를 상회할 것으로 분석했습니다. LG그룹은 자사주 소각과 주주환원 강화 계획을 발표하며 LG화학이 LG에너지솔루션 지분을 장기적으로 약 70%까지 낮출 것이라고 밝혔습니다.\n\n💰 수급 분석:\n하루 기준으로 외국인과 개인이 매도했으나 기관이 525억원 매수하며 저가 매수에 나섰습니다. 최근 1개월간 외국인이 2,833억원을 순매수하며 밸류에이션 매력에 주목하고 있습니다.\n\n🎯 증권가 컨센서스:\n평균 목표가는 516,000원으로 현재가 대비 약 25% 상승 여력이 있으나, 증권사 간 의견이 크게 엇갈립니다. 신영증권과 신한투자증권은 590,000원(매수)을 제시한 반면 LS증권은 368,000원(중립·하향)으로 목표가 격차가 60%에 달합니다. 67%가 매수 의견이나 단기 실적 부담과 중장기 ESS 성장성에 대한 평가가 분분한 상황입니다."
        ),
        news_summary="""<div class="news-item negative">
<div class="news-header">📉 11/28 북미 EV 수요 둔화로 주가 6% 하락 <span class="news-importance">★★★★★</span></div>
<div class="news-content">IRA 세금공제 종료로 북미 전기차 수요가 줄어들 것이라는 우려가 커지며 LG에너지솔루션 주가가 6.05% 하락했습니다. 분석가들은 ESS 수요가 AI 데이터센터 등에 힘입어 성장할 것으로 전망했습니다.</div>
</div>

<div class="news-item neutral">
<div class="news-header">⚪ 11/28 흥국證, EV 수요 현실화로 4분기 매출 8.4% 감소 전망·목표가 54만원으로 하향 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">흥국증권은 북미 EV 판매 둔화로 LG에너지솔루션의 4분기 매출을 전년 대비 8.4% 감소한 5조9000억 원, 영업손실 1,538억 원으로 예상하면서도 ESS와 소형전지 판매 호조를 언급하며 목표가를 540,000원으로 낮췄습니다.</div>
</div>

<div class="news-item neutral">
<div class="news-header">⚪ 11/28 LG그룹 밸류업 계획… LG화학, LG에너지솔루션 지분을 70% 수준까지 낮추기로 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">LG그룹은 자사주 소각과 주주환원 강화 계획을 발표하면서 LG화학이 LG에너지솔루션 지분을 장기적으로 약 70% 수준까지 감소시키고 포트폴리오 재편과 ESS 사업 확대를 통해 수익성을 높일 계획이라고 밝혔습니다.</div>
</div>

<div class="news-item neutral">
<div class="news-header">⚪ 11/27 LS증권 '미국 ESS 기대감 선반영' 발표… 주가 3.75% 상승 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">LS증권은 미국 IRA 30D 조기 일몰로 EV 수요가 약세를 보이지만 ESS 수익이 이를 상회할 것으로 분석했으며, 이날 주가는 전일 대비 3.75% 오른 429,000원으로 마감했습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/27 2026년 임원 인사… 전무 1명·상무 6명 승진, ESS 조직 강화 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">LG에너지솔루션은 전무 1명과 상무 6명을 승진시키는 임원 인사를 단행했습니다. 이번 인사에서 ESS사업본부와 신사업 연구조직을 강화해 시장 변화에 대응합니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/18 가정용 ESS '프라임 플러스·엔블록' 출시 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">회사는 북미용 19.2kWh/32kWh '프라임 플러스'와 유럽용 모듈형 '엔블록' ESS 제품을 출시했습니다. 이 제품들은 설치가 간편하고 용량을 확장할 수 있어 주택용 시장을 겨냥합니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/17 오창공장 LFP 배터리 국산화… 2027년 1GWh 양산 계획 <span class="news-importance">★★★★★</span></div>
<div class="news-content">LG에너지솔루션은 충북 오창공장에 ESS용 LFP 배터리 생산 라인을 구축해 2027년부터 연 1GWh 규모로 양산할 계획입니다. 국내에서는 최초의 ESS LFP 양산이며 백로그는 120GWh에 달합니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: 북미 EV 수요 둔화로 주가 6% 하락 등 1건의 부정 뉴스가 있으나, 2026년 임원 인사로 ESS 조직 강화, 오창공장 LFP 배터리 국산화로 2027년 1GWh 양산, 가정용 ESS 제품 출시 등 3건의 긍정 뉴스로 ESS 사업 확대에 집중하고 있습니다. 흥국증권·LS증권 전망과 LG그룹 밸류업 계획 등 3건의 중립 뉴스가 있습니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="-212억원",
            institution_net="+525억원",
            individual_net="-184억원",
            summary="외국인과 개인의 매도세가 나타났으나 기관의 강력한 매수세로 방어되고 있습니다. 중국 배터리 기업과의 가격 경쟁 심화와 전기차 수요 둔화 우려가 반영되고 있으나, 기관은 저가 매수 기회로 판단하고 있습니다.",
            period_data=[
                SupplyDemandPeriod(
                    period="1주일", 
                    foreign_net="+79억원", 
                    institution_net="+425억원", 
                    individual_net="-72억원",
                    summary="최근 1주일간 기관의 매수세가 두드러지며 425억원을 순매수했습니다. 주가 하락을 저가 매수 기회로 판단한 것으로 보입니다. 외국인도 79억원을 소폭 순매수하며 장기 전기차 시장 성장성을 재평가했습니다. 개인은 72억원을 순매도하며 단기 실적 부담을 우려했습니다."
                ),
                SupplyDemandPeriod(
                    period="1개월", 
                    foreign_net="+2,833억원", 
                    institution_net="-75억원", 
                    individual_net="-1,045억원",
                    summary="최근 1개월간 외국인이 2,833억원을 순매수하며 주가 하락을 저가 매수 기회로 활용했습니다. 밸류에이션이 낮아지면서 중장기 전기차 시장 성장성에 베팅하는 모습입니다. 반면 개인은 1,045억원을 순매도하며 단기 실적 부담과 중국 배터리 기업과의 경쟁 심화를 우려했습니다. 기관도 75억원을 소폭 순매도하며 신중한 태도를 보였습니다."
                )
            ]
        ),
        performance=Performance(
            revenue="23.3조원",
            operating_profit="1.45조원",
            net_profit="-1,414억원",
            summary="2025년 연간 실적 컨센서스는 전기차 수요 둔화와 중국 배터리 기업 가격 경쟁으로 어려운 한 해가 예상됩니다. 매출은 전년 대비 9.2% 감소한 23.3조원이지만, 영업이익은 구조조정 효과로 151.3% 증가한 1.45조원으로 전망됩니다. 순손실은 1,414억원으로 전년 대비 적자폭이 86.1% 축소될 것으로 보입니다.",
            revenue_yoy="-9.2%",
            revenue_qoq="N/A",
            operating_profit_yoy="+151.3%",
            operating_profit_qoq="N/A",
            operating_profit_vs_consensus="N/A",
            earnings_surprise="+86.1%"
        ),
        investment_points=InvestmentPoint(
            positive=[
                "글로벌 전기차 시장 장기 성장 트렌드 지속",
                "고성능 배터리 기술력과 고객 포트폴리오 다각화",
                "미국 현지 생산 확대로 공급망 안정화",
                "양극재 등 핵심 소재 자체 생산 확대"
            ],
            negative=[
                "중국 배터리 기업들의 가격 경쟁 심화",
                "전기차 수요 둔화로 배터리 주문 감소",
                "원자재 가격 상승으로 수익성 압박",
                "미국 IRA 규정 변경으로 보조금 혜택 축소 우려",
                "고객사들의 가격 재협상 압력 증가"
            ]
        ),
        recent_issues=[
            NewsItem(
                date="2025.11.26",
                title="중국 배터리 기업 가격 경쟁 더욱 심화",
                summary="CATL, BYD 등 중국 기업들의 추가 가격 인하로 수익성 압박 가중, 단가 격차 20-25%로 확대",
                url="#",
                sentiment="negative"
            ),
            NewsItem(
                date="2025.11.25",
                title="전기차 수요 둔화 지속, 배터리 주문 추가 감소",
                summary="글로벌 전기차 시장 성장세 둔화 지속으로 주요 고객사 주문 추가 감소, 2026년 상반기까지 영향 예상",
                url="#",
                sentiment="negative"
            ),
            NewsItem(
                date="2025.11.24",
                title="4분기 영업이익 컨센서스 대비 -18% 미달 전망",
                summary="배터리 단가 하락과 원자재 가격 상승으로 수익성 크게 악화, 영업이익률 2.3%로 하락 예상",
                url="#",
                sentiment="negative"
            ),
            NewsItem(
                date="2025.11.23",
                title="미국 IRA 세부 규정 변경으로 보조금 혜택 추가 축소",
                summary="IRA 규정 추가 변경으로 한국 배터리 기업 보조금 혜택 추가 축소, 공급망 재구성 비용 증가",
                url="#",
                sentiment="negative"
            )
        ],
        analyst_opinions=[
            AnalystOpinion(
                target_price="590,000원",
                opinion="ESS 시장 확대와 배터리 기술력 우위. 투자의견 매수 유지",
                firm="신영증권",
                trend="neutral"
            ),
            AnalystOpinion(
                target_price="590,000원",
                opinion="전기차 시장 장기 성장 전망, 글로벌 고객 포트폴리오 다각화. 투자의견 매수 유지",
                firm="신한투자증권",
                trend="neutral"
            ),
            AnalystOpinion(
                target_price="368,000원",
                opinion="중국 배터리 기업 가격 경쟁 심화와 수익성 압박. 목표가 하향, 투자의견 중립",
                firm="LS증권",
                trend="down"
            )
        ],
        analyst_summary="증권사들의 목표가 의견이 **극명하게 엇갈리고** 있습니다. 신영증권과 신한투자증권은 590,000원으로 높은 목표가를 제시하며 '매수' 의견을 유지한 반면, LS증권은 368,000원으로 대폭 하향하며 '중립' 의견으로 전환했습니다. 평균 목표가 516,000원은 현재가 대비 **약 34% 상승 여력**이 있으나, 증권사 간 격차가 222,000원(60%)에 달해 실적 전망이 매우 불확실한 상황입니다. 67%가 '매수' 의견이나, 중국 배터리 기업과의 가격 경쟁과 전기차 수요 둔화가 핵심 리스크로 지적되고 있습니다.",
        sector_name="배터리",
        sector_news=[
            SectorNews(
                date="2025.11.26",
                title="중국 배터리 기업, 글로벌 시장 점유율 빠르게 확대",
                summary="CATL, BYD 등 중국 배터리 기업들이 가격 경쟁력을 바탕으로 글로벌 시장 점유율을 빠르게 확대 중. 유럽 시장에서도 점유율 상승 가속화",
                sentiment="negative"
            ),
            SectorNews(
                date="2025.11.25",
                title="전기차 시장 성장세 둔화 지속, 배터리 수요 감소",
                summary="글로벌 전기차 시장 성장률이 전년 대비 둔화되면서 배터리 수요 증가세도 함께 둔화. 2026년 상반기까지 영향 지속 예상",
                sentiment="negative"
            ),
            SectorNews(
                date="2025.11.24",
                title="리튬 등 원자재 가격 상승 지속, 배터리 제조사 수익성 압박",
                summary="리튬, 니켈 등 배터리 핵심 원자재 가격이 상승세를 지속하면서 배터리 제조사들의 수익성에 압박 가중",
                sentiment="negative"
            ),
            SectorNews(
                date="2025.11.23",
                title="미국 IRA 규정 추가 변경, 한국 배터리 기업 영향 확대",
                summary="미국 IRA 세부 규정 추가 변경으로 한국 배터리 기업들의 보조금 혜택이 더욱 축소될 가능성. 공급망 재구성 비용 증가",
                sentiment="negative"
            )
        ],
        investment_metrics=InvestmentMetrics(
            per="–110.37배",
            pbr="4.71배",
            roe="–4.30%",
            dividend_yield="N/A",
            market_cap="96.6조원",
            shares_outstanding="2.34억주"
        )
    )
}

@router.get("/stock/{stock_code}", response_model=StockAnalysis)
async def get_stock_analysis(stock_code: str):
    """
    종목 코드로 AI 시황 분석 데이터 조회
    
    - **stock_code**: 종목 코드 (예: 005930)
    """
    if stock_code not in MOCK_DATA:
        raise HTTPException(status_code=404, detail="종목을 찾을 수 없습니다")
    
    return MOCK_DATA[stock_code]

@router.get("/stocks/list")
async def get_stock_list():
    """시연 가능한 종목 목록 조회"""
    return {
        "stocks": [
            {"code": "005930", "name": "삼성전자"},
            {"code": "000660", "name": "SK하이닉스"},
            {"code": "006800", "name": "미래에셋증권"},
            {"code": "373220", "name": "LG에너지솔루션"}
        ]
    }


