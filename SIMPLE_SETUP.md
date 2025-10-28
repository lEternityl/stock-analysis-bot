# 🚀 GitHub自动化股票分析 - 简化部署指南

## 📋 快速开始（3步完成）

### 1️⃣ 创建GitHub仓库并上传代码

```bash
# 1. 在GitHub上创建新仓库（例如：my-stock-bot）
# 2. 克隆到本地
git clone https://github.com/你的用户名/my-stock-bot.git
cd my-stock-bot

# 3. 复制项目文件
cp -r /path/to/auto-run/* .

# 4. 提交代码
git add .
git commit -m "🚀 初始化股票分析机器人"
git push origin main
```

### 2️⃣ 配置GitHub Secrets

在GitHub仓库页面：`Settings` → `Secrets and variables` → `Actions`

添加以下2个Secrets：

| Secret名称 | 值 |
|-----------|---|
| `DEEPSEEK_API_KEY` | `sk-32badf3759f74b41b7797ce0f60994da` |
| `TUSHARE_TOKEN` | `2876ea85cb005fb5fa17c809a98174f2d5aae8b1f830110a5ead6211` |

### 3️⃣ 启用GitHub通知

在GitHub个人设置中：`Settings` → `Notifications`

确保勾选：
- ✅ **Issues** - 接收Issue通知
- ✅ **Actions** - 接收Actions运行通知

## 🎯 运行方式

### 自动运行
- ⏰ **每天早上8点**自动分析股票池
- 📧 **自动创建Issue**通知你分析结果
- 📊 **报告自动提交**到仓库

### 手动运行
1. 进入仓库的 `Actions` 页面
2. 选择 `📊 每日股票分析` 工作流
3. 点击 `Run workflow` 按钮
4. 选择是否启用测试模式

## 📊 通知方式

### GitHub Issue通知
- ✅ **成功时**：创建包含分析结果的Issue
- ❌ **失败时**：创建错误诊断Issue
- 📧 **邮件通知**：GitHub会自动发送Issue通知到你的邮箱

### 报告查看
- 📋 **在线查看**：点击Issue中的链接
- 📦 **下载报告**：在Actions页面下载完整报告
- 📁 **仓库存储**：所有报告自动提交到`reports/`目录

## 🔧 自定义配置

### 修改股票池
编辑 `config/config.py` 中的 `STOCK_WATCHLIST`：

```python
STOCK_WATCHLIST = [
    "600519.SH",  # 贵州茅台
    "000858.SZ",  # 五粮液
    "600036.SH",  # 招商银行
    # 添加你关注的股票...
]
```

### 修改运行时间
编辑 `.github/workflows/daily-analysis.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 0:00 = 北京时间 8:00
  # 改为其他时间，例如：
  # - cron: '0 2 * * *'  # UTC 2:00 = 北京时间 10:00
```

## 📱 通知效果

### 成功通知示例
```
📊 每日股票分析报告 - 2024/1/15

今日股票分析完成！

📈 分析结果概览：
- 🟢 买入推荐: 2只
- 🟡 持有建议: 2只  
- 🔴 卖出建议: 1只

📎 点击查看详细报告...
```

### 失败通知示例
```
❌ 股票分析失败 - 2024/1/15

请检查API密钥或网络连接
📋 查看详细日志...
```

## 💡 优势特点

- 🆓 **完全免费**：使用GitHub免费额度
- 🤖 **全自动化**：无需人工干预
- 📧 **原生通知**：利用GitHub内置通知系统
- 📊 **专业报告**：AI生成详细投资分析
- 🔒 **安全可靠**：代码开源，数据透明

## 🚨 注意事项

1. **API配额**：注意DeepSeek和Tushare的使用限制
2. **GitHub额度**：免费用户每月有2000分钟Actions时间
3. **股票数量**：建议监控5-10只股票，避免超时
4. **时区设置**：cron时间为UTC，需要转换为北京时间

---

🎉 **完成！** 你的自动化股票分析机器人已经配置完成，每天会自动为你分析股票并通过GitHub Issue通知你！
