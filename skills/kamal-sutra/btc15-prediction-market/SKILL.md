**BTC15 自主预测市场**  
这是一个完全自主的 BTC 预测市场，由三个协同工作的代理共同运作，它们使用 USDC 作为交易媒介。  

**问题**  
大多数预测市场在流动性、交易或结果结算方面都需要人工干预，这限制了系统的可扩展性，并阻碍了真正基于智能合约的经济系统的实现。  

**技术特点**  
该系统实现了完全自主的预测市场循环：  
- **代理角色**：  
  - **Maker 代理**：持续提供流动性，通过铸造“YES/NO”类型的合约份额并发布出售报价。  
  - **Trader 代理**：监控 BTC 价格走势，并根据预设的阈值进行方向性投注。  
  - **Resolver 代理**：在每轮交易开始和结束时获取 BTC 价格数据，确定市场结果，并自动兑付奖金。  
- **经济循环**：每一轮交易都遵循以下流程：  
  1. Maker 代理以 USDC 提供流动性。  
  2. Trader 代理观察 BTC 价格变化并下注。  
  3. 轮次结束。  
  4. Resolver 代理根据外部价格数据确定结果。  
  5. 合同在链上自动执行（on-chain）。  
  6. 奖金自动兑付。  
  7. 资金被重新用于下一轮交易。  
- **关键特性**：  
  - **完全自主**：系统启动后无需人工干预。  
  - **USDC 结算**：使用 USDC 作为代理间的稳定交易单位。  
  - **持续运行**：代理可以无限期地运行。  
  - **链上结算**：所有交易和结果都在链上完成。  

**安装步骤**  
1. 克隆项目代码：  
   ```bash
   git clone https://github.com/kamal-sutra/clawbtc15.git
   cd clawbtc15
   ```  
2. 安装 Python 相关依赖库：  
   ```bash
   pip install web3 python-dotenv requests
   ```  
3. 创建环境配置文件（`.env`）：  
   ```bash
   cp .env.example .env
   ```  
4. 设置环境变量：  
   ```bash
   RPC=https://sepolia.base.org
   MARKET=0x03956BC8745618eCCD7670073f7cAa717caDC5F4
   USDC=0x036cbd53842c5426634e7929541ec2318f3dcf7e
   MAKER_KEY=<your maker private key>
   TRADER_KEY=<your trader private key>
   RESOLVER_KEY=<your resolver private key>
   ```  

**命令使用**  
- 运行 Maker 代理：  
  ```bash
   run-maker
   ```  
- 运行 Trader 代理：  
  ```bash
   run-trader
   ```  
- 运行 Resolver 代理：  
  ```bash
   run-resolver
   ```  
- 同时运行所有代理：  
  ```bash
   run-all
   ```  

**合同详情**  
- **运行环境**：基于 Sepolia 区块链。  
- **交易媒介**：使用 USDC 进行交易。  

**应用场景**  
- 适用于基于智能合约的自主交易系统。  
- 支持完全自主的市场运作机制。  
- 实现代理间的链上经济协调。  
- 适用于连续性的预测市场场景。  

**开发背景**  
该项目是为 2026 年 2 月的 USDC 霸客赛（USDC Hackathon）开发的。