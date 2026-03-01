---
name: gsc
description: 查询 Google Search Console 的 SEO 数据——包括搜索查询、热门页面、点击率（CTR）提升的机会、URL 检查以及站点地图（sitemaps）。该功能可用于分析搜索表现、寻找优化点或检查网站的索引状态。
homepage: https://developers.google.com/webmaster-tools
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires":
          {
            "anyBins": ["python3", "python"],
            "env": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"],
          },
      },
  }
---
# Google Search Console 技能

使用 Google Search Console（GSC）查询搜索分析数据、索引状态和 SEO 相关信息。

## 安全限制

- 该技能仅连接到 Google Search Console 的 API 端点。
- 该技能不会修改您的 Search Console 属性，仅执行只读查询。
- 该技能不会存储或传输超出当前会话范围的凭据。
- 使用该技能需要将 OAuth 凭据设置为环境变量。

## 设置

1. **凭据**：将 OAuth 凭据设置为环境变量（或通过 shell 加载的本地 `.env` 文件）。
2. **权限范围**：在 Google Cloud 的 OAuth 同意页面上，需要选择 `webmasters.readonly` 权限范围。
3. **访问权限**：您的 Google 账户必须具有访问 Search Console 属性的权限。

## 命令

### 列出可用网站
```bash
python scripts/gsc_query.py sites
```

### 热门搜索查询
```bash
python scripts/gsc_query.py top-queries \
  --site "https://www.nutrient.io" \
  --days 28 \
  --limit 20
```

### 流量最高的页面
```bash
python scripts/gsc_query.py top-pages \
  --site "https://www.nutrient.io" \
  --days 28 \
  --limit 20
```

### 寻找点击率低但展示次数高的页面
展示次数高但点击率低的页面意味着有优化空间：
```bash
python scripts/gsc_query.py opportunities \
  --site "https://www.nutrient.io" \
  --days 28 \
  --min-impressions 100
```

### 检查 URL 的索引状态
```bash
python scripts/gsc_query.py inspect-url \
  --site "https://www.nutrient.io" \
  --url "/sdk/web"
```

### 列出站点地图
```bash
python scripts/gsc_query.py sitemaps \
  --site "https://www.nutrient.io"
```

### 原始搜索分析数据（JSON 格式）
```bash
python scripts/gsc_query.py search-analytics \
  --site "https://www.nutrient.io" \
  --days 28 \
  --dimensions query page \
  --limit 100
```

## 可用的维度
- `query`：搜索查询
- `page`：着陆页 URL
- `country`：国家代码
- `device`：桌面设备、移动设备、平板电脑
- `date`：日期

## 返回的指标
- **clicks**：来自搜索的点击次数
- **impressions**：在搜索结果中显示的次数
- **ctr**：点击率（点击次数/展示次数）
- **position**：平均排名位置

## SEO 使用场景

1. **内容优化**：找到展示次数高但点击率低的页面，然后改进页面标题和描述。
2. **关键词研究**：查看哪些查询带来了流量，据此创建更多相关内容。
3. **技术 SEO**：检查索引状态，发现爬取问题。
4. **排名跟踪**：监控排名随时间的变化。
5. **站点地图健康检查**：验证站点地图是否已提交且没有错误。

## 注意事项

- 数据存在约 3 天的延迟（这是 Google Search Console 的限制）。
- 该技能使用的凭据也会被共享给 Google Analytics（GA4）技能。
- 检查 URL 的索引状态时，该页面必须已包含在您的 Search Console 属性中。