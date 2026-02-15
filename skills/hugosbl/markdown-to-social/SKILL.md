# markdown-to-social

将 Markdown 文章或文本转换为适合不同社交媒体的格式化帖子。
一个内容可以生成多种格式（Twitter 线程、LinkedIn 帖子、Reddit 帖子）。

## 使用方法

```bash
python3 scripts/md2social.py convert <file.md> --platform twitter|linkedin|reddit
python3 scripts/md2social.py convert <file.md> --all
python3 scripts/md2social.py convert --text "Direct text" --platform twitter
```

## 参数选项

| 参数 | 说明 |
|------|-------------|
| `--platform` | `twitter`、`linkedin` 或 `reddit` |
| `--all` | 一次性生成所有 3 种格式 |
| `--text` | 使用直接输入的文本，而不是文件内容 |
| `--output DIR` | 将结果保存到指定目录（例如：twitter.txt、linkedin.txt、reddit.md） |
| `--json` | 以 JSON 格式输出结果 |

## 各平台规则

### Twitter
- 每条推文前加上 🧵 标识，并使用编号格式（1/N, 2/N...）
- 每条推文长度严格控制在 280 个字符以内 |
- 智能分句（避免在句子中间截断）
- 最多发布 6-8 条推文，结尾包含呼吁行动（CTA） |

### LinkedIn
- 每段内容在“查看更多”之前显示（约 1300 个字符）
- 使用表情符号和换行符来适应移动设备阅读
- 最长 3000 个字符，结尾包含 5-8 个标签
- 保持专业且吸引人的语气

### Reddit
- 标题长度不超过 300 个字符
- 文章开头添加简短总结（TL;DR）
- 完整保留 Markdown 格式的正文（包括标题、加粗内容和项目符号列表）

## 所需依赖

仅需要 Python 3.10 及以上版本的标准库。无需外部包或 API 调用。

## 示例

```bash
# Twitter thread from an article
python3 scripts/md2social.py convert article.md --platform twitter

# All platforms, saved to files
python3 scripts/md2social.py convert article.md --all --output ./social-posts

# Quick text to LinkedIn
python3 scripts/md2social.py convert --text "Big news today..." --platform linkedin

# JSON output for automation
python3 scripts/md2social.py convert article.md --all --json
```

## 文件结构

```
skills/markdown-to-social/
├── SKILL.md              # This file
└── scripts/
    └── md2social.py      # Main CLI script
```