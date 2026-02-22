---
name: plane-so-cli
description: "使用一个无依赖关系的 Python CLI 来管理 Plane.so 项目和工作项。可以列出项目、创建/更新/分配问题、添加评论以及搜索工作区。plane-so-cli 可执行文件被打包在 scripts/ 目录中。"
license: MIT
compatibility: Requires Python 3.8+ and internet access to reach the Plane.so API.
homepage: https://github.com/luiseduardoaugusto/plane-so-cli
metadata: {"openclaw": {"requires": {"env": ["PLANE_API_KEY", "PLANE_WORKSPACE"], "bins": ["python3"]}, "primaryEnv": "PLANE_API_KEY", "emoji": "✈️", "homepage": "https://github.com/luiseduardoaugusto/plane-so-cli"}}
---
# Plane.so CLI 技能

通过一个简洁、易于审计的 Python CLI 来与 [Plane.so](https://plane.so) 项目管理工具进行交互。

**无依赖项** — 仅使用 Python 3.8 及更高版本的標準库。`plane-so-cli` 可执行文件包含在 `scripts/plane-so-cli` 目录中，安装完成后会添加到系统的 PATH 环境变量中。

## 设置

请设置以下环境变量：

```bash
export PLANE_API_KEY="your-api-key"
export PLANE_WORKSPACE="your-workspace-slug"
```

获取您的 API 密钥：**进入 Plane > 个人设置 > 个人访问令牌**

## 命令

### 用户与工作区

```bash
plane-so-cli me                        # Show current user
plane-so-cli projects list             # List all active projects
plane-so-cli members                   # List workspace members
```

### 问题（工作项）

```bash
plane-so-cli issues list -p PROJECT_ID
plane-so-cli issues list -p PROJECT_ID --state STATE_ID
plane-so-cli issues list -p PROJECT_ID --priority high
plane-so-cli issues list -p PROJECT_ID --assignee USER_ID
plane-so-cli issues get -p PROJECT_ID ISSUE_ID
plane-so-cli issues create -p PROJECT_ID --name "Fix bug" --priority high
plane-so-cli issues create -p PROJECT_ID --name "Task" --assignee USER_ID
plane-so-cli issues update -p PROJECT_ID ISSUE_ID --state STATE_ID
plane-so-cli issues update -p PROJECT_ID ISSUE_ID --priority medium
plane-so-cli issues assign -p PROJECT_ID ISSUE_ID USER_ID_1 USER_ID_2
plane-so-cli issues delete -p PROJECT_ID ISSUE_ID
plane-so-cli issues search "login bug"
plane-so-cli issues my
```

### 评论、状态与标签

```bash
plane-so-cli comments list -p PROJECT_ID -i ISSUE_ID
plane-so-cli comments add -p PROJECT_ID -i ISSUE_ID "Comment text"
plane-so-cli states -p PROJECT_ID
plane-so-cli labels -p PROJECT_ID
```

### 循环与模块

```bash
plane-so-cli cycles list -p PROJECT_ID
plane-so-cli cycles get -p PROJECT_ID CYCLE_ID
plane-so-cli modules list -p PROJECT_ID
plane-so-cli modules get -p PROJECT_ID MODULE_ID
```

## 输出格式

默认输出为人类可读的表格格式。若需要原始 JSON 格式，可以使用 `-f json` 命令：

```bash
plane-so-cli projects list -f json
```

## 典型工作流程

1. `plane-so-cli projects list` — 查找项目 ID
2. `plane-so-cli members` — 查找成员 ID 以分配任务
3. `plane-so-cli states -p PROJECT_ID` — 查看可用的项目状态
4. `plane-so-cli issues create -p PROJECT_ID --name "任务" --assignee USER_ID` — 创建新问题并指定负责人
5. `plane-so-cli comments add -p PROJECT_ID -i ISSUE_ID "开始处理..."` — 为问题添加评论

## 安全性与隐私

该工具仅通过 Plane.so API 进行通信。API 主机被硬编码为 `api.plane.so`，无法更改。

| 端点 | 发送的数据 | 目的 |
|----------|-----------|---------|
| `https://api.plane.so/api/v1/*` | API 密钥（请求头），项目/问题数据（请求体） | 所有 Plane.so 操作 |

- 您的 `PLANE_API_KEY` 会作为 `X-API-Key` 头部字段仅发送到 `https://api.plane.so`
- API 主机被硬编码，无法通过环境变量重定向请求到其他域名
- 无数据被缓存、记录或存储在本地
- 不会收集任何遥测数据或分析信息
- 完整的源代码可在 [github.com/luiseduardoaugusto/plane-so-cli](https://github.com/luiseduardoaugusto/plane-so-cli) 查看，并包含在 `scripts/plane-so-cli` 文件包中