---
name: market-maker
description: 为 Turbine 的 BTC 15 分钟预测市场创建一个做市商机器人。在为 Turbine 构建交易机器人时可以使用该机器人。
disable-model-invocation: true
argument-hint: "[algorithm-type]"
---

# Turbine市场做市商机器人生成器

您正在帮助一名程序员为Turbine的比特币15分钟预测市场创建一个市场做市商机器人。

## 第0步：环境上下文检测

在编写Python代码之前，请通过阅读`pyproject.toml`（如果存在）来检查项目的Python版本要求，以确保语法兼容性。

**环境规则：**
- 如果Python版本为3.9及以上：使用现代语法（`list[str]`、`dict[str, int]`、`X | None`）
- 如果Python版本为3.8或更低：使用`from typing import List, Dict, Optional`
- 使用`async`/`await`语法（所有Python 3.9及以上版本都支持）
- 对于数据类，使用`@dataclass`装饰器（Python 3.7及以上版本可用）

## 第1步：环境设置检查

首先，检查用户是否具备所需的设置：

1. 通过查看项目结构来确认是否可以导入`turbine_client`。
2. 检查`.env`文件是否存在，并且其中是否包含了所需的凭据。
3. 如果`.env`文件不存在，请指导用户创建它。

## 第2步：私钥设置

检查`.env`文件中是否设置了`TURBINE_PRIVATE_KEY`。如果没有：

1. 创建一个包含占位符值的`.env`模板文件（切勿要求或处理实际的私钥）：
```
# Turbine Trading Bot Configuration
# IMPORTANT: Add your private key below, then save this file.
# Use a dedicated trading wallet with limited funds.
# Get it from MetaMask: Settings > Security & Privacy > Export Private Key
TURBINE_PRIVATE_KEY=
TURBINE_API_KEY_ID=
TURBINE_API_PRIVATE_KEY=
```
2. 告诉用户在编辑器中打开`.env`文件并自行粘贴他们的私钥。
3. 提醒他们注意安全最佳实践：
   - 使用资金有限的专用交易钱包
   - 绝不要与任何人或任何工具共享您的私钥
   `.env`文件被git忽略，仅保留在本地

切勿要求、接受或写入用户的私钥。用户必须自行编辑`.env`文件。

## 第3步：API密钥自动注册

生成的机器人应在首次运行时使用SDK的`TurbineClient.request_api_credentials()`方法自动注册API凭据。该方法使用EIP-712签名认证（私钥在本地对挑战进行签名——永远不会被传输）。

如果项目中存在`examples/price_action_bot.py`，请阅读并复制其中的凭据注册示例。否则，请使用下面生成的机器人中的模板代码：
```python
# --- Generated bot runtime code (not executed by the agent) ---
import os
import re
from pathlib import Path
from turbine_client import TurbineClient

def get_or_create_api_credentials(env_path: Path = None):
    """Get existing API credentials or register new ones via EIP-712 signature.

    The private key is used locally to sign an authentication challenge.
    It is never transmitted — only the signature is sent to the API.
    """
    if env_path is None:
        env_path = Path(__file__).parent / ".env"

    api_key_id = os.environ.get("TURBINE_API_KEY_ID")
    api_private_key = os.environ.get("TURBINE_API_PRIVATE_KEY")

    if api_key_id and api_private_key:
        print("Using existing API credentials")
        return api_key_id, api_private_key

    private_key = os.environ.get("TURBINE_PRIVATE_KEY")
    if not private_key:
        raise ValueError("Set TURBINE_PRIVATE_KEY in your .env file")

    print("Registering new API credentials...")
    credentials = TurbineClient.request_api_credentials(
        host="https://api.turbinefi.com",
        private_key=private_key,
    )

    api_key_id = credentials["api_key_id"]
    api_private_key = credentials["api_private_key"]

    # Save API keys (not the private key) to .env for future runs
    _append_api_keys_to_env(env_path, api_key_id, api_private_key)
    os.environ["TURBINE_API_KEY_ID"] = api_key_id
    os.environ["TURBINE_API_PRIVATE_KEY"] = api_private_key

    print(f"API credentials saved to {env_path}")
    return api_key_id, api_private_key


def _append_api_keys_to_env(env_path: Path, api_key_id: str, api_private_key: str):
    """Append or update only API key values in an existing .env file.

    Never writes TURBINE_PRIVATE_KEY — that is managed by the user.
    """
    env_path = Path(env_path)
    if not env_path.exists():
        return  # User must create .env themselves

    content = env_path.read_text()
    if "TURBINE_API_KEY_ID=" in content:
        content = re.sub(r'^TURBINE_API_KEY_ID=.*$', f'TURBINE_API_KEY_ID={api_key_id}', content, flags=re.MULTILINE)
    else:
        content = content.rstrip() + f"\nTURBINE_API_KEY_ID={api_key_id}"
    if "TURBINE_API_PRIVATE_KEY=" in content:
        content = re.sub(r'^TURBINE_API_PRIVATE_KEY=.*$', f'TURBINE_API_PRIVATE_KEY={api_private_key}', content, flags=re.MULTILINE)
    else:
        content = content.rstrip() + f"\nTURBINE_API_PRIVATE_KEY={api_private_key}"
    env_path.write_text(content + "\n")
```

