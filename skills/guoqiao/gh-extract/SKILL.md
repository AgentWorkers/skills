---
name: gh-extract
description: 从 GitHub URL 中提取内容。
metadata: {"openclaw":{"always":false,"emoji":"🦞","homepage":"https://clawhub.ai/guoqiao/gh-extract","os":["darwin","linux","win32"],"requires":{"bins":["uv"]}}}
triggers:
- "/gh-extract <url>"
- "Extract content form this github url"
- "Download this github file"
---

# GitHub Extract

该功能用于从 GitHub URL 中提取内容。

当用户输入 `/gh-extract` 或请求提取/下载/汇总 GitHub URL 时，可以使用此功能。

## 功能描述
- 接受一个 GitHub URL（格式可以是 repo/tree/blob）。
- 将该 URL 转换为 GitHub 的原始 URL（raw URL）。
- 从原始 URL 中提取文件内容，或将其保存到临时路径中。

## 所需工具
- `uv`
- `wget`

## 使用方法

```bash
# print file content to stdout
uv run --script ${baseDir}/gh_extract.py <url>

# save file to a temp path, with a proper filename
uv run --script ${baseDir}/gh_extract.py <url> --save
```

## 注意事项
- 仅适用于公共仓库（public repos）。
- URL 可以是 repo/tree/blob 的形式。
- 对于 repo/tree 类型的 URL，系统会尝试获取 `README.md`、`SKILL.md` 或 `README.txt` 文件。