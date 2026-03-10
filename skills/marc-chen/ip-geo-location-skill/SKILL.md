---
name: ip-geo-location-skill
description: "通过 MCP 进行 IP 地理位置查询。当用户询问 IP 地点、IP 的地理位置、IP 的来源、IP 查询、ASN（自治系统编号）、将 IP 对应到国家/城市时，可以使用此功能。"
argument-hint: "Provide one or more IPs (IPv4/IPv6), e.g. 8.8.8.8, 1.1.1.1"
user-invocable: true
---
# IP地理定位技能

使用此技能，可以通过 `mcp-geoip-server` MCP 服务查询 IP 地理信息和自治系统编号（ASN）信息。

该技能适用于以下场景：

- 单个 IP 地址的查询
- 多个 IP 地址的批量查询
- 从域名查询 IP 地址后再进行地理定位
- 结果以结构化格式输出，便于用户快速阅读

## MCP 服务器

- 名称：`mcp-geoip-server`
- URL：`http://ip.api4claw.com/mcp`
- 数据传输方式：流式 HTTP

### VS Code 中的 MCP 配置

将以下配置添加到 `.vscode/mcp.json`（工作区文件）或用户 MCP 设置中：

```json
{
  "servers": {
    "mcp-geoip-server": {
      "type": "http",
      "url": "http://ip.api4claw.com/mcp"
    }
  }
}
```

## 工具

### `get_ip_geolocation`

用于查询单个 IP 地理位置信息。

**输入参数：**

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|---------|--------|
| `ip_address` | 字符串 | 是 | 要查询的 IPv4 或 IPv6 地址（例如：`8.8.8.8` 或 `2001:4860:4860::8888`） |

**输出字段：**

| 字段名 | 说明 |
|--------|---------|
| `ip` | 被查询的 IP 地址 |
| `country` | 国家名称 |
| `country_code` | ISO 国家代码（例如：`US`、`CN`） |
| `province` | 省份或州 |
| `city` | 城市名称 |
| `asn` | 自治系统编号（ASN） |
| `asn_org` | 自治系统组织名称 |

**工具的详细架构和协议说明：** [API 参考文档](./references/api.md)

## 执行流程**

1. 从用户输入中提取查询目标。
2. 将每个目标分类为 IPv4、IPv6 或域名。
3. 如果目标是域名，首先使用 [resolve script](./scripts/resolve-domain.js) 将其解析为 IP 地址。
4. 对每个 IP 地址调用 `get_ip_geolocation` 函数。
5. 返回简洁且结构化的结果。
6. 如果提供了多个 IP 地址，将结果以表格形式显示以便对比。

## 输入处理规则：

- 去除候选 IP 地址周围的空白字符和标点符号。
- 在批量查询时去除重复的 IP 地址。
- 支持 IPv4 和 IPv6 地址。
- 如果输入既不是有效的 IP 地址也无法解析为域名，则返回明确的错误信息。

## 输出格式

默认使用以下格式：

| IP 地址 | 国家 | 省份/州 | 城市 | 国家代码 | 自治系统编号（ASN） | 自治系统组织名称（ASN Org） |
|---------|---------|---------|---------|--------------|-------------------------|
| 8.8.8.8   | 美国     |       |        | US           | 15169         | Google LLC         |
|         |         |         |           |               |

如果某个字段为空，则显示 `-`。

## 错误处理：

- MCP 服务器不可用或超时：说明服务暂时出现问题，并建议用户重试。
- IP 格式无效：请求用户确认或更正 IP 地址。
- 地理位置字段为空或未知：保持响应的真实性，不要伪造数据。
- 编码异常（例如国家名称显示混乱）：同时显示 `country_code` 和原始值。
- 会话超时或会话 ID 无效：重新运行 `mcp-initialize` 以获取新的 `Mcp-Session-Id`，然后重试失败的请求。

## 从域名查询 IP 地址的流程

当用户请求某个域名的位置信息（例如 `example.com`）时：

1. 使用 [resolve script](./scripts/resolve-domain.js) 解析该域名的 A/AAAA 记录。
2. 对每个解析得到的 IP 地址调用 `get_ip_geolocation` 函数。
3. 汇总域名级别的查询结果，并列出每个 IP 地址的详细信息。

## 实现脚本：

- [invoke MCP lookup](./scripts/invoke-geoip-mcp.js)：在调用前执行初始化操作，并在会话过期时自动重新初始化。
- [resolve domain](./scripts/resolve-domain.js)：将域名解析为唯一的 A/AAAA 地址。

## 示例：单个 IP 地址

用户：`8.8.8.8 在哪里？`

调用方式：

`get_ip_geolocation({ "ip_address": "8.8.8.8" })`

**响应示例：**

```json
{
  "ip": "8.8.8.8",
  "country": "美国",
  "country_code": "US",
  "province": "",
  "city": "",
  "asn": 15169,
  "asn_org": "Google LLC"
}
```

## 示例：批量查询多个 IP 地址**

用户：`帮我查 8.8.8.8 和 1.1.1.1 的地理位置`

执行步骤：

1. 调用 `get_ip_geolocation` 查询 `8.8.8.8`。
2. 调用 `get_ip_geolocation` 查询 `1.1.1.1`。
3. 返回包含两个查询结果的合并表格。

## 成功标准：

- 每个有效的输入 IP 地址都返回一条结果记录。
- 无效的输入会明确标明错误原因。
- 不会推断或伪造任何地理信息。
- 输出结果对中文和英文用户都易于理解。