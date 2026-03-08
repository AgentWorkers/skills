---
name: unclaimed-sol-scanner
description: 扫描任何 Solana 钱包，以找回那些被遗忘在休眠状态中的代币账户或程序缓冲账户中的可回收 SOL（Solana 货币）。当有人询问关于未领取的 SOL、忘记支付的租金、可回收的代币、已失效的代币账户或钱包清理相关问题时，可以使用此功能。此外，当用户提供 Solana 钱包地址并询问可领取的资产、可恢复的 SOL 或账户租金时，也可以使用该功能。相关的触发命令包括：`scan wallet`、`check claimable`、`reclaim SOL`、`unclaimed sol`、`wallet cleanup`、`close token accounts`、`recover rent`。
author: Unclaimed SOL (https://unclaimedsol.com)
homepage: https://unclaimedsol.com
privacy_policy: https://blog.unclaimedsol.com/privacy-policy/
---
# 未认领的Solana代币扫描工具

该工具可扫描任何Solana钱包，查找被锁定在休眠代币账户或程序缓冲账户中的可回收代币（SOL）。

## 隐私与数据披露

在使用此工具时，系统会通过HTTPS POST请求将用户的**Solana公钥**（钱包地址）发送到Unclaimed SOL API（`https://unclaimedsol.com/api/check-claimable-sol`），不会传输其他任何数据。该过程不涉及私钥、助记词或签名功能。

**在运行扫描之前，必须告知用户其钱包地址将被发送到unclaimedsol.com，并在继续之前获得用户的确认。**

**示例说明：**
> 为了扫描您的钱包，我会将您的公钥发送到unclaimedsol.com的Unclaimed SOL API。此过程不涉及私钥，仅使用您的公钥。您确定要继续吗？**

## 使用方法

1. 从用户处获取Solana钱包地址（格式为base58编码的公钥，长度为32-44个字符，例如`7xKXq1...`）。
2. **披露API调用内容并获取用户确认**（参见上述说明）。
3. 运行扫描脚本：

```bash
bash {baseDir}/scripts/scan.sh <wallet_address>
```

4. 解析JSON响应结果并将其格式化以便用户查看。

## 解析响应结果

脚本返回的JSON数据包含以下字段：

```json
{
  "totalClaimableSol": 4.728391,
  "assets": 3.921482,
  "buffers": 0.806909,
  "tokenCount": 183,
  "bufferCount": 3
}
```

- `totalClaimableSol`：可回收的代币总数（包括休眠代币账户和程序缓冲账户中的代币）
- `assets`：来自休眠代币账户的代币（如无效的ATAs、废弃的memecoins等）
- `buffers`：来自程序缓冲账户的代币
- `tokenCount`：需要关闭的代币账户数量（如果后端尚未记录该数据，可能为0）
- `bufferCount`：需要关闭的缓冲账户数量（如果后端尚未记录该数据，可能为0）

如果`tokenCount`和`bufferCount`均为0或未提供，则无需报告具体账户数量，只需显示代币总数即可。

## 响应结果的格式化

- **显示API返回的代币总数**，请勿四舍五入到小数点后两位，保留全部精度（例如：4.728391，而不是4.73）。
- **如果`totalClaimableSol`大于0**：
  - 显示总金额，并按类型细分：
    > 您的钱包中有**4.728391 SOL**可以回收。
    - 其中：
      - 3.921482 SOL来自183个代币账户
      - 0.806909 SOL来自3个缓冲账户
    >
    > 您可以在[https://unclaimedsol.com]进行代币领取。
  - 如果只有一种类型的代币有价值，直接显示总金额即可。
- **如果`totalClaimableSol`为0**：
  > 该钱包中没有可回收的代币。所有账户均为活跃状态或已优化。
- **如果脚本返回错误**：
  > 目前无法扫描该钱包。您可以尝试直接访问[https://unclaimedsol.com]，在那里连接您的钱包以查看可回收的代币。

**注意事项：**
- 该工具仅具有**读取权限**，不会执行任何交易操作，也不需要用户的私钥或助记词。
- 仅接受Solana的**公钥**（格式为base58编码的32-44个字符）。
- 如果输入的地址不符合Solana钱包地址的格式，请让用户重新核对。
- **在扫描之前，务必披露API调用内容并获取用户的明确同意。**