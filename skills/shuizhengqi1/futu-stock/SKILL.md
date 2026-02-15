---
name: futu-stock
description: 通过MCP服务器访问富途（Futu）的股票市场数据——包括实时报价、K线图、期权信息以及香港/美国/中国市场的账户信息。
metadata: {"openclaw": {"emoji": "📈", "requires": {"bins": ["python3", "futu-mcp-server"], "env": ["FUTU_HOST", "FUTU_PORT"]}, "primaryEnv": "FUTU_HOST"}}
version: 1.0.0
---

# futu-stock 技能

该技能提供了对 Futu 股票市场数据 MCP 服务器的动态访问功能，支持实时报价、历史 K 线图、期权数据以及香港、美国和中国的股票市场账户信息。

## 先决条件

在使用此技能之前，您需要设置两个组件：

### 1. 安装 futu-stock-mcp-server

安装 MCP 服务器包：

```bash
pip install futu-stock-mcp-server
```

**仓库**: https://github.com/shuizhengqi1/futu-stock-mcp-server

安装完成后，验证命令是否可用：

```bash
which futu-mcp-server
# or
futu-mcp-server --help
```

### 2. 安装并配置 Futu OpenD

Futu OpenD 是连接 Futu 交易平台的网关服务。在使用此技能之前，必须先安装并运行它。

**安装指南**: https://openapi.futunn.com/futu-api-doc/opend/opend-cmd.html

**快速设置步骤**：
1. **下载适用于您平台的 OpenD**（Windows/MacOS/CentOS/Ubuntu）
2. **解压**包文件，并找到以下文件：
   - `FutuOpenD.xml`（或 `OpenD.xml`）- 配置文件
   - `Appdata.dat` - 必需的数据文件
3. **配置 `FutuOpenD.xml`：
   - 设置 `login_account`：您的 Futu 账户（平台 ID、电子邮件或电话）
   - 设置 `login_pwd`：您的登录密码（或使用 `login_pwd_md5` 表示 MD5 哈希值）
   - 设置 `api_port`：API 端口（默认：11111）
   - 设置 `ip`：监听地址（默认：127.0.0.1）
4. **测试运行**：启动 OpenD 以验证配置：
   ```bash
   # Windows
   FutuOpenD.exe
   
   # Linux
   ./FutuOpenD
   
   # MacOS
   ./FutuOpenD.app/Contents/MacOS/FutuOpenD
   ```
5. **在后台运行**：验证配置无误后，使用 `nohup` 在后台启动 OpenD：
   ```bash
   # Linux/MacOS
   nohup ./FutuOpenD > opend.log 2>&1 &
   
   # Or with specific config file
   nohup ./FutuOpenD -cfg_file=/path/to/FutuOpenD.xml > opend.log 2>&1 &
   ```

**重要说明**：
- 使用此技能之前，必须确保 OpenD 正在运行。
- 默认 API 端口为 `11111`（在 `FutuOpenD.xml` 中进行配置）。
- 确保 OpenD 可以在配置的 `FUTU_HOST` 和 `FUTU_PORT` 上访问。
- 在生产环境中，建议使用进程管理器（如 systemd、supervisor 等）而不是 `nohup`。

### 3. 验证设置

两个组件都安装完成后：

1. **检查 OpenD 是否正在运行**：
   ```bash
   # Check if port is listening
   netstat -an | grep 11111
   # or
   lsof -i :11111
   ```

2. **测试 MCP 服务器连接**：
   ```bash
   # Set environment variables
   export FUTU_HOST=127.0.0.1
   export FUTU_PORT=11111
   
   # Test MCP server
   futu-mcp-server
   ```

如果一切配置正确，您就可以使用此技能了。

## 完整设置流程

**完整设置过程总结**：
1. **安装 futu-stock-mcp-server**：
   ```bash
   pip install futu-stock-mcp-server
   ```

2. **安装并配置 Futu OpenD**：
   - 从 Futu 官网下载 OpenD
   - 解压并使用您的账户凭据配置 `FutuOpenD.xml`
   - 测试运行 OpenD 以确保配置正确
   - 使用 `nohup` 在后台启动 OpenD：
     ```bash
     nohup ./FutuOpenD > opend.log 2>&1 &
     ```

3. **配置环境变量**：
   - 设置 `FUTU_HOST`（默认：`127.0.0.1`）
   - 设置 `FUTU_PORT`（默认：`11111`）

4. **使用该技能**：在 OpenD 运行且环境变量设置完成后，您就可以使用此技能来访问 Futu 股票市场数据了。

**重要提示**：使用此技能之前，必须确保 OpenD 正在运行。如果 OpenD 停止，该技能将无法连接到 Futu 的服务。

## 效率对比

传统 MCP 方法：
- 启动时加载所有 20 多个工具
- 需要的上下文开销：500 多个令牌

该技能的方法：
- 仅加载元数据：约 100 个令牌
- 完整使用说明：约 5000 个令牌
- 工具执行：0 个令牌（通过外部执行）

## 工作原理

该技能不会预先加载所有 MCP 工具的定义，而是：
1. 显示可用的工具（仅显示名称和简要描述）
2. 根据用户请求选择要调用的工具
3. 生成用于调用该工具的 JSON 命令
4. 执行器负责实际的 MCP 通信

## 可用工具

