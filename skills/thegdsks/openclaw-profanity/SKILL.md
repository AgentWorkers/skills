---
name: openclaw-profanity
description: OpenClaw/Moltbot AI代理的内容审核插件。适用于构建需要过滤脏话的聊天机器人、在Discord/Slack/Telegram机器人中审核用户消息，或为OpenClaw代理添加内容审核功能的场景。
---

# OpenClaw 滥言检测插件

专为 OpenClaw 和 Moltbot AI 代理设计的滥用语言检测插件，可为您的聊天机器人提供自动化内容审核功能，支持俚语、Unicode 字符以及多语言检测。

## 安装

```bash
npm install openclaw-profanity
```

## 与 OpenClaw 配置

```javascript
import { OpenClaw } from 'openclaw';
import { profanityPlugin } from 'openclaw-profanity';

const bot = new OpenClaw({
  plugins: [
    profanityPlugin({
      action: 'warn',              // warn | censor | block | log
      detectLeetspeak: true,
      normalizeUnicode: true,
      languages: ['english'],
      customWords: [],
      ignoreWords: []
    })
  ]
});
```

## 配置选项

| 选项 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `action` | 字符串 | `'warn'` | 处理滥用语言的方式：`warn`（警告）、`censor`（审查）、`block`（屏蔽）、`log`（记录） |
| `detectLeetspeak` | 布尔值 | `true` | 检测 `f4ck`、`sh1t` 等俚语模式 |
| `normalizeUnicode` | 布尔值 | `true` | 检测类似西里尔字母的字符（如 `а` 替代 `a`） |
| `languages` | 数组 | `['english']` | 需要检查的语言 |
| `customWords` | 数组 | `[]` | 需要标记的额外词汇 |
| `ignoreWords` | 数组 | `[]` | 需要白名单的词汇 |
| `onViolation` | 函数 | - | 用于处理违规行为的自定义函数 |

## 处理方式

### `warn` - 发出警告
```javascript
profanityPlugin({ action: 'warn' })
// Bot responds: "Please keep the chat clean."
```

### `censor` - 替换内容后继续处理
```javascript
profanityPlugin({ action: 'censor', replaceWith: '***' })
// "What the ***" is processed normally
```

### `block` - 完全忽略消息
```javascript
profanityPlugin({ action: 'block' })
// Message is not processed
```

### `log` - 记录日志后继续处理
```javascript
profanityPlugin({ action: 'log' })
// Logs violation, processes normally
```

## 自定义违规处理函数

```javascript
profanityPlugin({
  action: 'custom',
  onViolation: async (message, result, context) => {
    // Track repeat offenders
    await trackViolation(message.userId, result.profaneWords);

    // Custom response
    if (getViolationCount(message.userId) > 3) {
      await banUser(message.userId);
      return { blocked: true };
    }

    return { blocked: false, warning: "First warning..." };
  }
})
```

## 平台示例

### Discord 机器人
```javascript
const bot = new OpenClaw({
  platform: 'discord',
  plugins: [
    profanityPlugin({
      action: 'censor',
      detectLeetspeak: true,
      languages: ['english', 'spanish']
    })
  ]
});
```

### Telegram 机器人
```javascript
const bot = new OpenClaw({
  platform: 'telegram',
  plugins: [
    profanityPlugin({
      action: 'warn',
      onViolation: (msg, result) => {
        return {
          reply: `Watch your language, ${msg.username}!`,
          deleteOriginal: true
        };
      }
    })
  ]
});
```

### Slack 机器人
```javascript
const bot = new OpenClaw({
  platform: 'slack',
  plugins: [
    profanityPlugin({
      action: 'log',
      onViolation: (msg, result) => {
        notifyModerators(msg.channel, msg.user, result);
      }
    })
  ]
});
```

## 检测能力

该插件能够检测以下内容：

- **直接使用的脏话**：常见的不文明用语
- **俚语**：`f4ck`、`sh1t`、`@$$`、`b1tch` 等
- **Unicode 欺骗手段**：使用西里尔字母替代普通字母（如 `а` 替代 `a`）
- **分词形式的滥用语言**：`f u c k`、`s.h.i.t`
- **混合形式的隐藏代码**：`fü©k`、`$h!t` 等

## 资源

- npm: https://www.npmjs.com/package/openclaw-profanity
- GitHub: https://github.com/GLINCKER/glin-profanity/tree/release/packages/openclaw
- 核心库文档: https://www.typeweaver.com/docs/glin-profanity