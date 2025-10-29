# 📊 AI股票分析系统

基于多智能体的股票自动分析系统，专注核心功能，简单高效。

## 🎯 核心功能

- ✅ **数据收集** - 通过Tushare获取全面的A股市场数据
- ✅ **专业分析** - 技术面、基本面、新闻面独立分析
- ✅ **结构化辩论** - 看涨/看跌研究员多轮辩论
- ✅ **综合决策** - 交易员基于所有信息做出投资建议
- ✅ **风险评估** - 风险管理员评估风险等级
- ✅ **报告生成** - 自动生成专业Markdown投资报告
- ✅ **定时推送** - 每天早上8点自动分析并推送

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
cd auto-run
pip install -r requirements.txt
```

### 2️⃣ 配置API密钥

创建 `.env` 文件（参考 `env_example.txt`）：

```bash
# 复制示例文件
cp env_example.txt .env

# 编辑 .env 文件，填入你的API密钥
DEEPSEEK_API_KEY=sk-你的DeepSeek密钥
TUSHARE_TOKEN=你的Tushare令牌
```

**获取API密钥：**
- DeepSeek: https://platform.deepseek.com/
- Tushare: https://tushare.pro/register

### 3️⃣ 配置股票池

编辑 `config/config.py`，设置要监控的股票：

```python
STOCK_WATCHLIST = [
    "600519.SH",  # 贵州茅台
    "000858.SZ",  # 五粮液
    "600036.SH",  # 招商银行
    # 添加你关注的股票...
]
```

### 4️⃣ 运行分析

#### 方式1: 命令行模式

```bash
# 分析单只股票
python main.py --stock 600519.SH

# 批量分析
python main.py --batch 600519.SH 000858.SZ 601318.SH

# 分析股票池
python main.py --watchlist

# 快速查看
python main.py --quick 600519.SH
```

#### 方式2: 交互模式

```bash
python main.py
# 然后按提示选择操作
```

#### 方式3: 定时任务

```bash
# 测试模式（立即执行一次）
python scheduler.py --test

# 正式运行（每天8点自动执行）
python scheduler.py
```

## 📁 项目结构

```
auto-run/
├── agents/              # 智能体模块
│   ├── llm_client.py   # DeepSeek客户端
│   ├── analysts.py     # 分析师（技术、基本面、新闻）
│   ├── researchers.py  # 研究员（看涨、看跌）
│   └── decision_maker.py # 决策层（交易员、风险管理）
├── data/               # 数据模块
│   ├── tushare_client.py # Tushare数据客户端
│   └── cache/          # 数据缓存目录
├── reports/            # 报告模块
│   └── report_generator.py # 报告生成器
├── config/             # 配置文件
│   └── config.py       # 系统配置
├── logs/               # 日志目录
├── main.py             # 主程序
├── scheduler.py        # 定时任务调度器
├── requirements.txt    # 依赖列表
└── README.md          # 说明文档
```

## 📊 分析流程

系统按以下6个阶段进行分析：

1. **数据收集** 📊
   - 获取股票基本信息
   - 获取历史行情数据
   - 获取财务数据和指标
   - 获取实时行情
   - 获取相关新闻

2. **专业分析** 👥
   - 技术分析师：技术指标、趋势判断
   - 基本面分析师：财务健康度、估值分析
   - 新闻分析师：市场情绪、事件影响

3. **结构化辩论** ⚖️
   - 看涨研究员：寻找投资亮点
   - 看跌研究员：识别风险隐患
   - 辩论协调器：组织多轮辩论

4. **综合决策** 💼
   - 交易员综合所有信息
   - 给出买入/持有/卖出建议
   - 设定目标价位和止损位

5. **风险评估** 🛡️
   - 评估市场风险、个股风险
   - 给出风险等级和评分
   - 提供风险控制建议

6. **报告生成** 📄
   - 自动生成Markdown格式报告
   - 保存JSON格式数据
   - 生成批量分析汇总

## 📈 报告示例

分析完成后会生成两种文件：

1. **个股报告** - `reports/600519.SH_20241028_080000.md`
   - 包含完整的6个阶段分析结果
   - Markdown格式，易读易分享

2. **汇总报告** - `reports/summary_20241028_080000.md`
   - 批量分析结果汇总
   - 投资建议统计

## ⚙️ 配置说明

### 股票池配置

在 `config/config.py` 中修改：

```python
STOCK_WATCHLIST = [
    "600519.SH",  # 沪市股票
    "000858.SZ",  # 深市股票
]
```

**股票代码格式：**
- 沪市：代码 + `.SH` （如：600519.SH）
- 深市：代码 + `.SZ` （如：000858.SZ）

### 定时任务配置

```python
DAILY_REPORT_TIME = "08:00"  # 每天8点执行
```

### 分析参数配置

```python
MAX_DEBATE_ROUNDS = 2  # 辩论轮次（1-3）
ANALYSIS_HISTORY_DAYS = 60  # 分析历史数据天数
ENABLE_NEWS_ANALYSIS = True  # 是否启用新闻分析
```

## 🔧 高级用法

### 在代码中使用

```python
from main import StockAnalysisSystem

