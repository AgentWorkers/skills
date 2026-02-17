# ClawRTC

使用您在 RustChain 网络中的 AI 代理来挖掘 RTC 代币。

## 安装

```bash
pip install clawrtc
# or
npm install -g clawrtc
```

## 使用方法

```bash
# Create an Ed25519 wallet
clawrtc wallet create

# Show wallet address and balance
clawrtc wallet show

# Start mining
clawrtc start

# Check miner status
clawrtc status

# Export wallet keys
clawrtc wallet export --public-only
```

## 主要特性

- **Ed25519 钱包**：使用 Ed25519 密钥对生成和管理 RTC 钱包
- **硬件指纹识别**：通过硬件验证机制来确认矿机的真实性和历史价值
- **平台优势**：PowerPC G4（性能提升 2.5 倍）、G5（性能提升 2.0 倍）、Apple Silicon（性能提升 1.2 倍）
- **防伪机制**：通过虚拟机检测防止虚假矿机的入侵
- **跨平台支持**：兼容 Linux、macOS、Windows 以及多种其他操作系统

## 链接

- [官方网站](https://rustchain.org)
- [GitHub 仓库](https://github.com/Scottcjn/Rustchain)
- [PyPI 仓库](https://pypi.org/project/clawrtc/)
- [npm 包](https://www.npmjs.com/package/clawrtc)
- [区块浏览器](https://rustchain.org/explorer)