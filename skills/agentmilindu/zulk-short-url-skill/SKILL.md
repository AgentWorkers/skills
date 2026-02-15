---
name: zulk-url-shortener
description: 这款高级工具专注于AI驱动的URL缩短服务，具备实时数据分析功能，并支持团队协作（通过MCP平台实现）。适用于营销活动中的链接缩短、追踪AI交互行为，以及自定义域名的管理。关键词：URL、短链服务、数据分析、链接管理、MCP。
license: MIT
compatibility: Requires an MCP-compatible client and internet access.
metadata:
  repository: https://github.com/Zu-lk/zulk-short-url-skill
  mcp_url: https://mcp.zu.lk/mcp
  mcp_sse_url: https://mcp.zu.lk/sse
  mcp_command: npx mcp-remote https://mcp.zu.lk/mcp
---

# Zulk URL缩短器技能

该技能使AI代理能够使用Zu.lk MCP（模型上下文协议，Model Context Protocol）服务器来管理短链接。

## 概述

Zu.lk是一款以AI为核心的高级URL缩短器，专为极致的性能和无缝的AI集成而设计。该技能将您的代理连接到Zulk MCP服务器，使其能够：

- 创建缩短后的URL（例如：`zu.lk/abcd`）
- 管理现有的链接和活动
- 查看实时分析数据
- 与团队成员协作

## 安装

要使用此技能，请将Zulk MCP服务器的配置添加到您的AI助手的设置文件中（例如：`mcp.json`或相应的文件）。

### 配置选项

选择最适合您环境的传输方式：

#### 1. Streamable HTTP（推荐）
最快的、最可靠的通信方式。
```json
{
  "mcpServers": {
    "zulk-url-shortener": { "url": "https://mcp.zu.lk/mcp" }
  }
}
```

#### 2. SSE（服务器发送事件，Server-Sent Events）
专为某些客户端设计的实时流式传输方式。
```json
{
  "mcpServers": {
    "zulk-url-shortener": { "url": "https://mcp.zu.lk/sse" }
  }
}
```

#### 3. Stdio（通过mcp-remote）
通过远程桥接使用标准输入/输出。
```json
{
  "mcpServers": {
    "zulk-url-shortener": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.zu.lk/mcp"]
    }
  }
}
```

## 分步操作说明

1. **准备**：确保您拥有Zu.lk账户，或准备好通过Google登录。
2. **配置**：将上述JSON配置之一添加到您的代理的MCP设置文件中。
3. **身份验证**：首次运行“shorten this link”等命令时，代理会提供一个OAuth链接。请按照链接进行身份验证。
4. **验证**：询问代理“List my recently created links”以确认连接是否正常。
5. **执行**：使用自然语言创建链接，例如：“为https://google.com创建一个别名为‘my-search’的短链接”。

## 使用示例

### 创建链接
**输入**：“Shorten https://github.com/Zu-lk/zulk-short-url-skill”
**输出**：“生成的短链接：https://zu.lk/z-skill”

### 查看分析数据
**输入**：“我的‘newsletter’链接昨天收到了多少点击量？”
**输出**：“您的‘newsletter’链接昨天收到了1,240次点击。”

## 边缘情况与故障排除

- **身份验证失败**：如果身份验证失败，请确保您使用的是正确的Google账户。您可能需要重新启动代理以重新触发OAuth流程。
- **别名已被占用**：如果自定义别名已被使用，代理会建议使用其他别名或添加一个随机字符串。
- **速率限制**：如果超过了您的计划链接限制，MCP服务器会返回错误提示。
- **链接过期**：如果链接突然无法使用，请检查该链接是否有过期日期。

## 参考资料
- [官方网站](https://zu.lk)
- [MCP文档](https://zu.lk/-/mcp)