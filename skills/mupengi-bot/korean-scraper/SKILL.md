---
name: korean-scraper
description: 一款专为韩国网站设计的爬虫工具，具备防机器人攻击功能（支持Naver、Coupang、Daum、Instagram等网站）。
version: 1.0.0
author: 무펭이 🐧
---
# korean-scraper

**韩国网站专用爬虫** — 基于Playwright框架，能够从Naver、Coupang、Daum等韩国主要网站中提取结构化数据。具备反爬虫保护功能。

## 使用场景

- 收集Naver博客的搜索结果或特定博客的文章内容
- 爬取Naver咖啡馆的热门文章/最新文章
- 收集Coupang的商品信息（价格、评论、评分）
- 提取Naver新闻/Daum新闻的文章内容
- 对韩国网站进行自动化数据采集

## 安装

```bash
cd skills/korean-scraper
npm install
npx playwright install chromium
```

## 快速入门

### Naver博客
```bash
# 검색 결과 수집
node scripts/naver-blog.js search "맛집 추천" --limit 10

# 특정 블로그 본문 추출
node scripts/naver-blog.js extract "https://blog.naver.com/..."
```

### Naver咖啡馆
```bash
# 인기글 수집
node scripts/naver-cafe.js popular "카페URL" --limit 20

# 최신글 수집
node scripts/naver-cafe.js recent "카페URL" --limit 20
```

### Coupang商品
```bash
# 상품 정보 추출
node scripts/coupang.js product "상품URL"

# 검색 결과 수집
node scripts/coupang.js search "무선 이어폰" --limit 20
```

### Naver新闻
```bash
# 검색 결과 수집
node scripts/naver-news.js search "AI" --limit 10

# 기사 본문 추출
node scripts/naver-news.js extract "https://n.news.naver.com/..."
```

### Daum新闻
```bash
# 검색 결과 수집
node scripts/daum-news.js search "경제" --limit 10

# 기사 본문 추출
node scripts/daum-news.js extract "https://v.daum.net/..."
```

## 输出格式

所有脚本均返回结构化的JSON数据：

### Naver博客搜索结果
```json
{
  "status": "success",
  "query": "맛집 추천",
  "count": 10,
  "results": [
    {
      "title": "서울 강남 맛집 추천 BEST 5",
      "url": "https://blog.naver.com/...",
      "blogger": "맛집탐험가",
      "date": "2026-02-15",
      "snippet": "강남역 근처 숨은 맛집들을..."
    }
  ]
}
```

### Naver博客文章内容
```json
{
  "status": "success",
  "url": "https://blog.naver.com/...",
  "title": "서울 강남 맛집 추천 BEST 5",
  "author": "맛집탐험가",
  "date": "2026-02-15",
  "content": "# 서울 강남 맛집 추천 BEST 5\n\n1. ...",
  "images": ["https://..."],
  "tags": ["맛집", "강남", "서울"]
}
```

### Coupang商品信息
```json
{
  "status": "success",
  "url": "https://www.coupang.com/...",
  "productName": "애플 에어팟 프로 2세대",
  "price": 299000,
  "originalPrice": 359000,
  "discount": "17%",
  "rating": 4.8,
  "reviewCount": 1523,
  "rocketDelivery": true,
  "seller": "쿠팡",
  "images": ["https://..."]
}
```

### Naver咖啡馆文章内容
```json
{
  "status": "success",
  "cafeUrl": "https://cafe.naver.com/...",
  "type": "popular",
  "count": 20,
  "posts": [
    {
      "title": "신입 회원 인사드립니다",
      "url": "https://cafe.naver.com/.../12345",
      "author": "닉네임",
      "date": "2026-02-17",
      "views": 523,
      "comments": 12
    }
  ]
}
```

### 新闻文章内容
```json
{
  "status": "success",
  "url": "https://n.news.naver.com/...",
  "title": "AI 시장 규모 급성장 전망",
  "media": "조선일보",
  "author": "홍길동 기자",
  "date": "2026-02-17 09:30",
  "content": "# AI 시장 규모 급성장 전망\n\n...",
  "category": "IT/과학",
  "images": ["https://..."]
}
```

