---
name: noticias-cangrejo
description: 从 GNews 中获取并汇总与用户提供的主题相关的最新新闻文章，然后生成一个包含日期、问候语以及热门链接的 Markdown 摘要。
homepage: https://gnews.io/
metadata: {"clawdbot":{"emoji":"🦀","requires":{"env":["GNEWS_API_KEY"]}}}
---
# NoticiasCangrejo

使用 GNews API 为任意主题生成 Markdown 新闻摘要。

## 使用场景

当用户请求关于政治、科学、创业、健康、金融、体育或本地事件等主题的最新新闻，并希望获得简洁且可链接的摘要时，可以使用此功能。

## 环境要求

在执行前需要设置以下环境变量：

- `GNEWS_API_KEY`

## 工作流程

1. 从用户处获取主题。
2. 验证 `GNEWS_API_KEY` 是否存在。
3. 使用主题和语言参数，通过 GNews 搜索 API 查询最多 20 篇文章。
4. 根据主题词与文章标题及描述之间的匹配程度来评估文章的相关性。
5. 保留排名前 15 的文章。
6. 以 Markdown 格式输出结果，包括：
   - 日期（`YYYY/MM/DD`）
   - 西班牙语问候语
   - 主题标题
   - 带有编号的文章标题和链接列表
7. （可选）使用 `--output` 参数将输出结果保存到文件中。

## 执行方式

OpenClaw 的标准执行方式在 `_meta.json` 文件的 `run` 部分有详细说明：

```bash
python3 scripts/fetch_news.py "<topic>"
```

可选参数：

- `--lang` （默认值：`en`）
- `--max-articles` （默认值：`20`）
- `--output` （用于将输出结果写入文件）

## 使用示例

```bash
export GNEWS_API_KEY="your_api_key_here"
python3 scripts/fetch_news.py "global markets" --lang en --max-articles 20 --output ./markets.md
```