## 第4步：算法选择

向用户展示以下用于预测市场的交易算法选项：

**选项1：价格行动交易者（推荐）**
- 使用来自Pyth Network的实时BTC价格（与Turbine使用的预言机相同）
- 将当前价格与市场的执行价格进行比较
- 如果BTC高于执行价格 → 买入（赌价格会保持高位）
- 如果BTC低于执行价格 → 卖出（赌价格会保持低位）
- 根据价格与执行价格的差距调整置信度
- 最适合：初学者，跟随价格走势
- 风险：中等 - 随当前价格行动

**选项2：简单价差做市商**
- 在中间价格附近放置买价和卖价订单，价差固定
- 最适合：学习基础知识，市场稳定时使用
- 风险：中等 - 在趋势市场中可能会积累库存

**选项3：库存意识做市商**
- 根据当前头寸调整报价以降低库存风险
- 偏移价格以鼓励减少头寸的交易
- 最适合：平衡风险敞口
- 风险：较低 - 主动管理库存

**选项4：趋势跟随交易者**
- 从近期交易中检测价格方向
- 当趋势上升时买入，当趋势下降时卖出
- 最适合：趋势市场，突破行情
- 风险：较高 - 可能在反转时判断错误

**选项5：均值回归交易者**
- 通过大幅波动来预测价格回归
- 在价格下跌后买入，在价格上涨后卖出
- 最适合：区间波动市场，过度反应时使用
- 风险：较高 - 可能在趋势反转时判断错误

**选项6：概率加权交易者**
- 使用与50%的距离作为信号
- 打赌极端价格会回归到不确定性范围内
- 最适合：价格过度自信的市场
- 风险：中等 - 基于市场效率假设

## 参考实现

**价格行动交易者**的完整、可生产使用的实现存在于**`examples/price_action_bot.py`中**：
- 在首次交易时签署一个无gas的最大USDC许可
- 所有后续订单使用现有的许可额度（无需每次订单都额外付费）
- 订单大小以USDC为单位，并跟踪头寸

在生成机器人时：
1. **以`examples/price_action_bot.py`为主要参考**
2. 完全复制其结构，仅根据需要自定义配置参数
3. **不要**使用此文档中的简化代码片段——它们是不完整的

对于**其他算法选项**，使用相同的机器人结构，但替换特定于算法的方法：
- `calculate_signal()` - 用所选算法的信号逻辑替换
- `execute_signal()` - 适应算法调整订单放置
- `price_action_loop()` - 重命名并调整主循环以适应算法

