---
name: openclaw-security-audit
description: 审计 OpenClaw 的配置以识别安全风险，并使用用户配置的 Large Language Model (LLM) 生成一份修复报告。
metadata:
  openclaw:
    requires:
      bins: ["cat", "jq"]
    os: ["darwin", "linux", "windows"]
---

# OpenClaw 安全审计技能

这是一项仅限本地使用的技能，用于审计 `~/.openclaw/openclaw.json` 配置文件。该技能会执行 15 项以上的安全检查，并根据用户现有的大型语言模型（LLM）配置生成详细的审计报告。无需使用任何外部 API 或密钥。

## 适用场景

- 用户希望对自身的 OpenClaw 实例进行安全审计。
- 用户需要针对配置风险制定相应的修复措施。
- 用户在准备 OpenClaw 的部署时，希望获得安全加固方面的建议。

## 工作原理

1. 使用标准工具（如 `cat`、`jq`）读取配置文件。
2. 提取与安全相关的设置（但不会包含实际的敏感信息）。
3. 构建一个包含元数据的结构化审计结果对象。
4. 通过 OpenClaw 的常规代理流程将审计结果传递给用户的大型语言模型。
5. 生成一份包含风险等级和修复建议的 Markdown 报告。

## 输入参数

- `target_config_path`（可选）：OpenClaw 配置文件的路径。
  - 默认值：`~/.openclaw/openclaw.json`

## 输出结果

- 一份 Markdown 格式的报告，内容包括：
  - 总体风险评分（0-100 分）
  - 按严重程度分类的审计结果（严重/高/中/低）
  - 每项审计结果的详细说明、问题原因、修复方法及示例配置
  - 优先级排序的修复建议

## 安全检查项目（共 15 项以上）

1. 配置文件中硬编码了 API 密钥（而非从环境变量中获取）
2. 网关认证令牌设置不安全或缺失
3. 网关的 `bind` 设置不安全（例如设置为 `0.0.0.0` 且未进行适当认证）
4. 缺少通道访问控制机制（`allowFrom` 未配置）
5. 工具权限设置不安全（某些工具被赋予了过高权限）
6. 沙箱功能被禁用（而实际上应该启用）
7. 通道访问没有设置速率限制
8. 日志中可能泄露敏感信息
9. OpenClaw 版本过旧
10. WhatsApp 配置不安全
11. Telegram 配置不安全
12. Discord 配置不安全
13. 特权操作缺乏审计日志记录
14. 文件系统访问权限设置过于宽松
15. Webhook 端点未受到限制
16. 管理员默认凭据不安全

## 数据处理规则

- 在分析之前会删除所有敏感信息。
- 仅报告配置项的存在、缺失或已配置的状态等元数据。
- 不会记录或暴露实际的密钥值。
- 该技能仅在本机执行，不涉及任何网络请求。

## 审计结果示例（部分内容已屏蔽）

```json
{
  "config_path": "~/.openclaw/openclaw.json",
  "openclaw_version": "present",
  "gateway": {
    "bind": "0.0.0.0",
    "auth_token": "missing"
  },
  "channels": {
    "allowFrom": "missing",
    "rate_limits": "missing"
  },
  "secrets": {
    "hardcoded": "detected"
  },
  "tool_policies": {
    "elevated": "unrestricted"
  }
}
```

## 报告格式要求

报告必须包含以下内容：
- 总体风险评分（0-100 分）
- 安全风险等级（严重/高/中/低）
- 每项安全问题的详细说明、问题原因、修复方法及示例配置
- 优先级排序的修复建议

## 技能执行流程（简化示意图）

```text
read_config_path = input.target_config_path || ~/.openclaw/openclaw.json
raw_config = cat(read_config_path)
json = jq parse raw_config
metadata = extract_security_metadata(json)
findings = build_findings(metadata)
report = openclaw.agent.analyze(findings, format=markdown)
return report
```

## 注意事项

- 该技能依赖于用户现有的 OpenClaw 大型语言模型配置（如 Opus、GPT、Gemini 等）。
- 不需要使用任何外部 API 或特殊模型。