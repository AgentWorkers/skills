---
name: rlm
description: 使用 RLM（递归语言模型）来进行代码执行、计算、数据分析以及任务分解。该模型会迭代地执行 Python 代码，直到产生经过验证的结果——完全不需要依赖大型语言模型（LLM）的猜测或推断。
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":["mcporter"]},"install":[{"id":"node","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter (npm)"}]}}
---

# RLM – 递归语言模型（Recursive Language Models）

通过 `mcporter MCP` 桥接器，使用**经过验证的代码执行**来执行任务。

RLM 会迭代地编写和执行 Python 代码，直到生成一个经过验证的答案。与直接的 LLM 响应不同，RLM 的计算结果具有**100% 的准确性**。

## 先决条件

### 1. 安装 `mcporter`（MCP 桥接器）
```bash
npm install -g mcporter
```

### 2. 安装 RLM MCP 服务器

**选项 A：克隆并设置（推荐）**
```bash
# Clone RLM project
git clone https://github.com/alexzhang13/rlm.git $HOME/rlm
cd $HOME/rlm
pip install -e .

# Create MCP server directory
mkdir -p $HOME/.claude/mcp-servers/rlm/src

# Download MCP server files
curl -o $HOME/.claude/mcp-servers/rlm/src/server.py \
  https://raw.githubusercontent.com/eesb99/rlm-mcp/main/src/server.py
curl -o $HOME/.claude/mcp-servers/rlm/run_server.sh \
  https://raw.githubusercontent.com/eesb99/rlm-mcp/main/run_server.sh
curl -o $HOME/.claude/mcp-servers/rlm/setup.sh \
  https://raw.githubusercontent.com/eesb99/rlm-mcp/main/setup.sh
curl -o $HOME/.claude/mcp-servers/rlm/requirements.txt \
  https://raw.githubusercontent.com/eesb99/rlm-mcp/main/requirements.txt

# Setup venv and install dependencies
chmod +x $HOME/.claude/mcp-servers/rlm/*.sh
cd $HOME/.claude/mcp-servers/rlm
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

**选项 B：手动设置**
```bash
# Create server directory
mkdir -p $HOME/.claude/mcp-servers/rlm/src

# Create venv and install dependencies
cd $HOME/.claude/mcp-servers/rlm
python3 -m venv venv
venv/bin/pip install mcp litellm

# Create run_server.sh
cat > $HOME/.claude/mcp-servers/rlm/run_server.sh << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
export PYTHONPATH="$HOME/rlm:$PYTHONPATH"
export RLM_MODEL="${RLM_MODEL:-openrouter/x-ai/grok-code-fast-1}"
export RLM_SUBTASK_MODEL="${RLM_SUBTASK_MODEL:-openrouter/openai/gpt-4o-mini}"
export RLM_MAX_DEPTH="${RLM_MAX_DEPTH:-2}"
export RLM_MAX_ITERATIONS="${RLM_MAX_ITERATIONS:-20}"
exec "$SCRIPT_DIR/venv/bin/python" -m src.server
EOF
chmod +x $HOME/.claude/mcp-servers/rlm/run_server.sh
```

### 3. 配置 MCP（用于 Claude 代码）

将以下配置添加到 `~/.mcp.json` 文件中（将 `YOUR_HOME` 替换为你的实际 home 路径，例如 `/Users/john` 或 `/home/john`）：
```json
{
  "mcpServers": {
    "rlm": {
      "command": "bash",
      "args": ["YOUR_HOME/.claude/mcp-servers/rlm/run_server.sh"]
    }
  }
}
```

**获取你的 home 路径：** `echo $HOME`

### 4. 设置 API 密钥

RLM 需要一个 OpenRouter API 密钥：
```bash
export OPENROUTER_API_KEY="your-key-here"
```

### 5. 验证安装

```bash
# Check mcporter sees RLM
mcporter list | grep rlm

