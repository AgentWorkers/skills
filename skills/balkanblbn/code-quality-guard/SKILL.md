---
name: code-quality-guard
description: 专业的部署前代码审查和质量控制机制：在正式发布新的构建版本之前，会确保所有导入的依赖项都是有效的、所有的标签（tags）都已被正确关闭（即没有未关闭的标签），并且代码逻辑遵循最佳实践。
---
# 代码质量守护者（Code Quality Guard）

更快地交付更干净的代码。永远不要让缺失的导入语句影响您的生产环境。

## 检查清单（Checklist）

1. **导入语句检查（Import Sweep）**：核对每个使用的组件是否与相应的导入语句相匹配。
2. **标签验证（Tag Verification）**：确保所有的 JSX/HTML 标签都是成对的（即有开始标签就有结束标签）。
3. **环境审计（Environment Audit）**：验证所需的环境变量和端口设置是否正确。
4. **日志审查（Log Review）**：检查代码中是否存在调试信息或敏感数据（如密码）。

## 使用方法（Usage）
将其作为预构建钩子（pre-build hook）运行，以便在开发人员发现错误之前就捕获它们。

## 安装方法（Installation）
```bash
clawhub install code-quality-guard
```