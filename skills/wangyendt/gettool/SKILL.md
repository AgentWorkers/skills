---
name: pywayne-bin-gettool
description: 从 `cpp_tools` 仓库中获取并安装 C++ 工具/库。当用户需要下载或克隆第三方 C++ 库（如 eigen、opencv、pcl、fmt）时，可以使用此功能。此外，该功能还支持使用 CMake 从源代码构建工具、通过安装脚本安装工具、列出可用的工具，以及管理 `cpp_tools` 仓库的 URL。该功能会在用户请求获取、下载或安装 C++ 工具/库时被触发。
---
# Pywayne Bin Gettool

这是一个用于从 cpp_tools 仓库获取 C++ 库的工具。支持稀疏检出（sparse checkout）、可选的 CMake/make 构建过程以及安装脚本。

## 快速入门

```bash
# List all supported tools
gettool -l

# Fetch a tool to default path (based on name_to_path_map.yaml)
gettool <tool_name>

# Fetch to specific path
gettool <tool_name> -t <target_path>

# Fetch and build (if buildable)
gettool <tool_name> -b

# Fetch and install (if installable)
gettool <tool_name> -i
```

## 使用模式

### 1. 列出可用工具

当用户想要查看有哪些工具可用时：

```bash
gettool -l
```

### 2. 简单下载工具源代码

将工具源代码下载到默认路径（由当前目录下的 `name_to_path_map.yaml` 文件确定）：

```bash
gettool opencv
gettool eigen
```

### 3. 下载到指定目录

将工具下载到指定的目录：

```bash
gettool opencv -t third_party/opencv
gettool eigen -t external/eigen
```

### 4. 从源代码构建工具

使用 CMake 和 make 来构建工具。要求：
- 工具在 `name_to_path_map.yaml` 中必须标记为 `buildable: true`
- 工具必须拥有 `CMakeLists.txt` 文件
- 构建后的输出文件（`lib/` 目录）会被复制到目标目录

```bash
gettool apriltag_detection -b
gettool <tool_name> -b -t build/<tool_name>
```

### 5. 仅下载源代码和头文件目录

如果存在 `src/` 和 `include/` 目录，仅下载这两个目录：

```bash
gettool eigen -c
```

### 6. 下载并安装工具

下载完成后，执行工具的安装脚本（如果已配置的话）：

```bash
gettool pcl -i
gettool pcl -i --global-install-flag true  # Use sudo make install
```

### 7. 下载特定版本

检出特定版本/标签/分支（仅适用于子模块工具）：

```bash
gettool fmt -v 9.1.0
```

### 8. 管理仓库 URL

```bash
# Show current URL
gettool --get-url

# Set custom URL
gettool --set-url <URL>

# Reset to default URL
gettool --reset-url
```

## 命令参考

| 参数 | 描述 |
|----------|-------------|
| `<name>` 或 `-n <name>` | 从 `name_to_path_map.yaml` 中获取的工具名称 |
| `-t <path>` | 目标输出目录（默认值：根据映射结果确定） |
| `-b` / `--build` | 使用 CMake 和 make 构建工具（如果工具支持构建） |
| `-c` / `--clean` | 仅复制源代码和头文件目录 |
| `-v <version>` | 检出特定版本（仅适用于子模块工具） |
| `-i` / `--install` | 运行工具的安装脚本（如果工具支持安装） |
| `--global-install-flag` | 设置为 `true` 以使用 `sudo make install` 进行全局安装 |
| `-l` / `--list` | 列出所有支持的工具 |
| `--get-url` | 显示当前仓库的 URL |
| `--set-url <URL>` | 设置仓库的 URL |
| `--reset-url` | 将仓库 URL 重置为默认值 |

## 工具类型及行为

### 子模块工具
- 作为独立的仓库进行克隆
- 支持使用 `-v` 参数来检出特定版本
- 不通过 CMake 进行构建（如果需要，可以使用 `-b` 参数进行源代码级别的构建）

### 非子模块工具（稀疏检出）
- 通过 git 的 `sparse-checkout` 功能从 cpp_tools 仓库下载
- 可以使用 `-b` 参数进行构建（需要 `buildable: true` 和 `CMakeLists.txt` 文件）
- 构建后的输出文件（`lib/` 目录）会被复制到目标目录

## 默认路径映射

当未指定 `-t` 参数时，目标路径将根据 `name_to_path_map.yaml` 中的 `path` 字段相对于当前工作目录来确定。

示例：如果 `opencv` 在 `name_to_path_map.yaml` 中映射到 `third_party/opencv`，那么运行 `gettool opencv` 会创建 `./third_party/opencv` 目录。

## 先决条件

- Git
- CMake 和 make （用于 `-b` 参数）
- 适当的 C++ 工具链（用于构建）
- 目标目录具有写入权限

## 常见工具名称

可用的工具示例（运行 `gettool -l` 可查看完整列表）：
- `eigen` - 线性代数库
- `opencv` - 计算机视觉库
- `pcl` - 点云库
- `fmt` - 格式化库
- `apriltag_detection` - AprilTag 识别库
- `spdlog` - 快速 C++ 日志库