### 市场数据查询
- `get_stock_quote`：获取指定股票的报价数据（价格、成交量等）
- `get_market_snapshot`：获取指定股票的买卖报价数据
- `get_cur_kline`：获取当前的 K 线图数据（需先订阅）
- `get_history_kline`：获取历史 K 线图数据（每 30 天限制 30 只股票）
- `get_rt_data`：获取实时数据（需订阅 RT_DATA）
- `get_ticker`：获取股票代码数据（需订阅 TICKER）
- `get_order_book`：获取订单簿数据（需订阅 ORDER_BOOK）
- `get_broker_queue`：获取经纪商队列数据（需订阅 BROKER）

### 订阅管理
- `subscribe`：订阅实时数据（QUOTE、ORDER_BOOK、TICKER、RT_DATA、BROKER、K-lines）
- `unsubscribe`：取消订阅实时数据

### 期权数据
- `get_option_chain`：获取期权链数据及希腊值
- `get_option_expiration_date`：获取期权到期日
- `get_option_condor`：获取期权 condor 策略数据
- `get_option_butterfly`：获取期权 butterfly 策略数据

### 账户信息
- `get_account_list`：获取账户列表
- `get_funds`：获取账户资金信息
- `get_positions`：获取账户持仓
- `get_max_power`：获取最大交易权限
- `get_margin_ratio`：获取证券的保证金比例

### 市场状态
- `get_market_state`：获取市场状态

**支持的市场**：
- HK：香港股票（例如：`HK.00700`
- US：美国股票（例如：`US.AAPL`
- SH：上海股票（例如：`SH.600519`
- SZ：深圳股票（例如：`SZ.000001`）

## 使用模式

当用户的请求符合该技能的功能时：

**步骤 1：从上述列表中选择合适的工具**

**步骤 2：生成 JSON 格式的工具调用命令**：

```json
{
  "tool": "tool_name",
  "arguments": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**步骤 3：通过 bash 执行**：

```bash
cd {baseDir}
python3 executor.py --call 'YOUR_JSON_HERE'
```

**重要提示**：使用 `{baseDir}` 来引用技能文件夹的路径。

## 获取工具详细信息

如果您需要了解特定工具的参数详情：

```bash
cd {baseDir}
python3 executor.py --describe tool_name
```

这将仅加载该工具的配置信息，而不会加载所有工具的配置。

## 示例

### 示例 1：获取股票报价

用户：查询 `HK.03690` 的最新价格

您的操作流程：
1. 选择工具：`get_stock_quote` 或 `get_market_snapshot`
2. 生成调用命令的 JSON 数据
3. 执行命令：
```bash
cd {baseDir}
python3 executor.py --call '{"tool": "get_market_snapshot", "arguments": {"symbols": ["HK.03690"]}}'
```

### 示例 2：订阅并获取实时数据

对于需要订阅的工具（如 `get_cur_kline`、`get_rt_data`）：

1. 先进行订阅：
```bash
cd {baseDir}
python3 executor.py --call '{"tool": "subscribe", "arguments": {"symbols": ["HK.03690"], "sub_types": ["QUOTE", "K_DAY"]}}'
```

2. 然后进行查询：
```bash
cd {baseDir}
python3 executor.py --call '{"tool": "get_cur_kline", "arguments": {"symbol": "HK.03690", "ktype": "K_DAY", "count": 100}}'
```

### 示例 3：获取历史 K 线图数据

```bash
cd {baseDir}
python3 executor.py --call '{"tool": "get_history_kline", "arguments": {"symbol": "HK.03690", "ktype": "K_DAY", "start": "2026-01-01", "end": "2026-02-13", "count": 100}}'
```

## 错误处理

如果执行器返回错误：
- 检查工具名称是否正确
- 确保提供了所有必需的参数
- 确保 MCP 服务器可以访问

## 性能说明

该技能与传统 MCP 方法的上下文使用情况对比：

| 场景 | MCP（预加载） | 该技能（动态加载） |
|----------|---------------|-----------------|
| 静态状态 | 500 多个令牌 | 约 100 个令牌 |
| 活动状态 | 500 多个令牌 | 约 5000 个令牌 |
| 执行阶段 | 500 多个令牌 | 0 个令牌 |

**节省效果**：在典型工作流程中，显著降低了上下文使用量。

## 配置要求

该技能需要：
- **Python 3**（系统路径中必须包含 `python3`）
- **futu-stock-mcp-server**：通过 `pip install futu-stock-mcp-server` 安装
- **Futu OpenD**：已安装并运行（见先决条件）
- **环境变量**：
  - `FUTU_HOST`：Futu OpenD 的主机地址（默认：`127.0.0.1`
  - `FUTU_PORT`：Futu OpenD 的 API 端口（默认：`11111`）

### OpenClaw 配置

在 `~/.openclaw/openclaw.json` 中进行配置：

```json5
{
  skills: {
    entries: {
      "futu-stock": {
        enabled: true,
        env: {
          FUTU_HOST: "your-futu-host",
          FUTU_PORT: "your-futu-port",
        },
      },
    },
  },
}
```

## 注意事项

- 股票代码格式：`{market}.{code}`（例如：`HK.00700`、`US.AAPL`、`SH.600519`）
- 某些工具在查询前需要订阅（详见工具说明）
- 历史 K 线图数据每 30 天仅限 30 只股票
- 每次订阅请求最多支持 100 只股票
- 每个 socket 连接最多支持 500 只股票

---

*该技能通过 MCP 服务器提供对 Futu 股票市场数据的动态访问功能。*