参考实现包括所有机器人**必须**保留的关键模式：
- 从API同步头寸（`sync_position()`、`verify_position()`）
- 待处理订单的交易记录（`pending_order_txs`集合）
- 交易验证（检查`failed_trades`、`pending_trades`、`recent_trades`）
- 使用`market_expiring`标志检测市场到期
- 发现之前会话中的未领取奖金
- 限制领取频率（每次领取之间有15秒的延迟）
- 使用异步HTTP客户端进行非阻塞的外部API调用
- 在进入新市场时使用无gas的最大许可（`ensure_settlement_approved()`）
- 基于USDC的订单大小（`calculate_shares_from_usdc()`）
- 以USDC为单位跟踪头寸（`position_usdc`字典）

## 第5步：生成机器人代码

根据用户选择的算法，生成一个完整的机器人文件。机器人应：
1. 从环境变量中加载凭据
2. 如有需要，自动注册API密钥
3. 连接到BTC 15分钟快速市场
4. 实现所选算法
5. 包含适当的错误处理
6. 在关闭时取消订单
7. **自动检测新的BTC市场并切换到这些市场**
8. 平稳处理市场到期
9. **处理无gas的USDC批准**，每次结算合同使用一次性的最大许可
10. **跟踪交易的市场并在市场结算后自动领取奖金**

以`examples/price_action_bot.py`为主要参考

