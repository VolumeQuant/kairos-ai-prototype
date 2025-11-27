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
            current_price=99200,
            change_rate=2.15,
            change_price=2100,
            volume=18200000,
            ai_summary="[긍정] 삼성전자는 최근 6건의 긍정 뉴스와 1건의 부정 뉴스가 보도되며 매우 강한 긍정적 흐름을 보이고 있습니다.\n\n📈 핵심 긍정 요인 (6건)\nHBM3E 양산 본격화로 엔비디아 공급량이 2배 확대되며 AI 메모리 시장 진입이 가속화되고 있습니다. 파운드리 2나노 공정 고객사 확대로 총 계약 규모가 15조원을 돌파했으며, 4분기 영업이익이 10.5조원으로 컨센서스 대비 +10% 상회할 것으로 전망됩니다. 갤럭시 S25의 사전 예약이 200만대를 돌파하며 전작 대비 25% 증가했고, DDR5와 HBM 가격이 각각 10%, 15% 상승하며 메모리 반도체 업황이 크게 개선되고 있습니다. 미국 반도체 보조금 추가 지원도 확정되었습니다.\n\n📉 주요 리스크 (1건)\n중국 정부의 반도체 수입 규제 강화로 중국 시장 매출에 일부 영향이 예상됩니다. 다만 고부가 제품 중심 포트폴리오와 파운드리 부문 강점으로 전체 영향은 제한적일 전망입니다.\n\n💰 수급 분석\n외국인과 기관의 동반 매수세가 지속되며 최근 1개월간 외국인 순매수 1.3조원을 기록했습니다. AI 반도체 기대감이 반영되고 있습니다.\n\n🎯 증권가 컨센서스\n평균 목표가 128,000원으로 현재가 대비 약 29% 상승 여력이 있으며, KB증권 135,000원, NH투자증권 128,000원, 미래에셋증권 122,000원으로 상향 조정 추세입니다."
        ),
        news_summary="""<div class="news-item positive">
<div class="news-header">📈 11/26 HBM3E 양산 본격화, 엔비디아 공급량 2배 확대 <span class="news-importance">★★★★★</span></div>
<div class="news-content">삼성전자가 HBM3E 12단 제품의 양산을 본격화하며 엔비디아에 대한 월간 공급량을 기존 대비 2배로 확대했습니다. 이로써 2026년 HBM 시장 점유율 30% 목표 달성에 한 걸음 더 다가섰습니다. 애널리스트들은 이번 양산 확대로 연간 6조원 이상의 추가 매출이 가능할 것으로 전망하고 있으며, 2026년 상반기까지 공급량이 지속적으로 증가할 것으로 예상됩니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/25 파운드리 2나노 공정 고객사 확대 발표 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">삼성전자가 차세대 2나노 파운드리 공정의 고객 포트폴리오를 확대한다고 발표했습니다. 기존 고객사 외에 추가로 3개사의 선주문 계약을 체결했으며, 총 계약 규모가 15조원을 넘어섰습니다. 특히 AI 반도체용 고성능 칩 수요가 급증하면서 2026년 파운드리 매출이 전년 대비 30% 이상 성장할 것으로 전망됩니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/25 미국 반도체 보조금 추가 65억 달러 지원 확정 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">미국 정부가 삼성전자 텍사스 파운드리 공장에 대한 CHIPS Act 보조금을 기존 계획 대비 65억 달러 추가 지원하기로 확정했습니다. 2나노 공정 라인 확장과 첨단 패키징 시설 구축에 투입되며, 2027년까지 미국 내 생산 능력을 현재 대비 3배 확대할 수 있게 되었습니다. 이는 미국 AI 반도체 공급망에서 삼성의 입지를 크게 강화시킬 전망입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/24 4분기 영업이익 10.5조원 전망, 컨센서스 +10% 상회 <span class="news-importance">★★★★★</span></div>
<div class="news-content">증권가는 삼성전자 4분기 영업이익을 10.5조원으로 상향 조정했으며, 이는 시장 컨센서스 9.5조원을 10% 이상 상회하는 수치입니다. HBM3E 양산 확대로 HBM 비중이 전체 메모리 매출의 22%까지 확대되고, DDR5 가격이 전분기 대비 10% 상승하면서 수익성이 크게 개선되고 있습니다. NAND 재고도 정상화 수준으로 감소했습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/23 갤럭시 S25 출시, 사전 예약 200만대 돌파 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">온디바이스 AI 기능을 대폭 강화한 갤럭시 S25 시리즈가 정식 출시되었으며, 사전 예약이 200만대를 돌파했습니다. 이는 전작 대비 25% 증가한 수치로, 특히 울트라 모델의 예약률이 45%를 넘어서며 평균 판매가(ASP) 상승에 크게 기여할 전망입니다. 출시 첫 주 판매량도 전작 대비 30% 증가할 것으로 예상됩니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/22 메모리 반도체 가격 상승세 가속화 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">DDR5와 HBM 가격이 전월 대비 각각 10%와 15% 상승하며 상승세가 가속화되고 있습니다. AI 서버 수요 급증과 공급 부족이 지속되면서 메모리 반도체 업황이 크게 개선되고 있습니다. 증권가는 이번 가격 상승세가 최소 3분기 이상 지속될 것으로 전망하고 있으며, 삼성전자의 메모리 사업부 영업이익률이 30%를 넘어설 것으로 예상됩니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/21 중국 반도체 규제 강화 우려 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">중국 정부가 반도체 수입 규제를 강화하면서 삼성전자의 중국 시장 매출에 일부 영향이 예상됩니다. 특히 레거시 반도체 부문에서 중국 고객사 주문이 15% 감소할 것으로 전망되며, 중국 내 생산 공장 가동률도 영향을 받을 수 있습니다. 다만 고부가 제품 중심 포트폴리오와 글로벌 고객사 다각화로 인해 전체적인 영향은 제한적일 것으로 보입니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: HBM3E 양산 본격화로 엔비디아 공급량 2배 확대, 미국 반도체 보조금 65억 달러 추가 지원, 4분기 영업이익 10.5조원 전망으로 컨센서스 +10% 상회, 파운드리 2나노 공정 고객사 확대, 갤럭시 S25 출시로 사전 예약 200만대 돌파, 메모리 반도체 가격 상승세 가속화 등 6건의 긍정 뉴스가 이어지고 있습니다. 중국 반도체 규제 강화 1건의 부정 요인이 있으나 전체적인 영향은 제한적입니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="+250억원",
            institution_net="+180억원",
            individual_net="-430억원",
            summary="외국인과 기관의 동반 매수세가 이어지며 개인 투자자의 차익실현 물량을 흡수하는 모습입니다. HBM3E 양산 소식이 나오며 AI 반도체에 대한 기대감이 반영되고 있습니다.",
            period_data=[
                SupplyDemandPeriod(
                    period="1주일", 
                    foreign_net="+1,200억원", 
                    institution_net="+850억원", 
                    individual_net="-2,050억원",
                    summary="최근 1주일간 외국인과 기관의 강한 매수세가 지속되고 있습니다. HBM3E 엔비디아 공급 승인 소식과 갤럭시 S25 사전 예약 호조로 투자 심리가 크게 개선되었습니다. 외국인은 파운드리와 HBM 사업부 성장 기대감으로 1,200억원 순매수했으며, 기관도 실적 개선 전망에 850억원을 매수했습니다."
                ),
                SupplyDemandPeriod(
                    period="1개월", 
                    foreign_net="+1.2조원", 
                    institution_net="+3,200억원", 
                    individual_net="-1.52조원",
                    summary="최근 1개월간 외국인의 압도적인 매수세가 이어지며 1.2조원의 순매수를 기록했습니다. AI 반도체 시장 확대와 메모리 반도체 가격 상승 사이클 진입으로 중장기 성장성에 대한 기대감이 반영되고 있습니다. 기관 역시 4분기 어닝 서프라이즈 가능성에 주목하며 3,200억원을 순매수했으며, 개인은 단기 차익 실현으로 일부 물량을 매도했습니다."
                )
            ]
        ),
        performance=Performance(
            revenue="72.5조원",
            operating_profit="10.2조원",
            net_profit="7.8조원",
            summary="2025년 4분기 실적 컨센서스는 메모리 반도체 부문의 지속적인 회복과 HBM3E 엔비디아 공급 승인으로 전년 동기 대비 큰 폭의 성장이 예상됩니다. 특히 HBM과 DDR5 고부가 제품 비중 확대로 영업이익률이 크게 개선될 것으로 전망됩니다.",
            revenue_yoy="+15.2%",
            revenue_qoq="+7.6%",
            operating_profit_yoy="+25.3%",
            operating_profit_qoq="+54.5%",
            operating_profit_vs_consensus="+7.3%",
            earnings_surprise="컨센서스 대비 +7.3%"
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
                target_price="130,000원",
                opinion="HBM3E 양산 본격화와 파운드리 수율 개선으로 실적 개선 기대. 목표주가 상향",
                firm="KB증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="125,000원",
                opinion="AI 반도체 시장 성장과 메모리 업황 회복세 지속. 투자의견 Buy 유지",
                firm="NH투자증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="120,000원",
                opinion="4분기 실적 개선 전망. HBM 비중 확대로 수익성 개선 예상",
                firm="미래에셋증권",
                trend="neutral"
            )
        ],
        analyst_summary="최근 3개월간 주요 증권사들의 목표가가 **지속적으로 상향 조정**되고 있습니다. KB증권은 130,000원으로 전월 대비 +8.3% 상향했으며, NH투자증권도 125,000원으로 +4.2% 올렸습니다. HBM3E 엔비디아 공급 승인과 파운드리 2나노 고객 확대가 주요 상향 근거입니다. 평균 목표가 125,000원은 현재가 대비 **26% 상승 여력**이 있으며, 컨센서스는 'Buy' 의견이 75%로 매수 우위입니다. AI 반도체 모멘텀 지속으로 추가 상향 가능성도 열려있습니다.",
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
            per="15.2배",
            pbr="1.28배",
            roe="8.5%",
            dividend_yield="2.31%",
            market_cap="597조원",
            shares_outstanding="59.7억주"
        )
    ),
    "000660": StockAnalysis(
        stock_info=StockInfo(
            code="000660",
            name="SK하이닉스",
            current_price=538700,
            change_rate=3.42,
            change_price=17800,
            volume=3650000,
            ai_summary="[긍정] SK하이닉스는 최근 5건의 긍정 뉴스와 2건의 부정 뉴스가 보도되며 HBM 시장 독점적 지위를 더욱 공고히 하고 있습니다.\n\n📈 핵심 긍정 요인 (5건)\n차세대 HBM4 샘플이 엔비디아 품질 테스트를 통과하며 2026년 상반기 양산이 확정되었습니다. 대역폭 50% 향상으로 삼성전자와의 기술 격차를 최소 2년 이상 유지할 것으로 전망됩니다. 미국 인디애나 패키징 공장 가동률이 90%에 달하며 미국 AI 공급망의 핵심 파트너로 부상했고, 4분기 영업이익이 7.8조원으로 컨센서스 대비 +8.5% 상회할 것으로 예상됩니다. HBM 매출 비중이 전체 매출의 35%를 넘어서며 수익성 개선을 주도하고 있으며, 엔비디아 GB200용 HBM3E 공급량 추가 확대로 2026년 HBM 매출이 22조원을 넘어설 전망입니다.\n\n📉 주요 리스크 (2건)\n삼성전자의 HBM3E 엔비디아 공급 승인으로 독점적 지위에 변화가 예상되며, 높은 밸류에이션으로 주가 변동성이 확대될 수 있습니다. 다만 HBM4 개발 선도와 생산 능력 우위로 단기 영향은 제한적입니다.\n\n💰 수급 분석\n외국인의 강력한 매수세가 지속되며 최근 2주간 9,000억원 이상, 1개월간 3.1조원의 순매수를 기록했습니다. AI 반도체 업사이클 기대감이 반영되고 있습니다.\n\n🎯 증권가 컨센서스\n평균 목표가 640,000원으로 현재가 대비 약 19% 상승 여력이 있으며, 삼성증권 680,000원, 한국투자증권 640,000원, 키움증권 620,000원으로 상향 조정 추세입니다."
        ),
        news_summary="""<div class="news-item positive">
