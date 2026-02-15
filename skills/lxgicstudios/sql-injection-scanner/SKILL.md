---
name: sql-injection-scanner
description: 检测代码库中的 SQL 注入漏洞。当您需要在数据库查询被利用之前发现不安全的查询时，请使用此工具。
---

# SQL注入扫描器

SQL注入攻击已经存在了几十年，至今仍位列OWASP十大安全威胁之中。该工具会扫描您的后端代码，检测其中是否存在不安全的SQL查询构造、字符串拼接以及未使用参数化查询的情况。它会发现这些安全漏洞，并为您提供修复建议。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-sql-check src/
```

## 功能介绍

- 扫描代码库中的SQL注入漏洞模式
- 检测SQL查询中的字符串拼接行为
- 查找未使用的参数化查询
- 识别不安全的ORM（对象关系映射）用法及原始查询调用
- 生成修复建议，提供正确的参数化查询版本

## 使用示例

```bash
# Scan your entire backend
npx ai-sql-check src/

# Check a specific API route
npx ai-sql-check src/routes/users.ts

# Scan all database related files
npx ai-sql-check "src/**/*.{ts,js}"
```

## 最佳实践

- **始终使用参数化查询**：即使您认为输入是安全的，SQL中的字符串拼接也是不可取的。
- **检查ORM中的原始查询调用**：ORM通常较为安全，但某些原始查询方法可能会绕过安全防护机制。
- **在每次发布前进行扫描**：新代码可能带来新的安全风险。
- **不要仅依赖输入验证**：参数化查询才是真正的防护措施；验证只是辅助手段。

## 适用场景

- 在安全审计或渗透测试之前
- 在向后端添加新的数据库查询时
- 在处理具有未知安全状况的旧代码库时
- 作为持续集成（CI）安全流程的一部分

## 该工具属于LXGIC开发工具包

这是LXGIC Studios开发的110多个免费开发者工具之一。免费版本无需支付费用、无需注册，也无需使用API密钥。这些工具都能正常使用。

**了解更多：**
- GitHub：https://github.com/LXGIC-Studios
- Twitter：https://x.com/lxgicstudios
- Substack：https://lxgicstudios.substack.com
- 官网：https://lxgic.dev

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。

```bash
npx ai-sql-check --help
```

## 工作原理

该工具会扫描您的源代码中的SQL查询模式，并分析用户输入如何被传递到数据库调用中。它通过模式匹配和人工智能分析来检测字符串拼接、查询中的模板字面量以及不安全的ORM使用情况。每个检测结果都会包含漏洞的严重程度、受影响的代码以及相应的参数化查询修复方案。

## 许可证

MIT许可证。永久免费使用，您可以随意使用该工具。