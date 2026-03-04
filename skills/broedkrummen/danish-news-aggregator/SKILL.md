---
name: danish-news-aggregator
description: >
  **综合丹麦新闻RSS聚合器**  
  该工具将100多个丹麦语RSS源整合为按类别分类的统一RSS源。  
  生成6个精选的RSS源：  
  - `danish-all.xml`（排名前30的来源）  
  - `danish-national.xml`（报纸）  
  - `danish-regional.xml`（地方新闻）  
  - `danish-sports.xml`（体育新闻）  
  - `danish-business.xml`（财经新闻）  
  - `danish-tech.xml`（科技新闻）  
  - `danish-english.xml`（丹麦的英文新闻）  
  系统每15分钟自动更新内容，处理重复数据，并根据来源的权威性对新闻进行排序。
---
# 丹麦新闻聚合器技能

该工具能够将100多个丹麦语RSS源的内容聚合为按类别分类的统一RSS源。

## 快速入门

```bash
# Install dependencies
pip install feedparser python-dateutil

# Run aggregator
python3 aggregator.py

# Output feeds in output/ directory
ls output/
```

## 配置

编辑 `feeds.json` 文件以自定义要包含的RSS源：

```json
{
  "refresh_interval": 900,  // seconds (15 min)
  "max_items_per_feed": 50,
  "deduplicate": true,
  "feeds": {
    "national": ["https://..."],
    "sports": ["https://..."]
  }
}
```

## 输出的RSS源

| RSS源 | 描述 | 来源 |
|------|-------------|---------|
| `danish-all.xml` | 所有新闻的汇总 | 前30条 |
| `danish-national.xml` | DR、Berlingske、Politiken | 8个来源 |
| `danish-regional.xml` | Nordjyske、Fyens等地区性报纸 | 5个来源 |
| `danish-sports.xml` | Bold、Tipsbladet、TV2 Sport | 8个来源 |
| `danish-business.xml` | Finans、Nationalbanken | 6个来源 |
| `danish-tech.xml` | Version2、Ingeniøren | 10个来源 |
| `danish-english.xml` | The Local、CPH Post | 5个来源 |

## 主要功能

- ✅ 按类别分类的RSS源
- ✅ 去重功能（避免重复的文章）
- ✅ 来源权威性排序（DR > 主要报纸 > 地区性报纸）
- ✅ 时间过滤功能（默认显示过去24小时的内容）
- ✅ 兼容RSS 2.0标准
- ✅ 使用UTF-8编码
- ✅ 自动刷新功能（每15分钟更新一次）
- ✅ 支持图片的媒体RSS格式

## 托管方式

### 自己托管（使用Docker）

```bash
docker build -t danish-news-aggregator .
docker run -d -p 8080:8080 danish-news-aggregator
```

### 使用Cron作业进行定时更新

```bash
# Add to crontab
*/15 * * * * cd /path/to/aggregator && python3 aggregator.py
```

## 订阅方式

将以下URL添加到您的RSS阅读器中：

- https://your-domain.com/danish-all.xml
- https://your-domain.com/danish-national.xml
- https://your-domain.com/danish-regional.xml
- https://your-domain.com/danish-sports.xml
- https://your-domain.com/danish-business.xml
- https://your-domain.com/danish-tech.xml
- https://your-domain.com/danish-english.xml

## 致谢

该工具整合了以下媒体的内容：DR、Berlingske、Politiken、Information、Nordjyske、Fyens、JydskeVestkysten、Bold.dk、Tipsbladet、TV2 Sport、Finans、Nationalbanken、Version2、Ingeniøren、Computerworld、The Local Denmark、The Copenhagen Post等。

---

*丹麦新闻聚合器 v1.0 - 由Nexus Orchestrator开发*