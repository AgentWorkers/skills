---
name: instruments-profiling
description: **使用说明：**  
当使用 Instruments/xctrace 对 macOS 或 iOS 原生应用程序进行性能分析时，请参考本文档。内容涵盖正确的二进制文件选择方法、命令行参数的使用、数据导出方式，以及常见的问题与注意事项。
metadata:
  short-description: Instruments profiling for macOS/iOS apps
---

# 工具分析（macOS/iOS）

当用户需要对原生应用程序进行性能分析或堆栈追踪时，请使用此技能。
重点工具：时间分析器（Time Profiler）、`xctrace` 命令行工具（CLI），以及选择正确的二进制文件或应用程序实例。

## 快速入门（CLI）

- 列出可用模板：`xcrun xctrace list templates`
- 开始记录时间分析器数据：
  - `xcrun xctrace record --template 'Time Profiler' --time-limit 60s --output /tmp/App.trace --launch -- /path/To/App.app`
- 附加到正在运行的应用程序进行记录：
  - 先启动应用程序，获取其进程 ID（PID），然后执行：
  - `xcrun xctrace record --template 'Time Profiler' --time-limit 60s --output /tmp/App.trace --attach <pid>`
- 在 Instruments 中打开分析结果：
  - `open -a Instruments /tmp/App.trace`

**注意：** `xcrun xctrace --help` 并不是一个有效的子命令。请使用 `xcrun xctrace help record` 来查看帮助信息。

## 选择正确的二进制文件（非常重要）

**注意事项：** Instruments 可能会分析错误的应用程序（例如，`/Applications` 目录下的应用程序），因为 LaunchServices 会自动选择其他可执行的二进制文件。
请遵循以下规则：
- 使用直接的二进制文件路径以确保分析结果的准确性：
  - `xcrun xctrace record ... --launch -- /path/App.app/Contents/MacOS/App`
- 如果要分析 `.app` 文件，请确认它确实是目标应用程序：
  - `open -n /path/App.app`
- 使用 `ps -p <pid> -o comm= -o command=` 命令验证进程信息。
- 如果系统中同时存在 `/Applications/App.app` 和本地编译的版本，请明确指定使用本地版本。
- 在开始分析之前，请确认应用程序的实际运行路径。

## `xctrace` 命令参数说明

- `--template 'Time Profiler'`：从 `xctrace list templates` 中选择的模板名称。
- `--launch -- <cmd>`：`--` 后面的参数表示要分析的目标命令或应用程序路径。
- `--attach <pid|name>`：附加到正在运行的进程。
- `--output <path>`：输出文件的路径。如果省略此参数，数据将保存在当前工作目录（CWD）下。
- `--time-limit 60s|5m`：设置数据捕获的持续时间。
- `--device <name|UDID>`：针对 iOS 设备使用时必需的参数。
- `--target-stdout -`：将目标进程的标准输出（stdout）输出到终端（对 CLI 工具非常有用）。

## 导出分析结果（CLI）

- 查看分析数据表：`xcrun xctrace export --input /tmp/App.trace --toc`
- 导出原始的时间分析数据：`xcrun xctrace export --input /tmp/App.trace --xpath '/trace-toc/run[@number="1"]/data/table[@schema="time-profile"]' --output /tmp/time-profile.xml`
- 可以在脚本（Python/Rust）中进一步处理这些数据以汇总堆栈信息。

## 使用 Instruments 的用户界面流程

- 选择“时间分析器”（Time Profiler）模板。
- 使用“记录”功能来捕获应用程序中的性能瓶颈（例如启动阶段或稳定运行状态下的性能问题）。
- 使用工具中的“调用树”（Call Tree）功能：
  - 隐藏系统库相关的调用记录。
  - 反转调用顺序。
  - 按线程分离数据。
  - 关注性能瓶颈所在的代码片段及其调用次数。

## 常见问题及解决方法

- **分析错误的应用程序**：LaunchServices 可能会自动选择系统安装的应用程序而非本地编译的版本。
  - 解决方法：使用直接的二进制文件路径，或使用 `--attach` 选项并指定进程 ID。
- **没有分析数据或分析结果为空**：可能是应用程序退出得太快，或者根本没有达到运行状态。
  - 解决方法：延长数据捕获时间，或在记录过程中触发应用程序的实际工作负载。
- **隐私权限问题**：`xctrace` 需要开发者工具的权限。
  - 解决方法：进入系统设置 → 隐私与安全 → 开发者工具，允许使用终端或 Xcode。
- **分析结果文件过大**：`time-profile` 文件可能非常庞大。
  - 解决方法：使用 XPath 过滤数据，并在离线环境中进行汇总处理；避免将结果直接输出到终端。

## iOS 特定说明

- 对于 iOS 设备，使用 `xcrun xctrace list devices` 查看可用设备列表，然后使用 `--device <UDID>` 指定目标设备。
- 如需通过 Xcode 启动应用程序，可以使用 `xctrace --attach` 选项进行附加。
- 确保应用程序已启用调试符号，以便获得准确的堆栈信息。

## 验证步骤

- 确认分析过程中使用的进程路径与目标应用程序的路径一致。
- 确保分析结果中显示的是目标应用程序的堆栈信息。
- 确保捕获的数据涵盖了应用程序的瓶颈操作（如启动或更新过程）。
- 如果需要自动化比较分析结果，请将堆栈数据导出以便进一步处理。