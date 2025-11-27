const { useState, useEffect, useCallback } = React;

// 로딩 컴포넌트
const LoadingScreen = ({ isLoading }) => {
    if (!isLoading) return null;
    
    return (
        <div className="loading-screen active">
            <div className="loading-container">
                <div className="loading-spinner"></div>
                <div className="loading-waves">
                    <div className="wave"></div>
                    <div className="wave"></div>
                    <div className="wave"></div>
                </div>
                <p className="loading-text">AI가 데이터를 분석하고 있습니다...</p>
                <div className="loading-progress">
                    <div className="progress-bar"></div>
                </div>
            </div>
        </div>
    );
};

// 헤더 컴포넌트
const Header = ({ onStockSelect, selectedStock }) => {
    const stocks = [
        { value: "", label: "종목을 선택하세요" },
        { value: "005930", label: "삼성전자 (005930)" },
        { value: "000660", label: "SK하이닉스 (000660)" },
        { value: "006800", label: "미래에셋증권 (006800)" },
        { value: "373220", label: "LG에너지솔루션 (373220)" }
    ];
    
    // 1번: 홈으로 돌아가기 핸들러
    const handleLogoClick = () => {
        onStockSelect('');  // 빈 문자열로 설정하여 EmptyState로 돌아감
    };
    
    return (
        <header className="header animate-slide-down">
            <div className="header-left">
                <div className="logo-container" onClick={handleLogoClick} style={{cursor: 'pointer'}}>
                    <span className="material-icons logo-icon">trending_up</span>
                    <h1 className="logo">KAIROS</h1>
                </div>
                <span className="subtitle">AI 종목 분석</span>
            </div>
            <div className="header-right">
                <div className="stock-selector">
                    <label>
                        <span className="material-icons">search</span>
                        종목 선택
                    </label>
                    <select 
                        id="stockSelector" 
                        value={selectedStock}
                        onChange={(e) => onStockSelect(e.target.value)}
                        className="stock-select-modern"
                    >
                        {stocks.map(stock => (
                            <option key={stock.value} value={stock.value}>
                                {stock.label}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
        </header>
    );
};

// 빈 상태 컴포넌트
const EmptyState = () => {
    return (
        <div className="empty-state animate-fade-in">
            <div className="empty-content">
                <div className="empty-icon-wrapper">
                    <span className="material-icons empty-icon">show_chart</span>
                </div>
                <h2>종목을 선택해주세요</h2>
                <p>상단에서 분석하실 종목을 선택하면<br/>AI가 종합 분석한 시황 정보를 제공합니다.</p>
                <div className="empty-features">
                    <div className="feature-item">
                        <span className="material-icons">auto_awesome</span>
                        <span>AI 뉴스 분석</span>
                    </div>
                    <div className="feature-item">
                        <span className="material-icons">insights</span>
                        <span>실시간 시황</span>
                    </div>
                    <div className="feature-item">
                        <span className="material-icons">analytics</span>
                        <span>투자 인사이트</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

// 종목 헤더 컴포넌트
const StockHeader = ({ stockInfo }) => {
    const isUp = stockInfo.change_rate > 0;
    const sign = isUp ? '+' : '';
    
    return (
        <section className="stock-header animate-slide-up">
            <div className="stock-header-top">
                <div className="stock-title">
                    <h2>{stockInfo.name}</h2>
                    <span className="stock-code">{stockInfo.code}</span>
                </div>
                <div className="stock-price-info">
                    <div className={`current-price ${isUp ? 'price-up' : 'price-down'}`}>
                        {stockInfo.current_price.toLocaleString('ko-KR')}
                        <span className="currency">원</span>
                    </div>
                    <div className={`price-change ${isUp ? 'price-up' : 'price-down'}`}>
                        <span className="change-price">{sign}{stockInfo.change_price.toLocaleString('ko-KR')}</span>
                        <span className="change-rate">({sign}{stockInfo.change_rate}%)</span>
                    </div>
                </div>
                <div className="stock-metrics-inline">
                    {[
                        { label: 'PER', value: stockInfo.investment_metrics?.per || '-' },
                        { label: 'PBR', value: stockInfo.investment_metrics?.pbr || '-' },
                        { label: 'ROE', value: stockInfo.investment_metrics?.roe || '-' },
                        { label: '배당률', value: stockInfo.investment_metrics?.dividend_yield || '-' }
                    ].map((metric, idx) => (
                        <div key={metric.label} className="metric-inline-item" style={{animationDelay: `${idx * 0.1}s`}}>
                            <span className="metric-inline-label">{metric.label}</span>
                            <span className="metric-inline-value">{metric.value}</span>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

// AI 종합 분석 배지
const SentimentBadge = ({ sentiment, large }) => {
    const getSentimentInfo = () => {
        if (sentiment === '긍정' || sentiment === 'positive') {
            return { icon: 'arrow_upward', class: 'positive', label: '긍정' };
        } else if (sentiment === '부정' || sentiment === 'negative') {
            return { icon: 'arrow_downward', class: 'negative', label: '부정' };
        }
        return { icon: 'remove', class: 'neutral', label: '중립' };
    };
    
    const info = getSentimentInfo();
    const className = large ? 'sentiment-badge-large' : 'sentiment-badge';
    
    return (
        <span className={`${className} sentiment-${info.class}`}>
            <span className="material-icons sentiment-icon">{info.icon}</span>
            {info.label}
        </span>
    );
};

// AI 종합 분석 (상단)
const AISummaryTop = ({ summary, sentiment }) => {
    return (
        <section className="ai-summary-top animate-slide-up" style={{animationDelay: '0.1s'}}>
            <div className="ai-summary-box">
                <div className="ai-badge">
                    <span className="material-icons">psychology</span>
                    AI 종합 분석
                </div>
                <div className="ai-summary-with-sentiment">
                    <SentimentBadge sentiment={sentiment} large />
                    <div className="ai-summary-text" dangerouslySetInnerHTML={{ __html: formatAiSummary(summary) }} />
                </div>
            </div>
        </section>
    );
};

// 뉴스 아이템 컴포넌트
const NewsItem = ({ news, index }) => {
    return (
        <div className={`news-item ${news.sentiment} animate-fade-in`} style={{animationDelay: `${index * 0.1}s`}}>
            <div className="news-header">
                <SentimentBadge sentiment={news.sentiment} />
                <span className="news-title-text">{news.title}</span>
                {news.importance && (
                    <span className="news-importance">{'★'.repeat(news.importance)}</span>
                )}
            </div>
            <div className="news-content">{news.content}</div>
        </div>
    );
};

// AI 뉴스 요약 카드
const AINewsCard = ({ newsSummary, sentiment }) => {
    return (
        <div className="card ai-main-card animate-scale-in">
            <div className="card-header">
                <span className="material-icons">bolt</span>
                <h2>AI 뉴스 요약</h2>
                <SentimentBadge sentiment={sentiment} large />
            </div>
            <div className="card-content">
                <div className="ai-main-summary-text" dangerouslySetInnerHTML={{ __html: newsSummary }} />
            </div>
        </div>
    );
};

// 섹터 동향 카드
const SectorNewsCard = ({ sectorName, sectorNews }) => {
    return (
        <div className="card sector-news-card animate-scale-in" style={{animationDelay: '0.1s'}}>
            <div className="card-header">
                <span className="material-icons">layers</span>
                <h3>{sectorName} 섹터 동향</h3>
            </div>
            <div className="card-content">
                <div className="sector-news-list">
                    {sectorNews.map((news, idx) => (
                        <div key={idx} className={`sector-news-item sentiment-${news.sentiment} animate-slide-in`} style={{animationDelay: `${idx * 0.1}s`}}>
                            <div className="sector-news-header">
                                <span className="sector-news-date">{news.date}</span>
                                <SentimentBadge sentiment={news.sentiment} />
                            </div>
                            <div className="sector-news-title">{news.title}</div>
                            <div className="sector-news-summary">{news.summary}</div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

// 투자 판단 포인트 카드
const InvestmentPointsCard = ({ investmentPoints }) => {
    return (
        <div className="card investment-points-card animate-scale-in" style={{animationDelay: '0.2s'}}>
            <div className="card-header">
                <span className="material-icons">info</span>
                <h3>투자 판단 포인트</h3>
            </div>
            <div className="card-content">
                <div className="investment-section positive-section">
                    <h4>
                        <span className="material-icons">check_circle</span>
                        긍정 요인
                    </h4>
                    <ul>
                        {investmentPoints.positive.map((point, idx) => (
                            <li key={idx} className="animate-slide-in" style={{animationDelay: `${idx * 0.05}s`}}>{point}</li>
                        ))}
                    </ul>
                </div>
                <div className="investment-section negative-section">
                    <h4>
                        <span className="material-icons">error</span>
                        유의 사항
                    </h4>
                    <ul>
                        {investmentPoints.negative.map((point, idx) => (
                            <li key={idx} className="animate-slide-in" style={{animationDelay: `${idx * 0.05}s`}}>{point}</li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

// 수급 요약 카드
const SupplyDemandCard = ({ supplyDemand }) => {
    const [activePeriod, setActivePeriod] = useState('1일');
    
    const getCurrentData = () => {
        if (activePeriod === '1일') {
            return {
                foreign: supplyDemand.foreign_net,
                institution: supplyDemand.institution_net,
                individual: supplyDemand.individual_net,
                summary: supplyDemand.summary  // 1일 요약
            };
        }
        const periodData = supplyDemand.period_data?.find(p => p.period === activePeriod);
        return periodData ? {
            foreign: periodData.foreign_net,
            institution: periodData.institution_net,
            individual: periodData.individual_net,
            summary: periodData.summary || supplyDemand.summary  // 기간별 요약 또는 기본 요약
        } : {
            foreign: supplyDemand.foreign_net,
            institution: supplyDemand.institution_net,
            individual: supplyDemand.individual_net,
            summary: supplyDemand.summary
        };
    };
    
    const data = getCurrentData();
    const periods = ['1일', '1주일', '1개월'];
    
    const getValueClass = (value) => {
        if (value.startsWith('+')) return 'positive';
        if (value.startsWith('-')) return 'negative';
        return '';
    };
    
    return (
        <div className="card supply-demand-card animate-scale-in" style={{animationDelay: '0.3s'}}>
            <div className="card-header">
                <span className="material-icons">payments</span>
                <h3>수급 요약</h3>
            </div>
            <div className="card-content">
                <div className="supply-tabs">
                    {periods.map(period => (
                        <button
                            key={period}
                            className={`supply-tab ${activePeriod === period ? 'active' : ''}`}
                            onClick={() => setActivePeriod(period)}
                        >
                            {period}
                        </button>
                    ))}
                </div>
                <div className="supply-grid">
                    <div className="supply-item animate-pop">
                        <span className="supply-label">
                            <span className="material-icons">public</span>
                            외국인
                        </span>
                        <span className={`supply-value ${getValueClass(data.foreign)}`}>{data.foreign}</span>
                    </div>
                    <div className="supply-item animate-pop" style={{animationDelay: '0.1s'}}>
                        <span className="supply-label">
                            <span className="material-icons">business</span>
                            기관
                        </span>
                        <span className={`supply-value ${getValueClass(data.institution)}`}>{data.institution}</span>
                    </div>
                    <div className="supply-item animate-pop" style={{animationDelay: '0.2s'}}>
                        <span className="supply-label">
                            <span className="material-icons">person</span>
                            개인
                        </span>
                        <span className={`supply-value ${getValueClass(data.individual)}`}>{data.individual}</span>
                    </div>
                </div>
                {/* AI 요약 아이콘 및 기간별 요약 */}
                <div className="ai-insight-summary">
                    <span className="material-icons ai-insight-icon">lightbulb</span>
                    <p className="supply-summary">{data.summary}</p>
                </div>
            </div>
        </div>
    );
};

// 실적 요약 카드
const PerformanceCard = ({ performance }) => {
    // 3번: 증가/하락 색상 클래스 반환 함수
    const getComparisonClass = (value) => {
        if (!value) return '';
        if (value.includes('+')) return 'comparison-positive';
        if (value.includes('-')) return 'comparison-negative';
        return '';
    };
    
    return (
        <div className="card performance-card animate-scale-in" style={{animationDelay: '0.4s'}}>
            <div className="card-header">
                <span className="material-icons">bar_chart</span>
                <h3>4분기 실적 컨센서스</h3>
            </div>
            <div className="card-content">
                <div className="performance-grid">
                    <div className="performance-item animate-slide-in">
                        <span className="performance-label">매출액</span>
                        <div className="performance-value-group">
                            <span className="performance-value">{performance.revenue}</span>
                            <div className="performance-comparison">
                                {performance.revenue_yoy && (
                                    <span className={`comparison-item ${getComparisonClass(performance.revenue_yoy)}`}>
                                        전년동기: {performance.revenue_yoy}
                                    </span>
                                )}
                                {performance.revenue_qoq && (
                                    <span className={`comparison-item ${getComparisonClass(performance.revenue_qoq)}`}>
                                        직전분기: {performance.revenue_qoq}
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                    <div className="performance-item animate-slide-in" style={{animationDelay: '0.1s'}}>
                        <span className="performance-label">영업이익</span>
                        <div className="performance-value-group">
                            <span className="performance-value">{performance.operating_profit}</span>
                            <div className="performance-comparison">
                                {performance.operating_profit_yoy && (
                                    <span className={`comparison-item ${getComparisonClass(performance.operating_profit_yoy)}`}>
                                        전년동기: {performance.operating_profit_yoy}
                                    </span>
                                )}
                                {performance.operating_profit_qoq && (
                                    <span className={`comparison-item ${getComparisonClass(performance.operating_profit_qoq)}`}>
                                        직전분기: {performance.operating_profit_qoq}
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                    <div className="performance-item animate-slide-in" style={{animationDelay: '0.2s'}}>
                        <span className="performance-label">순이익</span>
                        <span className="performance-value">{performance.net_profit}</span>
                    </div>
                </div>
                {/* 2번: AI 요약 아이콘 추가 */}
                <div className="ai-insight-summary">
                    <span className="material-icons ai-insight-icon">psychology</span>
                    <p className="performance-summary">{performance.summary}</p>
                </div>
            </div>
        </div>
    );
};

// 애널리스트 의견 카드
const AnalystCard = ({ analystOpinions, analystSummary }) => {
    // **텍스트**를 <strong>텍스트</strong>로 변환
    const formatSummary = (text) => {
        if (!text) return '';
        return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    };
    
    // 전체 트렌드 파악 (상향/하향/중립)
    const getOverallTrend = () => {
        const upCount = analystOpinions.filter(a => a.trend === 'up').length;
        const downCount = analystOpinions.filter(a => a.trend === 'down').length;
        
        if (upCount > downCount) return 'up';
        if (downCount > upCount) return 'down';
        return 'neutral';
    };
    
    const overallTrend = getOverallTrend();
    const trendIconClass = overallTrend === 'up' ? 'trend-up-icon' : 
                           overallTrend === 'down' ? 'trend-down-icon' : 'trend-neutral-icon';
    
    return (
        <div className="card analyst-card-right animate-scale-in" style={{animationDelay: '0.5s'}}>
            <div className="card-header">
                <span className="material-icons">groups</span>
                <h3>증권사 목표가 분석</h3>
            </div>
            <div className="card-content">
                <div className="analyst-list">
                    {analystOpinions.map((analyst, idx) => {
                        const trendIcon = analyst.trend === 'up' ? 'trending_up' : 
                                        analyst.trend === 'down' ? 'trending_down' : 'trending_flat';
                        const trendClass = `trend-${analyst.trend}`;
                        
                        return (
                            <div key={idx} className="analyst-item animate-slide-in" style={{animationDelay: `${idx * 0.1}s`}}>
                                <div className="analyst-header">
                                    <span className="analyst-firm">{analyst.firm}</span>
                                    <span className="analyst-target">
                                        {analyst.target_price}
                                        <span className={`trend-indicator ${trendClass}`}>
                                            <span className="material-icons">{trendIcon}</span>
                                        </span>
                                    </span>
                                </div>
                                <div className="analyst-opinion">{analyst.opinion}</div>
                            </div>
                        );
                    })}
                </div>
                {/* AI 목표가 트렌드 요약 */}
                {analystSummary && (
                    <div className="ai-insight-summary" style={{marginTop: '16px'}}>
                        <span className={`material-icons ai-insight-icon ${trendIconClass}`}>insights</span>
                        <p className="analyst-summary" dangerouslySetInnerHTML={{ __html: formatSummary(analystSummary) }} />
                    </div>
                )}
            </div>
        </div>
    );
};

// 유틸리티 함수
function formatAiSummary(text) {
    const cleaned = text.replace(/\[(긍정|부정|중립)\]\s*/, '');
    const sections = cleaned.split('\n\n');
    let formattedHTML = '';
    
    sections.forEach(section => {
        const trimmed = section.trim();
        if (!trimmed) return;
        
        if (trimmed.match(/^[📈📉💰🎯🏭]/)) {
            formattedHTML += `<div class="ai-summary-section-header">${trimmed}</div>`;
        } else {
            formattedHTML += `<div class="ai-summary-content">${trimmed}</div>`;
        }
    });
    
    return formattedHTML;
}

