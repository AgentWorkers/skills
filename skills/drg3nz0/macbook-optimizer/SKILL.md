---
name: macbook-optimizer
description: 完整的MacBook优化套件：包括监控、故障排查、系统清理以及性能调优功能。适用于所有Mac机型（Intel架构和Apple Silicon架构）。无需额外工具即可使用。
homepage: https://github.com/T4btc/macbook-optimizer
metadata:
  {
    "openclaw":
      {
        "emoji": "💻",
        "os": ["darwin"],
        "requires": { "bins": ["system_profiler", "top", "ps", "df", "du"] },
      },
  }
---

# 💻 MacBook 优化工具

**一套全面的 MacBook 健康与性能管理工具——无需安装**

这是一个功能齐全、易于使用的工具，用于监控、优化和排查 MacBook 的性能问题。它支持 **所有类型的 Mac**（无论是基于 Intel 还是 Apple Silicon 架构的），并且完全依赖于 macOS 自带的工具。与专业优化工具不同，该工具能提供具体的优化建议和自动修复方案。

## 为什么这个工具更优秀？

✅ **无需安装**：完全依赖 macOS 自带工具  
✅ **兼容所有 Mac**：无论是 Intel 还是 Apple Silicon 架构  
✅ **提供可操作的优化建议**：不仅仅是数据统计，还有具体的解决方案  
✅ **自动修复功能**：能够自动清理和优化系统  
✅ **用户友好**：使用通俗易懂的语言，避免专业术语  
✅ **功能齐全**：包括监控、故障排查和性能优化  
✅ **以图形界面为主**：为非技术用户提供直观的可视化工具  
✅ **可视化报告**：通过图表和表情符号直观展示系统状态  

## 主要功能  

### 🔍 系统监控  
- **CPU 分析**：实时显示 CPU 使用率、温度（通过 `powermetrics`）、负载情况以及各进程的详细信息  
- **内存管理**：监控 RAM 使用情况、内存压力、交换空间使用情况，并检测内存泄漏  
- **磁盘分析**：分析磁盘空间使用情况，查找大文件/文件夹，检测重复文件  
- **电池诊断**：显示电池健康状况、充电次数、容量和功耗  
- **温度监控**：监测系统温度，识别过热原因  
- **网络监控**：显示带宽使用情况、活跃连接数，以及占用大量带宽的应用程序  

### ⚡ 优化工具  
- **智能清理**：自动查找并删除缓存文件、日志文件、临时文件和重复文件  
- **进程管理**：识别占用系统资源的进程，提供优化建议，并安全地终止这些进程  
- **启动项优化**：管理登录项和后台应用程序，缩短启动时间  
- **存储优化**：查找大文件，建议删除不必要的文件，清空垃圾桶，清理缓存  
- **性能调优**：提供系统设置建议，关闭不必要的服务  

### 🛠 故障排查  
- **性能瓶颈分析**：识别性能瓶颈（CPU/内存/磁盘/网络方面）  
- **过热解决方案**：找出导致过热的进程，提供降温策略  
- **内存问题**：检测内存泄漏，建议重启相关应用程序或优化内存使用  
- **磁盘问题**：全面分析磁盘状况，解决权限问题  
- **电池问题**：评估电池健康状况，解决充电问题  

## 使用示例  

**全面系统检查（通过图形界面）：**  
```
Run a full system health check, show me the results visually, and fix any issues
```  

**性能优化（图形界面模式）：**  
```
My MacBook is slow. Open Activity Monitor and show me what's using resources
```  

**过热问题排查：**  
```
My MacBook is overheating. Show me the hot processes in Activity Monitor
```  

**磁盘清理（可视化界面）：**  
```
Show me my disk usage visually and clean up automatically
```  

**内存问题排查（图形界面）：**  
```
My Mac is using too much memory. Open Activity Monitor and highlight the memory hogs
```  

**电池健康状况检查（图形界面）：**  
```
Show me my battery health in System Settings and optimize power settings
```  

**启动项优化：**  
```
What's slowing down my Mac startup? Show me login items in System Settings
```  

**查找大文件（可视化界面）：**  
```
Find all files larger than 1GB, show them in Finder, and suggest what I can delete
```  

**以图形界面为主的工作流程：**  
```
Show me everything in Activity Monitor
Open System Settings to battery settings
Show me disk usage in a visual way
```  

## 高级命令  

该工具智能地利用了以下 macOS 工具：  

**系统信息查询：**  
- `system_profiler`：获取完整的硬件和软件信息  
- `sysctl`：系统参数和内核设置  
- `sw_vers`： macOS 版本信息  

**进程管理：**  
- `top` / `htop`：实时监控进程  
- `ps`：查看进程状态和详细信息  
- `lsof`：列出打开的文件和网络连接  
- `launchctl list`：查看后台服务和守护进程  

**资源监控：**  
- `vm_stat`：虚拟内存统计信息  
- `iostat`：磁盘 I/O 统计  
- `netstat` / `lsof -i`：网络连接信息  
- `powermetrics`：CPU/GPU 的功耗和温度（适用于 Apple Silicon 架构的 Mac）  
- `pmset -g therm`：系统温度信息（适用于 Intel Mac）  

