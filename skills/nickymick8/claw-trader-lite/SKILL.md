**如何自行创建该文件：**


1. **创建目录：**
   ```bash
   mkdir -p ~/.openclaw/workspace/skills/claw-trader-lite
   ```

2. **创建文件：**
   ```bash
   cat > ~/.openclaw/workspace/skills/claw-trader-lite/SKILL.md << 'EOF'
   ```
   
   ```markdown
   # 创建文件
   ```
   
   # 名称：claw-trader-lite
   ```
   
   **描述：**
   ```
   | 
   · 免费的、仅限读取的市场监控工具，适用于Hyperliquid和LN Markets。
   · 实时显示价格，查看公开账户余额，并监控DeFi及比特币衍生品平台上的持仓情况。
   · 完全无需私钥。
   ```
   
   **环境变量：**
   ```
   ```
   HYPERLIQUID_ACCOUNT_ADDRESS:
       description: "可选：用于查看余额/持仓的Hyperliquid钱包地址（例如：0x...）"
       required: false
   ```
   
   ```markdown
   
   **Claw Trader Lite**
   ```
   
   ***Hyperliquid和LN Markets的免费、仅限读取的市场监控工具。***
   ```
   实时监控价格，追踪投资组合，并查看DeFi及比特币衍生品平台上的持仓情况。非常适合在不承担执行风险的情况下监控交易情况。
   
   ```markdown
   
   **功能说明：**
   Claw Trader Lite提供**仅限读取**的市场数据和账户信息。它可以查看价格、余额和持仓情况，但**无法执行交易**——因此在任何环境中使用都非常安全。
   
   **支持的平台：**
   ```
   - **Hyperliquid**：DeFi衍生品（ETH、SOL、AVAX及100多种山寨币）
   - **LN Markets**：通过Lightning Network提供的比特币衍生品
   ```
   
   **主要特性：**
   ```
   ✅ **实时价格推送**：实时显示BTC、ETH、SOL等主要资产的价格
   ✅ **投资组合概览**：一目了然地查看余额和持仓情况
   ✅ **零风险**：仅限读取数据，无需私钥或API密钥
   ✅ **轻量级设计**：依赖性极低，可在任何环境中运行
   ✅ **永久免费**：无费用、无限制、无隐藏费用
   ```
   
   **安装方法：**
   ```bash
   pip install requests
   ```
   
   **快速入门：**
   ```python
   from claw_lite import create_monitor

   # 创建监控实例
   monitor = create_monitor()

   # 获取当前价格
   btc_price = monitor.get_price("BTC", "lnmarkets")
   eth_price = monitor.get_price("ETH", "hyperliquid")
   sol_price = monitor.get_price("SOL", "hyperliquid")
   print(f"BTC: {btc_price:,.2f}")
   print(f"ETH: {eth_price:,.2f}")
   print(f"SOL: {sol_price:,.2f}")
   ```
   
   **使用示例：**
   ```python
   # 获取单一资产的价格
   # 从LN Markets获取比特币价格
   btc_price = monitor.get_price("BTC", "lnmarkets")
   # 从Hyperliquid获取以太坊价格
   eth_price = monitor.get_price("ETH", "hyperliquid")
   
   # 获取多个资产的价格
   assets = ["BTC", "ETH", "SOL", "AVAX"]
   prices = monitor.get_prices(assets, "hyperliquid")
   for asset, price in prices.items():
       print(f"{asset}: {price:,.2f}")
   ```
   
   **查看账户余额（Hyperliquid）：**
   ```
   # 注意：需要设置您的公开钱包地址
   export HYPERLIQUID_ACCOUNT_ADDRESS="0xYourAddressHere"
   balance = monitor.get_balance("hyperliquid")
   print(f"账户余额：{balance:,.2f}")
   ```
   
   **查看持仓情况（Hyperliquid）：**
   ```
   # 注意：需要设置HYPERLIQUID_ACCOUNT_ADDRESS
   positions = monitor.get_positions("hyperliquid")
   for pos in positions:
       print(f"{pos['coin']}: {pos['size']} @ ${pos['entryPx}")
   ```
   
   **平台特定说明：**
   ```
   **Hyperliquid：**
   - 支持100多种山寨币
   - 查看余额/持仓需要设置HYPERLIQUID_ACCOUNT_ADDRESS环境变量
   - 使用公开API接口（获取价格时无需认证）
   
   **LN Markets：**
   - 专注于比特币
   - 价格数据为公开信息
   - 查看余额/持仓需要认证（Lite版本不支持）
   ```
   
   **API参考：**
   ```python
   def create_monitor():
       # 创建新的MarketMonitor实例
       return MarketMonitor()

   def get_price(asset, platform):
       # 获取指定资产在指定平台上的当前价格
       return market_monitor.get_price(asset, platform)

   def get_prices(assets, platform):
       # 同时获取多个资产的价格
       return market_monitor.get_prices(assets, platform)

   def get_balance/platform):
       # 获取指定平台的账户余额
       return market_monitor.get_balance/platform)

   def get_positions/platform):
       # 获取指定平台的持仓情况
       return market_monitor.get_positions/platform)
   ```
   
   **环境变量：**
   ```
   | 变量                | 是否必需 | 描述                                                         |
   | --------------------------- | -------- | ---------------------------------------------------------- |
   | HYPERLIQUID_ACCOUNT_ADDRESS | 可选 | 用于查看余额/持仓的Hyperliquid钱包地址                 |
   ```
   
   **限制：**
   ```
   · 仅提供读取功能：只能查看价格、余额和持仓情况
   · 无法执行交易或下达订单
   · 无法管理持仓
   ```
   
   **故障排除：**
   ```
   * 错误提示“Error fetching price”*
     - 检查网络连接
     - 确保资产符号正确（某些平台对大小写敏感）
     - 重新尝试（可能是临时性的API问题）
   
   * “HYPERLIQUID_ACCOUNT_ADDRESS未设置”*
     - 请导出您的钱包地址：`export HYPERLIQUID_ACCOUNT_ADDRESS="0x..."`
     * 或在代码中直接设置（不建议在共享环境中使用）
   ```
   
   **注意：**
   - LN Markets的余额数据需要认证
   - Lite版本仅提供公开的价格数据
   ```
   
   **技术细节：**
   ```
   **依赖库：**
   - `requests`：用于API请求的HTTP库
   **数据来源：**
   - Hyperliquid公开API（https://api.hyperliquid.xyz）
   - LN Markets公开API（https://api.lnmarkets.com）
   ```
   
   **许可证：** MIT许可证
   
   **关于：**
   ```
   专为希望获得简单、免费市场监控服务的交易者设计，无复杂操作和风险。
   
   🦞 永久免费。无需注册，无需API密钥。
   ```