---
name: vvvv-fundamentals
description: >
  **vvvv Gamma核心概念说明**  
  - **数据类型**：vvvv支持多种数据类型，用于存储和处理程序运行过程中的各种信息。  
  - **基于帧的执行模型**：vvvv采用基于帧的执行机制，确保程序能够高效地处理连续的数据流。  
  - **引脚（Pins）与焊盘（Pads）**：引脚用于连接外部硬件设备，焊盘则用于在电路板内部传输信号。  
  - **链接（Links）**：用于在程序内部或不同模块之间建立数据流。  
  - **节点浏览器（Node Browser）**：提供了一个可视化的界面，用于查看和操作程序中的各个节点及其连接关系。  
  - **实时编译（Live Compilation）**：支持在程序运行过程中实时编译代码，提高开发效率。  
  - **源代码项目与二进制文件的工作流程**：详细介绍了如何从源代码项目生成可执行的二进制文件。  
  - **.vl文档结构**：vvvv使用.vl文件来存储程序的结构和配置信息。  
  - **文件类型**：支持.vl、.sdsl、.cs和.csproj等文件格式。  
  - **生态系统概述**：介绍了vvvv所处的技术生态系统及其与其他组件的交互方式。  
  - **AppHost运行时检测**：能够自动检测并配置AppHost运行环境。  
  **适用场景**：  
  当用户询问vvvv的基础知识、工作原理、实时刷新机制、何时使用补丁或代码更新，或者需要了解其可视化编程环境时，本文档可提供详细的解答。
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.0"
---
# vvvv gamma 基础知识

## 什么是 vvvv gamma

vvvv gamma 是一个专为 .NET 8 设计的可视化编程环境。它结合了基于节点的编程方式与 C# 代码生成功能，主要针对 Stride（3D 引擎）和 .NET API 进行开发。用户可以通过在可视化编辑器中连接节点来构建程序。

vvvv gamma 是一个实时编程环境：在您编写程序的过程中，程序会持续运行。无论是可视化节点的修改还是 C# 代码的更改，都会立即生效，无需重新启动程序。vvvv gamma 会通过 Roslyn 在每次保存时自动将 C# 源代码编译成内存中的程序集。

## 文档结构

- **`.vl` 文件**：vvvv gamma 的文档文件（基于 XML，支持版本控制）
- 每个文档包含 **可视化程序（Patch）** 和 **数据类型/操作（Definition）**
- 文档可以引用 NuGet 包和其他 `.vl` 文件
- **Patch Explorer** 可以显示文档中的类型层次结构

## 执行模型

- **基于帧的评估**：主循环会在每一帧中评估整个程序结构（约 60 FPS）
- 数据会从左到右、从上到下通过节点之间的连接进行传输
- **处理节点（Process Nodes）** 在不同帧之间维护状态（构造函数 → 更新循环 → 销毁操作）
- **操作节点（Operation Nodes）** 是纯函数，在每一帧中都会被执行
- vvvv 会评估所有连接的节点，但会跳过未连接的子图

## 实时编译模型

在您编辑程序的过程中，vvvv gamma 会持续运行程序。对于可视化节点和着色器，不存在“编辑 → 编译 → 运行”的循环。对于 C# 代码，是否支持实时重新加载取决于代码的引用方式。

### 可视化节点的修改

- 对可视化节点的修改会立即生效
- 节点的状态（实例字段）会在修改后保持不变
- 新节点和连接会在下一帧中生效

### 着色器的修改

- 当 `.sdsl` 着色器文件被保存时，会立即重新加载
- vvvv 会在后台重新编译着色器，并将其应用到正在运行的程序中

### C# 的两种集成方式

C# 代码可以通过引用源项目或预编译的二进制文件来集成。具体选择方式取决于项目的规模和开发阶段：

**引用源项目（支持实时重新加载）**：
当 `.vl` 文档引用一个 `.csproj` 源项目时，vvvv gamma 会通过 Roslyn 自动将 `.cs` 文件编译成内存中的程序集。无需使用 `dotnet build` 或其他外部工具链。
- 在 `.cs` 文件保存时，vvvv gamma 会检测到变化并在后台重新编译
- 状态指示器：
  - 灰色：正在编译符号
  - 橙色：正在生成 C# 代码
- 编译成功后，相关节点会重新开始其生命周期：
  1. 调用旧实例的 `Dispose()`
  2. 运行新的构造函数（使用新的 `NodeContext`）
  3. 在下一帧中继续执行 `Update()`
- 重新加载时，静态字段会被重置；整个内存中的程序集会被替换
- 如果编译出现错误，程序会继续使用最后有效的代码运行

**引用预编译的二进制文件（不支持实时重新加载）**：
当 `.vl` 文档引用一个预编译的 DLL 或 NuGet 包时，程序集仅在程序启动时加载一次。要应用更改，需要外部重新构建 DLL（例如使用 `dotnet build`），然后重新启动 vvvv。这种方式适用于大型项目和稳定性要求较高的库，因为这些项目不需要实时重新加载的功能。