**磁盘管理：**  
- `df`：查看磁盘空间使用情况  
- `du`：分析目录大小  
- `find`：查找大文件  
- `mdutil`：管理 Spotlight 索引  

**电源与电池管理：**  
- `pmset`：电源管理设置  
- `ioreg`：I/O 注册表（电池相关设置）  
- `system_profiler SPPowerDataType`：电池详细信息  

**清理操作：**  
- `rm`：安全删除文件（需用户确认）  
- `purge`：清除内存缓存  
- 缓存文件位置：`~/Library/Caches`、`/Library/Caches`、`/var/folders`  

**图形界面工具（可视化界面）：**  
- `open -a "Activity Monitor"`：打开活动监视器（查看 CPU、内存、电池和网络使用情况）  
- `open -a "System Settings"`：打开系统设置  
- `open -a "x-apple.systempreferences:com.apple.preference.battery"`：电池设置  
- `open -a "System Settings" && open "x-apple.systempreferences:com.apple.preference.storage"`：存储管理设置  
- `open -a "System Settings" && open "x-apple.systempreferences:com.apple.loginItems-Settings.extension"`：登录项设置  
- `open -a "Finder"`：打开 Finder 文件管理器  
- `open ~/Library/Caches`：打开缓存文件夹  
- `open ~/Downloads`：打开下载文件夹  
- `open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"`：隐私设置  
- `open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"`：辅助功能权限设置  

**可视化报告：**  
- 生成包含图表的报告（显示 CPU、内存和磁盘使用情况的变化趋势）  
- 用表情符号（🟢 表示良好状态，🟡 表示警告，🔴 表示严重问题）直观展示系统状态  
- 根据检测结果自动打开相应的系统设置面板  

## 以图形界面为主的设计  

**适合喜欢可视化界面的用户**：  
- 自动打开活动监视器以展示系统性能数据  
- 便捷地导航至系统设置中的相关面板（电池、存储、隐私设置）  
- 打开 Finder 查找特定文件夹（如缓存、下载文件或大文件）  
- 生成包含图表和图形的可视化报告  
- 在图形界面中突出显示问题，并提供详细的操作步骤  

## 智能自动化功能  

- **自动清理**：在用户确认后，自动删除不必要的缓存文件和临时文件  
- 根据系统分析提供优化建议  
- 为常见问题提供详细的操作步骤（通过图形界面引导用户完成修复）  
- 可根据用户需求持续监控系统状态（通过 cron 任务实现）  
- 生成包含图表和实用建议的可视化报告  
- 在显示系统信息时自动打开相关图形界面工具  

## 安全性与隐私保护  

- 在删除文件或终止进程前会先询问用户  
- 保护系统文件和关键进程  
- 在执行任何操作前会显示具体删除内容  
- 仅在本地运行，不收集用户数据  
- 遵守隐私政策，绝不向外传输用户数据  

## 使用要求：  
- **仅支持 macOS 系统**（Intel 或 Apple Silicon 架构）  
- **无需安装**：完全依赖 macOS 自带工具  
- **可选**：安装 `htop` 以获得更美观的进程视图（`brew install htop`）  
- **可选**：安装 `mactop` 以获取更详细的 Apple Silicon 架构相关数据（`brew install mactop`）  

## 如何使用图形界面工具  

当用户需要查看系统信息或表示自己不熟悉技术操作时：  
- 在显示 CPU/内存/进程信息时，自动打开活动监视器  
- 自动导航至相关的系统设置面板  
- 在讨论文件时，打开 Finder 查找特定文件夹  
- 生成包含表情符号的可视化报告  
- 提供详细的图形界面操作步骤  

**图形界面导航命令示例：**  
- CPU 相关问题 → 打开活动监视器并按 CPU 使用率排序  
- 内存问题 → 打开活动监视器并按内存使用情况排序  
- 电池问题 → 打开系统设置查看电池信息  
- 存储问题 → 打开系统设置中的存储设置  
- 登录项问题 → 打开系统设置中的登录项设置  
- 查找大文件 → 打开 Finder 并按文件大小排序  

**与其他工具的比较：**  
| 功能 | macbook-optimizer | mactop |  
|---------|------------------|--------|  
| 是否需要安装 | ❌ 否 | ✅ 是（需安装 htop） |  
| 是否支持 Intel Mac | ✅ 是 | ❌ 不支持（仅支持 Apple Silicon） |  
| 是否提供可操作的优化建议 | ✅ 是 | ❌ 否（仅提供数据统计） |  
| 是否具有自动清理功能 | ✅ 是 | ❌ 否 |  
| 是否具备故障排查功能 | ✅ 是 | ❌ 否 |  
| 是否用户友好 | ✅ 是 | ⚠️ 需要一定技术知识 |  
| 功能是否齐全 | ✅ 是 | ⚠️ 仅提供监控功能 |  
| 是否以图形界面为主 | ✅ 是 | ❌ 仅支持命令行界面 |  
| 是否提供可视化报告 | ✅ 是 | ❌ 仅提供文本报告 |