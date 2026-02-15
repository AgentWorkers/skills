---
name: csp-gen
description: 从您的代码库中生成内容安全策略（Content Security Policy, CSP）头部信息。
---

# CSP 生成器

扫描您的应用程序，并生成合适的 Content Security Policy（内容安全策略）。避免因过于严格的规则而导致网站出现问题。

## 快速入门

```bash
npx ai-csp ./src
```

## 功能介绍

- 扫描外部资源（脚本、样式文件、图片）
- 识别需要哈希处理的内联脚本
- 生成有效的 CSP 头部信息
- 解释每一条安全策略指令

## 使用示例

```bash
# Scan and generate CSP
npx ai-csp ./public ./src

# Generate for specific strictness
npx ai-csp ./src --strict

# Output as meta tag
npx ai-csp ./src --format meta
```

## 输出格式

- HTTP 头部格式
- HTML meta 标签
- Next.js 配置文件
- Nginx 配置片段

## 系统要求

- Node.js 18.0 或更高版本
- 需要 OPENAI_API_KEY

## 许可证

MIT 许可证。永久免费使用。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-csp](https://github.com/lxgicstudios/ai-csp)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)