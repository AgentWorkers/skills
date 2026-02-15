---
name: mock-gen
description: 根据描述、类型或数据结构生成逼真的模拟数据。当需要快速获取测试数据时，可以使用这种方法。
---

# Mock Gen

每个开发者都遇到过这样的问题：需要测试数据，但最终却不得不手动编写重复的 JSON 数据，或者从 Stack Overflow 上的答案中复制数据。这款工具可以根据简单的英文描述、TypeScript 类型或 JSON 模式生成逼真的模拟数据。只需告诉它你需要什么数据、记录的数量以及数据格式，即可完成生成。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-mock-data "e-commerce users with name, email, address, and order history"
```

## 功能介绍

- 根据简单的英文描述生成逼真的模拟数据
- 支持使用 TypeScript 类型和 JSON 模式作为输入
- 输出格式可选：JSON、CSV 或 SQL 插入语句
- 记录数量可配置（默认为 10 条）
- 可使用 `--output` 标志直接将数据写入文件

## 使用示例

```bash
# Generate 10 user records as JSON
npx ai-mock-data "users with name, email, and signup date"

# Generate 50 product records as CSV
npx ai-mock-data "products with SKU, name, price, and category" -c 50 -f csv

# Generate from a TypeScript type file and save to disk
npx ai-mock-data "fill this schema" -s ./types/User.ts -o mock-users.json
```

## 最佳实践

- **描述要具体**：例如“具有真实美国地址的用户”比“用户”这样的描述更能生成准确的数据
- **使用数据模式确保一致性**：如果有 TypeScript 类型，请通过 `--schema` 参数传递，以实现字段的精确匹配
- **从小规模开始，逐步扩展**：先生成 5 条记录检查质量，再逐步增加数量
- **选择合适的格式**：CSV 适用于电子表格，SQL 适用于数据库初始化，JSON 适用于 API 模拟

## 适用场景

- 设置开发数据库时需要初始数据
- 构建前端原型时需要真实的 API 响应
- 编写测试用例时需要多样化的模拟数据
- 产品演示时需要美观的示例数据

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本完全开放，无需支付费用或注册账号，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-mock-data --help
```

## 工作原理

该工具会接收你的描述或数据模式文件，并将其传递给一个能够理解数据结构的 AI 模型。模型会根据你的要求生成真实且多样的数据记录。输出格式会根据你的选择设置为 JSON、CSV 或 SQL 插入语句。

## 许可证

MIT 许可证。永久免费使用，你可以随意使用这款工具。