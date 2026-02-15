---
name: test-gen
description: 使用人工智能从源文件生成单元测试。在增加测试覆盖率时可以使用此方法。
---

# Test Gen

您的代码的测试覆盖率仅为12%，经理对此表示担忧。这款工具可以从您的源代码文件自动生成单元测试，覆盖正常使用场景、边界条件以及错误处理情况。这些测试真正能够检验代码的功能，而不仅仅是为了满足覆盖率的要求。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-test-gen ./src/utils.ts
```

## 功能介绍

- 为您的函数和类生成单元测试
- 覆盖正常使用场景、边界条件及错误处理情况
- 生成适用于Jest、Vitest或Mocha框架的测试用例
- 自动模拟依赖项
- 包含有意义的断言语句（而不仅仅是“expect(true).toBe(true)”）

## 使用示例

```bash
# Generate tests for a single file
npx ai-test-gen ./src/auth.ts

# Generate for all files in a directory
npx ai-test-gen ./src/services/

# Specify test framework
npx ai-test-gen ./src/utils.ts --framework vitest

# Output to a specific location
npx ai-test-gen ./src/parser.ts --output ./tests/parser.test.ts
```

## 最佳实践

- **审核生成的测试用例**：虽然AI生成的测试是一个良好的起点，但并非最终目标
- **立即运行测试**：在问题刚出现时及时发现它们
- **补充自定义的边界条件**：您比AI更了解您的代码业务逻辑
- **不要仅依赖测试覆盖率**：优秀的测试应该能验证代码的实际行为，而不仅仅是代码的行数

## 适用场景

- 继承了一个没有测试的代码库
- 快速为新功能添加测试
- 为了满足持续集成（CI）的覆盖率要求
- 了解适合您代码的测试用例应该具备哪些特点

## 属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发者工具之一。免费版本无需支付费用、无需注册账号，也无需API密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。

```bash
npx ai-test-gen --help
```

## 工作原理

该工具会解析您的源代码文件，识别出可测试的单元（函数、类、方法），分析它们的签名和实现方式，然后生成涵盖正常运行、边界条件及错误处理的测试用例。

## 许可证

采用MIT许可证，永久免费。您可以随意使用该工具。

---

**由LXGIC Studios开发**

- GitHub: [github.com/lxgicstudios/test-gen](https://github.com/lxgicstudios/test-gen)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)