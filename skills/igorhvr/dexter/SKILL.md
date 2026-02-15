---
name: dexter
description: 自主财务研究代理，用于股票分析、财务报表、财务指标、价格数据、美国证券交易委员会（SEC）的文件以及加密货币相关数据的研究。
metadata: {"clawdbot":{"emoji":"📊","os":["darwin","linux"],"requires":{"bins":["bun","git"]}}}
---

# Dexter技能（Clawdbot）

Dexter是一个自主的金融研究助手，能够规划、执行并整合金融数据分析任务。您可以利用它来解答任何与股票、加密货币、公司基本面或市场数据相关的金融研究问题。

## 何时使用Dexter

Dexter适用于以下场景：
- 股票价格（实时及历史价格）
- 财务报表（收入、资产负债表、现金流量）
- 财务指标（市盈率、市净率、利润率、市值等）
- 美国证券交易委员会（SEC）文件（10-K、10-Q、8-K报告）
- 分析师预测
- 内幕交易信息
- 公司新闻
- 加密货币价格
- 对比财务分析
- 收入趋势和增长率

**注意**：Dexter的金融数据集API主要覆盖美国股票。对于国际股票（如欧洲交易所的股票），它会通过Tavily进行网络搜索来获取数据。

## 安装

如果尚未安装Dexter，请按照以下步骤操作：

### 1. 克隆并安装

```bash
DEXTER_DIR="/root/clawd-workspace/dexter"

# Clone if not exists
if [ ! -d "$DEXTER_DIR" ]; then
  git clone https://github.com/virattt/dexter.git "$DEXTER_DIR"
fi

cd "$DEXTER_DIR"

# Install dependencies
bun install
```

### 2. 配置API密钥

创建一个`.env`文件，用于存储所需的API密钥：

```bash
cat > "$DEXTER_DIR/.env" << 'EOF'
# LLM API Keys (at least one required)
ANTHROPIC_API_KEY=your-anthropic-key

# Stock Market API Key - Get from https://financialdatasets.ai
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-key

# Web Search API Key - Get from https://tavily.com (optional but recommended)
TAVILY_API_KEY=your-tavily-key
EOF
```

**API密钥来源**：
- Anthropic：https://console.anthropic.com/
- Financial Datasets：https://financialdatasets.ai（提供免费试用）
- Tavily：https://tavily.com（可选，用于网络搜索）

### 3. 仅使用Anthropic时的配置调整

Dexter的工具执行器默认使用OpenAI的`gpt-5-mini`模型。如果仅使用Anthropic，请进行如下配置调整：

```bash
# Fix hardcoded OpenAI model in tool-executor.ts
sed -i "s/const SMALL_MODEL = 'gpt-5-mini';/const SMALL_MODEL = 'claude-3-5-haiku-latest';/" \
  "$DEXTER_DIR/src/agent/tool-executor.ts"
```

### 4. 设置默认模型

将Claude设置为默认模型：

```bash
mkdir -p "$DEXTER_DIR/.dexter"
cat > "$DEXTER_DIR/.dexter/settings.json" << 'EOF'
{
  "provider": "anthropic",
  "modelId": "claude-sonnet-4-5"
}
EOF
```

### 5. 创建非交互式查询脚本

```bash
cat > "$DEXTER_DIR/query.ts" << 'SCRIPT'
#!/usr/bin/env bun
/**
 * Non-interactive Dexter query runner
 * Usage: bun query.ts "What is Apple's revenue growth?"
 */
import { config } from 'dotenv';
import { Agent } from './src/agent/orchestrator.js';
import { getSetting } from './src/utils/config.js';

config({ quiet: true });

const query = process.argv[2];
if (!query) {
  console.error('Usage: bun query.ts "Your financial question here"');
  process.exit(1);
}

const model = getSetting('modelId', 'claude-sonnet-4-5') as string;

async function runQuery() {
  let answer = '';
  
  const agent = new Agent({
    model,
    callbacks: {
      onPhaseStart: (phase) => {
        if (process.env.DEXTER_VERBOSE) {
          console.error(`[Phase: ${phase}]`);
        }
      },
      onPlanCreated: (plan) => {
        if (process.env.DEXTER_VERBOSE) {
          console.error(`[Tasks: ${plan.tasks.map(t => t.description).join(', ')}]`);
        }
      },
      onAnswerStream: async (stream) => {
        for await (const chunk of stream) {
          answer += chunk;
          process.stdout.write(chunk);
        }
      },
    },
  });

  try {
    await agent.run(query);
    if (!answer.endsWith('\n')) {
      console.log();
    }
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

runQuery();
SCRIPT
```

### 完整的一次性安装流程

完整的安装脚本（需要将API密钥设置为环境变量）：

```bash
#!/bin/bash
set -e

DEXTER_DIR="/root/clawd-workspace/dexter"

# Clone
[ ! -d "$DEXTER_DIR" ] && git clone https://github.com/virattt/dexter.git "$DEXTER_DIR"
cd "$DEXTER_DIR"

# Install deps
bun install

# Create .env (set these variables before running)
cat > .env << EOF
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-your-key-here}
FINANCIAL_DATASETS_API_KEY=${FINANCIAL_DATASETS_API_KEY:-your-key-here}
TAVILY_API_KEY=${TAVILY_API_KEY:-your-key-here}
EOF

# Patch for Anthropic
sed -i "s/const SMALL_MODEL = 'gpt-5-mini';/const SMALL_MODEL = 'claude-3-5-haiku-latest';/" \
  src/agent/tool-executor.ts

# Set model config
mkdir -p .dexter
echo '{"provider":"anthropic","modelId":"claude-sonnet-4-5"}' > .dexter/settings.json

echo "Dexter installed successfully!"
```

