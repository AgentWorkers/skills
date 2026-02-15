---
name: rust-analyzer-lsp
description: Rust语言服务器（rust-analyzer）为`.rs`文件提供代码智能和代码分析功能。当你需要使用Rust语言进行开发时，该工具可以协助实现自动补全、跳转到函数定义、查找代码引用、检测错误以及支持代码重构等功能。
---

# rust-analyzer LSP

Rust语言服务器集成，通过rust-analyzer提供全面的代码智能支持。

## 功能

- **代码智能**：自动补全、跳转到定义、查找引用
- **错误检测**：实时诊断编译错误
- **重构**：重命名符号、提取函数/变量
- **分析**：宏展开、类型提示、内联提示
- **支持的扩展名**：`.rs`

## 安装

### 使用rustup（推荐）
```bash
rustup component add rust-analyzer
```

### 使用Homebrew（macOS）
```bash
brew install rust-analyzer
```

### 使用包管理器（Linux）
```bash
# Ubuntu/Debian
sudo apt install rust-analyzer

# Arch Linux
sudo pacman -S rust-analyzer
```

### 手动下载
从[发布页面](https://github.com/rust-lang/rust-analyzer/releases)下载预构建的二进制文件。

验证安装：
```bash
rust-analyzer --version
```

## 使用方法

该语言服务器会在支持LSP的编辑器中自动运行。如需手动操作：

### 格式化代码
```bash
cargo fmt
```

### 运行代码检查工具（linter）
```bash
cargo clippy
```

### 编译和测试
```bash
cargo build
cargo test
```

### 无需编译即可进行检查
```bash
cargo check
```

## 配置

在项目根目录下创建`.rust-analyzer.json`文件：
```json
{
  "checkOnSave": {
    "command": "clippy"
  },
  "inlayHints": {
    "typeHints": true,
    "parameterHints": true
  }
}
```

## 集成方式

在编辑Rust代码时：
1. rust-analyzer提供实时诊断功能
2. 运行`cargo fmt`来格式化代码
3. 使用`cargo clippy`进行代码检查
4. 在提交代码前运行`cargo test`进行测试

## 常见的Cargo命令

- `cargo new <name>` - 创建新项目
- `cargo build` - 编译项目
- `cargo run` - 编译并运行程序
- `cargo test` - 运行测试
- `cargo check` - 快速编译检查
- `cargo clippy` - 运行代码检查工具
- `cargo fmt` - 格式化代码
- `cargo doc --open` - 生成并打开文档

## 更多信息

- [rust-analyzer官方网站](https://rust-analyzer.github.io/)
- [GitHub仓库](https://github.com/rust-lang/rust-analyzer)
- [Rust官方文档](https://doc.rust-lang.org/)