---
name: Android Studio
slug: android-studio
version: 1.0.0
homepage: https://clawic.com/skills/android-studio
description: 熟练掌握 Android Studio 集成开发环境（IDE），掌握调试、性能分析、代码重构以及提高开发效率的各种快捷方式。
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
changelog: Initial release with IDE workflows, debugging, profiling, and shortcuts.
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南。

## 使用场景

用户使用 Android Studio IDE。该插件可帮助用户使用调试工具、性能分析工具、布局检查器、代码导航功能、代码重构功能以及快捷键。

## 架构

插件相关数据存储在 `~/android-studio/` 目录下。具体目录结构请参阅 `memory-template.md`。

```
~/android-studio/
├── memory.md      # Preferences and project context
└── shortcuts.md   # Custom shortcuts learned
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存管理模板 | `memory-template.md` |
| 快捷键 | `shortcuts.md` |
| 调试 | `debugging.md` |

## 核心规则

### 1. 首先检查 IDE 版本
在推荐任何功能之前，请确认 Android Studio 的版本。不同版本（如 Arctic Fox、Bumblebee、Flamingo、Hedgehog 及更高版本）之间的功能可能存在显著差异。

### 2. 平台特定的快捷键
| 操作 | macOS | Windows/Linux |
|--------|-------|---------------|
| 全局搜索 | 双击 Shift | 双击 Shift |
| 查找操作 | Cmd+Shift+A | Ctrl+Shift+A |
| 最近使用的文件 | Cmd+E | Ctrl+E |
| 导航到类 | Cmd+O | Ctrl+N |
| 导航到文件 | Cmd+Shift+O | Ctrl+Shift+N |
| 重构当前文件 | Ctrl+T | Ctrl+Alt+Shift+T |
| 运行 | Ctrl+R | Shift+F10 |
| 调试 | Ctrl+D | Shift+F9 |

### 3. 使用 IDE 内置工具而非手动检查
- 对于 UI 问题，使用布局检查器而非打印输出进行调试。
- 对于性能分析，使用性能分析工具而非手动计时。
- 对于数据库操作，使用数据库检查器而非手动查询。
- 对于网络请求，使用网络检查器而非日志记录。

### 4. 利用代码生成功能
- 使用代码模板快速生成常见代码结构（例如通过输入缩写后按 Tab 键）。
- 使用文件模板创建新组件。
- 通过 Cmd/Alt+N 快捷键生成构造函数、getter 和 setter 方法。

### 5. 调试策略
1. 使用带条件的断点进行精准调试。
2. 使用 Alt+F8 查看运行时表达式的值。
3. 使用“监视”功能跟踪不同帧中的变量。
4. 通过帧视图导航调用栈。

## 调试常见陷阱
- 在循环中设置断点可能导致 IDE 停滞。请使用条件断点。
- 调试发布版本的应用程序时可能会缺少符号文件。请使用调试版本进行调试。
- 忽略 Logcat 的过滤设置可能导致日志信息过多。请按应用包或标签过滤日志。
- 未使用“附加调试器”功能可能导致应用程序无法启动。请附加到正在运行的进程进行调试。

## 性能分析常见陷阱
- 使用调试版本进行性能分析可能会得到误导性的结果。请使用发布版本进行分析。
- 不使用过滤条件进行 CPU 分析会导致数据量过大。请专注于特定方法进行分析。
- 在垃圾回收（GC）期间使用内存分析器可能会导致结果失真。请先触发垃圾回收。
- 忽略网络分析器可能会导致慢速 API 调用被忽略。请务必检查网络请求的耗时情况。

## IDE 的核心功能

### 布局检查器
- 可实时查看运行中应用程序的视图层次结构。
- 支持 3D 模式以显示层次深度。
- 提供属性检查功能，便于调试相关问题。
- 与 Compose 和 View 系统兼容。

### 数据库检查器
- 可实时查询 Room 数据库。
- 可直接编辑数据库中的值以进行测试。
- 可导出数据以供分析。
- 需要设备支持 Android API 26 及更高版本。

### 网络分析器
- 无需修改代码即可查看 OkHttp/Retrofit 的请求和响应内容。
- 可查看请求和响应的详细信息。
- 提供时间线功能，便于识别耗时的网络请求。
- 需要在应用的 `manifest` 文件中启用该功能（仅适用于发布版本）。

### 应用程序分析功能
- 可同时查看数据库、网络请求和后台任务的状态。
- 可监控 WorkManager 中的任务。
- 可检查后台任务的调度情况。

### 性能分析工具
| 工具 | 使用场景 |
|------|----------|
| CPU 分析器 | 分析方法执行时间、线程状态 |
| 内存分析器 | 检测内存泄漏、分配情况 |
| 能源分析器 | 分析电池使用情况 |
| 网络分析器 | 分析网络请求的耗时和数据大小 |

## 代码重构快捷键

| 重构操作 | macOS | Windows/Linux |
|-------------|-------|---------------|
| 重命名 | Shift+F6 | Shift+F6 |
| 提取方法 | Cmd+Alt+M | Ctrl+Alt+M |
| 提取变量 | Cmd+Alt+V | Ctrl+Alt+V |
| 提取常量 | Cmd+Alt+C | Ctrl+Alt+C |
| 内联代码 | Cmd+Alt+N | Ctrl+Alt+N |
| 移动代码 | F6 | F6 |
| 修改方法签名 | Cmd+F6 | Ctrl+F6 |

## 构建配置

### Gradle 同步问题
- 如遇到持续性问题，请尝试清除缓存并重启 Gradle。
- 最后手段：删除 `.gradle` 和 `.idea` 文件夹。
- 在设置中的“Gradle”选项卡下检查 Gradle 和 JDK 的版本。

### 构建变体
- 在“Build Variants”面板中选择不同的构建变体。
- 调试版本和发布版本会影响调试功能。
- 不同的构建变体适用于不同的应用程序配置。

### SDK 管理器
- 通过“Tools” → “SDK Manager”更新 Android SDK。
- 安装与目标设备匹配的平台工具。
- 确保构建工具始终保持最新状态，以获取最新功能。

## 模拟器使用技巧
- 使用“Quick Boot”模式可加快启动速度。
- 通过扩展控制栏（三个点）可查看传感器、位置和电池信息。
- 可创建快照以保存特定设备的状态。
- 可通过“Device Mirroring”功能模拟真实设备。

## 推荐插件

| 插件 | 功能 |
|--------|---------|
| Key Promoter X | 学习快捷键 |
| Rainbow Brackets | 括号匹配辅助工具 |
| ADB Idea | 快速执行 ADB 命令 |
| JSON To Kotlin Class | 将 JSON 数据转换为 Kotlin 类 |
| Compose Color Preview | 颜色可视化工具 |

## 相关技能
如果用户需要，可以使用以下命令安装相关插件：
- `clawhub install android`：学习 Android 开发技巧
- `clawhub install kotlin`：学习 Kotlin 语言特性
- `clawhub install java`：学习 Java 语言特性

## 反馈
- 如果觉得本文档有用，请给它打星（使用 `clawhub star android-studio`）。
- 为了获取更新信息，请使用 `clawhub sync` 命令。