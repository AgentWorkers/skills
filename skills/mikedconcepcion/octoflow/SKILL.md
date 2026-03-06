---
name: octoflow
display_name: OctoFlow
description: >
  **使用场景：**  
  当用户需要执行基于GPU加速的计算任务、分析数据、处理图像/音频/视频、训练机器学习模型，或从自然语言生成代码时，OctoFlow能够发挥作用。它通过Vulkan将用户的任务描述转换为GPU可执行的程序。OctoFlow同时也可以作为MCP服务器（`octoflow mcp-serve`）运行，并内置了7个功能丰富的工具。无需使用Python或CUDA，也无需任何额外的依赖库——仅需一个大小为4.5MB的二进制文件即可满足所有需求。它支持445个标准库模块，涵盖28个应用领域（如排序、搜索、图处理、矩阵运算、统计分析、数字信号处理、机器学习等），并配备了150个GPU计算内核。此外，OctoFlow还集成了Loom Engine GPU虚拟机技术，支持基于层流（layer-streaming）的Large Language Model（LLM）推理功能。  
  **典型应用示例：**  
  - “对一百万个数字进行排序”  
  - “对CSV文件进行数据聚类处理”  
  - “对图像进行模糊处理”  
  - “绘制数据图表”  
  - “计算统计数据”  
  - “运行回归分析”  
  - “处理音频文件”
version: 1.5.8
metadata:
  openclaw:
    emoji: "\U0001F419"
    requires:
      anyBins:
        - octoflow
    install:
      - id: github-release
        kind: download
        url: https://github.com/octoflow-lang/octoflow/releases/download/v1.5.8/
        bins: [octoflow]
        label: "Download OctoFlow v1.5.8 from GitHub Releases (4.5 MB, zero dependencies)"
    os: [linux, win32, darwin]
    always: false
tags: [gpu, vulkan, compute, data-analysis, image-processing,
       machine-learning, programming-language, natural-language,
       loom-engine, llm-inference]
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

OctoFlow是一种专为GPU设计的编程语言，允许用户用自然语言描述计算任务，并通过Vulkan技术在任意GPU上执行这些任务。

## 适用场景

**当您需要执行以下操作时，可以使用OctoFlow：**
- 在GPU上对大量数据进行排序
- 对CSV文件进行读取并展示统计信息
- 对数据集进行聚类分析（如K-means）
- 训练分类器
- 对图像进行模糊处理、调整大小或编码为GIF格式
- 绘制高度与重量的关系图
- 计算夏普比率（Sharpe Ratio）或相关性
- 查找质数
- 在GPU上生成随机数
- 对数据集进行线性回归分析
- 在GPU上运行大型语言模型（LLM）或进行推理

**不适用场景：**
- 当用户需要使用Python、JavaScript或Rust等编程语言时
- 当任务无法通过GPU加速或OctoFlow的内置功能实现时
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

OctoFlow采用类似Deno的权限控制机制。**所有操作默认都被拒绝。**

| 权限          | 默认设置 | 启用方法                                      | 示例                                      |
|------------------|-----------|---------------------------------------------|-----------------------------------------|
| 读取文件        | 拒绝        | `--allow-read=./data`                          | 仅允许读取`./data`目录中的文件                    |
| 写入文件        | 拒绝        | `--allow-write=./output`                          | 仅允许将结果写入`./output`目录                |
| 网络访问        | 拒绝        | `--allow-net=api.example.com`                          | 仅允许访问`api.example.com`域名                |
| 执行进程        | 拒绝        | `--allow-exec=curl`                          | 仅允许执行`curl`命令                        |

如果没有指定权限选项，OctoFlow仅能读取`.flow`源文件并输出到标准输出（stdout）。除非用户明确允许，否则无法访问文件、使用网络或执行子进程。

## MCP服务器

OctoFlow还可以作为MCP（Machine Learning Platform）服务器，用于集成AI代理：

```bash
octoflow mcp-serve
```

**如何将OctoFlow添加到OpenClaw、Claude Desktop或Cursor中：**
```json
{"mcpServers": {"octoflow": {"command": "octoflow", "args": ["mcp-serve"]}}}
```

