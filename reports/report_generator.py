"""
投资报告生成器
生成专业的投资分析报告
"""
from datetime import datetime
from typing import Dict, Any
import json
import os

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_report(self, stock_code: str, analysis_result: Dict[str, Any]) -> str:
        """生成完整的投资分析报告"""
        print(f"\n📄 正在生成投资报告...")
        
        # 创建新的文件夹结构：reports/股票代码/日期/
        date_str = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H%M%S")
        
        # 清理股票代码，移除.SH/.SZ等后缀用作文件夹名
        clean_stock_code = stock_code.replace('.SH', '').replace('.SZ', '').replace('.HK', '')
        
        # 创建目录结构
        stock_dir = os.path.join(self.output_dir, clean_stock_code)
        date_dir = os.path.join(stock_dir, date_str)
        os.makedirs(date_dir, exist_ok=True)
        
        # 生成文件名
        filename = os.path.join(date_dir, f"analysis_{timestamp}.md")
        json_filename = os.path.join(date_dir, f"analysis_{timestamp}.json")
        
        report_content = self._format_markdown_report(stock_code, analysis_result)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # 同时保存JSON格式
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 报告已生成:")
        print(f"   📋 Markdown: {filename}")
        print(f"   📊 JSON: {json_filename}")
        print(f"   📁 目录结构: {self.output_dir}/{clean_stock_code}/{date_str}/")
        
        return filename
    
    def _format_markdown_report(self, stock_code: str, data: Dict[str, Any]) -> str:
        """格式化Markdown报告"""
        
        stock_data = data.get('stock_data', {})
        basic_info = stock_data.get('basic_info', {})
        realtime_quote = stock_data.get('realtime_quote', {})
        
        analysts = data.get('analysis', {}).get('analysts', {})
        debate = data.get('analysis', {}).get('debate', {})
        decision = data.get('decision', {})
        risk = data.get('risk_assessment', {})
        
        timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        # 获取分析模式
        analysis_mode = data.get('analysis_mode', 'standard')
        mode_emoji = "🌅" if analysis_mode == "pre_market" else "🌆" if analysis_mode == "post_market" else "📊"
        mode_text = "开盘前分析" if analysis_mode == "pre_market" else "收盘后分析" if analysis_mode == "post_market" else "标准分析"
        
        report = f"""# {mode_emoji} 股票投资分析报告 - {mode_text}

---

## 📋 基本信息

**生成时间**: {timestamp}  
**分析类型**: {mode_emoji} {mode_text}  
**股票代码**: {stock_code}  
**股票名称**: {basic_info.get('name', 'N/A')}  
**所属行业**: {basic_info.get('industry', 'N/A')}  
**当前价格**: ¥{realtime_quote.get('close', 'N/A')}  
**涨跌幅**: {realtime_quote.get('pct_chg', 'N/A')}%  

---

## 🎯 投资决策 (核心结论)

### 💼 交易建议
- **操作建议**: {self._get_action_emoji(decision.get('action', ''))} **{decision.get('action', 'N/A')}**
- **仓位建议**: {decision.get('position_size', 'N/A')}
- **目标价位**: {decision.get('target_price', 'N/A')}
- **止损价位**: {decision.get('stop_loss', 'N/A')}
- **持有周期**: {decision.get('holding_period', 'N/A')}
- **决策信心**: {self._get_confidence_bar(decision.get('confidence', 0))} ({decision.get('confidence', 'N/A')}/10)

### 📝 决策理由
{decision.get('reasoning', 'N/A')}

### 🔑 关键因素
{self._format_list(decision.get('key_factors', []))}

---

## 🛡️ 风险评估

### ⚠️ 风险等级
- **总体风险**: {self._get_risk_emoji(risk.get('overall_risk_level', ''))} **{risk.get('overall_risk_level', 'N/A')}**
- **风险评分**: {self._get_risk_bar(risk.get('risk_score', 0))} ({risk.get('risk_score', 'N/A')}/10)
- **建议最大仓位**: {risk.get('max_position_size', 'N/A')}

### 📊 风险细分
- **市场风险**: {risk.get('market_risk', 'N/A')}
- **个股风险**: {risk.get('stock_specific_risk', 'N/A')}
- **行业风险**: {risk.get('industry_risk', 'N/A')}
- **流动性风险**: {risk.get('liquidity_risk', 'N/A')}
- **估值风险**: {risk.get('valuation_risk', 'N/A')}

### 🎯 风险控制建议
{self._format_list(risk.get('risk_control_suggestions', []))}

### 👁️ 监控要点
{self._format_list(risk.get('monitoring_points', []))}

---

## 📈 技术分析

**评分**: {analysts.get('technical', {}).get('technical_score', 'N/A')}/10

### 趋势判断
{analysts.get('technical', {}).get('trend', 'N/A')}

### 成交量分析
{analysts.get('technical', {}).get('volume_analysis', 'N/A')}

### 支撑和阻力
{analysts.get('technical', {}).get('support_resistance', 'N/A')}

### 短期展望
{analysts.get('technical', {}).get('short_term_outlook', 'N/A')}

### 中期展望
{analysts.get('technical', {}).get('medium_term_outlook', 'N/A')}

### 💡 技术面总结
{analysts.get('technical', {}).get('summary', 'N/A')}

---

## 💰 基本面分析

**评分**: {analysts.get('fundamental', {}).get('fundamental_score', 'N/A')}/10

### 盈利能力
{analysts.get('fundamental', {}).get('profitability', 'N/A')}

### 财务健康度
{analysts.get('fundamental', {}).get('financial_health', 'N/A')}

### 盈利质量
{analysts.get('fundamental', {}).get('profitability_quality', 'N/A')}

### 现金流分析
{analysts.get('fundamental', {}).get('cash_flow', 'N/A')}

### 估值分析
{analysts.get('fundamental', {}).get('valuation', 'N/A')}

### 💡 基本面总结
{analysts.get('fundamental', {}).get('summary', 'N/A')}

---

## 📰 新闻分析

**评分**: {analysts.get('news', {}).get('news_score', 'N/A')}/10  
**市场情绪**: {analysts.get('news', {}).get('sentiment', 'N/A')}

### 关键事件
{analysts.get('news', {}).get('key_events', 'N/A')}

### 影响分析
{analysts.get('news', {}).get('impact_analysis', 'N/A')}

### 💡 新闻面总结
{analysts.get('news', {}).get('summary', 'N/A')}

---

## ⚖️ 多空辩论

### 🐂 看涨观点 (信心指数: {debate.get('bull_initial', {}).get('bull_confidence', 'N/A')}/10)

**上涨潜力**: {debate.get('bull_initial', {}).get('upside_potential', 'N/A')}

**买入论点**: {debate.get('bull_initial', {}).get('buy_thesis', 'N/A')}

**利好因素**:
{self._format_list(debate.get('bull_initial', {}).get('bull_points', []))}

**催化剂**:
{self._format_list(debate.get('bull_initial', {}).get('catalysts', []))}

### 🐻 看跌观点 (担忧指数: {debate.get('bear_initial', {}).get('bear_confidence', 'N/A')}/10)

**下跌风险**: {debate.get('bear_initial', {}).get('downside_risk', 'N/A')}

**卖出论点**: {debate.get('bear_initial', {}).get('sell_thesis', 'N/A')}

**风险因素**:
{self._format_list(debate.get('bear_initial', {}).get('bear_points', []))}

**负面催化剂**:
{self._format_list(debate.get('bear_initial', {}).get('negative_catalysts', []))}

### 🎯 辩论总结

**平衡观点**: {debate.get('debate_summary', {}).get('balanced_view', 'N/A')}

**建议倾向**: {debate.get('debate_summary', {}).get('recommendation_lean', 'N/A')}

**信心等级**: {debate.get('debate_summary', {}).get('confidence_level', 'N/A')}/10

---

## ⚠️ 风险提示

本报告由AI多智能体系统自动生成，仅供参考，不构成投资建议。

**重要提示**:
- 股市有风险，投资需谨慎
- 请结合自身风险承受能力做出投资决策
- 建议咨询专业投资顾问
- 过往表现不代表未来收益

---

## 📌 报告信息

- **分析模型**: DeepSeek AI
- **数据来源**: Tushare
- **报告版本**: v1.0
- **生成时间**: {timestamp}

---

*本报告由自动化投资分析系统生成*
"""
        
        return report
    
    def _get_action_emoji(self, action: str) -> str:
        """获取操作对应的emoji"""
        emoji_map = {
            '买入': '🟢',
            '持有': '🟡',
            '卖出': '🔴',
            '观望': '⚪'
        }
        return emoji_map.get(action, '⚪')
    
    def _get_risk_emoji(self, risk_level: str) -> str:
        """获取风险等级对应的emoji"""
        emoji_map = {
            '低': '🟢',
            '中': '🟡',
            '高': '🔴'
        }
        return emoji_map.get(risk_level, '⚪')
    
    def _get_confidence_bar(self, score: int) -> str:
        """生成信心条"""
        try:
            score = int(score)
            filled = '█' * score
            empty = '░' * (10 - score)
            return filled + empty
        except:
            return '░' * 10
    
    def _get_risk_bar(self, score: int) -> str:
        """生成风险条"""
        try:
            score = int(score)
            if score <= 3:
                bar = '🟢' * score + '⚪' * (10 - score)
            elif score <= 7:
                bar = '🟡' * score + '⚪' * (10 - score)
            else:
                bar = '🔴' * score + '⚪' * (10 - score)
            return bar
        except:
            return '⚪' * 10
    
    def _format_list(self, items: list) -> str:
        """格式化列表"""
        if not items:
            return "- 无"
        return '\n'.join([f"- {item}" for item in items])
    
    def generate_summary_report(self, results: list) -> str:
        """生成批量分析汇总报告"""
        print(f"\n📊 正在生成汇总报告...")
        
        # 汇总报告放在根目录下，按日期命名
        date_str = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H%M%S")
        filename = os.path.join(self.output_dir, f"summary_{date_str}_{timestamp}.md")
        
        # 判断分析类型
        analysis_mode = os.getenv('ANALYSIS_MODE', 'standard')
        mode_emoji = "🌅" if analysis_mode == "pre_market" else "🌆" if analysis_mode == "post_market" else "📊"
        mode_text = "开盘前分析" if analysis_mode == "pre_market" else "收盘后分析" if analysis_mode == "post_market" else "标准分析"
        
        content = f"""# {mode_emoji} 批量股票分析汇总报告 - {mode_text}

**生成时间**: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}  
**分析类型**: {mode_emoji} {mode_text}  
**分析数量**: {len(results)} 只股票

---

## 📋 分析结果概览

| 股票代码 | 股票名称 | 操作建议 | 决策信心 | 风险等级 | 报告链接 |
|---------|---------|---------|---------|---------|---------|
"""
        
        for result in results:
            stock_data = result.get('stock_data', {})
            basic_info = stock_data.get('basic_info', {})
            decision = result.get('decision', {})
            risk = result.get('risk_assessment', {})
            
            ts_code = stock_data.get('ts_code', 'N/A')
            name = basic_info.get('name', 'N/A')
            action = decision.get('action', 'N/A')
            confidence = decision.get('confidence', 'N/A')
            risk_level = risk.get('overall_risk_level', 'N/A')
            report_file = result.get('report_file', 'N/A')
            
            # 修复报告链接路径 - 移除多余的reports/前缀
            if report_file.startswith('reports/'):
                relative_path = report_file[8:]  # 移除 'reports/' 前缀
            else:
                relative_path = report_file
            
            content += f"| {ts_code} | {name} | {action} | {confidence}/10 | {risk_level} | [{ts_code}]({relative_path}) |\n"
        
        content += f"""
---

## 🎯 投资建议统计

"""
        # 统计各类建议数量
        buy_count = sum(1 for r in results if r.get('decision', {}).get('action') == '买入')
        hold_count = sum(1 for r in results if r.get('decision', {}).get('action') == '持有')
        sell_count = sum(1 for r in results if r.get('decision', {}).get('action') == '卖出')
        
        content += f"""- 🟢 买入: {buy_count} 只
- 🟡 持有: {hold_count} 只
- 🔴 卖出: {sell_count} 只

---

*本汇总报告由自动化投资分析系统生成*
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 汇总报告已生成: {filename}")
        
        # 同时生成目录索引
        self._generate_index_file()
        
        return filename
    
    def _generate_index_file(self):
        """生成reports目录索引文件"""
        index_file = os.path.join(self.output_dir, "README.md")
        
        content = f"""# 📊 股票分析报告目录

