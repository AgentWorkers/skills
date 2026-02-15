# 社交媒体调度器

优化发布时间表以获得最大的互动效果。

## 平台

- **中国**：抖音、小红书、微信、微博、快手
- **国际**：Instagram、Twitter、Facebook、LinkedIn

## 使用方法

```bash
npx social-scheduler
```

## API

```typescript
import { getSchedule } from 'social-scheduler';

const schedule = await getSchedule({
  platform: 'xiaohongshu',
  contentType: 'product-review',
  frequency: 'daily'
});
```