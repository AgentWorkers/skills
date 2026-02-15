---
name: pipelock
description: 通过扫描代理来保护代理的 HTTP 请求，该代理能够捕获凭证泄露（credential leaks）、跨站请求伪造（SSRF）以及脚本注入（prompt injection）攻击。
homepage: https://github.com/luckyPipewrench/pipelock
user-invocable: true
metadata:
  clawdbot:
    emoji: "\U0001F512"
    requires:
      bins: ["pipelock"]
      os: ["darwin", "linux"]
---

# Pipelock 安全防护工具

Pipelock 是一个位于您与互联网之间的代理服务器。所有出站 HTTP 请求都会经过一个七层扫描流程，该流程能够检测 API 密钥泄露、SSRF（跨站请求伪造）攻击、提示注入（prompt injection）以及数据窃取行为。

## 安装

```bash
# Homebrew (macOS/Linux)
brew install luckyPipewrench/tap/pipelock

# Or Go
go install github.com/luckyPipewrench/pipelock/cmd/pipelock@latest
```

## 快速入门

生成配置文件并启动代理服务：

```bash
pipelock generate config --preset balanced -o pipelock.yaml
pipelock run --config pipelock.yaml
```

代理服务器监听地址为 `http://localhost:8888`。您需要将所有 HTTP 请求路由通过该代理服务器：

```bash
curl "http://localhost:8888/fetch?url=https://example.com/api/data"
```

## 与 MCP 服务器配合使用

将任何 MCP 服务器的响应数据传递给 Pipelock，以便检测提示注入攻击：

```bash
pipelock mcp proxy -- npx @modelcontextprotocol/server-filesystem /path/to/dir
```

## 支持的防护功能：

1. **SSRF 防御**：阻止对内部 IP 地址的请求，检测 DNS 重绑（DNS rebinding）行为。
2. **域名黑名单**：阻止数据窃取目标（如 pastebin、transfer.sh 等网站）的访问。
3. **速率限制**：检测异常的请求流量峰值。
4. **数据泄露防护（DLP）**：检测 URL 和请求体中的 API 密钥（如 Anthropic、OpenAI、AWS、GitHub 等服务的密钥）。
5. **环境变量泄露检测**：检测出站流量中是否包含实际的环境变量值。
6. **熵分析**：标记那些看似敏感信息的高熵字符串。
7. **URL 长度限制**：检测过长的 URL，以防止数据窃取行为。

## 威胁处理方式：

当检测到威胁时，您可以配置以下几种处理方式：
- `block`：拒绝请求。
- `strip`：删除相关内容后继续转发请求。
- `warn`：记录日志并允许请求通过。
- `ask`：在终端提示用户进行人工确认（y/N/s）。

## 预设配置选项：

- `balanced`：默认配置，适用于大多数场景。
- `strict`：严格防护，设置较低的触发阈值。
- `audit`：仅检测并记录日志，不阻止请求。
- `claude-code`：专为 Claude Code 代理框架优化。
- `cursor`：专为 Cursor IDE 优化。
- `generic-agent`：适用于任何代理框架。

## 工作区完整性检测：

检测工作区文件是否被未经授权的修改：

```bash
pipelock integrity init ./workspace
pipelock integrity check ./workspace
```

## 更多信息：

- [OWASP 安全漏洞映射](https://github.com/luckyPipewrench/pipelock/blob/main/docs/owasp-mapping.md)
- [Claude Code 集成指南](https://github.com/luckyPipewrench/pipelock/blob/main/docs/guides/claude-code.md)
- 使用 Apache 2.0 许可证，仅包含一个可执行文件，无依赖项。