### 可用工具

| 工具            | 功能描述                                      |
|------------------|---------------------------------------------|
| `octoflow_run`       | 直接执行OctoFlow代码                          |
| `octoflow_chat`       | 将自然语言指令转换为GPU可执行的代码                   |
| `octoflow_check`       | 验证`.flow`文件的语法是否正确                    |
| `octoflow_gpu_sort`      | 支持GPU加速的排序操作                        |
| `octoflow_gpu_stats`      | 提供GPU相关的统计功能                        |
| `octoflow_image`       | 处理BMP和GIF格式的图像                          |
| `octoflow_csv`       | 分析CSV文件中的数据                          |

## 常见应用场景

- **数据分析**                          |
- **GPU计算**                          |
- **机器学习**                          |
- **图像处理**                          |
- **统计分析**                          |

## 主要特性

- **内置功能**：超过210个内置函数
- **标准库支持**：涵盖28个领域的445个模块
- **GPU内核**：包含150个Vulkan计算着色器
- **GPU虚拟机**：Loom Engine支持SSBO（Shared Memory Block）技术、间接调度和层流处理
- **兼容性**：支持所有基于Vulkan的GPU（NVIDIA、AMD、Intel）
- **二进制文件大小**：仅4.5MB，无外部依赖
- **聊天模式**：支持英文输入，自动修复语法错误（最多尝试3次）
- **错误处理**：提供69种结构化的错误代码及自动修复建议
- **MCP服务器**：通过JSON-RPC 2.0提供7种工具接口
- **平台支持**：Windows、Linux、macOS（Apple Silicon）

## 数据存储

OctoFlow可选择将用户设置保存在`~/.octoflow/`（用户级）或`./octoflow/`（项目级）目录中。这些设置包括常用的标准库模块以及上一次会话中的修改内容。

- **无数据传输**：不会向外部发送任何数据。
- **无网络请求**：除非用户明确启用`--allow-net`选项。
- **数据本地化**：所有数据都存储在本地机器上。
- **完全禁用**：使用`--no-memory`选项可完全禁用数据存储功能。
- **项目配置**：通过项目根目录下的`OCTOFLOW.md`文件进行配置（类似`.eslintrc`或`pyproject.toml`文件）。

## 安装方法

**推荐下载方式：**

| 平台        | 文件名        | SHA-256哈希值                          |
|-------------|-----------------|-----------------------------------------|
| Windows x64     | [octoflow-v1.5.8-x86_64-windows.zip](https://github.com/octoflow-lang/octoflow/releases/download/v1.5.8/octoflow-v1.5.8-x86_64-windows.zip) | `2b26049565a2bfd2b1c4a1c103f2a64cd864dd14da619bd7be750ad3c6b356f2` |
| Linux x64     | [octoflow-v1.5.8-x86_64-linux.tar.gz](https://github.com/octoflow-lang/octoflow/releases/download/v1.5.8/octoflow-v1.5.8-x86_64-linux.tar.gz) | `d7306fc1f5a9a733a66ae3a4d5f3b145670efa7a079302935d867b4b75551845` |
| macOS (Apple Silicon) | [octoflow-v1.5.8-aarch64-macos.tar.gz](https://github.com/octoflow-lang/octoflow/releases/download/v1.5.8/octoflow-v1.5.8-aarch64-macos.tar.gz) | `33808c330dc5f08eb0008b52ecfb5f0ea532fb71b1c6996075c09b33dc5d8fd2` |

**验证安装包完整性：**使用`sha256sum octoflow-v1.5.8-*`命令（完整哈希值见[SHA256SUMS.txt](https://github.com/octoflow-lang/octoflow/releases/download/v1.5.8/SHA256SUMS.txt)）。**解压后直接将文件添加到系统PATH环境变量中，无需安装程序。

## 链接资源

- [GitHub仓库](https://github.com/octoflow-lang/octoflow)
- **官方文档**：[https://octoflow-lang.github.io/octoflow/]
- **版本更新**：[https://github.com/octoflow-lang/octoflow/releases]