---
name: opdscli
description: 使用 `opdscli` CLI 浏览、搜索和下载来自 OPDS 目录的电子书。该工具适用于添加/管理目录、搜索书籍、下载电子书或浏览最新添加的书籍。
homepage: https://github.com/rafadc/opdscli
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["opdscli"]},"install":[{"id":"brew","kind":"brew","tap":"rafadc/opdscli","formula":"opdscli","bins":["opdscli"],"label":"Install opdscli (brew)"}]}}
---
# opdscli

OPDS 是一个用于浏览目录和下载电子书的工具。请参考以下命令行接口（CLI）文档。

## 参考文档

- `references/cli-reference.md`（包含所有命令、参数及使用示例）

## 工作流程

1. 确认 CLI 是否已安装：`opdscli --version`。
2. 查看已配置的目录列表：`opdscli catalog list`。
3. 如果没有配置目录，请添加一个新的目录（具体操作请参见 `cli-reference` 文档中的认证相关说明）。
4. 如有需要，可以设置默认目录：`opdscli catalog set-default <name>`。
5. 根据需求执行搜索、浏览或下载操作。

## 常用操作模式

### 添加公共目录
```bash
opdscli catalog add gutenberg https://m.gutenberg.org/ebooks.opds/
```

### 添加需要身份验证的目录
```bash
# Basic auth (will prompt for credentials)
opdscli catalog add mylib https://my-library.example.com/opds --auth-type basic

# Bearer token
opdscli catalog add mylib https://my-library.example.com/opds --auth-type bearer
```

### 搜索并下载文件
```bash
opdscli search "don quixote"
opdscli download "Don Quixote"
opdscli download "Don Quixote" --format pdf --output ~/Books
```

### 浏览最新添加的文件
```bash
opdscli latest
opdscli latest --limit 50
```

## 使用注意事项

- 配置文件位于 `~/.config/opdscli.yaml`。请勿直接编辑该文件，应使用 `opdscli catalog` 等子命令进行操作。
- 配置文件中存储的凭据为明文形式。切勿泄露可能包含密码或访问令牌的配置信息。
- 下载文件时，请尊重用户的偏好格式和输出目录设置。
- 如果搜索结果为空，建议增加 `--depth` 参数的值或检查目录的 URL 是否正确。
- 使用 `--verbose` 选项可帮助排查连接问题；若需要静默输出结果，请使用 `--quiet` 选项。