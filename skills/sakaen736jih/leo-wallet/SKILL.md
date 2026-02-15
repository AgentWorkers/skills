---
name: leo-wallet
description: 与 Aleo 区块链交互：可以查询余额、查看交易记录，并深入了解这个注重隐私保护的区块链网络。该功能支持使用 Leo 钱包地址进行操作。
metadata: {"openclaw":{"requires":{"bins":["snarkos"]},"install":[{"id":"aleo","kind":"shell","command":"curl -sSf https://raw.githubusercontent.com/AleoHQ/snarkOS/mainnet/install.sh | bash","bins":["snarkos"],"label":"Install snarkOS CLI"}]}}
---

# Leo Wallet 命令行界面 (Leo Wallet CLI)

## 设置

安装 snarkOS：
```bash
curl -sSf https://raw.githubusercontent.com/AleoHQ/snarkOS/mainnet/install.sh | bash
```

安装 Leo（开发版本）：
```bash
curl -sSf https://raw.githubusercontent.com/AleoHQ/leo/mainnet/install.sh | bash
```

## 通过 API 检查余额

```bash
curl -s "https://api.explorer.aleo.org/v1/testnet3/program/credits.aleo/mapping/account/ADDRESS" | \
python3 -c "import sys; print(sys.stdin.read())"
```

## 获取最新区块

```bash
curl -s "https://api.explorer.aleo.org/v1/testnet3/latest/block" | python3 -m json.tool
```

## 区块高度

```bash
curl -s "https://api.explorer.aleo.org/v1/testnet3/latest/height"
```

## 获取交易记录

```bash
curl -s "https://api.explorer.aleo.org/v1/testnet3/transaction/TX_ID" | python3 -m json.tool
```

## 根据区块高度获取区块

```bash
curl -s "https://api.explorer.aleo.org/v1/testnet3/block/BLOCK_HEIGHT" | python3 -m json.tool
```

## 程序信息

```bash
curl -s "https://api.explorer.aleo.org/v1/testnet3/program/credits.aleo" | python3 -m json.tool
```

## 列出程序映射关系

```bash
curl -s "https://api.explorer.aleo.org/v1/testnet3/program/credits.aleo/mappings" | python3 -m json.tool
```

## 网络统计信息

```bash
python3 -c "
import urllib.request
import json

base = 'https://api.explorer.aleo.org/v1/testnet3'
height = urllib.request.urlopen(f'{base}/latest/height').read().decode()
print(f'Latest Block: {height}')
"
```

## 使用 snarkOS

启动客户端节点：
```bash
snarkos start --client
```

获取节点信息：
```bash
snarkos developer get-peer-count
```

## Leo CLI（开发模式）

创建新项目：
```bash
leo new my_program
```

编译程序：
```bash
leo build
```

运行程序：
```bash
leo run main
```

## 地址格式

- Aleo 地址以 `aleo1` 开头
- 长度：63 个字符
- 示例：aleo1rhgdu77hgyqd3xjj8ucu3jj9r2krwz6mnzyd80gncr5fxcwlh5rsvzp9dx

## 密钥类型

| 类型 | 前缀 | 用途 |
|------|--------|---------|
| 地址 | aleo1 | 公共标识符 |
| 查看密钥 | AViewKey1 | 解密传入的数据 |
| 私钥 | APrivateKey1 | 全权控制权限 |

## 探索器 API

| 网络 | 基本 URL |
|---------|----------|
| Testnet3 | https://api.explorer.aleo.org/v1/testnet3 |
| Mainnet | https://api.explorer.aleo.org/v1/mainnet （主网） |

## API 端点

| 端点 | 描述 |
|----------|-------------|
| /latest/block | 最新区块 |
| /latest/height | 当前区块高度 |
| /block/{height} | 根据高度获取区块 |
| /transaction/{id} | 交易详情 |
| /program/{id} | 程序源代码 |
| /program/{id}/mappings | 程序状态 |

## 注意事项

- Aleo 注重隐私保护；并非所有数据都公开可见 |
- Testnet3 是当前的测试网络 |
- Credits 是该平台的原生货币 |
- 程序使用 Leo 语言编写 |
- 零知识证明技术支持私密交易 |
- 主网预计即将上线，请访问 aleo.org 获取最新信息