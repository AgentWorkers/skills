---
name: plane-cli
description: `plane`（`developers.plane.so`）是一个基于 `Api2Cli`（`a2c`）开发的命令行工具（CLI）。它包含一个 `a2c` 工作区（`plane`），以及一个封装脚本，用于列出工作区/项目、获取问题（工作项）、设置问题状态以及添加 HTML 评论。
metadata: {"openclaw":{"emoji":"🗂️","requires":{"bins":["a2c"]}}}
---
# plane-cli

这是一个轻量级的 OpenClaw 技能封装工具，用于通过 **Api2Cli (a2c)** 来调用 **Plane API**。

该工具包含以下内容：
- 一个名为 `plane` 的 `a2c/` 工作区
- 一个封装脚本：`scripts/plane`

## 使用要求

- 确保 `a2c` 已安装，并且可以在 `PATH` 环境变量中找到
- 确保 Plane 的认证信息已配置在环境变量中：
  - `PLANE_API_KEY`（必需）
  - `PLANE_BASE_URL`（可选；默认值为 `https://api.plane.so`）

## 使用方法

建议通过封装脚本来使用该工具：

```bash
./scripts/plane --help
./scripts/plane whoami
./scripts/plane get_workspaces
./scripts/plane projects <workspace_slug>
./scripts/plane states <workspace_slug> <project_uuid>
./scripts/plane workitems <workspace_slug> <project_uuid>
./scripts/plane workitem <workspace_slug> <project_uuid> <issue_uuid>
./scripts/plane set-state <workspace_slug> <project_uuid> <issue_uuid> <state_uuid>
./scripts/plane comment <workspace_slug> <project_uuid> <issue_uuid> '<p>Hello</p>'
```

**注意事项：**
- 在 Plane API 中，工作项被称为 **issues**。
- `set-state` 命令用于发送数据 `{“state_id”: “...”}`。
- `comment` 命令用于发送数据 `{“comment_html”: “<p>...</p>”}`。

## 简单测试示例

```bash
# 1) Help works
./scripts/plane --help

# 2) Auth sanity check (requires valid env)
export PLANE_API_KEY="plane_api_..."
export PLANE_BASE_URL="https://api.plane.so"  # optional
./scripts/plane whoami
```