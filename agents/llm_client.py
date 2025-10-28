"""
DeepSeek LLM客户端
用于与DeepSeek API交互
"""
from openai import OpenAI
from typing import List, Dict, Any, Optional
import json

class DeepSeekClient:
    """DeepSeek客户端"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1", model: str = "deepseek-chat"):
        """初始化DeepSeek客户端"""
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """发送聊天请求"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ DeepSeek API调用失败: {e}")
            return f"错误: {str(e)}"
    
    def analyze_with_system_prompt(self, system_prompt: str, user_input: str, 
                                   temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """使用系统提示词进行分析"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        return self.chat(messages, temperature, max_tokens)
    
    def structured_analysis(self, role: str, task: str, data: str, 
                          output_format: str = "JSON", temperature: float = 0.7) -> str:
        """结构化分析"""
        system_prompt = f"""你是一位专业的{role}。
你的任务是：{task}

请以{output_format}格式输出结果，确保结构清晰、逻辑严谨。
"""
        return self.analyze_with_system_prompt(system_prompt, data, temperature)
    
    def parse_json_response(self, response: str) -> Optional[Dict[str, Any]]:
        """解析JSON响应"""
        try:
            # 尝试提取JSON部分
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except Exception as e:
            print(f"⚠️ JSON解析失败，返回原始文本: {e}")
            return {"raw_response": response}
    
    def multi_round_dialogue(self, system_prompt: str, conversation: List[Dict[str, str]], 
                            temperature: float = 0.7) -> str:
        """多轮对话"""
        messages = [{"role": "system", "content": system_prompt}] + conversation
        return self.chat(messages, temperature)

