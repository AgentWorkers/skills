---
name: gsc
description: 查询 Google Search Console 的 SEO 数据——包括搜索查询、热门页面、点击率（CTR）提升的机会、URL 检查以及站点地图（sitemaps）。该工具适用于分析搜索表现、寻找优化点或检查网站的索引状态。
---

# Google Search Console 技能

使用 Google Search Console（GSC）来获取搜索分析数据、索引状态以及 SEO 相关的洞察。

## 设置

1. **凭据**：使用与 GA4 技能相同的 OAuth 凭据（存储在 `.env` 文件中）。
2. **权限范围**：需要在 Google Cloud 的 OAuth 同意页面上选择 `webmasters.readonly` 权限范围。
3. **访问权限**：您的 Google 账户必须具有访问该 Search Console 资源的权限。

## 命令

### 列出可用网站
```bash
source /Users/admin/clawd/skills/gsc/.env && \
python /Users/admin/clawd/skills/gsc/scripts/gsc_query.py sites
```

### 热门搜索查询
```bash
source /Users/admin/clawd/skills/gsc/.env && \
python /Users/admin/clawd/skills/gsc/scripts/gsc_query.py top-queries \
  --site "https://www.nutrient.io" \
  --days 28 \
  --limit 20
```

### 流量最高的页面
```bash
source /Users/admin/clawd/skills/gsc/.env && \
python /Users/admin/clawd/skills/gsc/scripts/gsc_query.py top-pages \
  --site "https://www.nutrient.io" \
  --days 28 \
  --limit 20
```

### 寻找点击率低但展示次数高的页面
展示次数高但点击率低的页面意味着有优化潜力：
```bash
source /Users/admin/clawd/skills/gsc/.env && \
python /Users/admin/clawd/skills/gsc/scripts/gsc_query.py opportunities \
  --site "https://www.nutrient.io" \
  --days 28 \
  --min-impressions 100
```

### 检查 URL 的索引状态
```bash
source /Users/admin/clawd/skills/gsc/.env && \
python /Users/admin/clawd/skills/gsc/scripts/gsc_query.py inspect-url \
  --site "https://www.nutrient.io" \
  --url "/sdk/web"
```

### 列出站点地图
```bash
source /Users/admin/clawd/skills/gsc/.env && \
python /Users/admin/clawd/skills/gsc/scripts/gsc_query.py sitemaps \
  --site "https://www.nutrient.io"
```

### 原始搜索分析数据（JSON 格式）
```bash
source /Users/admin/clawd/skills/gsc/.env && \
python /Users/admin/clawd/skills/gsc/scripts/gsc_query.py search-analytics \
  --site "https://www.nutrient.io" \
  --days 28 \
  --dimensions query page \
  --limit 100
```

## 可用的维度
- `query`：搜索查询
- `page`：着陆页 URL
- `country`：国家代码
- `device`：桌面、移动设备、平板电脑
- `date`：日期

## 返回的指标
- **clicks**：来自搜索的点击次数
- **impressions**：在搜索结果中显示的次数
- **ctr**：点击率（点击次数 / 显示次数）
- **position**：平均排名位置

## SEO 应用场景

1. **内容优化**：找到展示次数高但点击率低的页面，然后优化其标题和描述。
2. **关键词研究**：了解哪些搜索查询带来了流量，据此创建更多相关内容。
3. **技术 SEO**：检查索引状态，发现爬取问题。
4. **排名监控**：随时间跟踪页面的排名变化。
5. **站点地图检查**：验证站点地图是否已正确提交且没有错误。

## 注意事项

- 数据存在约 3 天的延迟（这是 GSC 的限制）。
- 该技能使用的凭据与 GA4 技能共享。
- 检查 URL 的索引状态时，相关页面必须已添加到 Search Console 的资源列表中。