使用`examples/price_action_bot.py`作为所有机器人的结构模板。生成的机器人应遵循此高级结构：
```python
"""
Turbine Market Maker Bot - {ALGORITHM_NAME}
Generated for Turbine

Algorithm: {ALGORITHM_DESCRIPTION}
"""

import asyncio
import os
import time
from dotenv import load_dotenv
import httpx  # For Price Action Trader - fetching BTC price from Pyth Network

from turbine_client import TurbineClient, TurbineWSClient, Outcome, Side
from turbine_client.exceptions import TurbineApiError, WebSocketError

# Load environment variables
load_dotenv()

# ============================================================
# CONFIGURATION - Adjust these parameters for your strategy
# ============================================================
ORDER_SIZE = 1_000_000  # 1 share (6 decimals)
MAX_POSITION = 5_000_000  # Maximum position size (5 shares)
QUOTE_REFRESH_SECONDS = 30  # How often to refresh quotes
# Algorithm-specific parameters added here...

# Credential registration — include get_or_create_api_credentials()
# from Step 3 above (or copy from examples/price_action_bot.py if available)


class MarketMakerBot:
    """Market maker bot implementation with automatic market switching and winnings claiming."""

    def __init__(self, client: TurbineClient):
        self.client = client
        self.market_id: str | None = None
        self.settlement_address: str | None = None  # For USDC approval
        self.contract_address: str | None = None  # For claiming winnings
        self.strike_price: int = 0  # BTC price when market created (6 decimals) - used by Price Action Trader
        self.current_position = 0
        self.active_orders: dict[str, str] = {}  # order_hash -> side
        self.running = True
        # Track markets we've traded in for claiming winnings
        self.traded_markets: dict[str, str] = {}  # market_id -> contract_address
        # Algorithm state...

    async def get_active_market(self) -> tuple[str, int, int]:
        """
        Get the currently active BTC quick market.
        Returns (market_id, end_time, start_price) tuple.
        """
        quick_market = self.client.get_quick_market("BTC")
        return quick_market.market_id, quick_market.end_time, quick_market.start_price

    async def cancel_all_orders(self, market_id: str) -> None:
        """Cancel all active orders on a market before switching."""
        if not self.active_orders:
            return

        print(f"Cancelling {len(self.active_orders)} orders on market {market_id[:8]}...")
        for order_id in list(self.active_orders.keys()):
            try:
                self.client.cancel_order(market_id=market_id, order_id=order_id)
                del self.active_orders[order_id]
            except TurbineApiError as e:
                print(f"Failed to cancel order {order_id}: {e}")

    async def switch_to_new_market(self, new_market_id: str, start_price: int = 0) -> None:
        """
        Switch liquidity and trading to a new market.
        Called when a new BTC 15-minute market becomes active.

        Args:
            new_market_id: The new market ID to switch to.
            start_price: The BTC price when market was created (8 decimals).
                         Used by Price Action Trader to compare against current price.
        """
        old_market_id = self.market_id

        # Track old market for claiming winnings later
        if old_market_id and self.contract_address:
            self.traded_markets[old_market_id] = self.contract_address
            print(f"Tracking market {old_market_id[:8]}... for winnings claim")

        if old_market_id:
            print(f"\n{'='*50}")
            print(f"MARKET TRANSITION DETECTED")
            print(f"Old market: {old_market_id[:8]}...")
            print(f"New market: {new_market_id[:8]}...")
            print(f"{'='*50}\n")

            # Cancel all orders on the old market
            await self.cancel_all_orders(old_market_id)

        # Update to new market
        self.market_id = new_market_id
        self.strike_price = start_price  # Store for Price Action Trader
        self.active_orders = {}

        # Fetch settlement and contract addresses from markets list
        try:
            markets = self.client.get_markets()
            for market in markets:
                if market.id == new_market_id:
                    self.settlement_address = market.settlement_address
                    self.contract_address = market.contract_address
                    print(f"Settlement: {self.settlement_address[:16]}...")
                    print(f"Contract: {self.contract_address[:16]}...")
                    break
        except Exception as e:
            print(f"Warning: Could not fetch market addresses: {e}")

        strike_usd = start_price / 1e6 if start_price else 0
        print(f"Now trading on market: {new_market_id[:8]}...")
        if strike_usd > 0:
            print(f"Strike price: ${strike_usd:,.2f}")

    async def monitor_market_transitions(self) -> None:
        """
        Background task that polls for new markets and triggers transitions.
        Runs continuously while the bot is active.
        """
        POLL_INTERVAL = 5  # Check every 5 seconds

        while self.running:
            try:
                new_market_id, end_time, start_price = await self.get_active_market()

                # Check if market has changed
                if new_market_id != self.market_id:
                    await self.switch_to_new_market(new_market_id, start_price)

                # Log time remaining periodically
                time_remaining = end_time - int(time.time())
                if time_remaining <= 60 and time_remaining > 0:
                    print(f"Market expires in {time_remaining}s - preparing for transition...")

            except Exception as e:
                print(f"Market monitor error: {e}")

            await asyncio.sleep(POLL_INTERVAL)

    # ... Algorithm implementation ...


async def main():
    private_key = os.environ.get("TURBINE_PRIVATE_KEY")
    if not private_key:
        print("Error: Set TURBINE_PRIVATE_KEY in your .env file")
        print("Run: claude \"/turbine-setup\" to get started")
        return

    api_key_id, api_private_key = get_or_create_api_credentials()

    client = TurbineClient(
        host="https://api.turbinefi.com",
        chain_id=137,  # Polygon mainnet
        private_key=private_key,
        api_key_id=api_key_id,
        api_private_key=api_private_key,
    )

    print(f"Bot wallet address: {client.address}")

    quick_market = client.get_quick_market("BTC")
    print(f"Initial market: BTC @ ${quick_market.start_price / 1e6:,.2f}")

    bot = MarketMakerBot(client)

    try:
        await bot.switch_to_new_market(quick_market.market_id, quick_market.start_price)
        await bot.run("https://api.turbinefi.com")
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        bot.running = False
        if bot.market_id:
            await bot.cancel_all_orders(bot.market_id)
        client.close()
        print("Bot stopped cleanly.")


if __name__ == "__main__":
    asyncio.run(main())
```

## 第6步：验证`.env`文件并安装依赖项

1. 检查`.env`文件是否已经存在，并且`TURBINE_PRIVATE_KEY`是否已设置（非空值）。如果没有，那么在第2步中已经创建了模板——提醒用户打开文件并手动添加他们的密钥。

2. 通过运行以下命令安装依赖项：
```bash
pip install -e . python-dotenv httpx
```

注意：`httpx`被价格行动交易者用来从Pyth Network获取实时BTC价格。

