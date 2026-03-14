---
name: superrare-mint
description: 通过 Bankr，将 Mint 艺术品转换为兼容 SuperRare 的 ERC-721 标准的数字藏品，并上传到 SuperRare 平台。系统会默认执行安全测试（dry-run），同时生成可审计的铸币记录（mint receipts）。
homepage: https://github.com/aaigotchi/superrare-mint
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
        - curl
        - node
      env:
        - BANKR_API_KEY
    primaryEnv: BANKR_API_KEY
    optionalEnv:
      - ETH_MAINNET_RPC
      - ETH_SEPOLIA_RPC
      - SUPER_RARE_CONFIG_FILE
      - DRY_RUN
      - BANKR_SUBMIT_TIMEOUT_SECONDS
      - RECEIPT_WAIT_TIMEOUT_SECONDS
      - RECEIPT_POLL_INTERVAL_SECONDS
---
# superrare-mint

本工具可将Aigotchi艺术作品铸造成符合SuperRare标准的ERC-721代币，并使用Bankr进行签名验证。

## 脚本

- `./scripts/pin-metadata.mjs --name ... --description ... --image ... [--video ...] [--tag ...] [--attribute trait=value]`
  - 将媒体文件上传至SuperRare，并设置元数据。
  - 生成包含`tokenUri`和`gatewayUrl`的JSON响应。
- `./scripts/mint-via-bankr.sh --token-uri <uri> [--contract <address>] [--receiver <address>] [--royalty-receiver <address>] [--chain mainnet|sepolia] [--broadcast]`
  - 生成用于`mintTo(string,address,address)`或`addNewToken(string)`的调用参数。
  - 默认为模拟运行（dry-run）模式，除非指定了`--broadcast`或`DRY_RUN=0`。
  - 不等待Bankr的响应，直接向区块链提交交易，并通过轮询获取确认结果。
  - 成功提交后，会将确认信息写入JSON文件中。
- `./scripts/mint-art.sh --name ... --description ... --image ... [options]`
  - 一站式脚本：先上传元数据，再通过Bankr进行代币铸造。
  - 使用`--metadata-only`选项可仅在设置元数据后停止流程，并打印Token的URI。

## 配置文件

配置文件默认路径：
- 本工具目录下的`config.json`

可通过以下方式覆盖配置文件：
- `SUPER_RARE_CONFIG_FILE=/path/to/config.json`

配置文件中应包含的键：
- `chain`：`mainnet`或`sepolia`（指定运行链）
- `collectionContract`：代币合约地址
- `receiver`：接收者地址
- `royaltyReceiver`：版税接收者地址
- `rpcUrl`：Bankr的RPC接口地址
- `apiBaseUrl`：API基础URL
- `descriptionPrefix`：描述前缀

## 默认设置与安全机制

- 默认为模拟运行模式。只有通过`--broadcast`或`DRY_RUN=0`才会实际执行交易广播。
- 广播模式下，Bankr提交请求的等待时间较短，之后会直接从区块链获取确认结果，避免因长时间等待而导致的阻塞。
- `mint-art.sh`在模拟铸造前仍会先将媒体文件和元数据上传至SuperRare。如需仅在设置元数据后停止流程并查看Token URI，可使用`--metadata-only`选项。
- 如果未设置`receiver`或`royaltyReceiver`，工具将使用`addNewToken(string)`函数进行代币铸造。
- 如果设置了`receiver`或`royaltyReceiver`中的任意一个，另一个字段将自动使用相同的地址。
- 成功的广播操作会将确认信息保存到`receipts/`目录中。

## Bankr API密钥获取方式

- `BANKR_API_KEY`
- `systemctl --user show-environment`
- `~/.openclaw/skills/bankr/config.json`
- `~/.openclaw/workspace/skills/bankr/config.json`

## 快速使用示例

```bash
cp config.example.json config.json

./scripts/pin-metadata.mjs \
  --name "aaigotchi genesis #1" \
  --description "First aaigotchi genesis mint" \
  --image ./art.png

./scripts/mint-via-bankr.sh \
  --token-uri ipfs://... \
  --broadcast

./scripts/mint-art.sh \
  --name "aaigotchi genesis #1" \
  --description "First aaigotchi genesis mint" \
  --image ./art.png \
  --broadcast
```

## 超时设置

可选的环境变量：
- `BANKR_SUBMIT_TIMEOUT_SECONDS`（默认值：60秒）
- `RECEIPT_WAIT_TIMEOUT_SECONDS`（默认值：300秒）
- `RECEIPT POLL_INTERVAL_SECONDS`（默认值：5秒）