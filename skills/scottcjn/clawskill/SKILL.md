# ClawSkill — 使用您的AI代理挖掘RTC代币

通过证明您的代理在真实硬件上运行，您可以挖掘**RTC（RustChain代币）**。只需一个命令即可完成安装，系统会自动进行身份验证，并内置一个钱包。

## 安全性与透明度

**此工具为开源的挖掘软件**，绝非恶意软件。在安装之前，您可以验证所有相关内容：

```bash
# Preview what will happen — nothing installed
clawskill install --dry-run

# Show SHA256 hashes of bundled files
clawskill install --verify
```

| 关注点 | 我们的应对措施 |
|---------|-------------------|
| **代码来源** | 所有挖掘脚本都**包含在软件包内**——安装时无需外部下载。您可以在`data/`目录中自行查看这些脚本。源代码：[RustChain GitHub仓库](https://github.com/Scottcjn/Rustchain)。 |
| **后台服务** | **仅可选**。默认情况下，安装不会创建后台服务。您必须明确使用`--service`选项才能启用自动启动功能。如果没有该选项，挖掘程序仅会在您手动启动时在前台运行。 |
| **硬件指纹识别** | 这是Proof-of-Antiquity共识机制所必需的。系统会收集CPU型号、计时差异以及缓存延迟等信息——这些数据不会用于个人用途。在安装前，系统会向您展示所有收集到的信息，并征求您的同意。 |
| **网络端点** | RustChain节点使用**由CA签名的TLS证书**（Let's Encrypt）。所有通信均通过标准HTTPS协议进行，并经过证书验证。 |

### 收集的数据

在挖掘过程中（每隔几分钟），以下数据会被发送到RustChain节点：

- CPU型号和架构（例如：“AMD Ryzen 5 8645HS”、“x86_64”）
- 时钟计时差异（用于验证硬件是否为真实振荡器，而非模拟设备）
- 缓存延迟信息（用于确认L1/L2/L3缓存层的存在）
- 虚拟机检测标志（是否存在虚拟机管理程序）
- 钱包名称（您自定义的标识符）

**不会收集的数据**：文件内容、浏览历史记录、密码、IP地址、地理位置信息或您的文件系统中的任何个人数据。

### 清洁卸载

```bash
clawskill uninstall   # Removes ALL files, services, and configs
```

## 安装

```bash
# Python (recommended)
pip install clawskill

# Node.js
npm install -g clawskill
```

## 设置

```bash
# Install miner + configure wallet (shows disclosure, asks consent)
clawskill install --wallet my-agent-miner

# Start mining in foreground (Ctrl+C to stop)
clawskill start

# Or: start with background auto-restart (opt-in)
clawskill start --service
```

## 工作原理

1. **硬件指纹识别**：通过6项加密检查来验证您的硬件是否为真实设备：
   - 时钟偏移和振荡器漂移
   - 缓存延迟信息（L1/L2/L3缓存层的延迟）
   - SIMD单元类型（SSE/AVX/AltiVec/NEON）
   - 热量漂移情况
   - 指令路径抖动（与微架构相关）
   - 反模拟行为检测

2. **自动身份验证**：您的代理每隔几分钟会向RustChain网络发送一次身份验证信息

3. **每个周期的奖励**：每个周期（约10分钟）后，RTC代币会累积到您的钱包中

4. **虚拟机检测**：如果系统检测到虚拟机，将无法获得任何奖励。只有真实硬件才能获得奖励。

## 奖励倍数

| 硬件类型 | 奖励倍数 | 备注 |
|----------|-----------|-------|
| 现代x86/ARM架构 | **1.0倍** | 标准奖励 |
| Apple Silicon（M1/M2/M3） | **1.2倍** | 小额奖励 |
| IBM POWER8 | **1.5倍** | 服务器级硬件 |
| PowerPC G5 | **2.0倍** | 老式硬件奖励 |
| PowerPC G4 | **2.5倍** | 最高奖励 |
| **虚拟机/模拟器** | **约0倍** | 被检测到后将受到惩罚 |

## 命令

| 命令 | 描述 |
|---------|-------------|
| `clawskill install` | 解压挖掘脚本并创建钱包（系统会提示您是否同意使用该服务，默认情况下不会创建后台服务） |
| `clawskill install --service` | 安装并创建后台服务 |
| `clawskill install --dry-run` | 预览功能，不进行任何实际操作 |
| `clawskill install --verify` | 显示软件包内文件的SHA256哈希值 |
| `clawskill start` | 在前台启动挖掘程序 |
| `clawskill start --service` | 启动挖掘程序并创建自动重启服务 |
| `clawskill stop` | 停止挖掘 |
| `clawskill status` | 检查挖掘程序和网络状态以及文件哈希值 |
| `clawskill logs` | 查看挖掘程序的输出日志 |
| `clawskill uninstall` | 清洁卸载所有软件 |

## 安装内容

- 挖掘脚本（包含在软件包内，共2个Python文件，无需额外下载）
- 包含一个依赖项（`requests`的Python虚拟环境）
- 所有文件存储在`~/.clawskill/`目录中（用户级权限，无需root权限）
- **除非您使用`--service`选项，否则不会创建后台服务**

## 系统要求

- Python 3.8及以上版本（大多数系统已安装）
- Linux或macOS操作系统
- 真实硬件（非虚拟机）

## 链接

- **源代码**：https://github.com/Scottcjn/Rustchain（MIT许可证） |
- **PyPI**：https://pypi.org/project/clawskill/ |
- **npm**：https://www.npmjs.com/package/clawskill |
- **区块浏览器**：https://bulbous-bouffant.metalseed.net/explorer |
- **BoTTube**：https://bottube.ai |

## 许可证

MIT许可证 — [Elyan Labs](https://bottube.ai)