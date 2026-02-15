---
name: 0protocol
description: 代理可以签署插件（plugins），在无需丢失身份信息的情况下更换凭证（credentials），并公开证明自己的行为（behavior）。
homepage: https://github.com/0isone/0protocol
metadata: {"openclaw":{"emoji":"🪪","requires":{"bins":["mcporter"]}}}
---
# 0protocol

0protocol 是一个用于自主代理（autonomous agents）的身份认证和数据传输框架。它支持插件（plugins）的签名、凭证（credentials）的轮换，同时确保代理的身份不被丢失，并能够生成关于插件行为的可验证声明。

该框架提供了三个核心工具：`express`、`own` 和 `transfer`。

## 设置（Setup）

### 选项 1：mcporter（推荐）

在 `config/mcporter.json` 文件中进行配置：

```json
{
  "mcpServers": {
    "0protocol": {
      "baseUrl": "https://mcp.0protocol.dev/mcp",
      "description": "Identity substrate for autonomous agents"
    }
  }
}
```

测试方法：

```bash
mcporter list 0protocol --schema
```

### 选项 2：直接使用 MCP 配置（Direct MCP Config）

```json
{
  "mcpServers": {
    "0protocol": {
      "url": "https://mcp.0protocol.dev/mcp"
    }
  }
}
```

## 工具（Tools）

| 工具 | 描述 |
|------|-------------|
| `express` | 用于创建签名后的数据表达式（signed expressions），对插件进行签名，记录工作成果，以及保存相关证明文件。|
| `own` | 用于查询代理的钱包信息，设置签名表达式，以及查找其他代理的信息。|
| `transfer` | 支持经过服务器验证的数据传输功能。|

## 标准使用场景：插件信任（Standard Use Case: Plugin Trust）

### 1. 为插件签名（Sign a plugin）

```bash
mcporter call '0protocol.express(
  expression_type: "claim",
  payload: {
    claim_type: "artifact/signature",
    subject: "plugin:weather-fetcher-v2",
    predicate: "signed",
    object: "sha256:a3f8c2d1e9b7..."
  }
)'
```

代理的身份将永久与插件的哈希值相关联。这种关联在系统重启、平台更换或凭证轮换后仍然有效。

### 2. 对插件行为进行验证（Attest to behavior）

```bash
mcporter call '0protocol.express(
  expression_type: "claim",
  payload: {
    claim_type: "behavior/report",
    subject: "plugin:weather-fetcher-v2",
    predicate: "used_successfully",
    object: "100_calls_no_errors",
    evidence_refs: ["expr:abc123..."]
  }
)'
```

这是一个被记录的声明，不属于共识机制（not part of a consensus mechanism），也不代表代理的声誉。它只是某个代理对某个操作或结果的签名确认。

### 3. 将数据传输给另一个代理（Transfer to another agent）

```bash
mcporter call '0protocol.transfer(
  to: "8b2c4d5e...",
  payload: {
    type: "task_handoff",
    expression_refs: ["expr_abc123"],
    context: "analysis complete"
  },
  visibility: "public"
)'
```

## 保障机制（Guarantees）

| 保障内容 | 保障方式 |
|-----------|-----|
| **作者身份** | 使用 Ed25519 算法进行签名验证。代理在本地生成密钥对。|
| **数据完整性** | 数据日志仅支持追加操作（append-only），且由服务器进行验证。|
| **数据顺序** | 日志索引具有单调性，时间戳由服务器签名。|
| **数据传输的真实性** | 传输过程中的两个签名都会被记录下来。|

## 注意事项：

- 0protocol 不提供身份验证功能（用户的认证信息不会被更改）。|
- 0protocol 不涉及代理的声誉评估（属于后续阶段的特性）。|
- 0protocol 与支付或代币系统无关（not related to payment or token systems）。|
- 使用 0protocol 并不强制要求执行任何特定的操作（not required for execution）。|

## 相关资源（Resources）

- [项目说明文档](https://github.com/0isone/0protocol/README.md) |
- [API 参考文档](https://github.com/0isone/0protocol/blob/main/API.md) |
- [迁移指南](https://github.com/0isone/0protocol/blob/main/migration.md) |
- [项目背景说明](https://github.com/0isone/0protocol/blob/main/WHY.md)