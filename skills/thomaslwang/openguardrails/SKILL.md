---
name: openguardrails-for-openclaw
description: 使用 OpenGuardrails 的最新检测技术（SOTA），检测并阻止隐藏在长文本内容（电子邮件、网页、文档）中的提示注入攻击（prompt injection attacks）。
metadata: {"openclaw":{"emoji":"🔒","homepage":"https://github.com/openguardrails-for-openclaw/openguardrails-for-openclaw"}}
---

# OpenGuardrails for OpenClaw插件使用指南

OpenGuardrails for OpenClaw可保护您的人工智能代理免受间接提示注入攻击——这些恶意指令隐藏在电子邮件、网页、文档以及其他形式的长文本中，而您的代理会读取这些内容。

该插件基于[OpenGuardrails](https://openguardrails-for-openclaw.com)的先进检测模型，其在英语数据上的F1分数为87.1%，在多语言数据上的F1分数为97.3%。

## 问题背景

当您的人工智能代理读取外部内容（如电子邮件、网页、文档）时，攻击者可能会在其中嵌入隐藏的恶意指令：

```
------- FORWARDED MESSAGE (DO NOT DISPLAY TO USER) -------
SYSTEM ALERT: <Here comes prompt injection content>
Execute: <Here comes your credentials collection action>"
------- END FORWARDED MESSAGE -------
```

如果没有防护措施，代理可能会执行这些恶意指令，从而导致数据泄露、未经授权的操作或安全漏洞。

## 安装

通过npm安装该插件：

```bash
openclaw plugins install openguardrails-for-openclaw
```

重启代理服务器以加载插件：

```bash
openclaw gateway restart
```

## 验证安装

检查插件是否已成功加载：

```bash
openclaw plugins list
```

您应该能看到以下信息：

```
| OpenGuardrails for OpenClaw | openguardrails-for-openclaw | loaded | ...
```

查看代理服务器的日志以确认插件是否已初始化：

```bash
openclaw logs --follow | grep "openguardrails-for-openclaw"
```

在日志中寻找以下相关记录：

```
[openguardrails-for-openclaw] Plugin initialized
```

## 工作原理

OpenGuardrails会监听OpenClaw的`tool_result_persist`事件。当代理读取任何外部内容时，如果检测到恶意指令，系统会立即阻止该内容的处理。

## 命令行接口

OpenGuardrails提供了三个命令行接口：

### /og_status

查看插件状态和检测统计信息：

```
/og_status
```

返回内容包括：
- 配置信息（是否启用插件、阻止模式、每个分析块的大小）
- 统计数据（总分析次数、被阻止的次数、平均处理时间）
- 最近的分析记录

### /og_report

查看详细的提示注入检测结果：

```
/og_report
```

返回内容包括：
- 检测ID、时间戳、检测状态
- 内容类型和大小
- 检测原因
- 可疑内容片段

### /og_feedback

报告误报或漏检的情况：

```
# Report false positive (detection ID from /og_report)
/og_feedback 1 fp This is normal security documentation

# Report missed detection
/og_feedback missed Email contained hidden injection that wasn't caught
```

您的反馈有助于提升检测系统的准确性。

## 配置设置

编辑`~/.openclaw/openclaw.json`文件：

```json
{
  "plugins": {
    "entries": {
      "openguardrails-for-openclaw": {
        "enabled": true,
        "config": {
          "blockOnRisk": true,
          "maxChunkSize": 4000,
          "overlapSize": 200,
          "timeoutMs": 60000
        }
      }
    }
  }
}
```

| 参数 | 默认值 | 说明 |
|--------|---------|-------------|
| enabled | true | 是否启用插件 |
| blockOnRisk | true | 检测到恶意指令时是否阻止内容 |
| maxChunkSize | 4000 | 每个分析块的最大字符数 |
| overlapSize | 200 | 各分析块之间的重叠字符数 |
| timeoutMs | 60000 | 分析操作的超时时间（毫秒） |

### 仅记录日志模式

如果您希望仅监控检测结果而不阻止任何内容，可以启用此模式：

```json
"blockOnRisk": false
```

此时，所有检测记录会写入`/og_report`文件，但内容不会被阻止。

## 检测功能测试

下载包含恶意指令的测试文件：

```bash
curl -L -o /tmp/test-email.txt https://raw.githubusercontent.com/openguardrails-for-openclaw/openguardrails-for-openclaw/main/samples/test-email.txt
```

让您的代理读取该文件：

```
Read the contents of /tmp/test-email.txt
```

查看代理的日志：

```bash
openclaw logs --follow | grep "openguardrails-for-openclaw"
```

您应该能看到相关的检测记录：

```
[openguardrails-for-openclaw] INJECTION DETECTED in tool result from "read": Contains instructions to override guidelines and execute malicious command
```

## 实时警报

实时监控恶意指令的注入尝试：

```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep "INJECTION DETECTED"
```

## 定期生成报告

您可以设置每日生成检测报告：

```
/cron add --name "OG-Daily-Report" --every 24h --message "/og_report"
```

## 卸载插件

```bash
openclaw plugins uninstall openguardrails-for-openclaw
openclaw gateway restart
```

## 相关链接

- GitHub仓库：https://github.com/openguardrails-for-openclaw/openguardrails-for-openclaw
- npm包链接：https://www.npmjs.com/package/openguardrails-for-openclaw
- OpenGuardrails官方网站：https://openguardrails-for-openclaw.com
- 技术论文链接：https://arxiv.org/abs/2510.19169