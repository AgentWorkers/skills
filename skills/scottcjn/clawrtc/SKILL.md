# ClawRTC

使用 Proof-of-Antiquity 共识机制，通过您的 AI 代理来挖掘 RTC（Real-Time Clock）代币。

## 功能概述

- **一键安装**：`pip install clawrtc && clawrtc install --wallet my-agent`
- **硬件验证**：通过 6 种加密检查来确认您的设备是真实的（时钟漂移、缓存延迟、SIMD 特性、热熵、指令执行抖动、防模拟功能）
- **自动认证**：每隔几分钟向 RustChain 网络发送认证请求
- **每个时代周期的奖励**：每个时代周期（约 10 分钟）您的钱包会获得 RTC 代币
- **虚拟机检测**：虚拟机会被识别并无法获得任何奖励

## 安全性

- **安装过程中不收集任何数据** — 安装过程中不会进行网络请求
- **启用 TLS 验证** — 所有 RustChain API 调用都会验证 SSL 证书（由可信机构签名）
- **仅包含打包好的代码** — 所有挖矿脚本都包含在软件包中，无需额外下载
- **需要用户同意** — 安装前会显示交互式确认提示
- **试运行模式**：`clawrtc install --dry-run` 可以预览功能而无需实际安装
- **哈希验证**：`clawrtc install --verify` 可显示所有打包文件的 SHA256 哈希值
- **彻底卸载**：`clawrtc uninstall` 会删除所有文件、服务及配置
- **默认不启动后台服务** — 必须通过 `--service` 选项才能启用后台服务
- **源代码公开**：完整源代码可在 https://github.com/Scottcjn/Rustchain （MIT 许可证）获取

### 发送的数据

在认证过程中（即挖矿时），以下数据会被发送到 RustChain 节点：

- CPU 型号和架构（例如 "AMD Ryzen 5"、"x86_64"）
- 时钟计时精度（用于验证时钟的真实性）
- 缓存延迟信息（用于确认缓存层次结构）
- 虚拟机检测结果（是否为虚拟机）
- 钱包名称（您选择的标识符）

**不会发送的数据**：文件内容、浏览历史记录、凭证信息、IP 地理位置、个人数据。

## 安装方法

```bash
pip install clawrtc
```

## 使用方法

```bash
# Install miner + configure wallet
clawrtc install --wallet my-agent

# Start mining (foreground)
clawrtc start

# Check status
clawrtc status

# View logs
clawrtc logs

# Stop mining
clawrtc stop

# Clean uninstall
clawrtc uninstall
```

## 奖励系数

| 硬件类型 | 奖励系数 |
|----------|-----------|
| 现代 x86/ARM 处理器 | 1.0x |
| Apple Silicon (M1-M3) | 1.2x |
| PowerPC G5 | 2.0x |
| PowerPC G4 | 2.5x |
| 虚拟机/模拟器 | 约 0x（会被识别并受到惩罚） |

## 链接

- 源代码：https://github.com/Scottcjn/Rustchain
- PyPI：https://pypi.org/project/clawrtc/
- 块链浏览器：https://rustchain.org/explorer
- RustChain 官网：https://rustchain.org
- BoTTube：https://bottube.ai