---

name: dogecoin-node

version: 1.0.3

description: >
  **技能：配置并运行具有 RPC 访问功能、区块链工具以及可选的小费功能的 Dogecoin Core 全节点**
  **技能描述：**  
  本技能涵盖了如何设置和操作一个完整的 Dogecoin Core 节点，使其具备以下功能：  
  1. **RPC 访问**：允许通过远程过程调用（Remote Procedure Call）与 Dogecoin Core 服务器进行交互。  
  2. **区块链工具**：提供用于查询、分析和操作 Dogecoin 区块链的数据和工具。  
  3. **可选的小费功能**：用户可以选择是否为服务提供者提供小费（通过特定的交易方式）。  
  **技能要求：**  
  - 熟悉 Dogecoin Core 的基本架构和命令行接口（CLI）。  
  - 理解区块链技术的基本原理。  
  - 具备基本的 shell 或终端操作技能。  
  **技能应用场景：**  
  - 用于开发 Dogecoin 相关的应用程序或服务。  
  - 用于维护和优化 Dogecoin 网络的节点。  
  **技能步骤：**  
  1. **安装 Dogecoin Core：**  
     - 从官方渠道下载并安装 Dogecoin Core 的最新版本。  
     - 配置必要的环境变量（如 PATH、JAVA_HOME 等）。  
  2. **配置网络参数：**  
     - 设置节点的 IP 地址、端口以及网络配置（如比特币网络的默认参数）。  
  3. **启动节点：**  
     - 使用相应的命令启动 Dogecoin Core 节点。  
     - 监控节点的运行状态和日志以确认其正常运行。  
  4. **配置 RPC 服务：**  
     - 根据需要配置 RPC 服务的访问权限和安全性设置。  
  5. **集成区块链工具：**  
     - 编写脚本或使用现有的工具来查询、下载或上传 Dogecoin 块链数据。  
  6. **启用小费功能（可选）：**  
     - 根据项目需求，配置小费功能的实现细节（如接收小费的地址、交易类型等）。  
  7. **测试和调试：**  
     - 对节点进行全面的测试，确保所有功能正常工作。  
     - 根据测试结果进行必要的调试和优化。  
  **注意事项：**  
  - 请确保遵循 Dogecoin Core 的官方文档和社区指南进行操作。  
  - 定期更新 Dogecoin Core 以获取最新的安全补丁和功能改进。  
  - 对于涉及敏感数据（如私钥）的操作，请采取适当的安全措施。

---

# Dogecoin 节点技能

该技能旨在通过 RPC 完全自动化 Dogecoin Core 全节点及其命令行界面（CLI）的集成与操作，从而支持各种用例下的区块链工具和钱包管理，包括使用 SQLite 实现的小费功能。

## 功能

1. **获取钱包余额**

    - 获取指定 Dogecoin 钱包地址的当前余额。

    - 示例：`/dogecoin balance <wallet_address>`


2. **发送 DOGE**

    - 从已连接的钱包向指定地址发送 Dogecoin。

    - 示例：`/dogecoin send <recipient_address> <amount>`


3. **查看交易记录**

    - 获取钱包的最近交易详情。

    - 示例：`/dogecoin txs <wallet_address>`


4. **查询 DOGE 价格**

    - 获取最新的 Dogecoin 价格（以美元计）。

    - 示例：`/dogecoin price`


5. **帮助命令**

    - 显示命令的相关帮助信息。

    - 示例：`/dogecoin help`


## 安装

### 先决条件

1. 一个已完全同步的 Dogecoin Core RPC 节点。

2. 在 `dogecoin.conf` 文件中配置了 Dogecoin 的 `rpcuser` 和 `rpcpassword`。

3. OpenClaw Gateway 已更新至最新版本。


### 配置节点的步骤

1. **安装二进制文件并下载 Dogecoin Core**

```bash

cd ~/downloads

curl -L -o dogecoin-1.14.9-x86_64-linux-gnu.tar.gz \

  https://github.com/dogecoin/dogecoin/releases/download/v1.14.9/dogecoin-1.14.9-x86_64-linux-gnu.tar.gz

```


2. 解压并放置二进制文件

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


4. **配置 RPC 凭据（仅限本地主机）**

```bash

cat > ~/.dogecoin/dogecoin.conf <<'EOF'

server=1

daemon=1

listen=1

# optional: disable inbound until port-forwarding is set

# listen=0

rpcbind=127.0.0.1

rpcallowip=127.0.0.1

rpcuser=<strong-username>

rpcpassword=<strong-password>

txindex=1

EOF

```


5. 启动并同步节点

```bash

./dogecoind -datadir=$HOME/.dogecoin -daemon


```


检查同步状态：


```bash

./dogecoin-cli -datadir=$HOME/.dogecoin getblockcount

./dogecoin-cli -datadir=$HOME/.dogecoin getblockchaininfo


```


优雅地停止节点：


```bash

./dogecoin-cli -datadir=$HOME/.dogecoin stop


```


## 示例用法

（所有 Telegram 命令均可通过 Dogecoin CLI 实现；建议将所有 RPC/CLI 命令也添加到 Telegram 命令中）

