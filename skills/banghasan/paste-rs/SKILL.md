---
name: paste-rs
description: 将文本、Markdown 或 HTML 代码片段粘贴到 https://paste.rs，系统会生成一个可分享的 URL。当用户请求将文本/配置片段安全地以链接形式分享，或希望快速发布命令输出（而无需发送长消息）时，可以使用此方法。
---

# paste.rs

## 快速入门（推荐方式）

使用随附的脚本（该脚本会先在本地生成一个 `.md` 文件，然后再将其上传）：

```bash
# paste from stdin
some_command | python3 skills/paste-rs/scripts/paste_rs.py

# paste a file
python3 skills/paste-rs/scripts/paste_rs.py --file ./notes.md

# paste an inline snippet
python3 skills/paste-rs/scripts/paste_rs.py --text '<h1>Hello</h1>'

# choose where the .md file is saved (default: /tmp)
python3 skills/paste-rs/scripts/paste_rs.py --outdir ./tmp-pastes --text 'hello'
```

输出结果：
- **stdout**：URL `https://paste.rs/XXXX.md`
- **stderr**：路径 `saved: /tmp/paste-rs-YYYYMMDD-HHMMSS.md`

## 使用 Curl 命令（备用方式）

```bash
# stdin
some_command | curl -fsS https://paste.rs -d @-

# file
curl -fsS https://paste.rs -d @./file.txt
```

## 安全提示

- 请将粘贴的内容视为公开内容。
- 脚本 `scripts/paste_rs.py` 默认会自动对包含敏感信息（如 token、apiKey、botToken、password、Authorization 等）的部分进行隐藏处理。
- 如果确实需要保留原始内容（不推荐这样做），请使用 `--no-redact` 选项。

## 资源

- `scripts/paste_rs.py`：用于上传文件的脚本（支持标准输入、`--text` 或 `--file` 选项）
- `references/paste-rs-api.md`：基本的 API 参考文档