## 第7步：解释如何运行和部署

告诉用户：
```
Your bot is ready! To run it:

  python {bot_filename}.py

The bot will:
- Automatically register API credentials on first run (saved to .env)
- Connect to the current BTC 15-minute market
- Gaslessly approve USDC on first trade per settlement (one-time max permit, no gas needed)
- Start trading based on your chosen algorithm
- Automatically switch to new markets when they start
- Track traded markets and claim winnings when they resolve

To stop the bot, press Ctrl+C.


Want to run your bot 24/7 in the cloud? Deploy to Railway (free $5 credit for 30 days):

  claude "/railway-deploy"
```

## 核心机器人运行方法

每个生成的机器人都必须包含这个`run()`方法，该方法处理WebSocket流式传输、自动市场切换和奖金领取：

```python
async def run(self, host: str) -> None:
    """
    Main trading loop with WebSocket streaming, automatic market switching, and winnings claiming.
    """
    ws = TurbineWSClient(host)

    # Start background tasks
    monitor_task = asyncio.create_task(self.monitor_market_transitions())
    claim_task = asyncio.create_task(self.claim_resolved_markets())

    while self.running:
        try:
            # Ensure we have a current market
            if not self.market_id:
                market_id, _ = await self.get_active_market()
                await self.switch_to_new_market(market_id)

            current_market = self.market_id

            async with ws.connect() as stream:
                # Subscribe to the current market
                await stream.subscribe(current_market)
                print(f"Subscribed to market {current_market[:8]}...")

                # Place initial quotes
                await self.place_quotes()

                async for message in stream:
                    # Check if market has changed (set by monitor task)
                    if self.market_id != current_market:
                        print("Market changed, reconnecting to new market...")
                        break  # Exit inner loop to reconnect

                    if message.type == "orderbook":
                        await self.on_orderbook_update(message.orderbook)
                    elif message.type == "trade":
                        await self.on_trade(message.trade)
                    elif message.type == "order_cancelled":
                        self.on_order_cancelled(message.data)

        except WebSocketError as e:
            print(f"WebSocket error: {e}, reconnecting...")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            await asyncio.sleep(5)

    # Cleanup background tasks
    monitor_task.cancel()
    claim_task.cancel()
```

## 算法实现细节

在生成机器人时，使用以下实现：

### 价格行动交易者（推荐）

**⚠️ 重要提示：使用`examples/price_action_bot.py`中的参考实现**

请阅读该文件以获取完整的、可生产使用的实现。下面的简化代码片段是不完整的，缺少关键模式。

**参考实现中的关键方法：**

- `get_current_btc_price()` - 从Pyth Network获取BTC价格（异步，非阻塞）
- `calculate_signal()` - 根据价格与执行价格返回（行动、置信度）
- `execute_signal()` - 正确地放置订单并进行验证
- `price_action_loop()` - 主交易循环
- `sync_position()` / `verify_position()` - 头寸管理
- `cleanup_pending_orders()` - 处理待处理的订单
- `discover_unclaimed_markets()` - 发现之前会话中的奖金

**参考实现处理的内容（以下代码片段未处理）：**

- 用于非阻塞价格获取的异步HTTP客户端
- 每次尝试放置订单后的头寸验证
- 防止重复下单的待处理订单跟踪
- 提交订单后立即检测失败的交易
- 在市场到期前60秒停止交易的标志
- 处理交易ID以避免重复计算成交
- 限制领取频率，每次领取之间有15秒的延迟

**算法概述：**

- 从Pyth Network获取当前BTC价格（与Turbine使用的预言机相同）
- 将当前价格与市场的执行价格（存储在`quick_market.start_price`中，6位小数）进行比较
- 如果BTC高于执行价格一定阈值 → 买入（YES）
- 如果BTC低于执行价格一定阈值 → 卖出（NO）
- 置信度根据价格与执行价格的差距调整（上限为90%）

