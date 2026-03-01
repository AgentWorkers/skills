---
name: sanitize
description: 从文本文件中检测并删除个人身份信息（PII）。支持15种类型的敏感数据，包括信用卡号、社会安全号码（SSN）、电子邮件地址、API密钥、地址等——且完全不需要依赖任何外部库或服务。
version: "1.0.0"
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "\U0001F6E1"
    homepage: https://github.com/agentward-ai/agentward
  files:
    - scripts/sanitize.py
---
# AgentWard 数据清洗工具

该工具用于检测并替换文本文件中的个人身份信息（PII）。

## 重要提示 — PII 安全规则
- **切勿直接读取输入文件**，因为其中可能包含敏感的 PII 数据。
- **务必使用 `--output FILE` 选项将清洗后的结果写入指定文件**。
- **仅读取清洗后的输出文件，切勿直接查看原始输入文件**。
- **仅向用户展示清洗后的结果，切勿显示原始输入内容**。
- `--json` 和 `--preview` 选项是安全的，它们不会将原始 PII 数据输出到标准输出（stdout）。
- 当使用 `--output` 选项时，实体映射文件（原始 PII 数据与占位符的对应关系）会被保存到单独的文件（`*.entity-map.json`）中。请勿直接读取该文件。

## 功能介绍

该工具会扫描文件中的以下类型 PII 数据：信用卡号、社会安全号码（SSN）、电子邮件地址、电话号码、API 密钥、IP 地址、出生日期、护照号码、驾驶执照号码、银行路由号码、医疗执照号码以及保险会员 ID，并将这些数据替换为编号占位符（例如 `[CREDIT_CARD_1]`）。

## 使用方法

### 清洗文件（推荐使用：始终使用 `--output` 选项）
```bash
python scripts/sanitize.py patient-notes.txt --output clean.txt
```

### 预览模式（检测 PII 类型及位置，但不显示原始值）
```bash
python scripts/sanitize.py notes.md --preview
```

### JSON 格式输出（安全模式：无原始 PII 数据输出到 stdout）
```bash
python scripts/sanitize.py report.txt --json --output clean.txt
```

### 过滤特定类型的 PII 数据
```bash
python scripts/sanitize.py log.txt --categories ssn,credit_card,email --output clean.txt
```

## 支持的 PII 类型

请参阅 `references/SUPPORTED_PII.md` 文件，以获取完整的 PII 类型列表及相应的检测方法、误报处理方式。

| 类型 | 检测模式 | 示例 |
|---|---|---|
| `credit_card` | 经 Luhn 算法验证的 13-19 位数字 | 4111 1111 1111 1111 |
| `ssn` | 3-2-4 位的数字组合 | 123-45-6789 |
| `cvv` | 以特定关键词开头的 3-4 位数字 | CVV: 123 |
| `expiry_date` | 以特定关键词开头的日期格式 | expiry 01/30 |
| `api_key` | 根据提供商前缀识别的字符串 | sk-abc..., ghp_..., AKIA... |
| `email` | 标准电子邮件格式 | user@example.com |
| `phone` | 美国/国际电话号码 | +1 (555) 123-4567 |
| `ip_address` | IPv4 地址 | 192.168.1.100 |
| `date_of_birth` | 以特定关键词开头的日期格式 | DOB: 03/15/1985 |
| `passport` | 以特定关键词开头的字母数字字符串 | Passport: AB1234567 |
| `drivers_license` | 以特定关键词开头的字母数字字符串 | DL: D12345678 |
| `bankrouting` | 以特定关键词开头的 9 位数字 | routing: 021000021 |
| `address` | 街道地址 + 城市/州/邮政编码 | 742 Evergreen Terrace Dr, Springfield, IL 62704 |
| `medical_license` | 以特定关键词开头的执照编号 | License: CA-MD-8827341 |
| `insurance_id` | 以特定关键词开头的会员/保单编号 | Member ID: BCB-2847193 |

## 安全性与隐私保护

- **所有处理操作均在本地完成**，脚本不会进行任何网络请求，数据不会离开用户的设备。
- **无外部依赖**，仅使用 Python 标准库，无需安装第三方库。
- **原始 PII 数据永远不会被输出到标准输出（stdout）**。`--json` 和 `--preview` 选项会确保输出中不包含原始 PII 数据。当使用 `--output` 选项时，实体映射文件（包含原始 PII 数据与占位符的对应关系）才会被保存到磁盘上。
- **专为代理安全设计**：使用说明明确要求代理切勿直接读取原始输入文件或实体映射文件，仅查看清洗后的结果。

## 系统要求

- Python 3.11 及以上版本
- 无需安装任何外部依赖库（仅依赖 Python 标准库）。

## 关于作者

该工具由 [AgentWard](https://agentward.ai) 开发，AgentWard 是一个用于 AI 代理的开源权限控制平台。