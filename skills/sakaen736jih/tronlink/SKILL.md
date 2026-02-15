---
name: tronlink
description: 使用 TronLink 钱包：管理 TRX 和 TRC-20 代币，进行质押以获取能量/带宽，投票选举超级代表，并与 TRON 的去中心化应用程序（dApps）进行交互。
metadata: {"openclaw":{"requires":{"bins":["python3"]},"install":[{"id":"python","kind":"pip","package":"tronpy","bins":[],"label":"Install tronpy (pip)"}]}}
---

# TronLink 钱包

## 安装

- Chrome：https://chrome.google.com/webstore/detail/tronlink/ibnejdfjmmkpcnlpebklmnkoeoihofec  
- 移动设备：iOS App Store / Google Play  

## 支持的资产类型  

| 类型 | 示例 |
|------|----------|
| 原生资产 | TRX |
| TRC-20 | USDT、USDC、JST、BTT |
| TRC-10 | 传统代币（Legacy tokens） |
| TRC-721 | NFTs（非同质化代币） |

## 查看余额（命令行接口）  

TRX 余额：  
```bash
python3 -c "
from tronpy import Tron
client = Tron()
balance = client.get_account_balance('YOUR_TRONLINK_ADDRESS')
print(f'{balance} TRX')"
```  

通过 API 查看余额：  
```bash
curl -s "https://api.trongrid.io/v1/accounts/YOUR_ADDRESS" | \
python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"{d['data'][0].get('balance',0)/1e6:.2f} TRX\")"
```  

## TRC-20 代币余额  

USDT 余额：  
```bash
python3 -c "
from tronpy import Tron
client = Tron()
contract = client.get_contract('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
balance = contract.functions.balanceOf('YOUR_ADDRESS')
print(f'{balance / 1e6:.2f} USDT')"
```  

## 导入 TRC-20 代币  

步骤：  
**资产（Assets）** → **添加代币（Add Token）** → **自定义（Custom）**  

常见的 TRC-20 合同示例：  
```
USDT: TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
USDC: TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8
BTT: TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4
JST: TCFLL5dx5ZJdKnWuesXxi1VPwjLVmWZZy9
WIN: TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7
SUN: TSSMHYeV2uE9qYH95DqyoCuNCzEL1NvU3S
```  

## 资源（Energy & Bandwidth）  

- 查看资源使用情况：  
```bash
python3 -c "
from tronpy import Tron
client = Tron()
res = client.get_account_resource('YOUR_ADDRESS')
print(f\"Free Bandwidth: {res.get('freeNetUsed', 0)} / {res.get('freeNetLimit', 1500)}\")
print(f\"Energy: {res.get('EnergyUsed', 0)} / {res.get('EnergyLimit', 0)}\")"
```  

通过 API 查看资源使用情况：  
```bash
curl -s "https://api.trongrid.io/v1/accounts/YOUR_ADDRESS/resources" | python3 -m json.tool
```  

## 冻结 TRX 以获取资源  

在 TronLink 中的操作步骤：  
**资源（Resources）** → **冻结（Freeze）**  
- 冻结类型：带宽（Bandwidth）：限制交易  
- 冻结类型：能量（Energy）：限制智能合约调用  

**最低冻结要求**：1 TRX  
**冻结期限**：14 天（需质押 2.0 TRX）  

## 投票选举超级代表（Super Representatives）  

步骤：  
**资源（Resources）** → **投票（Vote）** → **选择超级代表（Select SR）**  
查看投票结果：  
```bash
curl -s "https://api.trongrid.io/v1/accounts/YOUR_ADDRESS" | \
python3 -c "
import sys, json
d = json.load(sys.stdin)
votes = d['data'][0].get('votes', [])
for v in votes:
    print(f\"{v['vote_address']}: {v['vote_count']} votes\")"
```  

## 交易历史  

```bash
curl -s "https://api.trongrid.io/v1/accounts/YOUR_ADDRESS/transactions?limit=10" | \
python3 -c "
import sys, json
data = json.load(sys.stdin)
for tx in data.get('data', []):
    txid = tx['txID'][:16]
    type = tx.get('raw_data', {}).get('contract', [{}])[0].get('type', 'Unknown')
    print(f'{txid}... | {type}')"
```  

TRC-20 转账记录：  
```bash
curl -s "https://api.trongrid.io/v1/accounts/YOUR_ADDRESS/transactions/trc20?limit=10" | python3 -m json.tool
```  

## 网络设置  

步骤：  
**设置（Settings）** → **节点设置（Node Settings）**  
默认节点地址：https://api.trongrid.io  
自定义节点配置：  
```
TronGrid: https://api.trongrid.io
Nile Testnet: https://nile.trongrid.io
Shasta Testnet: https://api.shasta.trongrid.io
```  

## 已连接的 dApps  

步骤：  
**设置（Settings）** → **已连接站点（Connected Sites）** → **管理（Manage）**  

## 导出账户信息  

步骤：  
**设置（Settings）** → **导出（Export）** → 输入密码  

## dApp 浏览器（移动设备）  

- 通过 TronLink 浏览 dApps：**  
**发现（Discover）** → **浏览 dApps（Browse dApps）**  

**热门 TRON dApps**：  
- JustLend（借贷服务）  
- SunSwap（去中心化交易所）  
- JUST（稳定币）  

## 交易费用  

| 操作类型 | 费用（Cost） |
|-----------|------|
| TRX 转账 | 约 1 单位带宽（Bandwidth） |
| TRC-20 转账 | 约 15,000 单位能量（Energy） |
| 智能合约调用 | 费用因合约而异 |

## 常见问题与解决方法  

**带宽不足**：  
**解决方案**：等待带宽恢复，或冻结 TRX 以释放更多带宽。  

**能量不足**：  
**解决方案**：冻结 TRX 以获取更多能量，或支付 TRX 以完成交易。  

**代币未显示**：  
**操作步骤**：  
**资产（Assets）** → **添加代币（Add Token）** → 粘贴代币合约地址。  

**交易待处理中**：  
```bash
# Check transaction
python3 -c "
from tronpy import Tron
client = Tron()
tx = client.get_transaction('TX_HASH')
print(tx)"
```  

## 地址格式  

TronLink 地址采用 Base58Check 编码格式，以 ‘T’ 开头，共 34 个字符。  
**示例地址**：TJYeasTPa6gpBZWqTcP4u1Q7bhLMWBL7ox  

## 注意事项：  

- TronLink 是官方的 TRON 钱包应用。  
- 每天免费提供 1500 单位带宽（带宽会自动恢复）。  
- 智能合约的运行需要消耗能量。  
- 需质押 2.0 TRX，冻结期限为 14 天。  
- 可通过投票选举超级代表并获得奖励。  
- 移动版本内置 dApp 浏览器。