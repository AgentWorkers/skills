# config-validator

这是一个用于验证 OpenClaw 配置文件（`openclaw.json`、`.env`、`package.json`）的工具，确保关键配置项存在且格式正确。

## 使用方法

```bash
node skills/config-validator/index.js [--fix]
```

## 主要功能

- 检查 `.env` 文件中是否包含所需的环境变量。
- 验证 `openclaw.json` 文件的结构是否正确。
- 核对 `package.json` 中声明的依赖项是否与实际安装的模块一致。
- 报告缺失或格式错误的配置项。
- 可选参数 `--fix` 可用于尝试进行基本的修复操作（例如，根据模板创建缺失的文件）。

## 依赖项

- 无（使用内置的 Node.js 模块）。