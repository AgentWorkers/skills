---
name: skill-review
version: 0.2.4
description: 从 ClawHub 上抓取所有与“Security Scan（VirusTotal/OpenClaw）”相关的技能页面信息，包括运行时要求以及用户评论。同时，还需要收集 Oliver 所有本地技能的相关数据，并将这些信息整理成一份 Markdown 格式的报告。
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

## 功能说明

- 遍历 `~/Developer/Skills` 目录下的所有技能文件（这些文件均为 `.SKILL.md` 格式）。
- 对于每个技能文件，会访问对应的 ClawHub 页面：`https://clawhub.ai/<owner>/<slug>`。
- 从该页面提取以下信息：
  - 安全扫描结果（VirusTotal 的状态及报告链接、OpenClaw 的状态/置信度/原因）
  - 运行时要求信息
  - 评论内容
- 将所有提取的信息写入 `/tmp/` 目录下的一个 Markdown 报告文件中。

## 配置要点（无需特殊设置）

- 每个技能文件中的 `SKILL.md` 文件的 `name:` 部分将被视为对应的 ClawHub 页面路径（即 **slug**）。
- 通过 `--slug-map path/to/map.json` 参数支持非标准路径映射情况。

## 使用方法

```bash
python3 scripts/skill_review.py \
  --owner odrobnik \
  --skills-dir ~/Developer/Skills \
  --out /tmp/clawhub-skill-review.md
```

### 可选：slug 映射文件

如果本地文件夹的名称与 ClawHub 的页面路径不匹配，可以提供一个映射文件来指定正确的对应关系：

```json
{
  "snapmaker": "snapmaker-2"
}
```

```bash
python3 scripts/skill_review.py --slug-map ./slug-map.json
```

## 系统要求

- 需要内部安装并使用 Playwright（一个基于 Python 的库）以及 Chromium 浏览器。

如果缺少这些依赖，请按照提示进行安装。典型的安装步骤如下：

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```