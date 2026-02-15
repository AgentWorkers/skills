# 产品描述生成器

为电子商务平台生成引人注目的产品描述。

## 支持的平台

- **中国平台**：淘宝、天猫、京东、拼多多、小红书
- **国际平台**：亚马逊、Shopify、eBay
- **社交媒体平台**：Instagram、Facebook、TikTok Shop

## 使用方式

### 交互式模式

```bash
npx product-description
```

### API模式

```typescript
import { generateProductDescription } from 'product-description';

const result = await generateProductDescription({
  product: "无线蓝牙降噪耳机",
  platform: "xiaohongshu",
  tone: "种草",
  highlights: ["-45dB降噪", "30小时续航", "HiFi音质"]
});
```

## 输入选项

| 选项 | 值 | 默认值 | 说明 |
|--------|--------|---------|-------------|
| product | string | 必填 | 产品名称 |
| platform | taobao/tmall/jd/xiaohongshu/amazon/shopify | xiaohongshu | 目标平台 |
| tone | promotional/emotional/humor/professional | promotional | 文章风格（促销/情感化/幽默/专业） |
| highlights | string[] | [] | 产品的主要特点 |

## 输出格式

```typescript
{
  title: "种草标题",
  description: "产品描述正文",
  sellingPoints: ["卖点1", "卖点2"],
  tags: ["#标签1", "#标签2"]
}
```