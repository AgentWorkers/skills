# XSS扫描器

在您的前端代码发布之前，检测其中的跨站脚本（XSS）漏洞。

## 快速入门

```bash
npx ai-xss-check
```

## 功能介绍

- 扫描JavaScript/TypeScript代码中的XSS漏洞
- 检测不安全的内联HTML（innerHTML）、`eval`语句以及DOM操作
- 识别模板中的未转义用户输入
- 检查React中的`dangerouslySetInnerHTML`用法
- 为每个发现的漏洞提供修复建议

## 使用方法

```bash
# Scan current directory
npx ai-xss-check

# Scan specific files
npx ai-xss-check ./src/components
```

## 适用场景

- 在进行安全审计之前
- 审查第三方代码时
- 设置持续集成（CI）的安全检查机制
- 培训初级开发人员了解XSS防护知识

## LXGIC开发工具包的一部分

LXGIC Studios提供的110多种免费开发工具之一。无需付费，也无需注册。

**了解更多：**
- GitHub: https://github.com/lxgic-studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 许可证

MIT许可证。永久免费使用。