## 使用位置

```
/root/clawd-workspace/dexter
```

## 快速查询（非交互式）

对于简单的金融查询，可以使用以下查询脚本：

```bash
cd /root/clawd-workspace/dexter && bun query.ts "Your financial question here"
```

**示例查询**：
```bash
bun query.ts "What is Apple's current P/E ratio?"
bun query.ts "Compare Microsoft and Google revenue growth over the last 4 quarters"
bun query.ts "What was Tesla's free cash flow in 2025?"
bun query.ts "Show me insider trades for NVDA in the last 30 days"
bun query.ts "What is Bitcoin's price trend over the last week?"
```

**详细输出（显示查询步骤）**：
```bash
DEXTER_VERBOSE=1 bun query.ts "Your question"
```

## 交互式模式（复杂研究）

对于需要多轮讨论或后续查询的场景，可以通过tmux使用交互式命令行界面：

```bash
SOCKET_DIR="${CLAWDBOT_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/clawdbot-tmux-sockets}"
SOCKET="$SOCKET_DIR/clawdbot.sock"
SESSION=dexter

# Start Dexter (if not running)
tmux -S "$SOCKET" kill-session -t "$SESSION" 2>/dev/null || true
tmux -S "$SOCKET" new -d -s "$SESSION" -n shell -c /root/clawd-workspace/dexter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- 'bun start' Enter
sleep 3

# Send a query
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -l -- 'Your question here'
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 Enter

# Check output
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
```

## 可用的工具（内部功能）

Dexter会根据您的查询自动选择并使用以下工具：

### 财务报表
- `get_income_statements` - 收入、支出、净利润
- `get_balance_sheets` - 资产、负债、所有者权益
- `get_cash_flow_statements` - 经营活动现金流、投资活动现金流、融资活动现金流
- `get_all_financial_statements` - 一次性获取所有财务报表

### 价格信息
- `get_price_snapshot` - 当前股票价格
- `get_prices` - 历史价格数据

### 加密货币
- `get_crypto_price_snapshot` - 当前加密货币价格（例如BTC-USD）
- `get_crypto_prices` - 历史价格数据
- `get_available_crypto_tickers` - 可用的加密货币代码列表

### 财务指标
- `get_financial_metrics_snapshot` - 当前财务指标（市盈率、市值等）
- `get_financial_metrics` - 历史财务指标

### SEC文件
- `get_10k_filing_items` - 年度报告内容
- `get_10q_filing_items` - 季度报告内容
- `get_8k_filing_items` - 最新季度报告内容
- `get_filings` - 所有报告的列表

### 其他数据
- `get_analyst_estimates` - 分析师预测
- `get_segmented_revenues` - 按业务部门划分的收入
- `get_insider_trades` - 内幕交易信息
- `get_news` - 公司新闻
- `search_web` - 通过Tavily进行网络搜索以获取通用信息

## 代理架构

Dexter采用多阶段工作流程：
1. **理解**：从查询中提取意图、股票代码和时间范围
2. **规划**：生成包含依赖关系的任务列表
3. **执行**：尽可能并行执行任务
4. **评估**：判断是否需要更多数据（最多可迭代5次）
5. **回答**：综合相关信息给出答案

## 示例查询

**股票分析**：
- “过去四个季度中AAPL的收入增长了多少？”
- “比较2025年MSFT和GOOG的营业利润率”
- “上个季度AMZN的资产负债率是多少？”

**财务健康状况**：
- “NVDA的现金流是否为正？请显示其趋势”
- “特斯拉的利润率与福特相比如何？”

**SEC文件**：
- “总结苹果公司最新的10-K报告中的风险因素”
- “Meta在最新的8-K报告中披露了哪些内容？”

**加密货币**：
- “今天的以太坊价格是多少？”
- “显示比特币过去一个月的价格走势”

**市场研究**：
- “分析师对亚马逊下个季度的收益有何预测？”
- “显示微软最近的内幕交易记录”

## 故障排除

### “缺少凭证... OPENAI_API_KEY”
请运行安装过程中的第3步（配置Anthropic密钥），因为Dexter的工具执行器默认使用OpenAI。

### 非美国股票的API错误
Financial Datasets API主要针对美国股票。如果配置了`TAVILY_API_KEY`，Dexter会使用Tavily进行国际股票的网络搜索。

### 响应缓慢
复杂查询可能需要30-60秒。Dexter会规划并执行多个API请求，然后综合结果给出答案。

## 使用提示：
1. **提供具体信息**：请提供股票代码和时间范围（如果已知）。
2. **美国股票效果最佳**：Financial Datasets API对美国股票的覆盖范围最全面。
3. **国际股票**：对于非美国股票，Dexter会使用网络搜索。
4. **加密货币格式**：使用`BTC-USD`、`ETH-USD`等格式表示加密货币代码。
5. **注意延迟**：复杂查询可能需要30-60秒，因为Dexter需要执行多个任务。