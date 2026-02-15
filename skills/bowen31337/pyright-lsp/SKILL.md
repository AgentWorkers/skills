---
name: pyright-lsp
description: Python语言服务器（Pyright）为.py和.pyi文件提供静态类型检查、代码智能提示以及LSP（Language Server Protocol）诊断功能。适用于需要类型检查、自动补全建议、错误检测或代码导航的Python代码开发场景。
---

# Pyright LSP

Pyright LSP（Language Server Protocol）是一个用于Python语言的集成插件，它通过Microsoft的Pyright工具提供静态类型检查和代码智能功能。

## 主要功能

- **类型检查**：对Python代码进行静态类型分析。
- **代码智能**：支持自动补全、跳转到函数定义、查找代码引用等功能。
- **错误检测**：实时检测类型错误和其他代码问题。
- **支持的文件扩展名**：`.py` 和 `.pyi`。

## 安装检查

在使用之前，请确认Pyright已经安装：

```bash
which pyright || npm install -g pyright
```

## 其他安装方法：

（可选的安装方式，请根据实际情况填写相应的代码块。）

## 使用方法

- 对单个Python文件进行类型检查：
  ```bash
pyright path/to/file.py
```

- 对整个项目进行类型检查：
  ```bash
cd project-root && pyright
```

## 配置

在项目根目录下创建`pyrightconfig.json`文件以自定义配置选项：

```json
{
  "include": ["src"],
  "exclude": ["**/node_modules", "**/__pycache__"],
  "typeCheckingMode": "basic",
  "pythonVersion": "3.10"
}
```

## 集成步骤

在编辑Python代码时，请按照以下步骤操作：
1. 在进行重大修改后运行Pyright。
2. 在提交代码之前解决所有类型错误。
3. 利用Pyright提供的诊断工具来提升代码质量。

## 更多信息

- [Pyright在npm上的官方页面](https://www.npmjs.com/package/pyright)
- [Pyright在PyPI上的官方页面](https://pypi.org/project/pyright/)
- [GitHub仓库](https://github.com/microsoft/pyright)