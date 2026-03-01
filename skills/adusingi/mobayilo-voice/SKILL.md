---
name: mobayilo-voice
description: 通过 Mobayilo 进行出站电话呼叫，采用安全的默认设置（默认为预览模式），并支持显式的实时执行。
metadata: {"openclaw":{"emoji":"📞","homepage":"https://mobayilo.com","requires":{"bins":["moby"],"env":["MOBY_HOST"]}}}
---
# Mobayilo Voice（测试版）

当工作流程需要通过电话进行沟通（如预订、确认或跟进）时，请使用此功能。

## 安全模型
- 默认行为为**预览模式**（不会实际拨打电话）。
- 要进行实际通话，需要明确执行`--execute`命令。
- 回拨和备用方案都是可选的设置。

## 操作步骤

### 1) 检查准备情况
```bash
cd {workspace}/integrations/mobayilo_voice
PYTHONPATH=. python actions/check_status.py
```

### 2) 启动预览模式下的通话
```bash
cd {workspace}/integrations/mobayilo_voice
PYTHONPATH=. python actions/start_call.py --destination +14155550123 --country US
```

### 3) 启动实际通话
```bash
cd {workspace}/integrations/mobayilo_voice
PYTHONPATH=. python actions/start_call.py \
  --destination +14155550123 \
  --country US \
  --execute
```

## 可选参数
- `--approved`（当启用了审批流程时使用）
- `--callback`（设置回调功能）
- `--fallback-callback`（设置备用回拨策略）
- `--require-agent-ready`（要求代理处于可用状态）

## 输出结果
- 为操作员提供易于理解的摘要信息
- 为自动化流程提供JSON格式的数据

## 已知限制（测试版）
桌面代理模式下的通话流程提示信息仍在优化中，以在所有环境中提供更加用户友好的体验。