## 节点类型

### 处理节点（Process Nodes）

- 具有构造函数（Create）、更新操作（Update）和销毁操作（Dispose）的生命周期
- 用 `[ProcessNode]` 属性在 C# 中定义
- 在不同帧之间维护内部状态
- 通过检测变化来避免不必要的计算

### 操作节点（Operation Nodes）

- 纯函数：相同的输入总是产生相同的输出
- 以静态 C# 方法的形式实现（由 vvvv 自动识别）
- 在不同帧之间没有状态保存
- 不需要 `[ProcessNode]` 属性

### 自适应节点（Adaptive Nodes）

- 根据连接的输入类型动态调整实现
- 例如：`+` 运算符可以接受 int、float、Vector3、string 等类型
- 在链接时确定其具体行为，而不是在运行时

## 针脚（Pins）、垫子（Pads）和连接（Links）

- **针脚（Pins）**：节点和区域上的输入/输出接口
- **垫子（Pads）**：用于在可视化节点中读取/写入属性的可视化元素；同名垫子表示相同的属性
- **连接（Links）**：定义数据流和执行顺序的连接方式
- **扩展功能（Spreading）**：当 `Spread<T>` 连接到单值输入时，节点会自动遍历相关数据

## 何时使用可视化编程 vs C# 代码

| 适用场景 | 选择方式 |
|---|---|
| 原型设计、数据流处理 | 可视化编程 |
| UI 组合 | 复杂算法 |
| 实时参数调整 | .NET 库的交互 |
| 数据流路由和扩展 | 本地资源管理 |

## 通道（Channels）——反应式数据流

- `IChannel<T>`：用于存储可观察值的容器
- `IChannel<T>.Value`：读取/写入当前值
- `Channel.IsValid()`：检查通道是否已连接
- 通道可以在会话之间保持状态
- 支持 UI 与可视化程序之间的双向数据绑定

有关 C# 通道的集成方式（如 `IChannelHub`、`PublicChannelHelper`、`CanBePublished`），请参阅 [vvvvv-channels](vvvvv-channels)。

## 主要数据类型

| 数据类型 | C# 对应类型 | 用途 |
|---|---|---|
| `Spread<T>` | `ImmutableArray<T>`：vvvv gamma 的不可变集合 |
| `SpreadBuilder<T>` | `ImmutableArray<T>.Builder`：用于高效构建数据结构 |
| `Float32`、`Int32` 等 | `float`、`int`：基本数据类型 |
| `Vector2/3/4` | `Stride.Core.Mathematics`：空间数学运算 |
| `Color4` | `Stride.Core.Mathematics`：RGBA 颜色值 |

## 文件类型

| 文件扩展名 | 用途 |
|---|---|
| `.vl` | vvvv gamma 文档文件（基于 XML） |
| `.sdsl` | Stride 着色器文件（使用 DSL 语言） |
| `.cs` | C# 源代码文件（用于自定义节点） |
| `.csproj` | .NET 项目文件 |
| `.nuspec` | NuGet 包的配置文件 |

## 生态系统概述

vvvv gamma 的功能可以通过 NuGet 包进行扩展，这些包包含了 `.vl` 文档、C# 节点和着色器。

| 领域 | 关键 NuGet 包 |
|---|---|
| 3D 渲染 | VL.Stride（Stride 引擎）、VL.Fuse（GPU 可视化编程库） |
| 2D 渲染 | VL.Skia、	ImGui、Avalonia、CEF/HTML |
| 硬件 I/O | DMX/Art-Net、ILDA 激光器、深度相机（Azure Kinect、ZED）、机器人技术（KUKA、Spot、Ultraleap、LiDAR） |
| 网络通信 | OSC、MIDI、MQTT、Redis、WebSocket、HTTP、TCP/UDP、ZeroMQ、Modbus、Ableton Link |
| 计算机视觉 | OpenCV、MediaPipe、YOLO（v8–v11）、ONNX 运行时 |
| 音频处理 | NAudio、VST 插件支持 |
| 通用 .NET 功能 | 通过 `.csproj` 引用数千个标准 NuGet 包 |

要添加新的 NuGet 包，只需在 `.vl` 文档的依赖项中引用它，或在 `.csproj` 文件中添加 `<PackageReference>`。有关 `.csproj` 的详细信息，请参阅 [vvvvv-dotnet](vvvvv-dotnet)。

## 应用程序宿主与运行时检测

```csharp
// 检测当前程序是作为可执行的 `.exe` 运行还是作为编辑器运行
bool isExported = nodeContext.AppHost.IsExported;

// 注册应用程序级的单例服务
nodeContext.AppHost.Services.RegisterService(myService);
```

更多详细信息，请参阅 [reference.md](reference.md)。