### 简单价差做市商
```python
SPREAD_BPS = 200  # 2% total spread (1% each side)

def calculate_quotes(self, mid_price):
    """Calculate bid/ask around mid price."""
    half_spread = (mid_price * SPREAD_BPS) // 20000
    bid = max(1, mid_price - half_spread)
    ask = min(999999, mid_price + half_spread)
    return bid, ask
```

### 库存意识做市商
```python
SPREAD_BPS = 200
SKEW_FACTOR = 50  # BPS skew per share of inventory

def calculate_quotes(self, mid_price):
    """Skew quotes based on inventory."""
    half_spread = (mid_price * SPREAD_BPS) // 20000

    # Skew to reduce inventory
    inventory_shares = self.current_position / 1_000_000
    skew = int(inventory_shares * SKEW_FACTOR)

    bid = max(1, mid_price - half_spread - skew)
    ask = min(999999, mid_price + half_spread - skew)
    return bid, ask
```

### 趋势跟随做市商
```python
MOMENTUM_WINDOW = 10  # Number of trades to consider
MOMENTUM_THRESHOLD = 0.6  # 60% same direction = trend

def detect_momentum(self, recent_trades):
    """Detect market momentum from recent trades."""
    if len(recent_trades) < MOMENTUM_WINDOW:
        return None

    buys = sum(1 for t in recent_trades[-MOMENTUM_WINDOW:] if t["side"] == "BUY")
    buy_ratio = buys / MOMENTUM_WINDOW

    if buy_ratio > MOMENTUM_THRESHOLD:
        return "UP"
    elif buy_ratio < (1 - MOMENTUM_THRESHOLD):
        return "DOWN"
    return None
```

### 均值回归
```python
REVERSION_THRESHOLD = 50000  # 5% move triggers fade
LOOKBACK_TRADES = 20

def should_fade(self, current_price, recent_trades):
    """Check if price moved enough to fade."""
    if len(recent_trades) < LOOKBACK_TRADES:
        return None

    avg_price = sum(t["price"] for t in recent_trades) / len(recent_trades)
    deviation = current_price - avg_price

    if deviation > REVERSION_THRESHOLD:
        return "SELL"  # Fade the up move
    elif deviation < -REVERSION_THRESHOLD:
        return "BUY"  # Fade the down move
    return None
```

### 概率加权做市商
```python
EDGE_THRESHOLD = 200000  # 20% from 50% = extreme

def find_edge(self, best_bid, best_ask):
    """Look for mispriced extremes."""
    mid = (best_bid + best_ask) // 2
    distance_from_fair = abs(mid - 500000)

    if distance_from_fair > EDGE_THRESHOLD:
        if mid > 500000:
            return "SELL"  # Market too bullish
        else:
            return "BUY"  # Market too bearish
    return None
```

## 自动市场切换

**所有生成的机器人都会自动处理市场切换。**当BTC 15分钟市场到期时：

1. **检测**：机器人每5秒检查一次新市场
2. **订单清理**：取消到期市场上的所有活跃订单
3. **无缝切换**：机器人自动连接到新市场
4. **继续交易**：在新市场上自动恢复交易

**工作原理：**
- 一个后台任务（`monitor_market_transitions`）持续运行
- 它将当前市场ID与API中的活跃市场进行比较
- 当检测到新市场时，`switch_to_new_market()`处理切换
- 头寸会保留（基于钱包），但订单需要重新放置

**到期前的警告：**
- 当剩余时间少于60秒时，机器人会发出警告
- 主动取消订单，以避免在到期市场上出现卡住的订单

## USDC批准

机器人使用**一次性的无gas最大许可**进行USDC批准。在每个结算合同的第一次交易时，机器人会签署一个EIP-2612最大许可（最大值，最大截止日期），并通过中继器提交。不需要使用原生gas。

