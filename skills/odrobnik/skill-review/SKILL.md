---
name: skill-review
version: 0.2.3
description: >
  Scrape ClawHub skill pages for Security Scan (VirusTotal/OpenClaw) + Runtime
  Requirements + Comments for all of Oliver's local skills, and write a markdown
  report.
homepage: https://github.com/odrobnik/skill-review-skill
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      bins: ["python3"]
      python: ["playwright"]
      env: ["VIRUSTOTAL_API_KEY"]
---

# 技能审核（ClawHub 安全扫描工具）

当你需要**审核 ClawHub 安全扫描结果**以评估自己的技能水平时，可以使用此工具。

## 功能介绍

- 遍历 `~/Developer/Skills` 目录下的所有技能文件（这些文件都是 `.SKILL.md` 格式）。
- 对于每个技能文件，会访问对应的 ClawHub 页面（网址格式为 `https://clawhub.ai/<owner>/<slug>`）。
- 从该页面提取以下信息：
  - 安全扫描结果（VirusTotal 的状态及报告链接、OpenClaw 的状态/置信度/原因）
  - 运行时环境要求
  - 评论信息
- 将所有提取到的信息写入 `/tmp/` 目录下的一个 Markdown 报告文件中。

## 配置要点（无需额外说明）

- 每个技能文件中的 `.SKILL.md` 文件的 `name:` 部分将被视为对应的 ClawHub 页面的 URL（即 **slug**）。
- 通过 `--slug-map path/to/map.json` 参数支持非标准的情况（即本地文件夹名称与 ClawHub 页面 URL 不匹配的情况）。

## 使用方法

```bash
python3 scripts/skill_review.py \
  --owner odrobnik \
  --skills-dir ~/Developer/Skills \
  --out /tmp/clawhub-skill-review.md
```

### 可选：slug 映射文件

如果本地文件夹的名称与 ClawHub 的 URL 不匹配，可以使用以下命令提供映射关系：

```json
{
  "snapmaker": "snapmaker-2"
}
```

```bash
python3 scripts/skill_review.py --slug-map ./slug-map.json
```

## 系统要求

- 需要安装并使用 Playwright（一个 Python 包）以及 Chromium 浏览器。

如果这些依赖项未安装，请根据错误提示进行安装。典型的安装步骤如下：

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```