# SAP FICO 专家 — OpenClaw 技能

## 📋 概述

| 属性 | 值 |
|----------|-------|
| **名称** | `sap-fico-expert` |
| **版本** | 1.0.0 |
| **平台** | OpenClaw（Telegram / 社交平台） |
| **目标大型语言模型（LLM）** | DeepSeek Chat（用于提供解释）/ DeepSeek Coder（用于处理 ABAP 相关问题） |
| **语言** | 法语技术术语（用于 SAP 相关内容） |
| **作者** | @chanfouricc |

## 🎯 目标

将任何 OpenClaw 机器人转变为具备高级 SAP 财务与控制咨询能力的专家，能够以生产级准确度回答关于配置、故障排除、模块间集成以及 S/4HANA 迁移等方面的问题。

## 📁 技能结构

```
sap-fico-skill/
├── SKILL.md                  # This documentation
├── skill.json                # OpenClaw skill configuration
├── system_prompt.md          # Full system prompt (to inject)
├── examples.json             # Calibrated few-shot Q&A examples
└── reference/
    ├── tcodes_index.md       # T-code index by domain
    ├── tables_index.md       # Critical SAP tables index
    └── error_codes.md        # Common FI/CO error messages
```

## 🚀 在 OpenClaw 上的安装

### 1. 将该技能复制到您的 VPS

```bash
scp -r sap-fico-skill/ user@vps:/opt/openclaw/skills/
```

### 2. 在 OpenClaw 中注册该技能

将其添加到您的 OpenClaw 配置文件（`config.json` 或等效文件）中：

```json
{
  "skills": {
    "sap-fico-expert": {
      "enabled": true,
      "trigger": "auto",
      "keywords": ["SAP", "FICO", "FI-GL", "FI-AP", "FI-AR", "FI-AA", "CO-CCA", "CO-PA", "CO-PC", "ACDOCA", "S/4HANA", "T-code", "BKPF", "BSEG", "OB52", "FB01", "KS01"],
      "system_prompt_path": "skills/sap-fico-expert/system_prompt.md",
      "examples_path": "skills/sap-fico-expert/examples.json",
      "model_override": "deepseek-chat",
      "parameters": {
        "max_tokens": 600,
        "temperature": 0.25,
        "presence_penalty": 0.1
      }
    }
  }
}
```

### 3. 触发激活

当消息中包含 SAP 相关关键词时，该技能会自动激活。用户也可以手动触发激活：

```
/skill sap-fico-expert
```

## 🔧 推荐设置

| 参数 | 值 | 说明 |
|-----------|-------|-----------|
| `temperature` | 0.25 | 确定性参数——确保在处理 SAP 配置时不会产生创造性回答 |
| `max_tokens` | 600 | 从初始的 450 个令牌增加到 600 个，以适应更复杂的问题 |
| `presence Penalty` | 0.1 | 适度增加词汇多样性，同时保持回答的连贯性 |
| `model` | `deepseek-chat` | 默认模型；当检测到 ABAP 相关内容时切换至 `deepseek-coder` |

> ⚠️ **注意**：令牌限制从最初的 450 个提高到了 600 个。涉及模块间集成或 S/4HANA 迁移的回答需要更多的信息空间，以确保其实用性。

## 📊 覆盖范围

### 第一级 — 核心专业知识（即时回答）
- 财务会计（FI-GL、FI-AP、FI-AR、FI-AA、FI-BL）配置
- 成本会计（CO-CCA、CO-PA、CO-PC、CO-OPA）配置
- 期末及年度结账处理
- 自动账户确定（FI-MM、FI-SD）
- T 代码、相关表格及自定义交易处理

### 第二级 — 高级专业知识（详细回答）
- S/4HANA 统一日记账（ACDOCA）
- 从 ECC 迁移到 S/4HANA（旧系统/新系统）
- SAP Cloud Public Edition 的具体内容
- 中央财务与集团报表
- Fxxx/Kxxx 类错误信息的故障排除

### 第三级 — 集成专业知识（基于上下文的回答）
- 生产订单结算（FI-PP）
- 工资单集成（FI-HR）
- 项目结算（FI-PS）
- 公司间处理与对账
- 税务报告（增值税、预扣税、国内税务）

## 🧪 测试

### 快速验证问题

| 编号 | 测试问题 | 验证内容 |
|---|--------------|--------|
| 1 | “如何在 S/4HANA 中配置文档拆分？” | 包含 T 代码、相关表格及操作步骤 |
| 2 | “过账时出现错误 F5 025” | 问题诊断、解决方案及配置说明 |
| 3 | “CO 模块中的评估与分配有何区别？” | 解释相关概念、T 代码及使用场景 |
| 4 | “GR/IR 清算流程是怎样的？” | 包含处理流程、FI-MM 的集成方式及相关 T 代码 |
| 5 | “如何将 FI-AA 迁移到新资产会计系统？” | 包含操作步骤、相关表格及 S/4HANA 的具体要求 |

### 质量标准

- ✅ 回答中必须提及 T 代码 |
- ✅ 必须列出相关的 SAP 表格 |
- 在适用情况下需引用配置信息 |
- 必须指出模块间的影响 |
- 在相关情况下需提及 S/4HANA 的差异 |
- 语言风格需专业且易于理解 |
- 回答需使用法语技术术语

## 📝 更新日志

| 版本 | 日期 | 更新内容 |
|---------|------|---------|
| 1.0.0 | 2026-02-08 | 首次发布——全面覆盖财务会计（FI/CO）领域 |