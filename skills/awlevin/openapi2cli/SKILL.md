---
name: openapi2cli
description: 根据 OpenAPI 规范生成命令行工具（CLI）。专为那些讨厌编写 `curl` 命令的 AI 代理程序设计。
homepage: https://github.com/Olafs-World/openapi2cli
metadata:
  {
    "openclaw":
      {
        "emoji": "🔧",
        "requires": { "bins": ["uvx"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "pip",
              "package": "uv",
              "bins": ["uvx"],
              "label": "Install uv (for uvx)",
            },
          ],
      },
  }
---

# 将 OpenAPI 规范转换为命令行工具（OpenAPI to CLI）

该工具能够根据 OpenAPI 或 Swagger 规范自动生成命令行工具，非常适合需要与 API 进行交互的 AI 代理，而无需手动编写 `curl` 命令。

## 快速入门

```bash
# generate a CLI from any OpenAPI spec
uvx openapi2cli generate https://api.example.com/openapi.json --output my-api

# use the generated CLI
python my-api.py users list
python my-api.py users get --id 123
python my-api.py posts create --title "Hello" --body "World"
```

## 主要特性

- **自动生成命令行工具**：支持 OpenAPI 3.x 规范
- **支持身份验证**：支持 API 密钥、Bearer 令牌以及基本身份验证（Basic Auth）
- **丰富的帮助信息**：在任何命令后加上 `--help` 可查看参数说明
- **JSON 输出**：返回结构化的响应数据，便于解析
- **试运行模式**：允许在不发送请求的情况下预览请求内容

## 使用方法

```bash
# from URL
uvx openapi2cli generate https://api.example.com/openapi.json -o my-cli

# from local file  
uvx openapi2cli generate ./spec.yaml -o my-cli

# with base URL override
uvx openapi2cli generate ./spec.json -o my-cli --base-url https://api.prod.com
```

## 生成的命令行工具示例

```bash
# set auth via env
export MY_CLI_API_KEY="sk-..."

# or via flag
python my-cli.py --api-key "sk-..." users list

# see available commands
python my-cli.py --help

# see command options
python my-cli.py users create --help
```

## 示例：GitHub API

```bash
uvx openapi2cli generate https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json -o github-cli

python github-cli.py repos list --owner octocat
```

## 为什么使用命令行工具（Why use CLI tools?）

与直接使用原始 HTTP 请求相比，命令行工具对 AI 代理更有优势：
- 可通过 `--help` 查看所有可用命令
- 支持 Tab 键补全
- 无需手动构造 JSON 请求体
- 可方便地通过管道（pipelines）进行命令链式执行

## 链接

- [PyPI 页面](https://pypi.org/project/openapi2cli/)
- [GitHub 项目页面](https://github.com/Olafs-World/openapi2cli)