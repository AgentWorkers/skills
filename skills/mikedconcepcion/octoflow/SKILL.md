---
name: octoflow
display_name: OctoFlow
description: 当用户需要执行由 GPU 加速的计算任务、分析数据、处理图像、训练机器学习模型或从自然语言生成代码时，可以使用 OctoFlow。OctoFlow 可以将英文任务描述转换为基于 Vulkan 的 GPU 程序，无需使用 Python 或 CUDA，也无需依赖任何其他外部库或框架。它仅提供一个大小为 3.2 MB 的二进制文件即可满足各种需求，例如：对一百万个数字进行排序、处理 CSV 文件、模糊处理图像、绘制数据图表、计算统计信息或运行回归分析等。
version: 1.2.2
metadata:
  openclaw:
    emoji: "\U0001F419"
    requires:
      anyBins:
        - octoflow
    install:
      - id: github-release
        kind: download
        url: https://github.com/octoflow-lang/octoflow/releases
        bins: [octoflow]
        label: "Download OctoFlow binary from GitHub Releases (3.2 MB)"
    os: [darwin, linux, win32]
    always: false
tags: [gpu, vulkan, compute, data-analysis, image-processing, llm,
       machine-learning, programming-language, ai, natural-language]
author: octoflow-lang
repository: https://github.com/octoflow-lang/octoflow
homepage: https://octoflow-lang.github.io/octoflow/
license: MIT
permissions:
  - file-read
  - file-write
  - network
  - process-exec
---
# OctoFlow

OctoFlow是一种专为GPU设计的编程语言，用户可以使用自然语言描述任务，然后通过Vulkan在任意GPU上执行这些任务。

## 适用场景

当用户需要执行以下操作时，可以使用OctoFlow：
- 在GPU上对大量数据进行排序
- 对CSV文件进行加载并展示统计信息
- 对数据集进行聚类分析
- 运行K-means算法
- 对图像进行模糊处理或尺寸调整
- 对GIF文件进行编码
- 绘制高度与重量的关系图
- 计算夏普比率（Sharpe Ratio）或相关系数
- 查找质数
- 在GPU上生成随机数
- 对数据集进行线性回归分析

**不适用场景**：
- 当用户需要使用Python、JavaScript或Rust等编程语言时（请使用相应的语言工具）
- 当任务无法通过GPU加速或OctoFlow的内置功能得到优化时
- 当用户明确要求使用其他编程语言时

## 使用方法

### 聊天模式（将自然语言转换为可执行的代码）
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

## 权限与安全

OctoFlow默认以沙箱模式运行：
- 禁止网络访问
- 禁止在当前工作目录（cwd）之外写入文件
- 禁止执行任何进程

**权限选项说明**：
| 标志 | 允许的操作 |
|------|---------------|
| `--allow-read=./data` | 仅允许读取`./data`目录中的文件 |
| `--allow-write=./output` | 仅允许将数据写入`./output`目录 |
| `--allow-net=api.example.com` | 仅允许访问`api.example.com`这个域名 |
| `--allow-exec=python` | 仅允许执行特定的Python命令 |

**默认情况下**，OctoFlow仅能读取`.flow`源文件并将结果输出到标准输出（stdout）。

## 常见应用场景

- **数据分析**  
- `read_csv`, `write_csv`, `json_parse`, `read_file`, `write_file`  
- **GPU计算**  
- `gpu_fill`, `gpu_add`, `gpu_matmul`, `gpu_sort`, `gpu_scale`  
- **机器学习**  
- `kmeans`, `knn_predict`, `linear_regression`, `train_test_split`  
- **图像处理**  
- `bmp_decode`, `gif_encode`, `h264_decode`, `wav_write`  
- **统计分析**  
- `mean`, `stddev`, `pearson`, `sma`, `ema`, `sharpe_ratio`  
- **媒体处理**  
- `http_get`, `http_post`, `http.listen`, `web_search`  
- **用户界面**  
- `window_open`, `plot_create`, `canvas`, `widgets`  
- **科学计算**  
- `calculus`, `interpolate`, `optimize`, `matrix`, `physics`  
- **人工智能**  
- `tokenizer`, `sampling`, `chat`, `gguf`  

**额外功能**：
- 支持加密、数据库操作、DevOps工具、终端交互、字符串处理、集合操作、编译器等功能

## 安装方法

请从[GitHub仓库](https://github.com/octoflow-lang/octoflow/releases)下载OctoFlow：
- **Windows:** `octoflow-vX.Y.Z-x86_64-windows.zip` — 解压后添加到系统路径（PATH）  
- **Linux:** `octoflow-vX.Y.Z-x86_64-linux.tar.gz` — 解压后添加到系统路径  
- **macOS:** `octoflow-vX.Y.Z-aarch64-macos.tar.gz` — 解压后添加到系统路径  

## 相关链接**

- [GitHub仓库](https://github.com/octoflow-lang/octoflow)  
- [官方文档](https://octoflow-lang.github.io/octoflow/)  
- [最新版本信息](https://github.com/octoflow-lang/octoflow/releases)