const { useState, useEffect } = React;

const App = () => {
    const [selectedStock, setSelectedStock] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [stockData, setStockData] = useState(null);
    const [error, setError] = useState(null);
    
    const loadStockAnalysis = async (stockCode) => {
        if (!stockCode) {
            setStockData(null);
            return;
        }
        
        setIsLoading(true);
        setError(null);
        
        try {
            const response = await fetch(`/api/stock/${stockCode}`);
            
            if (!response.ok) {
                throw new Error('데이터를 불러올 수 없습니다.');
            }
            
            const data = await response.json();
            
            // AI 분석 느낌을 위한 딜레이
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // 투자 지표를 stock_info에 추가
            data.stock_info.investment_metrics = data.investment_metrics;
            
            setStockData(data);
        } catch (err) {
            console.error('Error loading stock analysis:', err);
            setError('데이터를 불러오는 중 오류가 발생했습니다.');
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleStockSelect = (stockCode) => {
        setSelectedStock(stockCode);
        loadStockAnalysis(stockCode);
    };
    
    // AI 시황 분석 파싱
    const getAISummary = () => {
        if (!stockData) return { text: '', sentiment: '중립' };
        
        const aiSummaryText = stockData.stock_info.ai_summary;
        const sentimentMatch = aiSummaryText.match(/\[(긍정|부정|중립)\]/);
        const sentiment = sentimentMatch ? sentimentMatch[1] : '중립';
        const cleanedText = aiSummaryText.replace(/\[(긍정|부정|중립)\]\s*/, '');
        
        return { text: cleanedText, sentiment };
    };
    
    // 뉴스 요약 파싱
    const getNewsSummary = () => {
        if (!stockData) return { html: '', sentiment: '중립' };
        
        let newsHTML = stockData.news_summary;
        newsHTML = newsHTML.replace(/<div class="ai-conclusion">.*?<\/div>/s, '');
        
        // 뉴스 아이템 추출
        const newsItemRegex = /<div class="news-item (positive|negative|neutral)">[\s\S]*?<\/div>\s*(?=<div class="news-item|<div class="ai-conclusion|$)/g;
        const allNewsItems = [];
        let match;
        
        while ((match = newsItemRegex.exec(newsHTML)) !== null) {
            allNewsItems.push(match[0].trim());
        }
        
        // 각 뉴스 아이템에 배지 추가
        const processedItems = allNewsItems.map(item => {
            return item.replace(
                /<div class="news-item (positive|negative|neutral)">\s*<div class="news-header">/,
                (match, sentiment) => {
                    const sentimentIcon = sentiment === 'positive' ? 'arrow_upward' : 
                                        sentiment === 'negative' ? 'arrow_downward' : 'remove';
                    const sentimentLabel = sentiment === 'positive' ? '긍정' : 
                                         sentiment === 'negative' ? '부정' : '중립';
                    return `<div class="news-item ${sentiment}">
                            <div class="news-header">
                            <span class="news-sentiment-badge-inline sentiment-${sentiment}">
                                <span class="material-icons sentiment-icon">${sentimentIcon}</span>${sentimentLabel}
                            </span>`;
                }
            );
        });
        
        const overallSentimentMatch = allNewsItems[0]?.match(/class="news-item\s+(positive|negative|neutral)"/);
        const sentiment = overallSentimentMatch ? 
            (overallSentimentMatch[1] === 'positive' ? '긍정' : 
             overallSentimentMatch[1] === 'negative' ? '부정' : '중립') : '중립';
        
        return { html: processedItems.join('\n\n'), sentiment };
    };
    
    const aiSummary = getAISummary();
    const newsSummary = getNewsSummary();
    
    return (
        <div className="app-container">
            <Header onStockSelect={handleStockSelect} selectedStock={selectedStock} />
            
            <LoadingScreen isLoading={isLoading} />
            
            {error && (
                <div className="error-message animate-shake">
                    <span className="material-icons">error_outline</span>
                    {error}
                </div>
            )}
            
            {!stockData && !isLoading && !error && <EmptyState />}
            
            {stockData && !isLoading && (
                <main className="main-content">
                    <StockHeader stockInfo={stockData.stock_info} />
                    
                    <AISummaryTop 
                        summary={aiSummary.text} 
                        sentiment={aiSummary.sentiment} 
                    />
                    
                    <div className="content-layout">
                        <aside className="left-panel-ai">
                            <AINewsCard 
                                newsSummary={newsSummary.html} 
                                sentiment={newsSummary.sentiment} 
                            />
                            
                            <SectorNewsCard 
                                sectorName={stockData.sector_name} 
                                sectorNews={stockData.sector_news} 
                            />
                        </aside>
                        
                        <aside className="right-panel-components">
                            <InvestmentPointsCard investmentPoints={stockData.investment_points} />
                            <SupplyDemandCard supplyDemand={stockData.supply_demand} />
                            <PerformanceCard performance={stockData.performance} />
                            <AnalystCard 
                                analystOpinions={stockData.analyst_opinions} 
                                analystSummary={stockData.analyst_summary}
                            />
                        </aside>
                    </div>
                </main>
            )}
        </div>
    );
};

// React 앱 렌더링
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

