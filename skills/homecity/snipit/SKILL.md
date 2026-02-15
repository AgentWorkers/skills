---
name: snipit
description: 通过 `snipit.sh` 安全地共享代码片段和文件，采用 AES-256 加密技术。适用于需要保护代码、配置文件、日志、差异文件或敏感信息的场景，支持密码保护、读取后自动销毁数据或数据自动过期的功能。同时提供 CLI（`snipit`）和 `curl` API 两种使用方式作为备用选项。
metadata: {"openclaw":{"emoji":"📋","requires":{"anyBins":["snipit","curl"]},"install":[{"id":"npm","kind":"node","package":"snipit-sh","bins":["snipit"],"label":"Install snipit CLI (npm)"}]}}
---

# snipit.sh

这是一个用于安全共享代码片段的工具，支持使用 AES-256 对代码片段进行加密存储。

## 命令行界面（CLI）使用方法

```bash
# Install
npm install -g snipit-sh

# Create from file
snipit create server.py

# Pipe from stdin
cat code.js | snipit -l javascript

# With options
snipit create .env -t "Config" -p secret -b -e 1h

# Get snippet
snipit get abc123 -p secret
```

## 常用选项

| 选项          | 描述                                      |
|--------------|-----------------------------------------|
| `-t, --title`    | 为代码片段设置标题                          |
| `-l, --language` | 为代码片段启用语法高亮显示                    |
| `-p, --password` | 使用密码对代码片段进行加密保护                    |
| `-e, --expires` | 设置代码片段的过期时间（1小时、6小时、1天、3天、1周、2周或永不过期）       |
| `-b, --burn`    | 读取代码片段后将其永久保存到本地                  |
| `-c, --copy`    | 将代码片段的链接复制到剪贴板                        |

## API 接口（使用 curl 进行调用）

```bash
# Create
curl -X POST https://snipit.sh/api/snippets \
  -H "Content-Type: application/json" \
  -d '{"content":"code","language":"python","burnAfterRead":true}'

# Get
curl https://snipit.sh/api/snippets/{id}
```

## 常见使用场景

```bash
# Share git diff
git diff | snipit -t "Changes" -l diff

# Share logs (auto-expire 1h)
tail -100 app.log | snipit -e 1h

# Secure config (password + burn)
snipit create .env -p secret123 -b

# Build output
./build.sh 2>&1 | snipit -t "Build log"
```