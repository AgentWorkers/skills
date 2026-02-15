---
name: native-app-performance
description: 通过 `xctrace`/`Time Profiler` 以及仅使用命令行（CLI）来分析 `Instruments` 的跟踪数据（trace files），实现对原生 macOS/iOS 应用程序性能的监控与优化。当需要分析应用程序的性能、附加调试工具、记录运行数据或分析 `Instruments` 生成的 `.trace` 文件时，可以使用这些工具来定位性能瓶颈（hotspots），从而在不打开 `Instruments` 用户界面的情况下提升应用程序的性能。
---

# 原生应用性能分析（仅支持命令行界面）

**目标**：通过 `xctrace` 工具记录应用程序的性能数据，提取时间样本，进行符号化处理，并识别性能瓶颈，而无需打开任何调试工具。

## 快速入门（命令行界面）

1. **通过“attach”模式记录性能数据**：
   ```bash
   xcrun xctrace --attach <application_binary_path>
   ```

2. **通过“launch”模式记录性能数据**：
   ```bash
   xcrun xctrace --launch <application_binary_path>
   ```

3. **提取时间样本**：
   ```bash
   xcrun xctrace --extract-time-samples <trace_file.xml>
   ```

4. **获取符号化所需的加载地址**：
   ```bash
   xcrun xctrace --get-load-address <trace_file.xml>
   ```

5. **对性能瓶颈进行符号化处理并排序**：
   ```bash
   xcrun xctrace --symbolize <trace_file.xml> --top-hotspots
   ```

## 工作流程提示：
- 确保你正在分析正确的二进制文件（本地构建版本或 `/Applications` 目录下的版本）。使用 `--launch` 选项时，请提供二进制文件的完整路径。
- 在捕获数据期间，务必触发会导致性能下降的操作（例如打开/关闭菜单、刷新页面等）。
- 如果堆栈信息为空，建议延长捕获时间或跳过空闲的操作。
- 使用 `xcrun xctrace help record` 和 `xcrun xctrace help export` 命令可以查看正确的参数用法。

## 配置脚本：
- `scripts/record_time_profiler.sh`：用于通过“attach”或“launch”模式记录性能数据。
- `scripts/extract_time_samples.py`：用于从性能追踪文件中提取时间样本数据（XML格式）。
- `scripts/top_hotspots.py`：用于对性能瓶颈进行符号化处理并排序。

**注意事项**：
- 由于地址空间布局随机化（ASLR）的影响，你需要从 `vmmap` 中获取程序的 `__TEXT` 加载地址。
- 如果使用的是新构建的版本，请更新 `--binary` 参数的值；符号文件必须与实际运行的二进制文件匹配。
- 由于整个流程仅通过命令行界面完成，因此如果堆栈信息已经通过 `atos` 工具被符号化处理过，就无需再打开其他调试工具。