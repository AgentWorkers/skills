---
name: news-fetcher
description: 安装、配置、验证并运行这个用于聚合 RSS/Atom 和 HTML 新闻源的 Python CLI 工具。该工具具备去重、聚类、排名、源多样性分析以及生成摘要等功能。当需要从多个来源获取新闻、创建或验证配置文件，或解决新闻采集工具的安装问题时，可以使用该工具；同时，它还可以将新闻数据输出为 JSON、Markdown、CSV 或 RSS 格式。
---
# 新闻采集器（News Fetcher）

使用此技能来正确安装并运行 `news-fetcher`。

## 重要说明

- 安装 `ClawHub` 技能并不会自动安装 Python 包。请使用 `pip` 单独安装 Python 包。
- 请将全局配置选项放在 `run` 命令之前。

**正确示例：**
```bash
news-fetcher --config config.yaml --limit 10 run
```

**错误示例：**
```bash
news-fetcher run --config config.yaml --limit 10
```

## 最小化安装要求

以下是完成基本安装所需的步骤：
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install "git+https://github.com/miniade/news-fetcher.git@v0.1.4"
news-fetcher version
```

**预期版本：** `news-fetcher 0.1.4`

## 最小化配置要求

以下是一个简单的配置文件示例：
```bash
news-fetcher config example > config.yaml
```

**或手动创建配置文件：**
```yaml
sources:
  - name: BBC News
    url: http://feeds.bbci.co.uk/news/rss.xml
    weight: 1.0
    type: rss

  - name: Reuters Tech
    url: https://www.reutersagency.com/feed/?best-topics=tech
    weight: 1.2
    type: rss

  - name: Example HTML Source
    url: https://example.com/news
    weight: 0.9
    type: html
    selector: main article

thresholds:
  similarity: 0.8
  min_score: 0.3
  cluster_size: 2
  max_per_source: 3

weights:
  content: 0.6
  source: 0.2
  publish_time: 0.2
```

**验证配置文件：**
```bash
news-fetcher config validate config.yaml
```

## 常用命令

- 使用配置文件运行：  
  ```bash
  news-fetcher --config config_file.json
  ```
- 生成 Markdown 格式的输出：  
  ```bash
  news-fetcher --output output.md
  ```
- 按时间筛选结果：  
  ```bash
  news-fetcher --date-range "2021-01-01:2021-12-31"
  ```
- 提高评分阈值：  
  ```bash
  news-fetcher --thresholds.min_score 5
  ```
- 直接通过 CLI 覆盖数据源设置：  
  ```bash
  news-fetcher --source-url "https://example.com" --selector ".content"
  ```

## HTML 数据源

对于类型为 `html` 的数据源，如果网站没有使用标准的 `<article>` 标签结构，请手动设置 `selector` 参数：

**示例：**
```yaml
sources:
  - name: Example HTML Source
    url: https://example.com/news
    type: html
    selector: .story-card
```

## 故障排除

- 如果安装技能后 `news-fetcher` 仍然无法使用，请检查是否已正确安装 Python 包。
- 如果配置验证失败，请重新运行 `news-fetcher` 命令。
- 如果获取的结果数量过少，可以降低 `thresholds.min_score` 的值或提高 `thresholds.max_per_source` 的值。

## 参考资料

- 使用 `pip` 安装源代码：  
  ```bash
  pip install "git+https://github.com/miniade/news-fetcher.git@v0.1.4"
  ```
- （可选）PyPI 面包仓库：https://pypi.org/project/news-fetcher/
- 项目源代码地址：https://github.com/miniade/news-fetcher
- 本技能支持的版本：0.1.4