## 反爬虫机制

- **隐藏navigator.webdriver**：避免被自动化检测工具识别
- **使用真实的User-Agent**：随机切换移动端/桌面端用户代理
- **模拟人类行为**：设置随机延迟、滚动行为
- **Stealth插件**：增强Playwright的反爬虫能力
- **绕过Cloudflare**：自动调整等待时间

## 速率限制

所有脚本均具备基本的保护机制：

- 每次请求后随机等待2-5秒
- 同一域名每秒最多请求1次
- 遇到429错误时自动重试
- 可通过`--fast`参数减少延迟（请谨慎使用）

## 错误处理

| 错误类型 | 处理方式 |
|------|------|
| 404 | 以JSON格式返回错误信息并继续执行 |
| 403/被阻止 | 重试（最多3次） |
| 超时 | 延长等待时间后重试 |
| 需要登录 | 显示警告信息并仅返回可获取的数据 |

## 环境变量

```bash
# Headless 모드 끄기 (디버깅용)
HEADLESS=false node scripts/naver-blog.js ...

# 스크린샷 저장
SCREENSHOT=true node scripts/coupang.js ...

# 대기 시간 조정 (ms)
WAIT_TIME=10000 node scripts/naver-cafe.js ...

# User-Agent 커스텀
USER_AGENT="..." node scripts/naver-news.js ...
```

## 集成示例

### 与OpenClaw Agent集成
```javascript
// 네이버 블로그 검색
const result = await exec({
  command: 'node scripts/naver-blog.js search "AI 트렌드" --limit 5',
  workdir: '/path/to/skills/korean-scraper'
});
const data = JSON.parse(result.stdout);
```

### 批量处理
```bash
# 여러 URL 일괄 처리
cat urls.txt | while read url; do
  node scripts/naver-blog.js extract "$url" >> results.jsonl
done
```

## 限制事项

- **需要登录的内容**：仅允许已登录用户进行爬取（例如部分Coupang评论）
- **动态加载内容**：默认仅支持无限滚动10条数据（可通过`--scroll`参数扩展）
- **验证码**：需要手动绕过（无法自动处理）
- **IP限制**：频繁请求可能导致暂时被屏蔽（需遵守速率限制）

## 合规性与道德规范

- ✅ 仅收集公开可获取的信息
- ✅ 遵守robots.txt规则（默认设置）
- ✅ 通过速率限制降低服务器负担
- ❌ 禁止收集个人信息
- ❌ 禁止未经授权访问需要登录的内容
- ❌ 禁止将本工具用于侵犯版权的行为

## 故障排除

### 错误：403 Forbidden
**解决方法**：
1. 尝试更换User-Agent
2. 增加等待时间（`WAIT_TIME=15000`）
3. 关闭无头模式（`HEADLESS=false`）

### 错误：返回空结果
**解决方法**：
1. 检查URL格式
2. 确认网站结构是否发生变化（可能需要更新选择器）
3. 检查是否需要登录

### 错误：超时
**解决方法**：
1. 增加`WAIT_TIME`时间
2. 检查网络连接
3. 确认是否能够正常访问网站（可能需要使用VPN）

## 维护

由于韩国网站的UI经常更新，可能需要定期更新选择器。

选择器的位置：`scripts/`目录下每个文件的顶部`SELECTORS`对象

```javascript
const SELECTORS = {
  blogTitle: '.se-title-text',
  blogContent: '.se-main-container',
  // ...
};
```

## 未来改进计划

- [ ] 支持Instagram帖子爬取
- [ ] 比较Naver商城的商品价格
- [ ] 收集YouTube韩国频道的元数据
- [ ] 优化批量处理流程（支持并行执行）
- [ ] 管理Cookie/会话（保持登录状态）
- [ ] 支持代理服务器

## 参考资料

- [Playwright官方文档](https://playwright.dev/)
- [playwright-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)
- [Naver开发者中心](https://developers.naver.com/)