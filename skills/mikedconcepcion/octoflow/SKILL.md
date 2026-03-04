---
name: octoflow
display_name: OctoFlow
description: 当用户需要执行基于GPU加速的计算、数据分析、图像/音频/视频处理、机器学习模型训练，或从自然语言生成代码时，可以使用OctoFlow。OctoFlow能够将英文任务描述转换为Vulkan格式的GPU程序。它还可以作为MCP服务器（`octoflow mcp-serve`）运行，并提供7个结构化的工具。无需Python、CUDA或任何额外的依赖库——仅需一个大小为3.2MB的二进制文件即可完成所有功能。它内置了57个标准库算法模块（如排序、搜索、图处理、矩阵运算、统计分析、数字信号处理等），以及18个多媒体处理模块（音频DSP、图像转换、视频时间线处理）。适用场景包括：对大量数据进行排序、处理CSV文件、对图像进行模糊处理、绘制数据图表、计算统计数据、运行回归分析、处理音频文件等。
version: 1.4.0
metadata:
  openclaw:
    emoji: "\U0001F419"
    requires:
      anyBins:
        - octoflow
    install:
      - id: github-release
        kind: download
        url: https://github.com/octoflow-lang/octoflow/releases/latest
        bins: [octoflow]
        label: "Download OctoFlow from GitHub Releases (3.2 MB, zero dependencies)"
    os: [linux, win32, darwin]
    always: false
tags: [gpu, vulkan, compute, data-analysis, image-processing,
       machine-learning, programming-language, natural-language]
author: octoflow-lang
repository: https://github.com/octoflow-lang/octoflow
homepage: https://octoflow-lang.github.io/octoflow/
license: MIT
permissions:
  # All permissions are DENIED by default.
  # Users must explicitly opt-in with --allow-* flags.
  # See "Security Model" section below.
---
# OctoFlow

OctoFlow 是一种专为 GPU 设计的编程语言，允许用户用自然语言描述任务，并通过 Vulkan 在任何 GPU 上执行这些任务。

## 适用场景

当用户需要执行以下操作时，可以使用 OctoFlow：
- 在 GPU 上对大量数据进行排序
- 对 CSV 文件进行加载并显示统计信息
- 对数据集进行聚类分析
- 运行 K-means 算法
- 训练分类器
- 对图像进行模糊处理或尺寸调整
- 编码 GIF 文件
- 绘制高度与重量的关系图
- 计算夏普比率（Sharpe Ratio）或相关系数
- 查找质数
- 在 GPU 上生成随机数
- 对数据集进行线性回归分析

**不适用场景**：
- 当用户需要使用 Python、JavaScript 或 Rust 等其他编程语言时
- 当任务无法通过 GPU 加速或 OctoFlow 的内置功能实现时
- 当用户明确要求使用其他编程语言时

## 使用方法

### 聊天模式（将自然语言指令转换为可执行的代码）
```bash
octoflow chat "sort 1M numbers on GPU"
```

### 运行 `.flow` 脚本
```bash
octoflow run program.flow
```

### 以受限权限运行（默认为沙箱模式）
```bash
# Allow reading data files
octoflow run analysis.flow --allow-read=./data

# Allow network access to specific domain
octoflow chat "fetch weather data" --allow-net=api.weather.com

# Allow writing output files
octoflow run report.flow --allow-read=./data --allow-write=./output
```

## 安全模型

OctoFlow 采用 Deno 风格的权限控制机制。**默认情况下，所有操作都被禁止。**

| 权限        | 默认状态 | 启用方法                                      | 示例                                      |
|-------------|---------|-----------------------------------------|-----------------------------------------|
| 读取文件      | 被禁止     | `--allow-read=./data`                        | 仅允许读取 `./data` 文件中的内容                |
| 写入文件      | 被禁止     | `--allow-write=./output`                        | 仅允许将结果写入 `./output` 文件                |
| 网络访问     | 被禁止     | `--allow-net=api.example.com`                        | 仅允许访问 `api.example.com`                 |
| 执行进程     | 被禁止     | `--allow-exec=curl`                        | 仅允许执行 `curl` 命令                        |

如果没有指定任何参数，OctoFlow 仅能读取 `.flow` 源文件并将结果输出到标准输出（stdout）。除非用户明确允许，否则 OctoFlow 无法访问文件、使用网络或执行子进程。