**最后更新**: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}

## 📁 目录结构说明

```
reports/
├── README.md                    # 本索引文件
├── summary_YYYY-MM-DD_HHMMSS.md # 每日汇总报告
├── 股票代码1/                    # 按股票分类
│   ├── YYYY-MM-DD/              # 按日期分类
│   │   ├── analysis_HHMMSS.md   # 分析报告(Markdown)
│   │   └── analysis_HHMMSS.json # 分析数据(JSON)
│   └── YYYY-MM-DD/
└── 股票代码2/
    └── YYYY-MM-DD/
```

## 📈 股票分析报告

"""
        
        # 扫描现有报告，生成索引
        try:
            for item in os.listdir(self.output_dir):
                item_path = os.path.join(self.output_dir, item)
                
                # 跳过非目录和特殊文件
                if not os.path.isdir(item_path) or item.startswith('.'):
                    continue
                    
                content += f"### 📊 {item}\n\n"
                
                # 扫描日期目录
                dates = []
                for date_item in os.listdir(item_path):
                    date_path = os.path.join(item_path, date_item)
                    if os.path.isdir(date_path):
                        dates.append(date_item)
                
                # 按日期排序（最新的在前）
                dates.sort(reverse=True)
                
                for date in dates[:5]:  # 只显示最近5天
                    date_path = os.path.join(item_path, date)
                    reports = [f for f in os.listdir(date_path) if f.endswith('.md')]
                    
                    if reports:
                        # 取最新的报告
                        latest_report = sorted(reports)[-1]
                        report_path = f"{item}/{date}/{latest_report}"
                        content += f"- [{date}]({report_path}) - 最新分析报告\n"
                
                content += "\n"
                
        except Exception as e:
            print(f"⚠️ 生成索引时出错: {e}")
        
        content += f"""
## 🔍 使用说明

### 📋 报告类型
- **汇总报告**: `summary_*.md` - 每日所有股票的分析汇总
- **个股报告**: `股票代码/日期/analysis_*.md` - 单只股票的详细分析

### 📊 数据格式
- **Markdown格式** (`.md`) - 适合阅读的格式化报告
- **JSON格式** (`.json`) - 结构化数据，适合程序处理

### 🕒 更新频率
- 每天早上8:00自动分析并生成报告
- 手动触发也会生成报告

---

*本目录由AI股票分析系统自动维护*
"""
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📋 目录索引已更新: {index_file}")