<div class="news-header">📈 11/26 HBM4 샘플 엔비디아 테스트 통과, 2026년 상반기 양산 확정 <span class="news-importance">★★★★★</span></div>
<div class="news-content">차세대 HBM4 제품의 엔비디아 품질 테스트를 통과하며 2026년 상반기 양산이 확정되었습니다. HBM4는 HBM3E 대비 대역폭 50% 향상, 전력 효율 30% 개선으로 AI GPU 성능 혁신을 이끌 전망입니다. 삼성전자와의 기술 격차를 최소 2년 이상 유지할 수 있을 것으로 보이며, 엔비디아 차세대 GPU용 독점 공급이 예상됩니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/25 미국 인디애나 패키징 공장 가동률 90% 달성 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">미국 인디애나주 첨단 패키징 공장의 가동률이 90%에 달하며 본격 가동에 성공했습니다. 미국 AI 공급망의 핵심 파트너로 부상했으며, 현지 생산으로 공급망 안정성이 크게 강화되었습니다. 2026년 상반기까지 가동률 100% 달성을 목표로 하고 있습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/25 DDR5 가격 추가 상승, 메모리 업황 호조 지속 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">DDR5 DRAM 가격이 2개월 연속 상승하며 11월에만 12% 상승했습니다. 서버 및 PC 수요 증가로 공급 부족 현상이 심화되고 있으며, 증권가는 DDR5 가격 상승세가 2026년 1분기까지 이어질 것으로 전망합니다. SK하이닉스는 DDR5 시장 점유율 45%로 업계 1위를 유지하며 수혜를 받고 있습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/24 높은 밸류에이션 부담, 변동성 확대 우려 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">SK하이닉스의 PER가 동종업계 평균 대비 35% 높은 수준을 기록하며 밸류에이션 부담이 커지고 있습니다. 증권가는 단기 실적 모멘텀은 강력하지만, 높은 밸류에이션으로 조정 가능성을 배제할 수 없다고 지적했습니다. 특히 AI 투자 사이클 둔화 시 주가 변동성이 크게 확대될 수 있다는 우려가 제기되고 있습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/24 4분기 영업이익 7.8조원 전망, 컨센서스 +8.5% 상회 <span class="news-importance">★★★★★</span></div>
<div class="news-content">증권가는 SK하이닉스 4분기 영업이익을 7.8조원으로 상향 조정했으며, 이는 시장 컨센서스 7.2조원을 8.5% 상회하는 수치입니다. HBM3E 출하량이 전분기 대비 50% 증가하고, DDR5 가격도 12% 이상 상승하면서 영업이익률 42%를 기록할 것으로 예상됩니다. 특히 HBM 매출 비중이 전체 매출의 35%를 넘어서며 수익성 개선을 주도하고 있습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/23 엔비디아 GB200용 HBM3E 공급량 추가 확대 <span class="news-importance">★★★★★</span></div>
<div class="news-content">엔비디아의 차세대 AI 슈퍼칩 GB200에 대한 HBM3E 12단 제품 공급량을 추가로 확대하는 계약을 체결했습니다. GB200 한 대당 HBM 탑재량이 H100 대비 3배 증가하면서, 2026년 HBM 매출이 22조원을 넘어설 것으로 전망됩니다. 엔비디아와의 장기 공급 계약으로 수익성 안정성도 크게 향상되었습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/22 삼성전자 HBM 진입으로 경쟁 심화 우려 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">삼성전자가 HBM3E 엔비디아 공급 승인을 받으면서 SK하이닉스의 독점적 지위에 변화가 예상됩니다. 시장 점유율이 현재 60%에서 2026년 45%로 하락할 수 있다는 전망이 나오고 있습니다. 다만 HBM4 개발 선도와 기술력, 생산 능력 면에서 여전히 우위를 유지하고 있어 단기적인 영향은 제한적일 것으로 보입니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: HBM4 샘플 엔비디아 테스트 통과로 2026년 상반기 양산 확정, 4분기 영업이익 7.8조원 전망으로 컨센서스 +8.5% 상회, 엔비디아 GB200용 HBM3E 공급량 추가 확대, DDR5 가격 추가 상승 등 5건의 긍정 뉴스가 이어집니다. 다만 삼성전자의 HBM 시장 진입으로 경쟁 심화 우려와 높은 밸류에이션 부담 등 2건의 부정 요인도 존재합니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="+520억원",
            institution_net="+310억원",
            individual_net="-830억원",
            summary="외국인의 강력한 매수세가 지속되고 있으며 기관도 동반 매수 중입니다. HBM4 개발 순조와 엔비디아 독점 공급 지위 유지로 투자 심리가 매우 긍정적입니다.",
            period_data=[
                SupplyDemandPeriod(
                    period="1주일", 
                    foreign_net="+8,000억원", 
                    institution_net="+2,100억원", 
                    individual_net="-10,100억원",
                    summary="최근 1주일간 외국인의 폭발적인 매수세가 나타나며 8,000억원을 순매수했습니다. HBM4 샘플이 엔비디아 테스트를 통과하며 2026년 상반기 양산이 확정된 소식이 큰 호재로 작용했습니다. 기관도 독점적 시장 지위 유지에 베팅하며 2,100억원을 매수했으며, 개인은 주가 급등에 따른 차익 실현으로 1조원 이상 매도했습니다."
                ),
                SupplyDemandPeriod(
                    period="1개월", 
                    foreign_net="+2.8조원", 
                    institution_net="+5,200억원", 
                    individual_net="-3.32조원",
                    summary="최근 1개월간 외국인이 무려 2.8조원을 순매수하며 SK하이닉스에 대한 압도적인 선호도를 보여주고 있습니다. AI 메모리 시장 독점과 HBM3E/HBM4 기술 우위로 중장기 성장성이 가장 확실한 AI 수혜주로 평가받고 있습니다. 기관 역시 높은 영업이익률과 엔비디아 공급 독점 지위를 높이 평가하며 5,200억원을 순매수했습니다. 개인은 밸류에이션 부담으로 일부 차익 실현 중입니다."
                )
            ]
        ),
        performance=Performance(
            revenue="20.5조원",
            operating_profit="8.8조원",
            net_profit="7.2조원",
            summary="2025년 4분기 실적 컨센서스는 HBM4 개발 순조와 엔비디아 GB200용 HBM3E 12단 독점 공급으로 전년 동기 대비 폭발적인 성장이 예상됩니다. HBM 매출 비중이 35%를 넘어서며 영업이익률 43%를 기록할 것으로 전망됩니다.",
            revenue_yoy="+65.2%",
            revenue_qoq="+16.5%",
            operating_profit_yoy="+220.5%",
            operating_profit_qoq="+25.7%",
            operating_profit_vs_consensus="+8.5%",
            earnings_surprise="컨센서스 대비 +8.5%"
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
                target_price="650,000원",
                opinion="HBM 시장 독점적 지위와 AI 반도체 수퍼사이클 수혜. 목표가 상향 조정",
                firm="삼성증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="620,000원",
                opinion="HBM4 개발 순조, 2026년 매출 성장 가속화 전망. 투자의견 매수",
                firm="한국투자증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="600,000원",
                opinion="AI GPU 수요 증가로 HBM 출하 확대 지속. 실적 모멘텀 강력",
                firm="키움증권",
                trend="up"
            )
        ],
        analyst_summary="최근 3개월간 주요 증권사들의 목표가가 **가파르게 상향 조정**되고 있습니다. 삼성증권은 650,000원으로 전월 대비 +10.2% 대폭 상향했고, 한국투자증권도 620,000원으로 +8.8% 올렸습니다. HBM4 테스트 통과와 엔비디아 독점 공급 지위 유지가 핵심 근거입니다. 평균 목표가 623,000원은 현재가 대비 **16% 상승 여력**이 있으며, 모든 증권사가 'Strong Buy' 의견으로 일치된 낙관론을 보이고 있습니다. AI 메모리 시장 독점으로 추가 상향 전망이 우세합니다.",
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
            per="9.8배",
            pbr="1.85배",
            roe="19.2%",
            dividend_yield="1.68%",
            market_cap="392조원",
            shares_outstanding="7.3억주"
        )
    ),
    "006800": StockAnalysis(
        stock_info=StockInfo(
            code="006800",
            name="미래에셋증권",
            current_price=21900,
            change_rate=2.81,
            change_price=600,
            volume=4200000,
            ai_summary="[중립] 미래에셋증권은 최근 4건의 긍정 뉴스와 3건의 부정 뉴스가 보도되며 IB 부문 강세와 자산관리 성장세에도 불구하고 시장 환경 악화로 리스크가 공존하고 있습니다.\n\n📈 핵심 긍정 요인 (4건)\n대형 IPO 주관 수수료로 IB 부문 실적이 크게 개선되었고, 해외주식 거래량이 전월 대비 35% 급증했습니다. 웰스케어 자산관리 고객이 1.8만명을 돌파하며 총 관리자산이 99조원에 달했고, 4분기 순이익이 1.6조원으로 컨센서스 대비 +12% 상회할 것으로 전망됩니다.\n\n📉 주요 리스크 (3건)\n증시 거래대금이 전월 대비 18% 감소하며 브로커리지 수익에 빨간불이 켜졌고, 증권업계의 해외주식 수수료 인하 경쟁이 심화되며 수익성에 압박이 가중되고 있습니다. 시장 환경 악화로 단기 실적 불확실성이 증가하고 있습니다.\n\n💰 수급 분석\n외국인의 꾸준한 매수세가 이어지며 최근 1개월간 680억원 순매수를 기록했습니다. 증권주 중 가장 높은 선호도를 보이고 있습니다.\n\n🎯 증권가 컨센서스\n평균 목표가 25,000원으로 현재가 대비 약 14% 상승 여력이 있으며, 하나증권 26,500원, 신한투자증권 25,000원, 대신증권 24,000원으로 상향 조정 추세입니다."
        ),
        news_summary="""<div class="news-item positive">
<div class="news-header">📈 11/26 대형 IPO 3건 주관 수주, IB 부문 실적 호조 <span class="news-importance">★★★★★</span></div>
<div class="news-content">미래에셋증권이 11월 들어 시가총액 1조원 이상 대형 IPO 3건의 대표 주관사로 선정되며 IB 부문 실적이 크게 개선되고 있습니다. 총 공모 규모 3.5조원에 달하는 이번 IPO 주관으로 약 420억원의 수수료 수입이 예상됩니다. 특히 바이오·IT 분야 우량 기업 발굴 능력이 높이 평가받으며, 2026년 상반기에도 추가로 5건 이상의 대형 IPO 주관이 예정되어 있어 IB 부문 모멘텀이 지속될 전망입니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/26 증시 거래대금 감소, 브로커리지 수익 우려 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">코스피와 코스닥 일평균 거래대금이 11월 들어 전월 대비 18% 감소하며 증권사들의 브로커리지 수익에 빨간불이 켜졌습니다. 특히 개인투자자 거래 비중이 크게 줄어들면서 수수료 수입이 감소하고 있습니다. 증권가는 증시 거래대금 감소가 2026년 1분기까지 이어질 경우 미래에셋증권의 브로커리지 수익이 10% 이상 감소할 수 있다고 전망했습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/25 해외주식 거래량 전월 대비 35% 증가 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">미국 주식 거래 수수료를 0.07%로 인하한 효과가 나타나며 해외주식 거래량이 전월 대비 35% 증가했습니다. 이는 업계 최고 성장률로, 해외주식 거래 고객이 3개월 만에 20만명 증가하면서 브로커리지 수익이 크게 개선되고 있습니다. 특히 MZ세대 고객의 해외주식 투자 비중이 크게 늘어나고 있습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/25 수수료 인하 경쟁 심화, 수익성 압박 우려 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">증권업계의 해외주식 수수료 인하 경쟁이 격화되면서 수익성 압박이 가중되고 있습니다. 주요 증권사들이 앞다퉈 수수료를 0.07% 이하로 낮추면서 미래에셋증권도 추가 인하를 검토하고 있습니다. 증권가는 거래량 증가에도 불구하고 수수료 마진 축소로 브로커리지 부문 순이익률이 전년 대비 15% 감소할 것으로 우려하고 있습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/24 웰스케어 자산관리 고객 1.8만명 돌파 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">고액 자산가 대상 프리미엄 자산관리 서비스인 '웰스케어'의 고객이 1.8만명을 넘어섰습니다. 평균 예탁자산이 55억원으로 증가했으며, 총 관리자산이 99조원에 달합니다. 고수익 고객 확보로 수익성이 크게 개선되고 있으며, 2026년 목표인 고객 3만명, 관리자산 150조원 달성에 한 걸음 더 다가섰습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/23 주식 시장 변동성 확대, 실적 불확실성 증가 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">글로벌 금리 인상과 경기 둔화 우려로 주식 시장 변동성이 크게 확대되며 증권사 실적에 불확실성이 증가하고 있습니다. 코스피 변동성지수(VKOSPI)가 3개월 만에 최고치를 기록하며 투자심리 위축이 지속되고 있습니다. 증권가는 시장 불안정이 2026년 1분기까지 이어질 경우 미래에셋증권의 자산관리 부문 수익이 영향을 받을 수 있다고 경고했습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/23 4분기 순이익 1.6조원 전망, 컨센서스 +12% 상회 <span class="news-importance">★★★★★</span></div>
<div class="news-content">증권가는 미래에셋증권 4분기 순이익을 1.6조원으로 추정하고 있으며, 이는 시장 컨센서스 1.43조원을 12% 상회하는 수치입니다. 브로커리지 부문은 해외주식 거래 급증으로 전년 동기 대비 35% 성장했고, IB 부문도 대형 IPO 수수료 수입으로 호조를 보였습니다. 특히 ROE가 16.5%로 증권업계 최고 수준을 유지하고 있습니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: 대형 IPO 3건 주관 수주로 IB 부문 실적 호조, 해외주식 거래량 전월 대비 35% 증가, 웰스케어 자산관리 고객 1.8만명 돌파, 4분기 순이익 컨센서스 +12% 상회 등 4건의 긍정 뉴스가 있습니다. 다만 증시 거래대금 감소, 수수료 인하 경쟁 심화, 시장 변동성 확대 등 3건의 부정 요인이 공존하며 중립적 흐름을 보이고 있습니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="+85억원",
            institution_net="-42억원",
            individual_net="-43억원",
            summary="외국인의 꾸준한 매수세가 이어지고 있으며, 기관과 개인은 일부 차익실현 중입니다. AI 플랫폼 엠파워 성과와 해외주식 거래 확대가 긍정적으로 평가받고 있습니다.",
            period_data=[
                SupplyDemandPeriod(
                    period="1주일", 
                    foreign_net="+520억원", 
                    institution_net="-180억원", 
                    individual_net="-340억원",
                    summary="최근 1주일간 외국인이 520억원을 순매수하며 국내 증권주 중 가장 높은 선호도를 보이고 있습니다. AI 투자 플랫폼 '엠파워' 가입자가 10만명을 돌파하며 디지털 경쟁력이 입증된 점이 호평받고 있습니다. 기관과 개인은 주가 상승에 따른 차익 실현으로 각각 180억원, 340억원을 매도했습니다."
                ),
                SupplyDemandPeriod(
                    period="1개월", 
                    foreign_net="+520억원", 
                    institution_net="-420억원", 
                    individual_net="-100억원",
                    summary="최근 1개월간 외국인이 꾸준히 520억원을 순매수하고 있습니다. 해외주식 거래 플랫폼 강화와 웰스케어 자산관리 사업 성장으로 중장기 성장성이 긍정적으로 평가받고 있습니다. 특히 ROE 16% 이상의 높은 수익성과 안정적인 배당 정책이 외국인 투자자들에게 매력적으로 작용하고 있습니다. 기관은 단기 수익 실현으로 420억원 매도했으며, 개인도 일부 차익 실현 중입니다."
                )
            ]
        ),
        performance=Performance(
            revenue="5.8조원",
            operating_profit="2.1조원",
            net_profit="1.6조원",
            summary="2025년 4분기 실적 컨센서스는 AI 플랫폼 '엠파워' 출시와 해외주식 거래 급증으로 전년 동기 대비 18% 증가가 예상됩니다. 브로커리지 수수료 수입 증가와 IB 부문 호조가 지속되며 ROE 16%를 기록할 것으로 전망됩니다.",
            revenue_yoy="+18.5%",
            revenue_qoq="+11.5%",
            operating_profit_yoy="+25.3%",
            operating_profit_qoq="+16.7%",
            operating_profit_vs_consensus="+10.2%",
            earnings_surprise="컨센서스 대비 +10.2%"
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
                target_price="25,000원",
                opinion="해외주식 거래 플랫폼 경쟁력과 웰스케어 사업 성장. 투자의견 Buy",
                firm="하나증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="24,000원",
                opinion="디지털 자산 사업 확대와 MZ세대 고객 유입 지속. 실적 개선 전망",
                firm="신한투자증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="23,500원",
                opinion="브로커리지 및 IB 부문 안정적 실적. 배당 매력도 높음",
                firm="대신증권",
                trend="neutral"
            )
        ],
        analyst_summary="최근 2개월간 주요 증권사들의 목표가가 **완만하게 상향 조정**되고 있습니다. 하나증권은 25,000원으로 전월 대비 +4.2% 상향했고, 신한투자증권도 24,000원으로 +3.5% 올렸습니다. AI 플랫폼 '엠파워' 성과와 해외주식 거래 확대가 주요 근거입니다. 평균 목표가 24,167원은 현재가 대비 **10% 상승 여력**이 있으며, 67%가 'Buy' 의견으로 긍정적입니다. 디지털 혁신과 ROE 16% 이상의 높은 수익성이 추가 상향 모멘텀으로 작용할 전망입니다.",
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
            per="8.3배",
            pbr="0.75배",
            roe="9.1%",
            dividend_yield="4.11%",
            market_cap="14.2조원",
            shares_outstanding="6.5억주"
        )
    ),
    "373220": StockAnalysis(
        stock_info=StockInfo(
            code="373220",
            name="LG에너지솔루션",
            current_price=385000,
            change_rate=-3.52,
            change_price=-14000,
            volume=1200000,
            ai_summary="[부정] LG에너지솔루션은 최근 6건의 부정 뉴스와 1건의 긍정 뉴스가 보도되며 중국 기업과의 가격 경쟁 심화와 수요 둔화로 심각한 어려움을 겪고 있습니다.\n\n📉 핵심 부정 요인 (6건)\nCATL, BYD 등 중국 배터리 기업들이 추가 가격 인하를 단행하며 배터리 단가 격차가 20-25%로 확대되었고, 글로벌 전기차 시장 성장세 둔화로 주요 고객사들의 배터리 주문이 예상보다 추가 감소하고 있습니다. 원자재 가격 상승으로 원가 부담이 가중되고, 4분기 영업이익이 1,800억원으로 컨센서스 대비 -18% 미달할 것으로 전망됩니다. 미국 IRA 규정 추가 변경으로 한국 배터리 기업들의 보조금 혜택이 더욱 축소되고 있으며, 유럽 시장에서도 점유율이 하락하고 있습니다.\n\n📈 긍정 요인 (1건)\nESS(에너지저장장치) 부문에서 신규 수주가 증가하고 있으나, 전체 매출에서 차지하는 비중이 작아 실적 개선 효과는 제한적입니다.\n\n💰 수급 분석\n외국인과 기관의 매도세가 지속되며 최근 1개월간 외국인 순매도 8,500억원을 기록했습니다. 배터리 업황 악화 우려가 반영되고 있습니다.\n\n🎯 증권가 컨센서스\n평균 목표가 410,000원으로 현재가 대비 약 6% 상승 여력이 있으나 하향 조정 추세입니다. 하나증권 440,000원, 신한투자증권 420,000원, 대신증권 390,000원으로 제시되고 있습니다."
        ),
        news_summary="""<div class="news-item negative">
<div class="news-header">📉 11/26 중국 배터리 기업 가격 경쟁 더욱 심화 <span class="news-importance">★★★★★</span></div>
<div class="news-content">CATL, BYD 등 중국 배터리 기업들이 글로벌 시장에서 추가 가격 인하를 단행하면서 LG에너지솔루션의 수익성에 더 큰 압박이 가해지고 있습니다. 중국 기업들의 배터리 단가는 LG에너지솔루션 대비 20-25% 낮은 수준으로 확대되었으며, 고객사들의 가격 재협상 요구가 급증하고 있습니다. 특히 유럽 시장에서 중국 기업들의 점유율 확대가 가속화되고 있습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/25 전기차 수요 둔화 지속, 배터리 주문 추가 감소 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">글로벌 전기차 시장 성장세가 계속 둔화되면서 주요 고객사들의 배터리 주문이 예상보다 추가로 감소하고 있습니다. 특히 유럽 시장의 전기차 보조금 축소와 중국 시장의 경기 둔화가 지속되며, 2026년 상반기까지 주문 감소세가 이어질 것으로 전망됩니다. GM과 현대차의 2026년 배터리 주문량이 각각 15%, 10% 감소할 것으로 예상됩니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/25 원자재 가격 상승으로 원가 부담 가중 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">리튬과 니켈 등 배터리 핵심 원자재 가격이 3개월 연속 상승하며 원가 부담이 가중되고 있습니다. 특히 수산화리튬 가격이 톤당 15,000달러로 전월 대비 12% 상승했으며, 하이니켈 배터리용 니켈 가격도 8% 올랐습니다. 증권가는 원자재 가격 상승으로 4분기 영업이익이 추가로 500억원 감소할 것으로 전망했습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/24 4분기 영업이익 컨센서스 대비 -18% 미달 전망 <span class="news-importance">★★★★★</span></div>
<div class="news-content">증권가는 LG에너지솔루션 4분기 영업이익을 1,800억원으로 하향 조정했으며, 이는 시장 컨센서스 2,200억원을 18% 하회하는 수치입니다. 배터리 단가 하락과 원자재 가격 상승이 동시에 발생하면서 수익성이 크게 악화되었습니다. 영업이익률은 전년 동기 대비 3.5%p 하락한 2.3%를 기록할 것으로 예상됩니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/23 유럽 시장 점유율 하락, 경쟁 심화 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">LG에너지솔루션의 유럽 배터리 시장 점유율이 3분기 연속 하락하며 22%에서 18%로 떨어졌습니다. CATL과 BYD 등 중국 기업들이 유럽 현지 공장을 증설하며 공격적으로 시장을 잠식하고 있습니다. 특히 독일과 프랑스 자동차 업체들이 중국산 배터리 채택을 늘리면서 LG에너지솔루션의 입지가 축소되고 있습니다. 증권가는 2026년에도 유럽 시장 점유율 하락이 지속될 것으로 전망했습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/23 ESS 시장 확대, 신규 수주 증가 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">글로벌 에너지저장장치(ESS) 시장 성장으로 LG에너지솔루션의 ESS 부문 신규 수주가 증가하고 있습니다. 북미와 유럽 지역에서 총 5.2GWh 규모의 프로젝트를 수주했으나, ESS 매출은 전체의 8%에 불과해 전기차 배터리 부문 부진을 만회하기에는 역부족입니다. 그럼에도 ESS 부문은 마진이 높아 부분적인 수익성 개선에는 기여할 것으로 기대됩니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/23 미국 IRA 세부 규정 변경으로 보조금 혜택 추가 축소 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">미국 인플레이션 감소법(IRA)의 세부 규정이 추가로 변경되면서 한국 배터리 기업들의 보조금 혜택이 예상보다 더 축소될 가능성이 높아졌습니다. 특히 중국산 원자재 사용 비율 제한이 더욱 강화되면서 공급망 재구성 비용이 증가할 전망이며, 미국 현지 생산 비용도 상승 압력이 있습니다. 2026년 IRA 보조금 수혜액이 당초 예상 대비 25% 감소할 것으로 추정됩니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: 중국 배터리 기업 가격 경쟁 더욱 심화, 전기차 수요 둔화 지속으로 배터리 주문 추가 감소, 원자재 가격 상승, 4분기 영업이익 컨센서스 대비 -18% 미달 전망, 미국 IRA 규정 변경으로 보조금 혜택 추가 축소, 유럽 시장 점유율 하락 등 6건의 부정 뉴스가 지속되고 있습니다. ESS 시장 신규 수주 증가 1건의 긍정 요인이 있으나 전체 실적 개선에는 역부족입니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="-320억원",
            institution_net="-180억원",
            individual_net="+500억원",
            summary="외국인과 기관의 매도세가 지속되며 개인 투자자들이 하락세를 매수하고 있습니다. 중국 배터리 기업과의 가격 경쟁 심화와 전기차 수요 둔화 우려가 반영되고 있습니다.",
            period_data=[
                SupplyDemandPeriod(
                    period="1주일", 
                    foreign_net="-1,200억원", 
                    institution_net="-650억원", 
                    individual_net="+1,850억원",
                    summary="최근 1주일간 외국인과 기관의 매도세가 크게 강화되었습니다. 4분기 영업이익이 컨센서스 대비 18% 미달할 것이라는 전망이 나오며 외국인은 1,200억원, 기관은 650억원을 순매도했습니다. 중국 CATL, BYD와의 가격 경쟁 심화와 전기차 수요 둔화가 주요 매도 요인입니다. 개인은 주가 하락을 저점 매수 기회로 판단하며 1,850억원을 순매수했습니다."
                ),
                SupplyDemandPeriod(
                    period="1개월", 
                    foreign_net="-8,500억원", 
                    institution_net="-2,300억원", 
                    individual_net="+10,800억원",
                    summary="최근 1개월간 외국인이 무려 8,500억원을 순매도하며 배터리 업황에 대한 비관적 전망을 반영하고 있습니다. 중국 배터리 기업들의 공격적인 가격 인하와 글로벌 전기차 시장 성장 둔화, 미국 IRA 규정 변경 등이 복합적으로 작용했습니다. 기관 역시 2,300억원을 순매도하며 단기 실적 부담을 우려하고 있습니다. 반면 개인은 밸류에이션 매력과 중장기 전기차 시장 성장 기대감으로 1조원 이상을 순매수하며 저점 매수에 나섰습니다."
                )
            ]
        ),
        performance=Performance(
            revenue="7.8조원",
            operating_profit="2,200억원",
            net_profit="1,500억원",
            summary="2025년 4분기 실적 컨센서스는 중국 배터리 기업들의 가격 경쟁 심화와 전기차 수요 둔화로 전년 동기 대비 영업이익 35% 감소가 예상됩니다. 영업이익률은 2.8%로 전년 동기 대비 크게 악화될 것으로 전망되며, 컨센서스 대비 -15% 미달할 가능성이 높습니다.",
            revenue_yoy="+3.2%",
            revenue_qoq="-4.9%",
            operating_profit_yoy="-35.5%",
            operating_profit_qoq="-22.8%",
            operating_profit_vs_consensus="-15.0%",
            earnings_surprise="컨센서스 대비 -15.0%"
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
                target_price="450,000원",
                opinion="중국 기업 가격 경쟁과 전기차 수요 둔화로 단기 실적 부담. 목표가 하향",
                firm="하나증권",
                trend="down"
            ),
            AnalystOpinion(
                target_price="430,000원",
                opinion="배터리 업황 악화와 수익성 압박 지속. 투자의견 Hold로 전환",
                firm="신한투자증권",
                trend="down"
            ),
            AnalystOpinion(
                target_price="400,000원",
                opinion="단기 실적 부담 지속 예상. 중장기 회복 가능성은 있으나 신중 접근 필요",
                firm="대신증권",
                trend="neutral"
            )
        ],
        analyst_summary="최근 3개월간 주요 증권사들의 목표가가 **지속적으로 하향 조정**되고 있습니다. 하나증권은 450,000원으로 전월 대비 -8.2% 하향했고, 신한투자증권은 430,000원으로 -11.3% 대폭 낮췄습니다. 중국 배터리 기업과의 가격 경쟁 심화와 전기차 수요 둔화가 주요 하향 근거입니다. 평균 목표가 426,667원은 현재가 대비 **11% 상승 여력**에 불과하며, 67%가 'Hold' 또는 'Sell' 의견으로 신중론이 우세합니다. 단기 실적 부담과 업황 악화로 추가 하향 가능성도 있어 주의가 필요합니다.",
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
            per="45.2배",
            pbr="2.85배",
            roe="6.3%",
            dividend_yield="0.85%",
            market_cap="89조원",
            shares_outstanding="23.1억주"
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