# 创建分析系统
system = StockAnalysisSystem(
    deepseek_key="你的密钥",
    tushare_token="你的令牌"
)

# 分析单只股票
result = system.analyze_stock("600519.SH")

# 批量分析
results = system.batch_analyze(["600519.SH", "000858.SZ"])

# 快速查看
data = system.quick_view("600519.SH")
```

### 自定义分析

```python
# 只进行技术分析
from agents.analysts import TechnicalAnalyst
from agents.llm_client import DeepSeekClient
from data.tushare_client import TushareClient

llm = DeepSeekClient(api_key="你的密钥")
analyst = TechnicalAnalyst(llm)
tushare = TushareClient(token="你的令牌")

data = tushare.get_comprehensive_data("600519.SH")
result = analyst.analyze(data)
print(result)
```

## 💡 使用建议

1. **首次使用**
   - 先用 `--quick` 快速查看，确认数据正常
   - 再用单只股票测试完整分析流程
   - 最后配置股票池和定时任务

2. **API成本控制**
   - DeepSeek性价比高，成本约 ¥0.01-0.02/只股票
   - 建议股票池不超过10只
   - 分析频率：每天1次即可

3. **分析结果使用**
   - AI分析仅供参考，不构成投资建议
   - 建议结合自己的判断
   - 关注风险评估部分

## ⚠️ 注意事项

1. **API密钥安全**
   - 不要将 `.env` 文件提交到Git
   - 定期更换API密钥
   - 注意API使用额度

2. **数据准确性**
   - Tushare免费版有数据延迟
   - 重要决策建议人工核对数据
   - 注意股票停牌等特殊情况

3. **系统限制**
   - 目前只支持A股（沪深两市）
   - 新闻分析需要Tushare高级权限
   - 单次分析约需2-3分钟

## 🐛 故障排除

### 问题1: 配置验证失败

```
❌ 配置错误: 请设置 DEEPSEEK_API_KEY 环境变量
```

**解决方案：** 检查 `.env` 文件是否正确创建并填写了API密钥

### 问题2: Tushare权限不足

```
⚠️ 获取新闻数据失败（可能需要更高级别的Tushare权限）
```

**解决方案：** 新闻功能需要Tushare高级权限，可以设置 `ENABLE_NEWS_ANALYSIS = False` 跳过

### 问题3: DeepSeek API调用失败

```
❌ DeepSeek API调用失败
```

**解决方案：** 
- 检查API密钥是否正确
- 检查网络连接
- 检查API额度是否充足

## 📞 技术支持

- 项目基于：TradingAgents-CN
- 问题反馈：提交Issue
- 使用建议：查看代码注释

## ⚖️ 免责声明

本系统仅用于技术研究和学习目的：

- ❌ 不构成任何投资建议
- ❌ 不对投资损失承担责任
- ✅ 投资有风险，决策需谨慎
- ✅ 建议咨询专业投资顾问

---

**祝投资顺利！📈**

