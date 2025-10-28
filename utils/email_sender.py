"""
邮件发送器
支持发送股票分析报告到指定邮箱
"""
import smtplib
import os
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import List, Optional
import json

class EmailSender:
    """通用邮件发送器"""
    
    def __init__(self):
        """从环境变量初始化邮件配置"""
        self.enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.qq.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
        self.recipient_emails = [
            email.strip() 
            for email in os.getenv("RECIPIENT_EMAILS", "").split(",") 
            if email.strip()
        ]
        
        if not self.enabled:
            print("📧 邮件推送未启用")
            return
            
        # 验证配置
        if not all([self.sender_email, self.sender_password, self.recipient_emails]):
            print("❌ 邮件配置不完整，请检查环境变量")
            self.enabled = False
            return
            
        print(f"📧 邮件推送已启用: {self.sender_email} -> {len(self.recipient_emails)} 个收件人")
    
    def send_daily_report(self, reports_dir: str = "reports") -> bool:
        """发送每日分析报告"""
        if not self.enabled:
            print("📧 邮件推送未启用，跳过发送")
            return False
            
        try:
            # 查找今日生成的报告
            today = datetime.now().strftime("%Y%m%d")
            summary_files = glob.glob(f"{reports_dir}/summary_{today}_*.md")
            
            if not summary_files:
                print("❌ 未找到今日汇总报告")
                return False
            
            latest_summary = max(summary_files)  # 获取最新的汇总报告
            
            # 读取汇总报告
            with open(latest_summary, 'r', encoding='utf-8') as f:
                summary_content = f.read()
            
            # 查找所有今日报告
            all_reports = glob.glob(f"{reports_dir}/*{today}_*.md")
            json_reports = glob.glob(f"{reports_dir}/*{today}_*.json")
            
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ", ".join(self.recipient_emails)
            msg['Subject'] = f"📊 每日股票分析报告 - {datetime.now().strftime('%Y年%m月%d日')}"
            
            # 邮件正文
            body = self._create_email_body(summary_content, len(all_reports))
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 附件：汇总报告
            self._attach_file(msg, latest_summary)
            
            # 附件：详细报告（限制数量避免邮件过大）
            for report_file in all_reports[:10]:  # 最多10个详细报告
                self._attach_file(msg, report_file)
            
            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ 邮件发送成功: {len(self.recipient_emails)} 个收件人")
            print(f"   汇总报告: {os.path.basename(latest_summary)}")
            print(f"   详细报告: {len(all_reports)} 个")
            
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_email_body(self, summary_content: str, report_count: int) -> str:
        """创建邮件正文"""
        # 从Markdown提取关键信息
        lines = summary_content.split('\n')
        
        # 提取表格数据
        table_started = False
        stocks_info = []
        
        for line in lines:
            if '| 股票代码 |' in line:
                table_started = True
                continue
            elif table_started and line.startswith('|') and '---' not in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]  # 去掉首尾空元素
                if len(parts) >= 5:
                    stocks_info.append({
                        'code': parts[0],
                        'name': parts[1], 
                        'action': parts[2],
                        'confidence': parts[3],
                        'risk': parts[4]
                    })
            elif table_started and not line.startswith('|'):
                break
        
        # 统计建议
        buy_count = sum(1 for s in stocks_info if '买入' in s['action'])
        hold_count = sum(1 for s in stocks_info if '持有' in s['action'])
        sell_count = sum(1 for s in stocks_info if '卖出' in s['action'])
        
        # 生成HTML邮件
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px; }}
        .summary {{ background: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #007bff; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat-item {{ text-align: center; padding: 15px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #007bff; }}
        .stock-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .stock-table th, .stock-table td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        .stock-table th {{ background-color: #f8f9fa; font-weight: bold; }}
        .action-buy {{ color: #28a745; font-weight: bold; }}
        .action-hold {{ color: #ffc107; font-weight: bold; }}
        .action-sell {{ color: #dc3545; font-weight: bold; }}
        .footer {{ text-align: center; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
        .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 每日股票分析报告</h1>
        <p>{datetime.now().strftime('%Y年%m月%d日')} | AI智能分析</p>
    </div>
    
    <div class="summary">
        <h2>📋 分析概览</h2>
        <p><strong>分析股票数量:</strong> {len(stocks_info)} 只</p>
        <p><strong>报告生成时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>分析模型:</strong> DeepSeek AI + Tushare数据</p>
    </div>
    
    <div class="stats">
        <div class="stat-item">
            <div class="stat-number" style="color: #28a745;">{buy_count}</div>
            <div>🟢 买入推荐</div>
        </div>
        <div class="stat-item">
            <div class="stat-number" style="color: #ffc107;">{hold_count}</div>
            <div>🟡 持有建议</div>
        </div>
        <div class="stat-item">
            <div class="stat-number" style="color: #dc3545;">{sell_count}</div>
            <div>🔴 卖出建议</div>
        </div>
    </div>
    
    <h2>📈 详细分析结果</h2>
    <table class="stock-table">
        <thead>
            <tr>
                <th>股票代码</th>
                <th>股票名称</th>
                <th>操作建议</th>
                <th>决策信心</th>
                <th>风险等级</th>
            </tr>
        </thead>
        <tbody>
"""
        
        for stock in stocks_info:
            action_class = "action-buy" if "买入" in stock['action'] else "action-hold" if "持有" in stock['action'] else "action-sell"
            html_body += f"""
            <tr>
                <td>{stock['code']}</td>
                <td>{stock['name']}</td>
                <td class="{action_class}">{stock['action']}</td>
                <td>{stock['confidence']}</td>
                <td>{stock['risk']}</td>
            </tr>
"""
        
        html_body += f"""
        </tbody>
    </table>
    
    <div class="warning">
        <h3>⚠️ 重要提示</h3>
        <p>本报告由AI系统自动生成，仅供参考，不构成投资建议。投资有风险，决策需谨慎。</p>
    </div>
    
    <div class="footer">
        <p>📎 详细分析报告请查看邮件附件</p>
        <p>🤖 由GitHub Actions自动生成 | DeepSeek AI驱动</p>
        <p><small>报告包含 {report_count} 个详细分析文件</small></p>
    </div>
</body>
</html>
"""
        
        return html_body
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """添加文件附件"""
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(file_path)}'
            )
            msg.attach(part)
        except Exception as e:
            print(f"⚠️ 添加附件失败 {file_path}: {e}")


def main():
    """主函数 - 用于GitHub Actions调用"""
    print("\n📧 开始发送每日报告邮件...")
    
    sender = EmailSender()
    success = sender.send_daily_report()
    
    if success:
        print("✅ 邮件发送任务完成")
    else:
        print("❌ 邮件发送任务失败")
        exit(1)


if __name__ == "__main__":
    main()
