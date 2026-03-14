---
name: multi-search-engine
description: 构建可在中文和全球搜索引擎上使用的可审计搜索URL，支持地区/语言筛选、高级搜索操作符、时间范围设置、以隐私保护为优先的搜索选项、比较模式，并且无需使用API密钥。
version: 2.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      config:
        - config.json
        - resources/engine-catalog.json
    install: []
    emoji: "🔎"
    homepage: https://clawhub.com/skills/multi-search-engine
---
# 多搜索引擎 v2.1.0

这是一个专为 OpenClaw 设计的搜索编排技能，可帮助代理**选择合适的搜索引擎、生成安全的搜索 URL、跨多个搜索引擎比较搜索结果，并解释为何选择某个特定的搜索引擎**。

此版本将该技能从一个静态的搜索引擎列表升级为一个**可重用的工具包**，具备以下功能：

- 支持搜索引擎的别名设置及地区选择功能
- 先进的搜索操作符组合（如 `site:`、`filetype:`、精确短语搜索、排除项、`OR` 等）
- 支持设置搜索操作符的时间范围
- 提供多引擎搜索结果的比较功能
- 预设了以隐私保护为优先级的搜索选项
- 提供命令行辅助脚本，支持输出 `json`、`markdown` 或纯文本格式的结果
- 为直接访问网页提供了明确的安全指导

## 适用场景

当用户需要执行以下操作时，可以使用此技能：

1. 在多个搜索引擎上搜索相同的查询内容
2. 偏重使用中国国内的搜索引擎或全球性的搜索引擎
3. 优先选择注重隐私保护的搜索引擎
4. 可靠地构建复杂的搜索操作符
5. 在打开网页之前比较不同搜索引擎的搜索覆盖范围
6. 在无需 API 密钥的情况下生成用于直接访问网页的 URL

## 推荐的工作流程

1. 明确用户的搜索目的：
   - 普通网页搜索
   - 专注于中国的搜索
   以隐私保护为优先的搜索
   搜索文档、代码、论文或文件
   计算相关内容或查询事实信息

2. 有针对性地选择搜索引擎：
   - **中国/本地网页**：百度、搜狗、360、抖音、微信
   - **全球通用搜索引擎**：谷歌、必应、Brave、雅虎
   **注重隐私保护的搜索引擎**：DuckDuckGo、Startpage、Brave、Qwant
   **知识查询/计算工具**：WolframAlpha
   **社区/专业金融领域**：Jisilu

3. 仅在确实需要的情况下使用搜索操作符来构建查询：
   - `site:` 用于限制搜索来源
   - `filetype:` 用于搜索 PDF 文件或文档
   - 使用引号进行精确短语搜索
   - 使用 `-term` 来排除不需要的内容
   - 使用 `OR` 来组合多个搜索条件

4. 对于涉及敏感信息的搜索任务，建议使用比较模式：
   - 选择一个注重隐私保护的搜索引擎
   - 选择一个主流搜索引擎
   （如适用）选择一个特定地区的搜索引擎

5. 在检查生成的 URL 后，仅打开最符合需求的结果页面。

## 命令行脚本用法

```bash
python3 scripts/build_search_urls.py --query "openclaw skills" --engine google
python3 scripts/build_search_urls.py --query "量化投资" --preset cn-research --time week --format markdown
python3 scripts/build_search_urls.py --query "react hooks" --site github.com --exact "useEffect" --compare google,ddg,brave
python3 scripts/build_search_urls.py --query "100 USD to CNY" --engine wolframalpha --format json
```

## OpenClaw 的典型使用方式

```text
User asks for recent AI papers as PDFs
→ build a Google / Brave compare query
→ add filetype:pdf and time scope
→ inspect URLs before opening pages
```

## 安全性与隐私保护

- 该技能**不需要** API 密钥。
- 该技能**不会**执行任何远程代码。
- 它仅根据本地模板生成确定的搜索 URL。
- 网络访问仅在代理明确点击生成的 URL 时才会发生。
- 搜索引擎可能会记录请求日志；在需要保护隐私的情况下，请使用相应的隐私预设设置。

## 相关文件

- `SKILL.md` — 主要说明和元数据
- `README.md` — 安装指南、使用场景、示例、常见问题解答及风险提示
- `scripts/build_search_urls.py` — 用于生成搜索 URL 和比较结果的辅助脚本
- `resources/engine-catalog.json` — 搜索引擎的详细信息（包括别名和功能）
- `resources/search-operator-cheatsheet.md` — 搜索操作符参考手册
- `examples/example-prompt.md` — 为代理提供的搜索提示模板
- `tests/smoke-test.md` — 手动测试用例
- `SELF_CHECK.md` — 自我检查及发布流程清单