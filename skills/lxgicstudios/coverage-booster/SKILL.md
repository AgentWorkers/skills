---
name: coverage-booster
description: 查找未经过测试的代码路径，并生成相应的测试用例以提高代码覆盖率。当您的测试覆盖率过低、需要填补这些空白时，可以使用此方法。
---

# 覆盖率提升工具

你的代码覆盖率报告显示只有47%，而你的经理要求达到80%。这款工具能够识别项目中未被测试的代码路径，并自动生成缺失的测试用例。当有工具可以帮你发现这些漏洞并填补空白时，就别再手动编写重复的测试代码了。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-coverage-boost src/
```

## 功能介绍

- 扫描你的源代码文件，识别出没有测试覆盖率的函数、代码分支和代码行；
- 为这些未被覆盖的代码生成兼容Jest或Vitest的测试文件；
- 根据代码的复杂度对未测试的部分进行优先级排序，让你先修复风险最高的代码；
- 处理异常处理程序和条件分支等边缘情况；
- 生成可执行的测试文件，并确保这些测试能够通过。

## 使用示例

```bash
# Boost coverage for your whole src directory
npx ai-coverage-boost src/

# Target a specific file
npx ai-coverage-boost src/utils/parser.ts

# Scan all TypeScript files
npx ai-coverage-boost "src/**/*.ts"
```

## 最佳实践

- **先运行现有的测试**：在生成新的测试之前，先了解当前的代码覆盖率基准；
- **审查生成的测试用例**：它们是一个良好的起点，但可能需要根据你的具体环境进行调整；
- **关注业务逻辑**：不要把时间浪费在提升一些无关紧要的getter和setter方法的覆盖率上；
- **与持续集成（CI）系统集成**：设置一个覆盖率阈值，当覆盖率低于该阈值时使用这款工具。

## 适用场景

- 在添加大型功能后，代码覆盖率下降到团队设定的阈值以下；
- 继承了一个几乎没有任何测试代码的项目；
- 需要达到发布前的代码覆盖率要求；
- 希望在生产环境中出现问题之前找到那些存在风险的未测试代码。

## 作为LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多种免费开发者工具之一。免费版本无需支付费用、无需注册账号，也无需使用API密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。

```bash
npx ai-coverage-boost --help
```

## 工作原理

该工具会扫描你的源代码文件，并将其与现有的测试文件进行对比，找出测试遗漏的部分。它会识别出未被测试的函数、代码分支和错误路径，然后生成针对这些路径的测试用例。生成的测试文件兼容Jest或Vitest框架。

## 许可证

采用MIT许可证，永久免费。你可以自由使用这款工具。