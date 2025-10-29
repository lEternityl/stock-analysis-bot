"""
决策智能体
包括：交易员（综合决策）、风险管理员（风险评估）
"""
from typing import Dict, Any
from .llm_client import DeepSeekClient
import json

class Trader:
    """交易员 - 综合所有信息做出最终交易决策"""
    
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client
        self.role = "资深交易员"
        
    def make_decision(self, all_analysis: Dict[str, Any], stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """做出最终交易决策"""
        print(f"\n💼 {self.role}正在做出决策...")
        
        ts_code = stock_data.get('ts_code', 'N/A')
        basic_info = stock_data.get('basic_info', {}) or {} or {}
        realtime_quote = stock_data.get('realtime_quote', {}) or {}
        
        # 整合所有分析结果
        context = f"""
股票信息:
- 代码: {ts_code}
- 名称: {basic_info.get('name', 'N/A')}
- 行业: {basic_info.get('industry', 'N/A')}
- 当前价格: {realtime_quote.get('close', 'N/A')}元

分析师团队意见:
{json.dumps(all_analysis.get('analysts', {}), ensure_ascii=False, indent=2)}

研究员辩论结果:
{json.dumps(all_analysis.get('debate', {}), ensure_ascii=False, indent=2)}
"""
        
        system_prompt = """你是一位经验丰富的股票交易员，负责做出最终的投资决策。

你已经听取了技术分析师、基本面分析师、新闻分析师的专业意见，
也参考了看涨和看跌研究员的深度辩论。

现在，请基于所有信息做出最终决策：

1. 投资建议: 买入/持有/卖出
2. 建议仓位: 轻仓/半仓/重仓（如果是买入）
3. 目标价位: 预期价格范围
4. 止损价位: 风险控制价位
5. 持有周期: 短期/中期/长期
6. 决策信心: 1-10分
7. 决策理由: 详细说明

请以JSON格式输出：
{
    "action": "买入/持有/卖出",
    "position_size": "仓位建议",
    "target_price": "目标价位",
    "stop_loss": "止损价位",
    "holding_period": "持有周期",
    "confidence": 决策信心(1-10),
    "reasoning": "详细决策理由",
    "key_factors": ["关键因素1", "关键因素2", ...],
    "risks": ["主要风险1", "主要风险2", ...],
    "summary": "决策总结"
}"""
        
        response = self.llm.analyze_with_system_prompt(system_prompt, context, temperature=0.6)
        result = self.llm.parse_json_response(response)
        
        action = result.get('action', 'N/A')
        confidence = result.get('confidence', 'N/A')
        print(f"✅ 交易决策完成: {action}, 信心: {confidence}/10")
        
        return result


class RiskManager:
    """风险管理员 - 评估投资风险"""
    
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client
        self.role = "风险管理员"
        
    def assess_risk(self, trading_decision: Dict[str, Any], all_analysis: Dict[str, Any], 
                   stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估风险等级"""
        print(f"\n🛡️ {self.role}正在评估风险...")
        
        ts_code = stock_data.get('ts_code', 'N/A')
        basic_info = stock_data.get('basic_info', {}) or {}
        
        context = f"""
股票信息:
- 代码: {ts_code}
- 名称: {basic_info.get('name', 'N/A')}
- 行业: {basic_info.get('industry', 'N/A')}

交易决策:
{json.dumps(trading_decision, ensure_ascii=False, indent=2)}

完整分析:
{json.dumps(all_analysis, ensure_ascii=False, indent=2)}
"""
        
        system_prompt = """你是一位专业的风险管理员，负责评估投资风险并提供风险控制建议。

请从以下维度评估风险：

1. 市场风险: 市场整体波动对该股票的影响
2. 个股风险: 公司特定风险（财务、经营、治理等）
3. 行业风险: 行业周期和政策风险
4. 流动性风险: 成交量和流动性评估
5. 估值风险: 当前估值是否合理
6. 新闻舆情风险: 负面新闻和舆论风险

综合评估：
- 总体风险等级: 低/中/高
- 风险评分: 1-10分（10分表示风险极高）
- 风险控制建议

请以JSON格式输出：
{
    "market_risk": "市场风险评估",
    "stock_specific_risk": "个股风险评估",
    "industry_risk": "行业风险评估",
    "liquidity_risk": "流动性风险评估",
    "valuation_risk": "估值风险评估",
    "sentiment_risk": "舆情风险评估",
    "overall_risk_level": "低/中/高",
    "risk_score": 风险评分(1-10),
    "risk_control_suggestions": ["建议1", "建议2", ...],
    "max_position_size": "建议最大仓位",
    "monitoring_points": ["监控点1", "监控点2", ...],
    "summary": "风险评估总结"
}"""
        
        response = self.llm.analyze_with_system_prompt(system_prompt, context, temperature=0.5)
        result = self.llm.parse_json_response(response)
        
        risk_level = result.get('overall_risk_level', 'N/A')
        risk_score = result.get('risk_score', 'N/A')
        print(f"✅ 风险评估完成: {risk_level}风险, 评分: {risk_score}/10")
        
        return result

