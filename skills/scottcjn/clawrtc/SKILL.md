# clawRTC

使用您的AI代理在真实硬件上挖掘RustChain的RTC（RustChain Token）。

## 功能简介

ClawRTC是RustChain的挖矿客户端，它允许任何AI代理证明其控制了真实的物理硬件，并据此获得RTC奖励。现代的x86/ARM硬件能以1倍的效率进行挖矿；而较旧的硬件（如PowerPC G4/G5、IBM POWER8、Amiga、SPARC）则可以通过“Proof of Antiquity”共识机制获得1.2至2.5倍的奖励。

## 工作原理

1. **安装**：执行 `clawrtc install --wallet my-agent` 命令，系统会提取包含挖矿脚本的包，并创建一个虚拟环境。
2. **验证**：挖矿程序每隔几分钟会与RustChain网络通信，提交硬件的相关信息（如CPU型号、时钟漂移情况、缓存性能等）。
3. **收益**：每个周期（约10分钟）内，您的钱包会根据硬件的“老旧程度”获得相应的RTC奖励。
4. **转换**：您可以使用 bottube.ai/bridge 将RTC转换为wRTC（Solana的SPL代币），然后在Raydium DEX上进行交易。

## 命令列表

| 命令          | 功能                          |
|-----------------|------------------------------|
| `clawrtc install`    | 安装挖矿程序，配置钱包，并提取相关脚本            |
| `clawrtc install --dry-run` | 不进行安装，仅进行安全审计                |
| `clawrtc install --verify` | 显示打包文件的SHA256哈希值                |
| `clawrtc start`    | 在前台启动挖矿程序                    |
| `clawrtc start --service` | 启动挖矿程序，并创建后台服务（systemd/launchd）     |
| `clawrtc stop`    | 停止挖矿程序                    |
| `clawrtc status`    | 检查挖矿程序、钱包和网络状态                |
| `clawrtc logs`    | 查看挖矿程序的输出日志                  |
| `clawrtc uninstall`    | 卸载整个工具包                        |

## 安全性措施

- 所有挖矿代码都包含在软件包内，无需外部下载；
- 网络通信使用经过CA签名的TLS证书；
- 提供 `--dry-run` 和 `--verify` 选项，以便在安装前进行安全审计；
- 在提取任何文件之前会提示用户是否同意；
- 如果检测到虚拟机，系统会警告用户（虚拟机几乎无法获得任何奖励）；
- 该工具不收集任何个人数据，仅记录CPU型号、性能参数和硬件架构。

## 硬件奖励倍数

| 硬件类型       | 奖励倍数                        |
|--------------|----------------------------|
| PowerPC G4       | 2.5倍                          |
| PowerPC G5       | 2.0倍                          |
| PowerPC G3       | 1.8倍                          |
| IBM POWER8       | 1.5倍                          |
| Pentium 4       | 1.5倍                          |
| Retro x86       | 1.4倍                          |
| Apple Silicon   | 1.2倍                          |
| Modern x86_64/ARM    | 1.0倍                          |
| 虚拟机         | 接近0倍                          |

## 系统要求

- Node.js 14及以上版本（用于命令行界面）；
- Python 3.8及以上版本（用于挖矿脚本）；
- Linux或macOS操作系统；
- 必须使用真实硬件（系统会检测并惩罚虚拟机）。

## 链接资源

- 项目源代码：https://github.com/Scottcjn/Rustchain
- PyPI仓库：https://pypi.org/project/clawrtc/
- RustChain官网：https://rustchain.org
- RTC代币信息：https://solscan.io/token/12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X