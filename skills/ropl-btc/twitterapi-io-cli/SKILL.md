---
name: twitterapi-io
description: 使用 twitterapi.io 获取和分页 Twitter/X 的数据。当您需要获取一条推文、用户资料、用户的最新推文、回复、引用推文、推文线程的上下文或提及信息，或者执行复杂的搜索查询时，可以使用此工具，而无需每次都手动发送原始的 API 请求。
---
# twitterapi-io

请使用已安装的 `twitterapi-io` CLI 来访问 twitterapi.io 的只读数据。

这个工具的目的是简化对 twitterapi.io 的常见读取操作，避免每次都需要重新构建自定义的 API 调用。

## 快速使用规则

- 仅将此工具用于读取操作。
- 不要自行编写用于发布、点赞、回复或删除数据的脚本。
- 默认情况下，输出格式为简洁的 JSON 数据。
- 仅在确实需要完整的 API 对象时使用 `--raw` 选项。
- 在验证 API 端点行为时，请优先参考 `references/links.md` 中提供的官方文档链接。

## 安装建议

建议使用已安装的 CLI，而不是硬编码的脚本路径。

推荐的安装方式：

```bash
pipx install git+https://github.com/ropl-btc/twitterapi-io-cli.git
```

如果在仓库中执行安装，可以使用以下命令：

```bash
pip install .
```

安装完成后，可以使用以下命令：

`twitterapi-io`

## 命令

### 显示内置帮助信息

```bash
twitterapi-io help
```

### 进行一次身份验证

```bash
twitterapi-io auth --api-key YOUR_KEY
```

您也可以通过环境变量来设置认证信息：

```bash
export TWITTERAPI_IO_KEY='YOUR_KEY'
```

### 获取一条推文

```bash
twitterapi-io tweet --url 'https://x.com/jack/status/20'
```

或：

```bash
twitterapi-io tweet --id 20
```

### 获取一个用户的信息

```bash
twitterapi-io user --username OpenAI
```

### 获取用户的最新推文

```bash
twitterapi-io user-tweets --username OpenAI --limit 10
```

**包含回复**：

```bash
twitterapi-io user-tweets --username OpenAI --limit 10 --include-replies
```

### 获取某条推文的回复

```bash
twitterapi-io replies --url 'https://x.com/jack/status/20' --limit 20
```

### 可选的 Unix 时间过滤条件

```bash
twitterapi-io replies --id 20 --since-time 1741219200 --until-time 1741305600 --limit 20
```

### 获取引用推文

```bash
twitterapi-io quotes --id 20 --limit 20
```

### 获取推文的讨论线程信息

```bash
twitterapi-io thread-context --id 20 --limit 40
```

### 获取用户的提及信息

```bash
twitterapi-io mentions --username OpenAI --limit 20
```

### 高级搜索

```bash
twitterapi-io search --query 'AI agents -filter:replies' --from-user OpenAI --within-time 24h --max-tweets 50
```

**需要时使用 `Top` 参数获取热门结果**：

```bash
twitterapi-io search --query 'AI agents' --queryType Top --max-pages 2
```

**需要时使用明确的 Unix 时间格式**：

```bash
twitterapi-io search --query '$BTC' --since-time 1741219200 --until-time 1741305600 --max-tweets 50
```

## 工作流程

1. 如果需要查看 twitterapi.io 的官方文档链接，请阅读 `references/links.md`。
2. 确保已安装 `twitterapi-io` CLI。
3. 通过 `auth` 或环境变量设置 API 密钥。
4. 根据需要使用 `tweet`、`user`、`user-tweets`、`replies`、`quotes`、`thread-context`、`mentions` 或 `search` 等命令。
5. 确保读取操作的目标明确且具有针对性。

## 预期输出

CLI 返回的格式为 JSON 数据。请对其进行解析，而不是直接获取原始文本。

默认输出格式简洁且信息量较少。只有在确实需要完整的 API 数据时才使用 `--raw` 选项。

## 相关文件

- 包存库：`https://github.com/ropl-btc/twitterapi-io-cli`
- 兼容性封装脚本：`scripts/twitterapi_io.py`
- 官方文档链接：`references/links.md`
- 配置文件：`~/.config/twitterapi-io/config.json`

## 何时停止并寻求帮助

在以下情况下，请停止操作并寻求帮助：
- 添加写入/发布功能
- 添加登录/cookie 相关的功能
- 添加大规模/高成本的爬取操作
- 修改 API 密钥的存储方式