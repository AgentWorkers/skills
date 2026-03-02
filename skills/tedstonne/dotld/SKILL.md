---
name: dotld
description: >
  **搜索域名可用性和注册价格**  
  当用户提到域名（domain names）、顶级域名（TLDs）、域名注册（domain registration）或域名可用性（domain availability），或者希望查找、检查或构思域名时，可以使用该功能。该功能通过运行 `dotld` CLI 来查询 Dynadot API，以获取实时的价格和可用性信息。
version: 1.0.7
license: MIT
allowed-tools: Bash(dotld*)
metadata:
  tags: [domains, dns, dynadot]
  openclaw:
    requires:
      bins: [dotld]
      env: [DYNADOT_API_PRODUCTION_KEY]
    primaryEnv: DYNADOT_API_PRODUCTION_KEY
---
# dotld — 域名可用性及价格查询

## 安装

如果您的系统中尚未安装 `dotld`，请先进行安装：

```bash
curl -fsSL https://raw.githubusercontent.com/tedstonne/dotld/main/scripts/install.sh | bash
```

## 先决条件

使用 `dotld` 需要一个 Dynadot 的生产环境 API 密钥。密钥的获取方式如下：

1. 使用 `--dynadot-key <key>` 标志（该密钥也会自动保存到配置文件中，以便后续使用）；
2. 设置 `DYNADOT_API_PRODUCTION_KEY` 环境变量；
3. 从 `~/.config/dotld/config.json` 文件中读取已保存的密钥。

您可以在以下链接获取 API 密钥：https://www.dynadot.com/account/domain/setting/api.html

如果未找到密钥，`dotld` 会输出错误信息，并提供获取密钥的链接。

## 运行模式

### 查找特定域名

当输入的字符串包含点（.）时，`dotld` 会查询该特定域名：

```bash
dotld example.com
```

输出结果：

```
example.com · Taken
```

如果该域名可用，输出如下：

```
example.com · $9.99 · https://www.dynadot.com/domain/search?domain=example.com&rscreg=github
```

### 关键词扩展

当输入的字符串不包含点时，`dotld` 会自动查询 9 个常见的顶级域名（com、net、org、io、ai、co、app、dev、sh）：

```bash
dotld acme
```

输出结果：

```
acme
├─ acme.com · Taken
├─ acme.net · Taken
├─ acme.org · Taken
├─ acme.io  · $39.99 · https://www.dynadot.com/domain/search?domain=acme.io&rscreg=github
├─ acme.ai  · Taken
├─ acme.co  · Taken
├─ acme.app · Taken
├─ acme.dev · Taken
└─ acme.sh  · Taken
```

### 同时查询多个域名

您可以通过传递多个参数或使用 `--file` 标志来查询多个域名：

```bash
dotld acme.com startup.io mybrand

dotld --file domains.txt
```

## 输出解析

- `domain · 已注册 · 不可用`：表示该域名已被注册，无法使用；
- `domain · $39.99 · https://...`：表示该域名可用，同时提供注册价格和购买链接；
- 价格以美元（USD）显示。

## 常用标志

| 标志 | 描述 |
|------|-------------|
| `--json` | 以结构化 JSON 格式输出结果（而非表格形式） |
| `--file <path>` | 从文件中读取域名（每行一个域名） |
| `--dynadot-key <key>` | 提供 API 密钥（自动保存到配置文件） |
| `--timeout <duration>` | 设置请求超时时间（例如：5s、500ms，默认为 10s） |
| `--currency USD` | 设置价格显示的货币单位（仅支持 USD） |

## 工作流程指南

- **用户有特定域名**：直接查询该域名的可用性；
- **用户有一个品牌名称或关键词**：使用关键词进行查询；
- **用户需要获取多个域名建议**：建议尝试不同的域名组合，然后批量查询它们的可用性；
- **以排名列表形式展示结果**：按价格排序的可用域名列表，包含购买链接；建议用户下一步操作（如点击购买链接、查询其他顶级域名或尝试其他域名组合）；
- **从文件中批量查询**：当用户提供域名列表时，可以使用此方式；
- **结构化输出**：适用于需要程序化解析查询结果的情况。

## 示例

- **检查域名是否已被注册**：
  ```bash
$ dotld example.com
example.com · Taken
```

- **查询包含特定关键词的域名**：
  ```bash
$ dotld acme
acme
├─ acme.com · Taken
├─ acme.net · Taken
├─ acme.org · Taken
├─ acme.io  · $39.99 · https://www.dynadot.com/domain/search?domain=acme.io&rscreg=github
├─ acme.ai  · Taken
├─ acme.co  · Taken
├─ acme.app · Taken
├─ acme.dev · Taken
└─ acme.sh  · Taken
```

- **用于脚本的 JSON 输出**：
  ```bash
$ dotld example.com --json
{
  "results": [
    {
      "domain": "example.com",
      "available": false,
      "price": null,
      "currency": "USD",
      "buyUrl": null,
      "cached": false,
      "quotedAt": "2026-02-21T00:00:00.000Z"
    }
  ]
}
```