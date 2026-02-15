# Code Roaster

这款工具会以幽默的方式对你的代码进行“严厉”的点评，并提供实用的反馈——就像那位既风趣又专业的资深开发人员在进行代码审查一样。

## 快速开始

```bash
npx ai-roast ./your-file.js
```

## 功能介绍

- 用尖锐（但准确的）评论来分析你的代码
- 指出评论背后的实际问题
- 发现代码中的命名错误、反模式（不良编程习惯）以及令人困惑的地方
- 在点评结束后给出切实可行的改进建议
- 让代码审查过程变得既有趣又富有收获

## 使用方法

```bash
# Roast a specific file
npx ai-roast ./src/index.js

# Roast your whole src folder
npx ai-roast ./src
```

## 示例输出

```
🔥 Line 42: "password123" as a default? Bold strategy.
   FIX: Use environment variables for credentials.

💀 Line 89: A 200-line function named "doStuff"? 
   Truly a monument to ambiguity.
   FIX: Break into smaller, well-named functions.
```

## LXGIC 开发工具包的一部分

LXGIC Studios 提供的 110 多款免费开发工具之一，无需支付费用，也无需注册。

**了解更多：**
- GitHub: https://github.com/lxgic-studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 许可证

MIT 许可证。永久免费使用。