* `/dogecoin balance D8nLvyHGiDDjSm2UKnWxWehueu5Me5wTix`


* `/dogecoin send D8nLvyHGiDDjSm2UKnWxWehueu5Me5wTix 10`


* `/dogecoin txs D8nLvyHGiDDjSm2UKnWxWehueu5Me5wTix`


* `/dogecoin price`


* `/dogecoin help`


## RPC/CLI 命令速查表

以下是常用的 Dogecoin CLI 命令列表。使用这些命令与节点进行交互；如需查看完整命令列表，请执行 `./dogecoin-cli help`。


### 区块链相关命令


```bash

./dogecoin-cli getblockcount # Get the current block height

./dogecoin-cli getbestblockhash # Get the hash of the latest block

./dogecoin-cli getblockchaininfo # Detailed blockchain stats

./dogecoin-cli getblockhash 1000 # Get the hash of block 1000

./dogecoin-cli getblock <blockhash> # Details for a specific block


```


### 网络相关命令


```bash

./dogecoin-cli getconnectioncount # Number of connections to the network

./dogecoin-cli getpeerinfo # Info about connected peers

./dogecoin-cli addnode <address> onetry # Try a one-time connection to a node

./dogecoin-cli ping # Ping all connected nodes


```


### 钱包相关命令


```bash

./dogecoin-cli getwalletinfo # Wallet details (balance, keys, etc.)

./dogecoin-cli sendtoaddress <address> <amount> # Send Dogecoin to an address

./dogecoin-cli listunspent # List all unspent transactions

./dogecoin-cli getnewaddress # Generate a new receiving address

./dogecoin-cli dumpprivkey <address> # Export private key for an address (use with caution)


```


### 实用工具命令


```bash

./dogecoin-cli stop # Stop the Dogecoin node safely

./dogecoin-cli help # List all available commands and usage details


```


对于未列出的动态查询需求，请随时参考：`./dogecoin-cli help`。


---

## 自动化健康检查（可选功能）：

该文件可作为维护 Dogecoin 节点运行状态的主要验证工具。


### 健康检查脚本设置：

1. 要启用健康检查功能，请在此位置（`.openwork/workspace/archive/health/`）创建 `doge_health_check.sh` 文件，并添加以下代码：


```bash

mkdir -p ~/.openwork/workspace/archive/health/


cat > ~/.openwork/workspace/archive/health/doge_health_check.sh <<'EOF'

#!/bin/bash


# --- Dogecoin Health Check Automation ---

# Target: ~/.openwork/workspace/archive/health/doge_health_check.sh


echo "Starting Health Check: $(date)"


# 1. Check if Dogecoin Node is Running

if pgrep -x "dogecoind" > /dev/null; then

    echo "[PASS] Dogecoin node process detected."

else

    echo "[FAIL] Dogecoin node is offline. Attempting to start..."

    ~/dogecoind -datadir=$HOME/.dogecoin -daemon

fi


# 2. Check Node Connectivity (Peers)

PEERS=$(~/dogecoin-cli getconnectioncount 2>/dev/null)

if [[ "$PEERS" -gt 0 ]]; then

    echo "[PASS] Node is connected to $PEERS peers."

else

    echo "[WARN] Node has 0 peers. Checking network..."

fi


# 3. Check Disk Space (Alert if < 10GB)

FREE_GB=$(df -BG ~/.dogecoin | awk 'NR==2 {print $4}' | sed 's/G//')

if [ "$FREE_GB" -lt 10 ]; then

    echo "[CRITICAL] Low Disk Space: Only ${FREE_GB}GB remaining!"

fi


# 4. Validate Tipping Database Integrity

DB_PATH="$HOME/.openwork/workspace/archive/tipping/dogecoin_tipping.db"

if [ -f "$DB_PATH" ]; then

    DB_CHECK=$(sqlite3 "$DB_PATH" "PRAGMA integrity_check;")

    if [ "$DB_CHECK" == "ok" ]; then

        echo "[PASS] Tipping database integrity verified."

    else

        echo "[FAIL] Database Error: $DB_CHECK"

    fi

else

    echo "[INFO] Tipping database not yet created."

fi


echo "Health Check Complete."

EOF


```


# 5. 授予执行权限

chmod +x ~/.openwork/workspace/archive/health/doge_health_check.sh


---

## 小费集成（可选功能）：

在设置并同步节点后，您可以启用小费功能。该功能允许您发送 Dogecoin 小费、维护用户钱包数据库并记录交易记录。


### 小费脚本设置：

1. 要启用小费功能，请在此位置（`.openwork/workspace/archive/tipping/`）创建 `dogecoin_tipping.py` 文件，并添加以下代码：


```bash

mkdir -p ~/.openwork/workspace/archive/tipping/


cat > ~/.openwork/workspace/archive/tipping/dogecoin_tipping.py <<'EOF'

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

    tipping.db.add_user("alice", "D6c9nY8GMEiHVfRA8ZCd8k9ThzLbLc7nfj")

    tipping.db.add_user("bob", "DA2SwTnNNMFJcLjZoRNBrurnzGRFchy54g")


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

相关技术细节已在前文文档中说明。如需优化或扩展功能，请随时联系我们！