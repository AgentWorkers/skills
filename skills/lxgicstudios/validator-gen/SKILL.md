---
name: validator-gen
description: 根据 TypeScript 类型生成 Zod 和 Yup 验证模式。当您需要在运行时进行与类型匹配的验证时，可以使用这些模式。
---

# Validator Gen

你的 TypeScript 类型在运行时不会被自动验证。这个工具会生成与你的现有类型相匹配的 Zod 或 Yup 模式（schema）。通过这种方式，你可以在不重复编写代码的情况下实现类型安全性和运行时验证。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-validator types.ts
```

## 它的功能

- 从 TypeScript 接口和类型生成 Zod 或 Yup 模式
- 支持嵌套对象、数组、联合类型（unions）以及可选字段
- 添加合理的约束条件（如电子邮件格式、长度限制等）
- 提供用户易于理解的错误信息
- 输出可直接使用的验证代码

## 使用示例

```bash
# Generate Zod schemas from your types
npx ai-validator src/types/user.ts

# Use Yup instead
npx ai-validator src/types/user.ts --library yup

# Include custom error messages
npx ai-validator src/types/user.ts --with-messages

# Save to file
npx ai-validator src/types/user.ts > src/validators/user.ts
```

## 最佳实践

- **将类型和验证器放在同一个文件或相邻的文件中**
- **从验证器中推断类型**：使用 `z.infer(typeof schema)` 来确保类型信息的准确性
- **手动添加自定义规则**：虽然 AI 可以处理结构，但你需要了解业务规则
- **测试边缘情况**：验证器能捕捉到更多潜在问题，请确保这符合你的需求

## 适用场景

- 构建 API 时需要请求体验证
- 需要与数据类型匹配的表单验证
- 从无验证的状态迁移到有类型验证的状态
- 不希望手动同步类型和验证器

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、注册或使用 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-validator --help
```

## 工作原理

该工具解析你的 TypeScript 源代码以提取类型定义，然后将每种类型转换为相应的 Zod 或 Yup 模式代码，并为常见的类型（如电子邮件、URL 和日期）添加相应的验证规则。同时保留原始类型的结构和可选性。

## 许可证

采用 MIT 许可证，永久免费。你可以随意使用该工具。