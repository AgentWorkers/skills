---
name: rlm-controller
description: RLM风格的长时间上下文控制器：将输入视为外部上下文，支持切片、预览、搜索操作，并在严格的安全限制下生成递归子调用。适用于处理大型文档、密集型日志数据或进行仓库级别的分析。
metadata: {"clawdbot": {"emoji": "🧠"}}
---

# RLM控制器技能（RLM Controller Skill）

## 功能概述  
该技能提供了一个基于策略的安全框架，用于处理非常长的输入数据：  
- 将输入数据存储为外部上下文文件；  
- 对输入数据进行预览、搜索或分块处理；  
- 批量发起子任务；  
- 汇总处理结果。  

## 使用场景  
- 输入数据量超出上下文窗口的容量；  
- 需要对输入数据进行密集访问的任务；  
- 大型日志文件、数据集或多文件分析场景。  

## 核心文件  
与该技能相关的可执行辅助脚本包含在以下文件中（运行时不会被下载）：  
- `scripts/rlm_ctx.py`：用于存储上下文数据及执行预览/搜索/分块操作；  
- `scripts/rlm_auto.py`：用于生成处理计划及提示信息；  
- `scripts/rlm_async_plan.py`：用于批量任务调度；  
- `scripts/rlm_async_spawn.py`：用于发起子任务；  
- `scripts/rlm.emit_toolcalls.py`：用于生成工具调用所需的JSON格式数据；  
- `scripts/rlm_trace_summary.py`：用于日志汇总；  
- `docs/policy.md`：包含处理策略及安全限制说明；  
- `docs/flows.md`：包含手动操作流程及异步处理流程。  

## 使用步骤（高级概述）  
1. 通过 `rlm_ctx.py` 存储输入数据；  
2. 通过 `rlm_auto.py` 生成处理计划；  
3. 通过 `rlm_async_plan.py` 创建异步任务批次；  
4. 通过 `sessions_spawn` 发起子任务；  
5. 在主会话中汇总处理结果。  

## 所使用的工具  
- 该技能依赖于 OpenClaw 提供的工具：`read`、`write`、`exec`、`sessions_spawn`；  
- `exec` 仅用于调用 `scripts/` 目录中列出的安全辅助脚本；  
- 不会执行模型输出中的任意代码；  
- 所有生成的工具调用请求在输出前都会经过明确的安全性检查。  

## 自动执行机制  
- 该技能默认不会设置 `disableModelInvocation: true`；  
- 需要在每次执行前获取用户确认的操作员应在 OpenClaw 配置中将该选项设置为 `true`；  
- 在默认模式下，模型可以自动调用该技能，所有操作仍受策略限制的约束。  

## 安全性措施  
- 仅会调用经过安全审核的辅助脚本；  
- 最大递归深度为 1；  
- 对输入数据的切片和子任务调用有严格限制；  
- 输入的提示信息被视为数据，而非执行指令；  
- 详细的安全保障措施请参阅 `docs/security.md`；  
- 运行前/运行中/运行后的安全检查流程请参阅 `docs/security_checklist.md`。  

## OpenClaw 子代理的限制  
根据 OpenClaw 的文档（subagents.md）：  
- 子代理不能创建其他子代理；  
- 子代理默认没有会话管理相关工具（如 `sessions_*`）；  
- `sessions_spawn` 是非阻塞的，并会立即返回执行结果。  

## 清理操作  
运行完成后，请使用 `scripts/cleanup.sh` 命令清除临时文件；  
- 文件保留策略：`CLEAN_RETENTION=N`；  
- 可忽略的文件规则请参阅 `docs/cleanup_ignore.txt`（通过子字符串匹配确定）。  

## 配置信息  
具体配置参数（如阈值和默认限制）请参阅 `docs/policy.md`。