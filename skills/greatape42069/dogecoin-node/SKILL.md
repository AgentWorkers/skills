---
name: dogecoin-node
version: 1.0.5
description: >
  **技能：配置并运行具备 RPC 访问功能、区块链工具以及可选的小费功能的 Dogecoin Core 全节点**
  **描述：**  
  本技能涵盖如何搭建并操作一个 Dogecoin Core 全节点，使其具备远程过程调用（RPC）访问能力、使用区块链相关工具，并支持可选的小费功能。用户将学习如何配置网络参数、安装必要的软件组件、启动节点服务以及管理节点的运行状态。
---
# Dogecoin 节点技能

该技能旨在通过 RPC 完全自动地集成和操作 Dogecoin Core 全节点及 CLI，从而支持各种用例下的区块链工具和钱包管理，包括使用 SQLite 实现的小费功能。

## 功能

1. **获取钱包余额**
    - 获取 Dogecoin 钱包地址的当前余额。
    - 示例：`/dogecoin-node balance <wallet_address>`

2. **发送 DOGE**
    - 从连接的钱包向指定地址发送 Dogecoin。
    - 示例：`/dogecoin-node send <recipient_address> <amount>`

3. **查看交易记录**
    - 查看钱包的最新交易详情。
    - 示例：`/dogecoin-node txs <wallet_address>`

4. **查询 DOGE 价格**
    - 获取最新的 Dogecoin 价格（以 USD 为单位）。
    - 示例：`/dogecoin-node price`

5. **帮助命令**
    - 显示命令的相关帮助信息。
    - 示例：`/dogecoin-node help`

---

## 安装

### 先决条件

1. 一个已完全同步的 Dogecoin Core RPC 节点。
2. 在 `dogecoin.conf` 文件中配置了 Dogecoin 的 `rpcuser` 和 `rpcpassword`。
3. OpenClaw Gateway 已更新至最新版本。
4. 主机上已安装 `jq`（命令：`sudo apt install jq`）。

### 配置节点的步骤

1. **安装二进制文件并下载 Dogecoin Core**
```bash
cd ~/downloads
curl -L -o dogecoin-1.14.9-x86_64-linux-gnu.tar.gz \
  [https://github.com/dogecoin/dogecoin/releases/download/v1.14.9/dogecoin-1.14.9-x86_64-linux-gnu.tar.gz](https://github.com/dogecoin/dogecoin/releases/download/v1.14.9/dogecoin-1.14.9-x86_64-linux-gnu.tar.gz)

```

2. **解压并放置二进制文件**
```bash
tar xf dogecoin-1.14.9-x86_64-linux-gnu.tar.gz
mkdir -p ~/bin/dogecoin-1.14.9
cp -r dogecoin-1.14.9/* ~/bin/dogecoin-1.14.9/
ln -sf ~/bin/dogecoin-1.14.9/bin/dogecoind ~/dogecoind
ln -sf ~/bin/dogecoin-1.14.9/bin/dogecoin-cli ~/dogecoin-cli

```

3. **设置 Prime 数据目录（用于 ~/.dogecoin）**
```bash
./dogecoind -datadir=$HOME/.dogecoin -server=1 -listen=0 -daemon
# Wait for RPC to initialize ~30s then stop once RPC is responsive
sleep 30
./dogecoin-cli -datadir=$HOME/.dogecoin stop

```

4. **配置 RPC 凭据（仅限本地连接）**
```bash
cat > ~/.dogecoin/dogecoin.conf <<'EOF'
server=1
daemon=1
listen=1
rpcbind=127.0.0.1
rpcallowip=127.0.0.1
rpcuser=<strong-username>
rpcpassword=<strong-password>
txindex=1
EOF

```

5. **启动并同步节点**
```bash
./dogecoind -datadir=$HOME/.dogecoin -daemon

```

6. **检查同步状态**
```bash
./dogecoin-cli -datadir=$HOME/.dogecoin getblockcount

./dogecoin-cli -datadir=$HOME/.dogecoin getblockchaininfo
```

---

## RPC/CLI 命令速查表

### 区块链相关命令
```bash
./dogecoin-cli getblockcount # Get the current block height
./dogecoin-cli getblockchaininfo # Detailed blockchain stats
./dogecoin-cli getbestblockhash # Get the hash of the latest block
./dogecoin-cli getblockhash <height> # Get the hash of a block 
./dogecoin-cli getblock <blockhash> # Details for a specific block

```

