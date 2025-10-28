# 🚀 GitHub Actions 自动化部署指南

本指南将帮助你在GitHub上设置自动化股票分析系统，每天定时分析并发送邮件报告。

## 📋 前置准备

### 1. 获取API密钥

#### DeepSeek API Key
1. 访问 [DeepSeek平台](https://platform.deepseek.com/)
2. 注册并登录账户
3. 在API管理页面创建新的API Key
4. 复制保存API Key（格式：`sk-xxxxxx`）

#### Tushare Token
1. 访问 [Tushare官网](https://tushare.pro/)
2. 注册并登录账户
3. 在个人中心获取Token
4. 复制保存Token

#### 邮箱配置（以QQ邮箱为例）
1. 登录QQ邮箱，进入设置 → 账户
2. 开启SMTP服务
3. 生成授权码（不是QQ密码）
4. 记录邮箱地址和授权码

## 🔧 GitHub仓库配置

### 1. 创建GitHub仓库

```bash
# 1. 在GitHub上创建新仓库（例如：stock-analysis-bot）
# 2. 克隆到本地
git clone https://github.com/你的用户名/stock-analysis-bot.git
cd stock-analysis-bot

# 3. 复制项目文件到仓库目录
cp -r /path/to/auto-run/* .

# 4. 提交代码
git add .
git commit -m "🚀 初始化股票分析系统"
git push origin main
```

### 2. 配置GitHub Secrets

在GitHub仓库页面，进入 `Settings` → `Secrets and variables` → `Actions`，添加以下Secrets：

#### 必需的Secrets

| Secret名称 | 说明 | 示例值 |
|-----------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | `sk-xxxxxxxxxxxxxx` |
| `TUSHARE_TOKEN` | Tushare数据接口Token | `your_tushare_token` |

#### 邮件配置Secrets

| Secret名称 | 说明 | 示例值 |
|-----------|------|--------|
| `EMAIL_ENABLED` | 是否启用邮件推送 | `true` |
| `SMTP_SERVER` | SMTP服务器地址 | `smtp.qq.com` |
| `SMTP_PORT` | SMTP端口 | `587` |
| `SENDER_EMAIL` | 发送者邮箱 | `your_email@qq.com` |
| `SENDER_PASSWORD` | 邮箱授权码（不是密码） | `your_auth_code` |
| `RECIPIENT_EMAILS` | 接收者邮箱（多个用逗号分隔） | `email1@qq.com,email2@163.com` |

#### 常用邮箱SMTP配置

| 邮箱服务商 | SMTP服务器 | 端口 | 说明 |
|-----------|-----------|------|------|
| QQ邮箱 | `smtp.qq.com` | `587` | 需要开启SMTP并获取授权码 |
| 163邮箱 | `smtp.163.com` | `587` | 需要开启SMTP并获取授权码 |
| Gmail | `smtp.gmail.com` | `587` | 需要开启两步验证并生成应用密码 |
| Outlook | `smtp-mail.outlook.com` | `587` | 使用账户密码 |

### 3. 配置股票监控列表

编辑 `config/config.py` 文件中的 `STOCK_WATCHLIST`：

```python
STOCK_WATCHLIST = [
    "600519.SH",  # 贵州茅台
    "000858.SZ",  # 五粮液
    "600036.SH",  # 招商银行
    "000001.SZ",  # 平安银行
    "601318.SH",  # 中国平安
    # 添加更多股票...
]
```

### 4. 配置运行时间

默认每天北京时间8:00运行，如需修改，编辑 `.github/workflows/daily-analysis.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 0:00 = 北京时间 8:00
  # 改为其他时间，例如：
  # - cron: '0 2 * * *'  # UTC 2:00 = 北京时间 10:00
```

## 🚀 启动自动化

### 1. 手动测试

在GitHub仓库页面：
1. 点击 `Actions` 标签
2. 选择 `📊 每日股票分析` 工作流
3. 点击 `Run workflow`
4. 选择 `测试模式` 并运行

### 2. 查看运行结果

- **日志**: 在Actions页面查看详细运行日志
- **报告**: 下载Artifacts中的分析报告
- **邮件**: 检查邮箱是否收到报告

### 3. 定时运行

配置完成后，系统将每天自动运行，无需手动干预。

## 📊 功能特性

### 自动化流程
1. **数据收集**: 自动获取股票行情、财务数据
2. **AI分析**: 技术面、基本面、新闻面多维分析
3. **智能辩论**: 看涨/看跌观点辩论
4. **决策生成**: 综合决策和风险评估
5. **报告生成**: 专业格式的分析报告
6. **邮件推送**: 自动发送到指定邮箱
7. **文件存储**: 报告自动提交到GitHub仓库

### 邮件报告内容
- 📊 分析概览和统计
- 📈 详细投资建议表格
- 📎 完整分析报告附件
- ⚠️ 风险提示

### 报告文件
- `reports/summary_YYYYMMDD_HHMMSS.md` - 汇总报告
- `reports/STOCK_CODE_YYYYMMDD_HHMMSS.md` - 个股详细报告
- `reports/*.json` - 结构化数据

## 🔧 故障排除

### 常见问题

#### 1. API调用失败
```
❌ DeepSeek API调用失败: Invalid API key
```
**解决方案**: 检查 `DEEPSEEK_API_KEY` 是否正确设置

#### 2. 数据获取失败
```
❌ 获取股票数据失败: Token无效
```
**解决方案**: 检查 `TUSHARE_TOKEN` 是否有效

#### 3. 邮件发送失败
```
❌ 邮件发送失败: Authentication failed
```
**解决方案**: 
- 检查邮箱授权码是否正确
- 确认SMTP服务已开启
- 验证SMTP服务器和端口配置

#### 4. 工作流权限错误
```
❌ Permission denied (publickey)
```
**解决方案**: 确保仓库有写入权限，检查Actions权限设置

### 调试方法

1. **查看Actions日志**: GitHub仓库 → Actions → 选择运行记录
2. **手动测试**: 使用 `workflow_dispatch` 手动触发
3. **本地测试**: 在本地环境运行代码验证
4. **逐步调试**: 注释部分代码，逐步定位问题

## 📈 高级配置

### 1. 自定义分析参数

编辑 `config/config.py`：

```python
# 分析配置
MAX_DEBATE_ROUNDS = 3  # 增加辩论轮次
ANALYSIS_HISTORY_DAYS = 90  # 增加历史数据天数

# LLM配置
LLM_CONFIG = {
    "temperature": 0.5,  # 降低随机性
    "max_tokens": 6000,  # 增加输出长度
}
```

### 2. 多时间段运行

修改 `.github/workflows/daily-analysis.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'   # 每天8:00
  - cron: '0 6 * * *'   # 每天14:00
  - cron: '0 9 * * 1-5' # 工作日17:00
```

### 3. 条件运行

添加市场开盘检查：

```yaml
- name: 检查交易日
  run: |
    # 添加交易日检查逻辑
    python utils/market_calendar.py
```

## 💡 最佳实践

1. **API配额管理**: 合理设置股票数量，避免超出API限制
2. **错误处理**: 监控Actions运行状态，及时处理失败
3. **数据备份**: 定期下载报告文件进行备份
4. **安全管理**: 定期更换API密钥和邮箱授权码
5. **成本控制**: 监控DeepSeek API使用量和费用

## 📞 技术支持

如遇问题，可以：
1. 查看GitHub Issues
2. 检查Actions运行日志
3. 参考故障排除部分
4. 提交新的Issue求助

---

🎉 **恭喜！** 你的自动化股票分析系统已配置完成，将每天为你提供专业的投资分析报告！
