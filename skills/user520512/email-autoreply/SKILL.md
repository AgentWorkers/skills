# 电子邮件自动回复生成器

生成具有上下文意识的电子邮件回复。

## 使用方法

```bash
npx email-autoreply
```

## API

```typescript
import { generateReply } from 'email-autoreply';

const reply = await generateReply({
  scenario: "product-inquiry",
  tone: "professional",
  originalEmail: "你们的产品多少钱？"
});
```