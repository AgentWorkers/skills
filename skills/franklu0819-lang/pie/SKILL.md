---
name: pie
description: >
  **Personal Insight Engine (PIE)**  
  ——一种战略分析工具，它能够扫描本地的会话日志（文件扩展名为 `.md`），并通过大型语言模型（LLMs）提取出三项关键的策略性洞察。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"], "env": ["ZHIPU_API_KEY", "GEMINI_API_KEY"] },
      },
  }
---
# PIE（个人洞察引擎）

通过从您的记忆日志中提取战略模式，来分析您的创业历程。

## 设置

**1. 配置 API 密钥：**
确保您的 `.env` 文件或系统环境中至少包含以下一个密钥：
- `ZHIPU_API_KEY`（GLM 的默认密钥）
- `GEMINI_API_KEY`（备用密钥）

**2. 依赖项：**
需要 `openai` 和 `python-dotenv` 这两个 Python 包。

## 使用方法

### 运行每周回顾
默认情况下，会扫描过去 7 天的记忆文件：

```bash
python3 scripts/pie.py
```

### 自定义回顾
可以扫描特定数量的天数（例如，过去 30 天）：

```bash
python3 scripts/pie.py --days 30
```

## 工作原理

1. **发现**：扫描 `memory/` 目录下的最新 Markdown 文件。
2. **清理**：去除 JSON 元数据和系统头部信息。
3. **综合分析**：使用大型语言模型（LLM）提取 3 个核心洞察（决策模式、痛点、关键转折点）。
4. **输出**：生成格式化的 Markdown 报告。

---
*由 Cipher 使用 OpenSpec 开发。*