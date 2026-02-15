---
name: swarm
version: 1.0.4
description: 使用 Gemini Flash 工作者执行并行任务：成本仅为 Opus 的 1/200。适用于所有可并行化的任务，有助于节省系统资源（如带宽、计算能力等）。
homepage: https://github.com/Chair4ce/node-scaling
license: MIT
author: Chair4ce
metadata:
  {
    "openclaw": {
      "emoji": "🐝",
      "requires": {
        "bins": ["node"],
        "env": ["GEMINI_API_KEY"]
      },
      "primaryEnv": "GEMINI_API_KEY",
      "install": [
        {
          "id": "release-download",
          "kind": "download",
          "url": "https://github.com/Chair4ce/node-scaling/archive/refs/tags/v1.0.4.zip",
          "archive": "zip",
          "extract": true,
          "stripComponents": 1,
          "targetDir": "~/.openclaw/skills/node-scaling",
          "label": "Download v1.0.4 from GitHub",
          "postInstall": "cd ~/.openclaw/skills/node-scaling && npm install --production"
        }
      ]
    }
  }
---

# Swarm

Swarm 是一个用于并行执行 AI 任务的工具，它将任务分配到廉价的 LLM（Large Language Model）计算资源（如 Gemini Flash）上，从而避免浪费昂贵的计算资源。

**核心优势：** 成本降低 200 倍，执行速度提升 157 倍。

---

## 安装

```bash
git clone https://github.com/Chair4ce/node-scaling.git ~/.openclaw/skills/node-scaling
cd ~/.openclaw/skills/node-scaling
npm install
npm run setup
```

系统会提示您输入 API 密钥。建议使用 Gemini 的 API 密钥进行配置。

---

## 快速入门

```bash
swarm start                    # Start the daemon
swarm status                   # Check if running
swarm parallel "Q1" "Q2" "Q3"  # Run prompts in parallel
swarm bench --tasks 30         # Benchmark throughput
```

---

## 性能测试

### 单节点环境

| 任务数量 | 执行时间 | 吞吐量 |
|--------|---------|---------|
| 10     | 700 毫秒   | 14 个/秒   |
| 30     | 1,000 毫秒   | 30 个/秒   |
| 50     | 1,450 毫秒   | 35 个/秒   |

### 分布式环境（6 个节点）

在 Mac mini 和 5 台 Linux 服务器上进行的实际性能测试结果：

| 节点    | 任务数量 | 执行时间 | 吞吐量 |
|--------|---------|---------|---------|
| Mac mini | 100     | 3.76 秒   | 26.6 个/秒   |
| Worker 2 | 100     | 3.20 秒   | 31.3 个/秒   |
| Worker 3 | 100     | 3.23 秒   | 31.0 个/秒   |
| Worker 5 | 100     | 3.27 秒   | 30.6 个/秒   |
| Worker 6 | 100     | 3.21 秒   | 31.2 个/秒   |
| Worker 7 | 100     | 3.32 秒   | 30.2 个/秒   |
| **总计：** 600 个任务，耗时 3.8 秒 |

**总吞吐量：** 181 个任务/秒

---

## 成本对比

| 方法        | 600 个任务 | 执行时间 | 成本     |
|------------|---------|---------|
| Opus（顺序执行） | 约 10 分钟 | 约 $9.00   |
| Swarm（分布式执行） | 3.8 秒   | 约 $0.045   |

**执行速度提升 157 倍，成本降低 200 倍。**

---

## 使用场景

- 需要同时处理 3 个或更多独立的研究查询时  
- 需要比较多个主题或数据时  
- 需要批量分析文档时  
- 需要从多个 URL 获取数据并对其进行总结时  
- 任何可以并行处理的 LLM 相关任务  

如果仍然选择顺序执行任务，那可能意味着你的使用方式并不高效。

---

## 配置文件

配置文件路径：`~/.config/clawdbot/node-scaling.yaml`

```yaml
node_scaling:
  enabled: true
  limits:
    max_nodes: 20
    max_concurrent_api: 20
  provider:
    name: gemini
    model: gemini-2.0-flash
  cost:
    max_daily_spend: 10.00
```

---

## 多节点部署

通过在更多机器上部署 Swarm，可以实现线性扩展：

```bash
git clone https://github.com/Chair4ce/node-scaling.git ~/.openclaw/skills/node-scaling
cd ~/.openclaw/skills/node-scaling && npm install && npm run setup
swarm start
```

每增加一个节点，系统的总吞吐量大约会增加 30 个任务/秒。

---

## 安全性

- 需要使用自己的 API 密钥（系统不会硬编码任何认证信息）  
- 可以选择集成 Supabase，但默认情况下该功能是关闭的  
- 系统默认使用本地文件进行任务协调  
- 所有的 LLM 请求都会发送到您配置的提供商那里  

---

## 相关资源

- [GitHub 仓库](https://github.com/Chair4ce/node-scaling)  
- [更新日志](https://github.com/Chair4ce/node-scaling/blob/main/CHANGELOG.md)  
- [安装指南](https://github.com/Chair4ce/node-scaling/blob/main/INSTALL.md)