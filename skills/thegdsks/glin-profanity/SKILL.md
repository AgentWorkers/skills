---
name: glin-profanity
description: 这是一个用于检测脏话和进行内容审核的库，能够识别“leetspeak”（一种网络用语）、Unicode中的同形异义字符（即外观相似但含义不同的字符），并利用机器学习技术进行检测。该库适用于过滤用户生成的内容、审核评论、检查文本中的脏话、屏蔽消息，或将其功能集成到各种应用程序中。支持24种语言。
---

# Glin Profanity - 内容审核库

这是一个用于检测脏话的库，能够识别各种规避手段，如使用缩写（如 `f4ck`、`sh1t`）、Unicode 字符的伪装形式（例如模仿西里尔字母的字符），以及经过混淆的文本。

## 安装

```bash
# JavaScript/TypeScript
npm install glin-profanity

# Python
pip install glin-profanity
```

## 快速使用

### JavaScript/TypeScript

```javascript
import { checkProfanity, Filter } from 'glin-profanity';

// Simple check
const result = checkProfanity("Your text here", {
  detectLeetspeak: true,
  normalizeUnicode: true,
  languages: ['english']
});

result.containsProfanity  // boolean
result.profaneWords       // array of detected words
result.processedText      // censored version

// With Filter instance
const filter = new Filter({
  replaceWith: '***',
  detectLeetspeak: true,
  normalizeUnicode: true
});

filter.isProfane("text")           // boolean
filter.checkProfanity("text")      // full result object
```

### Python

```python
from glin_profanity import Filter

filter = Filter({
    "languages": ["english"],
    "replace_with": "***",
    "detect_leetspeak": True
})

filter.is_profane("text")           # True/False
filter.check_profanity("text")      # Full result dict
```

### React Hook

```tsx
import { useProfanityChecker } from 'glin-profanity';

function ChatInput() {
  const { result, checkText } = useProfanityChecker({
    detectLeetspeak: true
  });

  return (
    <input onChange={(e) => checkText(e.target.value)} />
  );
}
```

## 主要功能

| 功能 | 描述 |
|---------|-------------|
| 缩写检测 | 能够识别 `f4ck`、`sh1t`、`@$$` 等缩写形式 |
| Unicode 规范化 | 将西里尔字母表示的 `fսck` 自动转换为 `fuck` |
| 支持 24 种语言 | 包括阿拉伯语、中文、俄语、印地语等 |
| 上下文白名单 | 支持医疗、游戏、技术等领域 |
| 机器学习集成 | 可选集成 TensorFlow.js 进行内容毒性检测 |
| 结果缓存 | 采用 LRU 缓存机制提升性能 |

## 配置选项

```javascript
const filter = new Filter({
  languages: ['english', 'spanish'],     // Languages to check
  detectLeetspeak: true,                 // Catch f4ck, sh1t
  leetspeakLevel: 'moderate',            // basic | moderate | aggressive
  normalizeUnicode: true,                // Catch Unicode tricks
  replaceWith: '*',                      // Replacement character
  preserveFirstLetter: false,            // f*** vs ****
  customWords: ['badword'],              // Add custom words
  ignoreWords: ['hell'],                 // Whitelist words
  cacheSize: 1000                        // LRU cache entries
});
```

## 基于上下文的分析

```javascript
import { analyzeContext } from 'glin-profanity';

const result = analyzeContext("The patient has a breast tumor", {
  domain: 'medical',        // medical | gaming | technical | educational
  contextWindow: 3,         // Words around match to consider
  confidenceThreshold: 0.7  // Minimum confidence to flag
});
```

## 批量处理

```javascript
import { batchCheck } from 'glin-profanity';

const results = batchCheck([
  "Comment 1",
  "Comment 2",
  "Comment 3"
], { returnOnlyFlagged: true });
```

## 基于机器学习的检测（可选）

```javascript
import { loadToxicityModel, checkToxicity } from 'glin-profanity/ml';

await loadToxicityModel({ threshold: 0.9 });

const result = await checkToxicity("You're the worst");
// { toxic: true, categories: { toxicity: 0.92, insult: 0.87 } }
```

## 常见检测模式

### 聊天/评论审核
```javascript
const filter = new Filter({
  detectLeetspeak: true,
  normalizeUnicode: true,
  languages: ['english']
});

bot.on('message', (msg) => {
  if (filter.isProfane(msg.text)) {
    deleteMessage(msg);
    warnUser(msg.author);
  }
});
```

### 发布前的内容验证
```javascript
const result = filter.checkProfanity(userContent);

if (result.containsProfanity) {
  return {
    valid: false,
    issues: result.profaneWords,
    suggestion: result.processedText  // Censored version
  };
}
```

## 资源

- 文档：https://www.typeweaver.com/docs/glin-profanity
- 测试演示：https://www.glincker.com/tools/glin-profanity
- GitHub 仓库：https://github.com/GLINCKER/glin-profanity
- npm：https://www.npmjs.com/package/glin-profanity
- PyPI：https://pypi.org/project/glin-profanity/