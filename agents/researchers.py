"""
研究员智能体
包括：看涨研究员、看跌研究员、辩论协调器
"""
from typing import Dict, Any, List
from .llm_client import DeepSeekClient
import json

class BullResearcher:
    """看涨研究员 - 寻找买入理由"""
    
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client
        self.role = "看涨研究员"
        
    def research(self, analysis_results: Dict[str, Any], stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """从看涨角度研究"""
        print(f"\n🐂 {self.role}正在研究...")
        
        ts_code = stock_data.get('ts_code', 'N/A')
        basic_info = stock_data.get('basic_info', {}) or {}
        
        # 整合分析结果
        context = f"""
股票信息:
- 代码: {ts_code}
- 名称: {basic_info.get('name', 'N/A')}
- 行业: {basic_info.get('industry', 'N/A')}

各分析师观点:
技术分析: {json.dumps(analysis_results.get('technical', {}), ensure_ascii=False, indent=2)}

基本面分析: {json.dumps(analysis_results.get('fundamental', {}), ensure_ascii=False, indent=2)}

新闻分析: {json.dumps(analysis_results.get('news', {}), ensure_ascii=False, indent=2)}
"""
        
        system_prompt = """你是一位看涨研究员，你的任务是从乐观的角度评估投资机会。

请基于各分析师的观点，从看涨角度进行深度研究：
1. 找出所有利好因素和投资亮点
2. 分析上涨潜力和催化剂
3. 提出买入理由和价格目标
4. 评估风险但保持乐观态度
5. 给出看涨信心指数（1-10分）

请以JSON格式输出：
{
    "bull_points": ["利好点1", "利好点2", ...],
    "upside_potential": "上涨潜力分析",
    "catalysts": ["催化剂1", "催化剂2", ...],
    "buy_thesis": "买入论点",
    "price_target": "目标价位分析",
    "bull_confidence": 看涨信心(1-10),
    "summary": "看涨观点总结"
}"""
        
        response = self.llm.analyze_with_system_prompt(system_prompt, context)
        result = self.llm.parse_json_response(response)
        
        print(f"✅ 看涨研究完成，信心指数: {result.get('bull_confidence', 'N/A')}/10")
        return result


class BearResearcher:
    """看跌研究员 - 寻找风险和卖出理由"""
    
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client
        self.role = "看跌研究员"
        
    def research(self, analysis_results: Dict[str, Any], stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """从看跌角度研究"""
        print(f"\n🐻 {self.role}正在研究...")
        
        ts_code = stock_data.get('ts_code', 'N/A')
        basic_info = stock_data.get('basic_info', {}) or {}
        
        context = f"""
股票信息:
- 代码: {ts_code}
- 名称: {basic_info.get('name', 'N/A')}
- 行业: {basic_info.get('industry', 'N/A')}

各分析师观点:
技术分析: {json.dumps(analysis_results.get('technical', {}), ensure_ascii=False, indent=2)}

基本面分析: {json.dumps(analysis_results.get('fundamental', {}), ensure_ascii=False, indent=2)}

新闻分析: {json.dumps(analysis_results.get('news', {}), ensure_ascii=False, indent=2)}
"""
        
        system_prompt = """你是一位看跌研究员，你的任务是从谨慎的角度评估投资风险。

请基于各分析师的观点，从看跌角度进行深度研究：
1. 识别所有风险因素和利空点
2. 分析下跌风险和负面催化剂
3. 提出卖出或观望理由
4. 评估估值是否过高
5. 给出看跌担忧指数（1-10分）

请以JSON格式输出：
{
    "bear_points": ["风险点1", "风险点2", ...],
    "downside_risk": "下跌风险分析",
    "negative_catalysts": ["负面催化剂1", "负面催化剂2", ...],
    "sell_thesis": "卖出/观望论点",
    "valuation_concern": "估值担忧",
    "bear_confidence": 看跌担忧(1-10),
    "summary": "看跌观点总结"
}"""
        
        response = self.llm.analyze_with_system_prompt(system_prompt, context)
        result = self.llm.parse_json_response(response)
        
        print(f"✅ 看跌研究完成，担忧指数: {result.get('bear_confidence', 'N/A')}/10")
        return result


class DebateCoordinator:
    """辩论协调器 - 组织看涨和看跌研究员辩论"""
    
    def __init__(self, llm_client: DeepSeekClient):
        self.llm = llm_client
        self.role = "辩论协调器"
        
    def coordinate_debate(self, bull_view: Dict[str, Any], bear_view: Dict[str, Any], 
                         stock_data: Dict[str, Any], max_rounds: int = 2) -> Dict[str, Any]:
        """协调多轮辩论"""
        print(f"\n⚖️ {self.role}正在组织辩论...")
        
        ts_code = stock_data.get('ts_code', 'N/A')
        basic_info = stock_data.get('basic_info', {}) or {}
        
        debate_history = []
        
        for round_num in range(1, max_rounds + 1):
            print(f"\n  📢 第 {round_num}/{max_rounds} 轮辩论")
            
            # 看涨方反驳
            if round_num > 1:
                bull_rebuttal = self._get_rebuttal(
                    "看涨方", bull_view, bear_view, 
                    debate_history, stock_data
                )
                debate_history.append({"round": round_num, "speaker": "bull", "content": bull_rebuttal})
            
            # 看跌方反驳
            bear_rebuttal = self._get_rebuttal(
                "看跌方", bear_view, bull_view,
                debate_history, stock_data
            )
            debate_history.append({"round": round_num, "speaker": "bear", "content": bear_rebuttal})
        
        # 总结辩论
        debate_summary = self._summarize_debate(bull_view, bear_view, debate_history, stock_data)
        
        print(f"✅ 辩论完成，共 {max_rounds} 轮")
        
        return {
            "bull_initial": bull_view,
            "bear_initial": bear_view,
            "debate_rounds": debate_history,
            "debate_summary": debate_summary
        }
    
    def _get_rebuttal(self, side: str, own_view: Dict[str, Any], 
                     opponent_view: Dict[str, Any], history: List[Dict],
                     stock_data: Dict[str, Any]) -> str:
        """生成辩论反驳"""
        
        context = f"""
股票: {stock_data.get('basic_info', {}).get('name', 'N/A')} ({stock_data.get('ts_code', 'N/A')})

你的初始观点（{side}）:
{json.dumps(own_view, ensure_ascii=False, indent=2)}

对方观点:
{json.dumps(opponent_view, ensure_ascii=False, indent=2)}

辩论历史:
{json.dumps(history, ensure_ascii=False, indent=2)}
"""
        
        system_prompt = f"""你是{side}的代表，在进行投资辩论。

请针对对方的观点进行反驳和补充论证：
1. 指出对方观点的不足或偏颇之处
2. 强化自己的核心论点
3. 提供新的证据或角度
4. 保持专业和客观

请直接输出反驳内容，无需JSON格式。"""
        
        rebuttal = self.llm.analyze_with_system_prompt(system_prompt, context, temperature=0.8)
        return rebuttal
    
    def _summarize_debate(self, bull_view: Dict[str, Any], bear_view: Dict[str, Any],
                         history: List[Dict], stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """总结辩论结果"""
        
        context = f"""
股票: {stock_data.get('basic_info', {}).get('name', 'N/A')} ({stock_data.get('ts_code', 'N/A')})

看涨观点:
{json.dumps(bull_view, ensure_ascii=False, indent=2)}

看跌观点:
{json.dumps(bear_view, ensure_ascii=False, indent=2)}

完整辩论过程:
{json.dumps(history, ensure_ascii=False, indent=2)}
"""
        
        system_prompt = """你是一位客观的投资顾问，需要总结看涨和看跌双方的辩论。

请提供一个平衡的总结：
1. 双方的核心论点
2. 最有说服力的观点
3. 关键分歧点
4. 综合风险评估
5. 平衡建议倾向（偏看涨/中性/偏看跌）

请以JSON格式输出：
{
    "bull_key_points": "看涨核心论点",
    "bear_key_points": "看跌核心论点",
    "most_convincing": "最有说服力的观点",
    "key_disagreements": "关键分歧",
    "balanced_view": "平衡观点",
    "recommendation_lean": "建议倾向(偏看涨/中性/偏看跌)",
    "confidence_level": "建议信心(1-10)"
}"""
        
        response = self.llm.analyze_with_system_prompt(system_prompt, context)
        result = self.llm.parse_json_response(response)
        
        return result

