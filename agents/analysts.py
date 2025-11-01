"""
分析师智能体
包括：技术分析师、基本面分析师、新闻分析师
"""
from typing import Dict, Any
from .llm_client import DeepSeekClient
import json

class TechnicalAnalyst:
    """技术分析师"""
    
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client
        self.role = "技术分析师"
        
    def analyze(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """技术面分析"""
        print(f"\n📈 {self.role}正在分析...")
        
        # 准备数据
        ts_code = stock_data.get('ts_code', 'N/A')
        basic_info = stock_data.get('basic_info', {}) or {}
        daily_data = stock_data.get('daily_data', []) or []
        realtime_quote = stock_data.get('realtime_quote', {}) or {}
        intraday_data = stock_data.get('intraday_data', []) or []
        is_trading_time = stock_data.get('is_trading_time', False)
        
        # 构建分析输入
        data_summary = f"""
股票代码: {ts_code}
股票名称: {basic_info.get('name', 'N/A')}
所属行业: {basic_info.get('industry', 'N/A')}
数据获取时间: {stock_data.get('fetch_time', 'N/A')}
是否交易时间: {'是' if is_trading_time else '否'}

最新行情:
- 收盘价: {realtime_quote.get('close', 'N/A')}
- 涨跌幅: {realtime_quote.get('pct_chg', 'N/A')}%
- 成交量: {realtime_quote.get('vol', 'N/A')}手
- 成交额: {realtime_quote.get('amount', 'N/A')}千元

近期行情数据（最近10个交易日）:
{json.dumps(daily_data[-10:] if len(daily_data) > 10 else daily_data, ensure_ascii=False, indent=2)}
"""
        
        # 如果有盘中数据，添加到分析中
        if intraday_data:
            data_summary += f"""

盘中数据（最近1小时）:
{json.dumps(intraday_data[-10:] if len(intraday_data) > 10 else intraday_data, ensure_ascii=False, indent=2)}
"""
        
        system_prompt = """你是一位资深的股票技术分析师，擅长通过技术指标和K线形态判断股票走势。

请基于提供的行情数据，进行全面的技术分析，包括：
1. 价格趋势分析（上升/下降/震荡）
2. 成交量分析
3. 支撑位和阻力位
4. 短期和中期走势判断
5. 技术面评分（1-10分）

请以JSON格式输出，包含以下字段：
{
    "trend": "趋势判断",
    "volume_analysis": "成交量分析",
    "support_resistance": "支撑和阻力位",
    "short_term_outlook": "短期展望",
    "medium_term_outlook": "中期展望",
    "technical_score": 技术面评分(1-10),
    "summary": "技术面总结"
}"""
        
        response = self.llm.analyze_with_system_prompt(system_prompt, data_summary)
        result = self.llm.parse_json_response(response)
        
        print(f"✅ 技术分析完成，评分: {result.get('technical_score', 'N/A')}/10")
        return result


class FundamentalAnalyst:
    """基本面分析师"""
    
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client
        self.role = "基本面分析师"
        
    def analyze(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """基本面分析"""
        print(f"\n💰 {self.role}正在分析...")
        
        ts_code = stock_data.get('ts_code', 'N/A')
        basic_info = stock_data.get('basic_info', {}) or {}
        financial_data = stock_data.get('financial_data', {}) or {}
        financial_indicators = stock_data.get('financial_indicators', []) or []
        
        data_summary = f"""
股票代码: {ts_code}
股票名称: {basic_info.get('name', 'N/A')}
所属行业: {basic_info.get('industry', 'N/A')}
上市日期: {basic_info.get('list_date', 'N/A')}

财务数据:
{json.dumps(financial_data, ensure_ascii=False, indent=2)}

财务指标:
{json.dumps(financial_indicators, ensure_ascii=False, indent=2)}
"""
        
        system_prompt = """你是一位资深的基本面分析师，擅长通过财务报表和财务指标评估公司价值。

请基于提供的财务数据，进行全面的基本面分析，包括：
1. 盈利能力分析（营收、净利润增长）
2. 财务健康度（资产负债率、流动比率）
3. 盈利质量（ROE、ROA、毛利率）
4. 现金流状况
5. 估值水平判断
6. 基本面评分（1-10分）

请以JSON格式输出，包含以下字段：
{
    "profitability": "盈利能力分析",
    "financial_health": "财务健康度",
    "profitability_quality": "盈利质量",
    "cash_flow": "现金流分析",
    "valuation": "估值分析",
    "fundamental_score": 基本面评分(1-10),
    "summary": "基本面总结"
}"""
        
        response = self.llm.analyze_with_system_prompt(system_prompt, data_summary)
        result = self.llm.parse_json_response(response)
        
        print(f"✅ 基本面分析完成，评分: {result.get('fundamental_score', 'N/A')}/10")
        return result


class NewsAnalyst:
    """新闻分析师"""
    
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client
        self.role = "新闻分析师"
        
    def analyze(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """新闻面分析"""
        print(f"\n📰 {self.role}正在分析...")
        
        ts_code = stock_data.get('ts_code', 'N/A')
        basic_info = stock_data.get('basic_info', {}) or {}
        news_data = stock_data.get('news', []) or []
        
        if not news_data:
            print("⚠️ 没有新闻数据，跳过新闻分析")
            return {
                "sentiment": "中性",
                "key_events": "无重大新闻事件",
                "impact_analysis": "无明显影响",
                "news_score": 5,
                "summary": "近期无重大新闻，市场情绪中性"
            }
        
        data_summary = f"""
股票代码: {ts_code}
股票名称: {basic_info.get('name', 'N/A')}

近期相关新闻:
{json.dumps(news_data[:10], ensure_ascii=False, indent=2)}
"""
        
        system_prompt = """你是一位资深的新闻分析师，擅长从新闻和舆情中判断市场情绪和事件影响。

请基于提供的新闻数据，进行全面的新闻面分析，包括：
1. 市场情绪分析（积极/中性/消极）
2. 关键事件识别
3. 事件影响程度
4. 舆情风险评估
5. 新闻面评分（1-10分，10分表示极度利好）

请以JSON格式输出，包含以下字段：
{
    "sentiment": "市场情绪(积极/中性/消极)",
    "key_events": "关键事件总结",
    "impact_analysis": "影响分析",
    "risk_assessment": "舆情风险",
    "news_score": 新闻面评分(1-10),
    "summary": "新闻面总结"
}"""
        
        response = self.llm.analyze_with_system_prompt(system_prompt, data_summary)
        result = self.llm.parse_json_response(response)
        
        print(f"✅ 新闻分析完成，情绪: {result.get('sentiment', 'N/A')}, 评分: {result.get('news_score', 'N/A')}/10")
        return result