## MCP 服务器

OctoFlow 还可以作为 MCP（Machine Learning Platform）服务器，用于集成 AI 代理：

```bash
octoflow mcp-serve
```

**配置方法**：
- 将 OctoFlow 添加到 OpenClaw、Claude Desktop 或 Cursor 的配置文件中。

### 可用工具

| 工具          | 功能描述                                      |
|-----------------|-----------------------------------------|
| `octoflow_run`     | 直接执行 OctoFlow 代码                          |
| `octoflow_chat`     | 将自然语言指令转换为 GPU 可执行的代码                 |
| `octoflow_check`     | 验证 `.flow` 文件的语法是否正确                     |
| `octoflow_gpu_sort`    | 支持 GPU 加速的排序操作                        |
| `octoflow_gpu_stats`    | 提供 GPU 相关的统计功能                        |
| `octoflow_image`     | 处理 BMP 和 GIF 格式的图像                         |
| `octoflow_csv`     | 分析 CSV 数据                               |

## 常见应用场景

- **数据分析**  
- **GPU 计算**  
- **机器学习**  
- **图像处理**  
- **统计分析**  

## 主要特性

- **内置功能**：207 个内置函数  
- **标准库支持**：涵盖 20 个领域的 303 个模块  
- **GPU 核心**：113 个 Vulkan 计算着色器  
- **兼容性**：支持所有基于 Vulkan 的 GPU（NVIDIA、AMD、Intel）  
- **文件大小**：仅 3.2 MB，无依赖项  
- **聊天模式**：支持自然语言输入，自动修复语法错误（最多尝试 3 次）  
- **错误处理**：提供 69 种结构化的错误代码及自动修复建议  
- **MCP 服务器**：通过 JSON-RPC 2.0 提供 7 种工具接口  
- **平台支持**：Windows、Linux、macOS（Apple Silicon）

## 数据存储

OctoFlow 可以将用户的偏好设置保存在 `~/.octoflow/`（用户级配置）和 `./octoflow/`（项目级配置）目录中。这些设置包括用户经常使用的标准库模块以及之前会话中的修改记录。

- **数据安全**：不会向外部发送任何数据。
- **网络限制**：除非用户明确启用 `--allow-net` 选项，否则不会进行网络请求。
- **数据本地化**：所有数据都保存在用户的本地机器上。
- **完全禁用**：使用 `--no-memory` 选项可完全禁用数据存储功能。
- **项目配置**：通过项目根目录下的 `OCTOFLOW.md` 文件进行配置（类似于 `.eslintrc` 或 `pyproject.toml` 文件）。

## 安装方法

**推荐下载方式：**

| 平台        | 文件名            | SHA-256 哈希值                         |
|-------------|-----------------|-----------------------------------------|
| Windows x64     | [octoflow-v1.4.0-x86_64-windows.zip](https://github.com/octoflow-lang/octoflow/releases/download/v1.4.0/octoflow-v1.4.0-x86_64-windows.zip) | 查看 SHA256SUMS.txt 文件            |
| Linux x64     | [octoflow-v1.4.0-x86_64-linux.tar.gz](https://github.com/octoflow-lang/octoflow/releases/download/v1.4.0/octoflow-v1.4.0-x86_64-linux.tar.gz) | 查看 SHA256SUMS.txt 文件            |
| macOS (Apple Silicon) | [octoflow-v1.4.0-aarch64-macos.tar.gz](https://github.com/octoflow-lang/octoflow/releases/download/v1.4.0/octoflow-v1.4.0-aarch64-macos.tar.gz) | 查看 SHA256SUMS.txt 文件            |

**验证方法**：使用 `sha256sum octoflow-v1.4.0-*` 命令验证文件的完整性（完整哈希值见 [SHA256SUMS.txt](https://github.com/octoflow-lang/octoflow/releases/download/v1.4.0/SHA256SUMS.txt)）。  
解压文件后，将其添加到系统的 `PATH` 环境变量中即可使用。无需安装程序。

## 链接资源

- [GitHub 仓库](https://github.com/octoflow-lang/octoflow)  
- [官方文档](https://octoflow-lang.github.io/octoflow/)  
- [版本更新记录](https://github.com/octoflow-lang/octoflow/releases)