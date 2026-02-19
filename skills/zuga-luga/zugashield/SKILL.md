---
name: zugashield
description: 适用于 OpenClaw 的 7 层 AI 安全扫描器。能够同时阻止通过所有渠道（Signal、Telegram、Discord、WhatsApp 和网页）进行的提示注入（prompt injection）、跨站请求伪造（SSRF）、命令注入（command injection）、数据泄露（data leakage）以及内存破坏（memory poisoning）等攻击行为。
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - python
      primaryModel: any
    permissions:
      - subprocess
  author: Zuga-luga
  license: MIT
  homepage: https://github.com/Zuga-luga/ZugaShield
  npm: zugashield-openclaw-plugin
---
# ZugaShield 安全扫描器

这是一个专为 OpenClaw 设计的 7 层人工智能安全扫描插件。它通过拦截所有流量的入口点（即 Gateway）来同时保护所有通信渠道。

## 防御内容

| 攻击类型 | 防御机制 | 检测方式 |
|--------|------|-----------|
| 提示注入（Prompt Injection） | 请求预处理（preRequest） | 通过 150 多种签名检测、Unicode 欺骗以及编码绕过技术进行识别 |
| SSRF/命令注入（SSRF/Command Injection） | 工具执行前（preToolExecution） | 通过检测云服务元数据 URL 和 shell 元字符来阻止攻击（此类攻击会被立即阻断） |
| 机密信息/个人身份信息泄露（Secret/PII Leakage） | 响应预处理（preResponse） | 检测 API 密钥、令牌、凭据等高熵字符串 |
| 内存污染（Memory Poisoning） | 数据回收前（preRecall） | 通过检测嵌入在回收内存中的恶意指令或潜伏性负载来防止攻击 |
| DNS 数据泄露（DNS Exfiltration） | 响应预处理（preResponse） | 通过检测高熵子域名和 DNS 数据中的恶意模式来阻止攻击 |
| 路径遍历（Path Traversal） | 工具执行前（preToolExecution） | 通过检测目录遍历序列和符号链接攻击来阻止攻击 |

## 安装

```bash
pip install "zugashield[mcp]"
npm install zugashield-openclaw-plugin
openclaw plugins install ./node_modules/zugashield-openclaw-plugin
openclaw restart
```

## 验证安装

执行以下命令后，应显示“CONNECTED”状态，并确认有 7 个安全防护层处于激活状态：

```
/shield status
```

## 配置

在 `openclaw.json` 文件的 `plugins.entries.openclaw-plugin.config` 部分，可以配置以下选项：

- `fail_closed`（默认值：true）：当扫描器无法正常工作时，阻止所有请求 |
- `strict_mode`（默认值：false）：不仅阻止高危险级别的攻击，也阻止中等危险级别的攻击 |
- `scan.inputs` / `scan.outputs` / `scan.tool_calls` / `scan.memory`：分别控制各个安全防护机制的启用状态

## 工作原理

ZugaShield 会作为一个受管理的子进程（Python MCP 服务器）运行。所有消息、工具调用以及响应数据都会在 <15 毫秒内通过扫描器进行检测。该插件利用 OpenClaw 的 Gateway 防护机制，因此一次安装即可同时保护 Signal、Telegram、Discord、WhatsApp 和 Web 等所有通信渠道。

**注意：** 无论配置如何，所有工具调用都会被立即阻断（fail-closed），因为 SSRF 和命令注入这类攻击的风险实在太大，无法被允许通过。

## 链接

- [GitHub](https://github.com/Zuga-luga/ZugaShield)：官方仓库 |
- [npm](https://www.npmjs.com/package/zugashield-openclaw-plugin)：npm 包下载地址 |
- [PyPI](https://pypi.org/project/zugashield/)：PyPI 包下载地址