# Test RLM
mcporter call 'rlm.rlm_status()'
```

## 可用工具

| 工具 | 用途 | 参数 |
|------|---------|------------|
| `rlm_execute` | 执行通用任务、进行计算 | `task`（必需），`context`（可选） |
| `rlm_analyze` | 数据分析 | `data`，`question`（两者均必需） |
| `rlm_code` | 生成经过测试的代码 | `description`（必需），`language`（可选，默认：python） |
| `rlm_decompose` | 复杂的多步骤任务 | `complex_task`，`num_subtasks`（默认：5） |
| `rlm_status` | 检查系统状态 | （无参数） |

## 快速命令

**简单计算：**
```bash
mcporter call 'rlm.rlm_execute(task: "calculate 127 * 389")'
```

**前 N 个质数：**
```bash
mcporter call 'rlm.rlm_execute(task: "calculate the first 100 prime numbers")'
```

**数据分析：**
```bash
mcporter call 'rlm.rlm_analyze(data: "[23, 45, 67, 89, 12, 34]", question: "what is the mean, median, and standard deviation?")'
```

**生成代码：**
```bash
mcporter call 'rlm.rlm_code(description: "function to check if a number is prime")'
```

**分解复杂任务：**
```bash
mcporter call 'rlm.rlm_decompose(complex_task: "analyze a $500K portfolio with 60/30/10 allocation, calculate risk metrics and 10-year projection", num_subtasks: 5)'
```

**检查状态：**
```bash
mcporter call 'rlm.rlm_status()'
```

## 何时使用 RLM

**适用于以下场景：**
- 需要精确度的数学计算 |
- 统计分析（平均值、标准差、相关性） |
- 金融计算（复利、净现值、内部收益率） |
- 算法执行（质数判断、排序、搜索） |
- 数据转换和聚合 |
- 生成并验证代码 |

**不适用以下场景：**
- 简单的事实性问题（使用直接响应） |
- 创意写作或头脑风暴 |
- 需要网络搜索或实时数据的任务 |
- 非常简单的计算（如 2+2）

## 工作原理

```
1. You give RLM a task
2. RLM writes Python code to solve it
3. Code executes in sandbox
4. If not complete, RLM iterates
5. Returns verified final answer
```

**使用的模型：**
- 主模型：`grok-code-fast-1`（快速代码执行） |
- 子任务模型：`gpt-4o-mini`（高效的子查询模型） |

## 配置

**环境变量：**
| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `RLM_MODEL` | `openrouter/x-ai/grok-code-fast-1` | 主执行模型 |
| `RLM_SUBTASK_MODEL` | `openrouter/openai/gpt-4o-mini` | 子任务模型 |
| `RLM_MAX_DEPTH` | `2` | 最大递归深度 |
| `RLM_MAX_ITERATIONS` | `20` | 每个任务的最大迭代次数 |
| `OPENROUTER_API_KEY` | （必需） | OpenRouter API 密钥 |

**服务器位置：`$HOME/.claude/mcp-servers/rlm/` |

## 故障排除**

**“服务器离线”或“找不到名为‘mcp’的模块”：**
```bash
# Reinstall dependencies
cd $HOME/.claude/mcp-servers/rlm
python3 -m venv venv
venv/bin/pip install mcp litellm
```

**“mcporter: 命令未找到”：**
```bash
npm install -g mcporter
```

**“rlm 不在 mcporter 列表中”：**
- 确保 `$HOME/.mcp.json` 文件存在，并且其中包含 RLM 的配置信息 |
- 确保 `run_server.sh` 可执行：`chmod +x $HOME/.claude/mcp-servers/rlm/run_server.sh`

**响应缓慢：**
- RLM 需要执行实际代码，通常需要 10-30 秒 |
- 复杂任务（尤其是经过分解的任务）执行时间会更长 |

## 参考资料**

- **论文：** [递归语言模型](https://arxiv.org/abs/2512.24601)（作者：Zhang, Kraska, Khattab，2025 年） |
- **RLM 库：** [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm) |
- **MCP 服务器：** [github.com/eesb99/rlm-mcp](https://github.com/eesb99/rlm-mcp) |
- **MCP SDK：** [modelcontextprotocol.io](https://modelcontextprotocol.io) |
- **mcporter：** [mcporter.dev](http://mcporter.dev)