```python
def ensure_settlement_approved(self, settlement_address: str) -> None:
    """Ensure USDC is approved for this settlement contract via gasless max permit."""
    if settlement_address in self.approved_settlements:
        return

    # Check on-chain allowance
    current = self.client.get_usdc_allowance(spender=settlement_address)
    if current >= MAX_APPROVAL_THRESHOLD:  # half of max uint256
        self.approved_settlements[settlement_address] = current
        return

    # Sign and submit gasless max permit via relayer
    result = self.client.approve_usdc_for_settlement(settlement_address)
    # Wait for TX confirmation...
    self.approved_settlements[settlement_address] = 2**256 - 1
```

**关键点：**

- 在进入每个新市场时调用`ensure_settlement_approved()`
- 如果提交的订单没有`permit_signature`字段——使用现有的许可额度
- 不需要原生gas令牌（中继器支付gas）
- 每个结算合同仅使用一次——所有未来的订单重用该许可额度
- 订单大小以USDC为单位，根据价格转换为份额

## 自动领取奖金

**机器人必须跟踪它们交易过的市场，并在市场结算后自动领取奖金。**

### 实现模式

在您的机器人类中添加以下字段：
```python
class MarketMakerBot:
    def __init__(self, client: TurbineClient):
        self.client = client
        self.market_id: str | None = None
        self.settlement_address: str | None = None
        self.contract_address: str | None = None  # Current market contract
        self.current_position = 0
        self.active_orders: dict[str, str] = {}
        self.running = True
        # Track markets we've traded in for claiming winnings
        # market_id -> contract_address
        self.traded_markets: dict[str, str] = {}
```

### 切换市场时跟踪市场

在切换到新市场时，保存旧市场以供后续领取：
```python
async def switch_to_new_market(self, new_market_id: str, start_price: int = 0) -> None:
    """Switch liquidity to a new market.

    Args:
        new_market_id: The new market ID.
        start_price: BTC strike price (6 decimals) - used by Price Action Trader.
    """
    old_market_id = self.market_id

    # Track old market for claiming winnings later
    if old_market_id and self.contract_address:
        self.traded_markets[old_market_id] = self.contract_address
        print(f"Tracking market {old_market_id[:16]}... for winnings claim")

    if old_market_id:
        await self.cancel_all_orders()

    self.market_id = new_market_id
    self.strike_price = start_price  # Store for Price Action Trader
    self.active_orders = {}

    # Fetch settlement and contract addresses
    markets = self.client.get_markets()
    for market in markets:
        if market.id == new_market_id:
            self.settlement_address = market.settlement_address
            self.contract_address = market.contract_address
            break

    if start_price:
        print(f"Strike price: ${start_price / 1e6:,.2f}")
```

### 领取奖金的背景任务

添加一个后台任务来检查已结算的市场并领取奖金：
```python
async def claim_resolved_markets(self) -> None:
    """Background task to claim winnings from resolved markets."""
    while self.running:
        try:
            if not self.traded_markets:
                await asyncio.sleep(30)
                continue

            markets_to_remove = []
            for market_id, contract_address in list(self.traded_markets.items()):
                try:
                    # Check if market is resolved
                    markets = self.client.get_markets()
                    market_resolved = False
                    for market in markets:
                        if market.id == market_id and market.resolved:
                            market_resolved = True
                            break

                    if market_resolved:
                        print(f"\nMarket {market_id[:16]}... has resolved!")
                        print(f"Attempting to claim winnings...")
                        try:
                            result = self.client.claim_winnings(contract_address)
                            tx_hash = result.get("txHash", result.get("tx_hash", "unknown"))
                            print(f"Winnings claimed! TX: {tx_hash}")
                            markets_to_remove.append(market_id)
                        except TurbineApiError as e:
                            if "no winnings" in str(e).lower() or "no position" in str(e).lower():
                                print(f"No winnings to claim for {market_id[:16]}...")
                                markets_to_remove.append(market_id)
                            else:
                                print(f"Failed to claim winnings: {e}")
                except Exception as e:
                    print(f"Error checking market {market_id[:16]}...: {e}")

            # Remove claimed markets from tracking
            for market_id in markets_to_remove:
                self.traded_markets.pop(market_id, None)

        except Exception as e:
            print(f"Claim monitor error: {e}")

        await asyncio.sleep(30)  # Check every 30 seconds
```

