---
name: clangd-lsp
description: C/C++语言服务器（clangd）为.c、.h、.cpp、.cc、.cxx、.hpp、.hxx文件提供代码智能、诊断和格式化功能。适用于需要自动完成代码、跳转到定义位置、查找引用、错误检测或重构支持的C或C++代码开发场景。
---

# clangd LSP

这是一个用于C/C++语言的代码智能服务，通过clangd（LLVM的一部分）提供全面的代码辅助功能。

## 功能

- **代码智能**：自动完成代码、跳转到函数定义、查找代码引用
- **错误检测**：实时显示编译错误
- **代码格式化**：使用clang-format进行代码格式化
- **重构**：重命名变量/函数、提取代码片段
- **支持的文件扩展名**：`.c`, `.h`, `.cpp`, `.cc`, `.cxx`, `.hpp`, `.hxx`, `.C`, `.H`

## 安装

### 使用Homebrew（macOS）
```bash
brew install llvm
# Add to PATH
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
```

### 使用包管理器（Linux）
```bash
# Ubuntu/Debian
sudo apt install clangd

# Fedora
sudo dnf install clang-tools-extra

# Arch Linux
sudo pacman -S clang
```

### Windows
```bash
winget install LLVM.LLVM
```

或者从[LLVM官方仓库](https://github.com/llvm/llvm-project/releases)下载。

安装完成后，请验证是否安装成功：
```bash
clangd --version
```

## 使用方法

该语言服务会在支持LSP的编辑器中自动运行。如需手动操作：

### 编译代码
```bash
gcc file.c -o output      # C
g++ file.cpp -o output    # C++
clang file.c -o output    # with clang
```

### 格式化代码
```bash
clang-format -i file.cpp
```

### 静态分析
```bash
clang-tidy file.cpp -- -std=c++17
```

## 配置

在项目根目录下创建`.clangd`文件（推荐方式）：
```yaml
CompileFlags:
  Add: [-std=c++17, -Wall, -Wextra]
  Remove: [-W*]
Diagnostics:
  UnusedIncludes: Strict
  MissingIncludes: Strict
```

对于复杂项目，可以使用`compile_commands.json`文件进行配置：
```bash
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON .
# or
bear -- make
```

## 集成流程

在编辑C/C++代码时：
1. clangd会读取`compile_commands.json`文件以了解项目配置
2. 使用`clang-format`对代码进行格式化
3. 使用`clang-tidy`进行静态分析
4. 使用`-Wall -Wextra`选项编译代码以启用警告提示

## 常用编译选项

- `-std=c++17`：指定使用C++17标准
- `-Wall -Wextra`：启用所有警告
- `-O2`：优化编译级别
- `-g`：生成调试符号
- `-I<path>`：指定包含文件路径
- `-L<path>`：指定库文件路径

**`clang-tidy`的检查项包括：**
```bash
clang-tidy file.cpp --checks='*' --
clang-tidy file.cpp --fix --  # Auto-fix
```

## 更多信息

- [clangd官方网站](https://clangd.llvm.org/)
- [使用指南](https://clangd.llvm.org/installation)
- [LLVM项目官网](https://llvm.org/)