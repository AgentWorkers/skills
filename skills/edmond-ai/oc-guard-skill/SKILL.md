---
name: oc_guard
description: 安全的 OpenClaw 配置规划/应用工作流程，支持双语执行记录。
metadata: {"openclaw":{"requires":{"bins":["python3","openclaw","opencode"]}}}
---
# oc-guard 技能

## 目的
所有修改配置的请求都必须通过 `oc-guard` 进行处理。  
请勿直接编辑 `~/.openclaw/openclaw.json` 文件。  
在可能的情况下，应使用位于 `{baseDir}/scripts/oc-guard.py` 的命令行工具来执行相关操作。

## 严格规定
1. 在执行任何配置更改之前，必须先使用 `oc-guard plan` 命令进行规划。
2. 高风险的配置更改需要使用 `oc-guard apply --confirm` 命令来确认。
3. 操作完成后，必须首先返回执行结果。
4. 如果命令未能成功执行，应返回提示信息「【模型说明-未执行】」。
5. 未经 `oc-guard` 的正式确认，切勿声称操作成功。

## 常用命令
- `{baseDir}/scripts/oc-guard.py --help`：显示帮助信息。
- `{baseDir}/scripts/oc-guard.py plan "<要求>"`：制定配置更改计划。
- `{baseDir}/scripts/oc-guard.py apply --confirm "<要求>"`：应用配置更改并确认。
- `{baseDir}/scripts/oc-guard.py plan --proposal <文件>"`：生成配置更改提案。
- `{baseDir}/scripts/oc-guard.py apply --confirm --proposal <文件>"`：应用配置更改提案并确认。