### 网络、工具及钱包相关命令
```bash
./dogecoin-cli getconnectioncount # Number of peer connections
./dogecoin-cli getpeerinfo # Info about connected peers
./dogecoin-cli addnode <address> onetry # Try a one-time connection to a node
./dogecoin-cli ping # Ping all connected nodes
./dogecoin-cli getnewaddress # Generate a new receiving address
./dogecoin-cli getwalletinfo # Wallet details (balance, etc.)
./dogecoin-cli listunspent # List all unspent transactions
./dogecoin-cli sendtoaddress <address> <amount> # Send DOGE
./dogecoin-cli dumpprivkey <address> # Export private key for an address (use this with extreme caution its for backing up your key or using it elsewhere if needed , THIS WILL PRINT YOUR CURRENT PRIV KEY, CAUTION!!)

./dogecoin-cli stop # Stop the Dogecoin node safely
./dogecoin-cli help # List all available commands and usage details
```

对于未列出的动态查询需求，请始终参考：`./dogecoin-cli help`。

---

## 自动化健康检查（v1.0.5 强化版）

当前的健康检查功能包括区块链元数据解析、磁盘监控以及从 CoinGecko 获取实时价格。

### 健康检查脚本设置：

1. 在 `~/.openclaw/workspace/archive/health/doge_health_check.sh` 文件中创建健康检查脚本：
```bash
mkdir -p ~/.openclaw/workspace/archive/health/

cat > ~/.openclaw/workspace/archive/health/doge_health_check.sh <<'EOF'
#!/bin/bash

# --- Dogecoin Health Check Automation ---
echo "Starting Health Check: $(date)"
DOGE_CLI="$HOME/dogecoin-cli"
DATA_DIR="$HOME/.dogecoin"
COINGECKO_API="[https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=usd](https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=usd)"

# 1. Check Node Process
if pgrep -x "dogecoind" > /dev/null; then
    echo "[PASS] Dogecoin node process detected."
else
    echo "[FAIL] Dogecoin node is offline. Attempting restart..."
    ~/dogecoind -datadir=$DATA_DIR -daemon
fi

# 2. Blockchain Sync & Status
NODE_INFO=$($DOGE_CLI -datadir=$DATA_DIR getblockchaininfo 2>/dev/null)
if [ $? -eq 0 ]; then
    CHAIN=$(echo $NODE_INFO | jq -r '.chain')
    BLOCKS=$(echo $NODE_INFO | jq -r '.blocks')
    PROGRESS=$(echo $NODE_INFO | jq -r '.verificationprogress')
    SYNC_PCT=$(echo "$PROGRESS * 100" | bc 2>/dev/null || echo "0")
    echo "[PASS] Chain: $CHAIN | Height: $BLOCKS | Sync: ${SYNC_PCT}%"
else
    echo "[FAIL] RPC Unresponsive. Check credentials in dogecoin.conf."
fi

# 3. Market Price Check
PRICE=$(curl -s "$COINGECKO_API" | jq -r '.dogecoin.usd')
if [ "$PRICE" != "null" ] && [ -n "$PRICE" ]; then
    echo "[INFO] Live Price: \$$PRICE USD"
else
    echo "[WARN] Could not fetch market price."
fi

# 4. Disk Space Check
FREE_GB=$(df -BG $DATA_DIR | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$FREE_GB" -lt 10 ]; then
    echo "[CRITICAL] Low Disk Space: Only ${FREE_GB}GB remaining!"
else
    echo "[PASS] Disk Space: ${FREE_GB}GB available."
fi

# 5. Tipping Database Integrity
DB_PATH="$HOME/.openclaw/workspace/archive/tipping/dogecoin_tipping.db"
if [ -f "$DB_PATH" ]; then
    DB_CHECK=$(sqlite3 "$DB_PATH" "PRAGMA integrity_check;")
    if [ "$DB_CHECK" == "ok" ]; then
        echo "[PASS] Tipping database integrity verified."
    else
        echo "[FAIL] Database Error: $DB_CHECK"
    fi
fi

echo "Health Check Complete."
EOF

chmod +x ~/.openclaw/workspace/archive/health/doge_health_check.sh

```

