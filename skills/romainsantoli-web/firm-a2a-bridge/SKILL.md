---
name: firm-a2a-bridge
version: 1.0.0
description: OpenClaw代理之间的代理对代理（A2A）协议v1.0 RC版本。该协议支持代理发现、身份验证、任务生命周期管理以及推送通知配置等功能，完全符合A2A规范的要求。它填补了第7阶段开发路线图中从G1到G6的各个技术空白。
author: romainsantoli-web
license: MIT
metadata:
  openclaw:
    registry: ClawHub
    requires:
      - mcp-openclaw-extensions >= 2.0.0
tags:
  - a2a
  - agent-card
  - discovery
  - interoperability
  - multi-agent
  - protocol
---
# firm-a2a-bridge

> ⚠️ 本内容由人工智能生成，需人工审核后方可在生产环境中部署。

## 目的

该技能实现了 OpenClaw 的 **A2A 协议 v1.0 RC**（Agent-to-Agent），允许代理节点之间相互发现、交换任务，并接收推送通知——所有这些操作均通过标准化的 MCP 接口完成。

**已解决的缺陷：**
| 缺陷 | 严重程度 | 工具 |
|-----|----------|-------|
| G1 — 无法生成代理卡片 | 严重 | `openclaw_a2a_card_generate` |
| G2 — 无法验证代理卡片 | 严重 | `openclaw_a2a_card_validate` |
| G3 — 无法发送 A2A 任务 | 高度 | `openclaw_a2a_task_send` |
| G4 — 无法跟踪 A2A 任务的状态 | 高度 | `openclaw_a2a_task_status` |
| G5 — 无法发送 A2A 推送通知 | 中等 | `openclaw_a2a_push_config` |
| G6 — 无法发现代理节点 | 高度 | `openclaw_a2a_discovery` |

## 工具

### `openclaw_a2a_card_generate`
根据 SOUL.md 文件生成 `.well-known/agent-card.json` 文件。
自动从 SOUL.md 的 frontmatter 和正文部分提取代理节点的标识、能力、功能及安全配置。

**参数：**
- `soul_path` (str, 必需) — SOUL.md 文件的路径
- `base_url` (str, 必需) — 代理节点可访问的基 URL
- `output_path` (str, 可选) — JSON 文件的输出路径
- `capabilities` (dict, 可选) — A2A 功能（如流式传输、推送通知）
- `security_schemes` (dict, 可选) — OAuth2、apiKey 或 http 安全方案
- `extensions` (list, 可选) — A2A 扩展信息

**示例：**
```json
{
  "name": "openclaw_a2a_card_generate",
  "arguments": {
    "soul_path": "./souls/ceo/SOUL.md",
    "base_url": "https://agents.example.com/ceo"
  }
}
```

### `openclaw_a2a_card_validate`
根据 A2A v1.0 RC 规范验证代理卡片的有效性。
检查必填字段、URL 格式、技能结构以及安全配置。

**参数：**
- `card_path` (str, 可选) — 代理卡片 JSON 文件的路径
- `card_json` (dict, 可选) — 代理卡片的 JSON 内容（可选）

### `openclaw_a2a_task_send`
向远程代理节点发送消息或任务。
在 A2A 生命周期中创建任务（状态：submitted → working → completed/failed）。
包含针对 localhost URL 的 SSRF（Same-Origin Security Framework）防护机制。

**参数：**
- `agent_url` (str, 必需) — 目标代理节点的 URL
- `message` (str, 必需) — 要发送的文本消息
- `context_id` (str, 可选) — 用于分组任务的上下文 ID
- `blocking` (bool, 可选) — 是否等待任务完成
- `metadata` (dict, 可选) — 额外元数据

### `openclaw_a2a_task_status`
获取任务的状态或列出所有任务。
实现 A2A 协议中的 GetTask 和 ListTasks 操作。

**参数：**
- `task_id` (str, 可选) — 特定任务的 ID（用于 GetTask）
- `context_id` (str, 可选) — 用于 ListTasks 的过滤条件
- `include_history` (bool, 可选) — 是否包含消息历史记录

### `openclaw_a2a_push_config`
用于管理 A2A 推送通知的配置。
支持创建（create）、获取（get）、列出（list）和删除（delete）操作，并提供 SSRF 防护。

**参数：**
- `task_id` (str, 必需) — 相关任务的 ID
- `action` (str) — 操作类型（create、get、list、delete）
- `webhook_url` (str, 可选) — Webhook 的 URL（创建操作时必需）
- `auth_token` (str, 可选) — 用于发送通知的认证令牌
- `config_id` (str, 可选) | 配置 ID（获取/删除操作时必需）

### `openclaw_a2a_discovery`
通过代理节点的 Agent Card 端点或本地扫描 SOUL.md 文件来发现代理节点。

**参数：**
- `urls` (list[str], 可选) — 需要扫描的代理节点 URL 列表
- `souls_dir` (str, 可选) — 包含 SOUL.md 文件的本地目录
- `check_reachability` (bool, 可选) — 检查 URL 的可访问性

## 架构

```
SOUL.md files                    A2A Protocol v1.0 RC
     │                                  │
     ├── card_generate ──► .well-known/agent-card.json
     │                                  │
     ├── card_validate ◄── Spec validation (8 checks)
     │                                  │
     ├── task_send ────────► SendMessage (submitted → working → completed)
     │                                  │
     ├── task_status ──────► GetTask / ListTasks
     │                                  │
     ├── push_config ──────► CRUD webhook configs (SSRF-safe)
     │                                  │
     └── discovery ────────► Agent Card endpoint probe + local SOUL.md scan
```

## 安全性

- **文件路径防护**：所有文件路径均通过 Pydantic 进行验证
- **SSRF 防护**：`task_send` 和 `push_config` 操作禁止访问 localhost/127.0.0.1/0.0.0.0/::1
- **URL 格式验证**：仅接受 http/https 协议
- **令牌隐藏**：认证令牌会隐藏最后 4 个字符
- **输入验证**：所有参数均通过 Pydantic v2 进行严格验证

## 测试

```bash
python -m pytest tests/test_smoke.py -k "TestA2aBridge" -v
```

共有 15 项测试用例，涵盖以下内容：
- 从有效的 SOUL.md 文件生成代理卡片
- 处理缺失文件的情况
- 防止路径遍历攻击
- 验证代理卡片的合法性
- 在 SSRF 保护机制下发送任务
- 获取任务状态（GetTask/ListTasks）
- 管理推送通知配置（CRUD 操作）
- 本地发现代理节点