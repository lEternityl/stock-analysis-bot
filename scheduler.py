"""
定时任务调度器
每天早上8点自动分析股票池中的股票并推送报告
"""
import schedule
import time
from datetime import datetime
from typing import List
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import (
    STOCK_WATCHLIST, 
    DAILY_REPORT_TIME, 
    validate_config,
    DEEPSEEK_API_KEY,
    TUSHARE_TOKEN
)
from main import StockAnalysisSystem

class DailyScheduler:
    """每日定时任务调度器"""
    
    def __init__(self):
        """初始化调度器"""
        print("🚀 初始化定时任务调度器...")
        
        # 验证配置
        validate_config()
        
        # 创建分析系统
        self.analysis_system = StockAnalysisSystem(
            deepseek_key=DEEPSEEK_API_KEY,
            tushare_token=TUSHARE_TOKEN
        )
        
        self.watchlist = STOCK_WATCHLIST
        print(f"📊 监控股票池: {len(self.watchlist)} 只股票")
        print(f"⏰ 推送时间: 每天 {DAILY_REPORT_TIME}")
        
    def daily_analysis_task(self):
        """每日分析任务"""
        print("\n" + "="*80)
        print(f"📅 执行每日分析任务 - {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        print("="*80)
        
        try:
            # 批量分析
            results = self.analysis_system.batch_analyze(self.watchlist)
            
            # 生成汇总报告
            summary_file = self.analysis_system.report_generator.generate_summary_report(results)
            
            print("\n" + "="*80)
            print(f"✅ 每日分析任务完成！")
            print(f"📊 分析股票: {len(results)} 只")
            print(f"📄 汇总报告: {summary_file}")
            print("="*80 + "\n")
            
            # 这里可以添加推送逻辑（邮件、微信、钉钉等）
            self._send_notification(summary_file, results)
            
        except Exception as e:
            print(f"\n❌ 每日分析任务失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _send_notification(self, summary_file: str, results: list):
        """发送通知（可扩展）"""
        print("\n📧 推送通知...")
        print(f"   汇总报告: {summary_file}")
        print(f"   分析完成: {len(results)} 只股票")
        
        # TODO: 实现邮件推送
        # TODO: 实现企业微信推送
        # TODO: 实现钉钉推送
        
        print("   ✅ 通知推送完成（当前为控制台输出）")
    
    def run_once_now(self):
        """立即执行一次（用于测试）"""
        print("\n🧪 测试模式：立即执行一次分析任务")
        self.daily_analysis_task()
    
    def start(self, test_mode: bool = False):
        """启动调度器"""
        if test_mode:
            # 测试模式：立即执行一次
            self.run_once_now()
            return
        
        # 正式模式：按时间调度
        print(f"\n⏰ 调度器已启动，将在每天 {DAILY_REPORT_TIME} 执行分析")
        print("💡 提示: 按 Ctrl+C 停止调度器\n")
        
        # 设置定时任务
        schedule.every().day.at(DAILY_REPORT_TIME).do(self.daily_analysis_task)
        
        # 显示下次执行时间
        next_run = schedule.next_run()
        if next_run:
            print(f"📅 下次执行时间: {next_run.strftime('%Y年%m月%d日 %H:%M:%S')}\n")
        
        # 持续运行
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n\n⏹️ 调度器已停止")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='股票分析定时调度器')
    parser.add_argument('--test', action='store_true', help='测试模式：立即执行一次')
    parser.add_argument('--once', action='store_true', help='执行一次后退出（同 --test）')
    
    args = parser.parse_args()
    
    scheduler = DailyScheduler()
    
    if args.test or args.once:
        scheduler.start(test_mode=True)
    else:
        scheduler.start(test_mode=False)


if __name__ == "__main__":
    main()