---

## 小费集成（可选功能）：

在设置并同步节点后，您可以启用小费功能。该功能允许您发送 Dogecoin 小费、维护用户钱包数据库并记录交易记录。

### 小费脚本设置：

1. 要启用小费功能，请在 `~/.openclaw/workspace/archive/tipping/` 目录下创建 `dogecoin_tipping.py` 文件，并添加以下代码：
```bash
mkdir -p ~/.openclaw/workspace/archive/tipping/

cat > ~/.openclaw/workspace/archive/tipping/dogecoin_tipping.py <<'EOF'
import sqlite3
import time
from typing import Optional

class DogecoinTippingDB:
    def __init__(self, db_path: str = "dogecoin_tipping.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    wallet_address TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    receiver TEXT NOT NULL,
                    amount REAL NOT NULL,
                    timestamp INTEGER NOT NULL
                )
            """)

    def add_user(self, username: str, wallet_address: str) -> bool:
        try:
            with self.conn:
                self.conn.execute("INSERT INTO users (username, wallet_address) VALUES (?, ?)", (username, wallet_address))
            return True
        except sqlite3.IntegrityError:
            return False

    def get_wallet_address(self, username: str) -> Optional[str]:
        result = self.conn.execute("SELECT wallet_address FROM users WHERE username = ?", (username,)).fetchone()
        return result[0] if result else None

    def list_users(self) -> list:
        return [row[0] for row in self.conn.execute("SELECT username FROM users").fetchall()]

    def log_transaction(self, sender: str, receiver: str, amount: float):
        timestamp = int(time.time())
        with self.conn:
            self.conn.execute("INSERT INTO transactions (sender, receiver, amount, timestamp) VALUES (?, ?, ?, ?)", (sender, receiver, amount, timestamp))

    def get_sent_tips(self, sender: str, receiver: str) -> tuple:
        result = self.conn.execute("SELECT COUNT(*), SUM(amount) FROM transactions WHERE sender = ? AND receiver = ?", (sender, receiver)).fetchone()
        return result[0], (result[1] if result[1] else 0.0)

class DogecoinTipping:
    def __init__(self):
        self.db = DogecoinTippingDB()

    def send_tip(self, sender: str, receiver: str, amount: float) -> str:
        if amount <= 0: return "Amount must be > 0."
        if not self.db.get_wallet_address(sender): return f"Sender '{sender}' not found."
        if not self.db.get_wallet_address(receiver): return f"Receiver '{receiver}' not found."
        
        self.db.log_transaction(sender, receiver, amount)
        return f"Logged tip of {amount} DOGE from {sender} to {receiver}."

    def command_list_wallets(self) -> str:
        users = self.db.list_users()
        return "Registered wallets: " + ", ".join(users)

    def command_get_address(self, username: str) -> str:
        address = self.db.get_wallet_address(username)
        if address:
            return f"{username}'s wallet address is {address}."
        return f"User '{username}' not found."

    def command_get_tips(self, sender: str, receiver: str) -> str:
        count, total = self.db.get_sent_tips(sender, receiver)
        return f"{sender} has sent {count} tips totaling {total} DOGE to {receiver}."

if __name__ == "__main__":
    tipping = DogecoinTipping()
    print("Dogecoin Tipping System Initialized...MANY TIPS... MUCH WOW")

    # Sample workflow
    print("Adding users...")
    tipping.db.add_user("alice", "DGKGv8wP8iRJmjdRUEdvVL2b5BywKC65JT")
    tipping.db.add_user("bob", "DBpLvNcR1Zj8B6dKJp4n3XEAT4FmRxbnJb")

    print("Listing wallets...")
    print(tipping.command_list_wallets())

    print("Fetching wallet addresses...")
    print(tipping.command_get_address("alice"))
    print(tipping.command_get_address("bob"))

    print("Sending tips...")
    print(tipping.send_tip("alice", "bob", 12.5))
    print(tipping.send_tip("alice", "bob", 7.5))

    print("Getting tip summary...")
    print(tipping.command_get_tips("alice", "bob"))
EOF
```

---

相关的技术使用方法已在之前的文档中说明。如需改进或扩展功能，请随时联系我们！