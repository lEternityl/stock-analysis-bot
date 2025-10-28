"""
股票分析系统主程序
整合所有模块，提供完整的分析流程
"""
import sys
import os
from typing import List, Dict, Any
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.tushare_client import TushareClient
from agents.llm_client import DeepSeekClient
from agents.analysts import TechnicalAnalyst, FundamentalAnalyst, NewsAnalyst
from agents.researchers import BullResearcher, BearResearcher, DebateCoordinator
from agents.decision_maker import Trader, RiskManager
from reports.report_generator import ReportGenerator
from config.config import (
    DEEPSEEK_API_KEY, 
    DEEPSEEK_API_BASE, 
    DEEPSEEK_MODEL,
    TUSHARE_TOKEN,
    MAX_DEBATE_ROUNDS,
    LLM_CONFIG,
    validate_config
)

class StockAnalysisSystem:
    """股票分析系统"""
    
    def __init__(self, deepseek_key: str = None, tushare_token: str = None):
        """初始化系统"""
        print("="*80)
        print("🚀 初始化股票分析系统")
        print("="*80)
        
        # 使用提供的key或配置文件中的key
        self.deepseek_key = deepseek_key or DEEPSEEK_API_KEY
        self.tushare_token = tushare_token or TUSHARE_TOKEN
        
        # 初始化数据客户端
        print("\n📊 初始化Tushare数据客户端...")
        self.tushare_client = TushareClient(self.tushare_token)
        
        # 初始化LLM客户端
        print("🤖 初始化DeepSeek AI客户端...")
        self.llm_client = DeepSeekClient(
            api_key=self.deepseek_key,
            base_url=DEEPSEEK_API_BASE,
            model=DEEPSEEK_MODEL
        )
        
        # 初始化分析师团队
        print("👥 初始化分析师团队...")
        self.technical_analyst = TechnicalAnalyst(self.llm_client)
        self.fundamental_analyst = FundamentalAnalyst(self.llm_client)
        self.news_analyst = NewsAnalyst(self.llm_client)
        
        # 初始化研究员
        print("🔬 初始化研究员团队...")
        self.bull_researcher = BullResearcher(self.llm_client)
        self.bear_researcher = BearResearcher(self.llm_client)
        self.debate_coordinator = DebateCoordinator(self.llm_client)
        
        # 初始化决策层
        print("💼 初始化决策层...")
        self.trader = Trader(self.llm_client)
        self.risk_manager = RiskManager(self.llm_client)
        
        # 初始化报告生成器
        print("📄 初始化报告生成器...")
        self.report_generator = ReportGenerator()
        
        print("\n✅ 系统初始化完成！")
        print("="*80 + "\n")
    
    def analyze_stock(self, stock_code: str, save_cache: bool = True) -> Dict[str, Any]:
        """分析单只股票"""
        print("\n" + "="*80)
        print(f"📊 开始分析股票: {stock_code}")
        print("="*80)
        
        start_time = datetime.now()
        
        # 1. 数据收集
        print("\n【阶段 1/6】数据收集")
        print("-" * 80)
        stock_data = self.tushare_client.get_comprehensive_data(stock_code)
        
        if save_cache:
            self.tushare_client.save_data_to_cache(stock_code, stock_data)
        
        # 2. 专业分析
        print("\n【阶段 2/6】专业分析")
        print("-" * 80)
        
        technical_result = self.technical_analyst.analyze(stock_data)
        fundamental_result = self.fundamental_analyst.analyze(stock_data)
        news_result = self.news_analyst.analyze(stock_data)
        
        analysis_results = {
            'technical': technical_result,
            'fundamental': fundamental_result,
            'news': news_result
        }
        
        # 3. 结构化辩论
        print("\n【阶段 3/6】结构化辩论")
        print("-" * 80)
        
        bull_view = self.bull_researcher.research(
            {'analysts': analysis_results}, stock_data
        )
        bear_view = self.bear_researcher.research(
            {'analysts': analysis_results}, stock_data
        )
        
        debate_result = self.debate_coordinator.coordinate_debate(
            bull_view, bear_view, stock_data, max_rounds=MAX_DEBATE_ROUNDS
        )
        
        # 4. 综合决策
        print("\n【阶段 4/6】综合决策")
        print("-" * 80)
        
        all_analysis = {
            'analysts': analysis_results,
            'debate': debate_result
        }
        
        trading_decision = self.trader.make_decision(all_analysis, stock_data)
        
        # 5. 风险评估
        print("\n【阶段 5/6】风险评估")
        print("-" * 80)
        
        risk_assessment = self.risk_manager.assess_risk(
            trading_decision, all_analysis, stock_data
        )
        
        # 6. 报告生成
        print("\n【阶段 6/6】报告生成")
        print("-" * 80)
        
        final_result = {
            'stock_data': stock_data,
            'analysis': all_analysis,
            'decision': trading_decision,
            'risk_assessment': risk_assessment,
            'analysis_time': datetime.now().isoformat(),
            'duration_seconds': (datetime.now() - start_time).total_seconds()
        }
        
        report_file = self.report_generator.generate_report(stock_code, final_result)
        final_result['report_file'] = report_file
        
        # 完成
        duration = datetime.now() - start_time
        print("\n" + "="*80)
        print(f"✅ 分析完成！耗时: {duration.total_seconds():.1f}秒")
        print(f"📋 报告文件: {report_file}")
        print("="*80 + "\n")
        
        return final_result
    
    def batch_analyze(self, stock_codes: List[str]) -> List[Dict[str, Any]]:
        """批量分析多只股票"""
        print("\n" + "="*80)
        print(f"📊 批量分析模式: {len(stock_codes)} 只股票")
        print("="*80 + "\n")
        
        results = []
        
        for i, stock_code in enumerate(stock_codes, 1):
            print(f"\n{'='*80}")
            print(f"进度: [{i}/{len(stock_codes)}] 分析 {stock_code}")
            print('='*80)
            
            try:
                result = self.analyze_stock(stock_code)
                results.append(result)
            except Exception as e:
                print(f"\n❌ 分析 {stock_code} 失败: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # 生成汇总报告
        if results:
            print("\n" + "="*80)
            print("📊 生成批量分析汇总报告")
            print("="*80)
            summary_file = self.report_generator.generate_summary_report(results)
            print(f"\n✅ 批量分析完成！")
            print(f"   成功: {len(results)}/{len(stock_codes)} 只")
            print(f"   汇总报告: {summary_file}")
            print("="*80 + "\n")
        
        return results
    
    def quick_view(self, stock_code: str):
        """快速查看（只获取数据，不做深度分析）"""
        print(f"\n📊 快速查看: {stock_code}")
        stock_data = self.tushare_client.get_comprehensive_data(stock_code)
        
        basic_info = stock_data.get('basic_info', {})
        realtime_quote = stock_data.get('realtime_quote', {})
        
        print("\n" + "="*60)
        print(f"股票名称: {basic_info.get('name', 'N/A')}")
        print(f"股票代码: {stock_code}")
        print(f"所属行业: {basic_info.get('industry', 'N/A')}")
        print(f"当前价格: ¥{realtime_quote.get('close', 'N/A')}")
        print(f"涨跌幅: {realtime_quote.get('pct_chg', 'N/A')}%")
        print(f"成交量: {realtime_quote.get('vol', 'N/A')} 手")
        print("="*60 + "\n")
        
        return stock_data


def main():
    """主函数 - 命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AI驱动的股票分析系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 分析单只股票
  python main.py --stock 600519.SH
  
  # 批量分析
  python main.py --batch 600519.SH 000858.SZ 601318.SH
  
  # 快速查看
  python main.py --quick 600519.SH
  
  # 分析股票池中的所有股票
  python main.py --watchlist
        """
    )
    
    parser.add_argument('--stock', '-s', type=str, help='分析单只股票（例如: 600519.SH）')
    parser.add_argument('--batch', '-b', nargs='+', help='批量分析多只股票')
    parser.add_argument('--watchlist', '-w', action='store_true', help='分析配置的股票池')
    parser.add_argument('--quick', '-q', type=str, help='快速查看股票信息')
    
    args = parser.parse_args()
    
    # 验证配置
    try:
        validate_config()
    except ValueError as e:
        print(f"\n❌ 配置错误: {e}")
        print("\n请检查以下配置:")
        print("  1. 创建 .env 文件（可参考 env_example.txt）")
        print("  2. 设置 DEEPSEEK_API_KEY")
        print("  3. 设置 TUSHARE_TOKEN")
        return
    
    # 创建分析系统
    system = StockAnalysisSystem()
    
    # 执行操作
    if args.quick:
        # 快速查看
        system.quick_view(args.quick)
    
    elif args.stock:
        # 分析单只股票
        system.analyze_stock(args.stock)
    
    elif args.batch:
        # 批量分析
        system.batch_analyze(args.batch)
    
    elif args.watchlist:
        # 分析股票池
        from config.config import STOCK_WATCHLIST
        system.batch_analyze(STOCK_WATCHLIST)
    
    else:
        # 交互模式
        print("\n欢迎使用股票分析系统！")
        print("\n请选择操作:")
        print("  1. 分析单只股票")
        print("  2. 批量分析")
        print("  3. 快速查看")
        print("  4. 分析股票池")
        print("  0. 退出")
        
        choice = input("\n请输入选项 (0-4): ").strip()
        
        if choice == '1':
            stock_code = input("请输入股票代码 (例如: 600519.SH): ").strip()
            system.analyze_stock(stock_code)
        
        elif choice == '2':
            codes_input = input("请输入股票代码，用空格分隔 (例如: 600519.SH 000858.SZ): ").strip()
            codes = codes_input.split()
            system.batch_analyze(codes)
        
        elif choice == '3':
            stock_code = input("请输入股票代码 (例如: 600519.SH): ").strip()
            system.quick_view(stock_code)
        
        elif choice == '4':
            from config.config import STOCK_WATCHLIST
            print(f"\n将分析股票池中的 {len(STOCK_WATCHLIST)} 只股票:")
            for code in STOCK_WATCHLIST:
                print(f"  - {code}")
            confirm = input("\n确认开始分析? (y/n): ").strip().lower()
            if confirm == 'y':
                system.batch_analyze(STOCK_WATCHLIST)
        
        elif choice == '0':
            print("\n再见！")
        
        else:
            print("\n❌ 无效选项")


if __name__ == "__main__":
    main()

