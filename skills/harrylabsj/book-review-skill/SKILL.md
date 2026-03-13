---
name: book-review
description: "将阅读洞察扩展为使用本地模板进行的深入分析。安全版本：无需调用外部 API、无需访问文件系统，也无需任何敏感信息（如密码）。"
---
# 书籍评论功能（安全版）

**仅使用本地模板**，将阅读笔记扩展为深入的书籍评论。

## 🔒 安全特性

- **无需外部 API 调用**：所有处理都在本地完成，数据不会发送到任何外部服务。
- **不访问文件系统**：不会读取或写入您的文件系统。
- **无需任何敏感信息**：无需 API 密钥、令牌或凭证。
- **隐私优先**：您的阅读笔记始终保留在本地环境中。

## 功能特点

- 📖 **扩展阅读笔记**：将简短的阅读笔记扩展为详细的书籍评论。
- 🔒 **本地处理**：所有模板都在本地处理，无需依赖任何外部服务。
- 📋 **多种格式选项**：提供简短、详细或全面的评论格式。
- 💡 **相关概念**：提供与该阅读笔记相关的学习建议。

## 命令行操作

- `/book-review [阅读笔记内容]`：生成详细的书籍评论。
- `/book-review-brief [阅读笔记内容]`：生成简短的书籍评论。
- `/book-review-related [阅读笔记内容]`：获取与该阅读笔记相关的学习内容。

## 使用示例

```
/book-review Today I read about deliberate practice and found it very inspiring
/book-review-brief The importance of spaced repetition in learning
/book-review-related How to build effective learning habits
```

## 技术细节

- **实现语言**：TypeScript。
- **集成工具**：OpenClaw SDK。
- **纯本地处理**：不进行网络请求，也不进行文件读写操作。
- **版本**：1.0.4（安全版本）。

## 安全保障

该功能专为解决 ClawHub 的安全问题而设计：
1. ✅ **无外部依赖**：已移除所有外部 API 调用。
2. ✅ **不访问文件系统**：不会读取用户的本地笔记或文件。
3. ✅ **无需敏感信息**：无需使用环境变量或 API 密钥。
4. ✅ **透明处理**：所有处理逻辑均可见于源代码中。

## 安装说明

```bash
clawhub install book-review-skill
```

## 系统要求

- Node.js 版本：≥ 18.0.0
- OpenClaw 版本：≥ 2026.3.0