### 启动领取任务

在`run()`方法中，启动领取奖金的任务以及其他后台任务：
```python
async def run(self, host: str) -> None:
    """Main trading loop with automatic market switching and winnings claiming."""
    ws = TurbineWSClient(host=host)

    # Start background tasks
    monitor_task = asyncio.create_task(self.monitor_market_transitions())
    claim_task = asyncio.create_task(self.claim_resolved_markets())

    try:
        # ... main trading loop ...
    finally:
        monitor_task.cancel()
        claim_task.cancel()
```

**关键点：**
- `claim_winnings(contract_address)`使用无gas的EIP-712许可
- API通过中继器处理所有链上赎回
- 市场在成功领取后或没有头寸时从跟踪中移除
- 每30秒检查一次以及时发现结算情况

## 关键模式（来自examples/price_action_bot.py）

这些模式在参考示例中已经实现，并且**必须**在所有生成的机器人中保留：

### 头寸跟踪

- `current_position`跟踪净头寸（YES份额 - NO份额）
- `sync_position()`在市场切换时从API获取
- `verify_position()`在订单后纠正内部跟踪

### 待处理订单管理

- `pending_order_txs: set[str]`跟踪正在结算的订单的交易哈希
- 在有任何待处理订单时不要放置新订单
- `cleanup_pending_orders()`检查API并清除已结算的交易

### 交易验证流程

放置订单后：
1. 等待2秒以完成处理
2. 检查`get_failed_trades()`以获取立即失败的交易
3. 检查`get_pending_trades()`以获取链上结算的情况
4. 检查`get_trades()`以获取已完成的交易
5. 检查`get_orders()`以获取未完成的订单
6. 调用`verify_position()`以从API同步信息

### 市场到期处理

- 当`market_expiring`标志设置为`True`时，表示市场即将到期（剩余时间少于60秒）
- 在标志为`True`时不要放置新订单
- 在切换到新市场时重置标志
- 在市场切换时清除`processed_trade_ids`和`pending_order_txs`

### 奖金领取

- `discover_unclaimed_markets()`查找之前会话中的头寸
- 扫描所有用户头寸，找出在已结算市场中的盈利份额
- 将发现的市场添加到领取跟踪列表中
- 领取奖金时限制频率，每次领取之间有15秒的延迟

## 对用户的重要提示

- **风险警告**：交易涉及风险。从小额开始交易。
- **先在测试网测试**：考虑先在Base Sepolia（chain_id=84532）上进行测试。
- **监控头寸**：始终监控您的机器人并设置止损逻辑。
- **市场到期**：BTC 15分钟市场到期时间很短。机器人会自动处理！
- **Gas/费用**：在Polygon上进行交易时gas成本很低，但请注意费用。
- **连续运行**：机器人设计为24/7运行，自动在市场之间切换。
- **USDC批准**：机器人使用每次结算合同一次性的无gas最大许可。不需要原生gas。

## 快速参考

**价格缩放**：价格范围为0-1,000,000，表示0-100%
- 500000 = 50%的概率
- 250000 = 25%的概率

**大小缩放**：大小使用6位小数
- 1_000_000 = 1份
- 500_000 = 0.5份

**结果值**：
- 结果.YES (0) = BTC价格高于执行价格
- 结果.NO (1) = BTC价格低于执行价格

**执行价格（对于价格行动交易者）：**
- 可通过`quick_market.start_price`获取（6位小数）
- 示例：95000000000 = $95,000.00
- 从Pyth Network获取的当前BTC价格（与Turbine使用的预言机相同）：
  - URL：`https://hermes.pyth.network/v2/updates/price/latest?ids[]=0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43`
  - BTC数据源ID：`0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43`
- 如果当前价格 > 执行价格 → 买入（YES），如果当前价格 < 执行价格 → 卖出（NO）