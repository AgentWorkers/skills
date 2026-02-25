---
name: entradex
description: >
  使用 EntradeX CLI 来处理 DNS（Domain Name System）相关的工作流程。适用场景包括：  
  (1) 通过环境变量或配置文件设置 DNS API 凭据；  
  (2) 读取账户信息、市场数据以及订单详情；  
  (3) 下单、修改或取消实际交易。
metadata:
  openclaw:
    requires:
      bins:
        - entradex
      env:
        - DNSE_API_KEY
        - DNSE_API_SECRET
    primaryEnv: DNSE_API_KEY
    install:
      - kind: node
        package: entradex-cli
        bins:
          - entradex
        label: Install EntradeX CLI (npm)
    homepage: https://www.npmjs.com/package/entradex-cli
---
# EntradeX CLI

## 安装

```bash
npm i -g entradex-cli
```

## 使用方法

```bash
entradex [global-options] [command]
```

## 配置

**凭据优先级：**
1. 配置文件（`~/.entradex-cli/config.json`） - 推荐使用
2. 环境变量（`DNSE_API_KEY`, `DNSE_API_SECRET`）
3. 全局命令选项（`--api-key`, `--api-secret`）

**配置文件的设置与检查：**

```bash
entradex config set --key "<api-key>" --secret "<api-secret>"
entradex config set
entradex config get
entradex config clear
```

## 安全性注意事项：**

**在使用本工具之前：**
- 验证npm包的信息：`npm view entradex-cli`，确认作者为`hieuhani`且仓库信息正确。
- 查看包内容：`npm pack entradex-cli --dry-run` 或在 [npmjs.com](https://www.npmjs.com/package/entradex-cli) 上查看详细信息。
- 将 `DNSE_API_KEY` 和 `DNSE_API_SECRET` 视为高度敏感的交易凭据。

**自动执行警告：**
- 本工具会使用提供的凭据执行真实交易，请确保使用具有有限权限的账户。
- 如果怀疑存在未经授权的访问，请定期更换API密钥。

## 全局选项：**
- `--api-key <key>`：DNSE API密钥
- `--api-secret <secret>`：DNSE API密钥
- `--base-url <url>`：API基础URL（默认：`https://openapi.dnse.com.vn`）
- `--debug`：显示请求详情
- `-V, --version`：显示CLI版本
- `-h, --help`：显示帮助信息

## 命令：

### 配置相关命令

```bash
entradex config set [--key <key>] [--secret <secret>] [--url <url>]
entradex config get
entradex config clear
```

### 账户相关命令

```bash
entradex account list
entradex account balances <accountNo>
entradex account loan-packages <accountNo> <marketType> [--symbol <symbol>]
```

### 交易相关命令

```bash
entradex trade order <marketType> <symbol> <side> <orderType> <price> <quantity> <tradingToken> [--price-stop <price>]
entradex trade modify <accountNo> <orderId> <marketType> <symbol> <side> <orderType> <price> <quantity> <tradingToken> [--price-stop <price>]
entradex trade cancel <accountNo> <orderId> <marketType> <tradingToken>
```

**参数说明：**
- `marketType`（枚举类型）：`STOCK`（股票）、`DERIVATIVE`（衍生品）
- `side`（枚举类型）：`NB`（买入）、`NS`（卖出）
- `orderType`（枚举类型）：`ATO`（开市价）、`ATC`（收盘价）、`LO`（限价单）、`MTL`（市价单修改）、`MOK`（市价单取消）、`PLO`（挂限价单）
  - `ATO`：开市价成交
  - `ATC`：收盘价成交
  - `LO`：限价单
  - `MTL`：市价单修改为限价单
  - `MOK`：市价单取消
  - `PLO`：挂限价单
- `price`（数字）：单价；需符合DNSE的跳动价位/市场规则
  - 如果 `orderType` 为 `LO`，`price` 必须大于 `0`。
  - 如果 `orderType` 为 `ATO`、`ATC`、`MTL`、`MOK`、`PLO` 之外的类型，`price` 必须精确为 `0`。
- `quantity`（整数）：订单数量；必须符合市场最小交易量规则
  - 对于 `marketType=STOCK`，有效数量为：
    - 成交单位：100的倍数（如 `100`、`200` 等）
    - 非整数单位：1到99之间的整数
  - 对于 `marketType=STOCK`，如 `101`、`102` 等非整数数量将被视为无效订单。
- `tradingToken`（字符串）：通过 `entradex auth create-token` 命令生成的交易令牌

**用户指令解析规则：**
- 用户输入“buy”/“sell”时，系统会自动转换为 `NB`/`NS`。
- 执行前所有参数需转换为大写（如 `marketType`、`side`、`orderType`）。
- 如果输入的参数属于不支持的枚举值，系统会停止执行并要求用户输入有效值。
- 如果目标市场/会话不支持某个 `orderType`，系统会停止执行并要求用户选择支持的类型。

### 下单相关命令

```bash
entradex order list <accountNo> <marketType>
entradex order detail <accountNo> <orderId> <marketType>
entradex order history <accountNo> <marketType> [--from <date>] [--to <date>] [--page-size <size>] [--page-index <index>]
entradex order deals <accountNo> <marketType>
```

### 市场相关命令

```bash
entradex market secdef <symbol> [--board-id <id>]
entradex market ppse <accountNo> <marketType> <symbol> <price> <loanPackageId>
```

### 用户认证相关命令

```bash
entradex auth send-otp <email> [--otp-type <type>]
entradex auth create-token <otpType> <passcode>
```

### 测试执行（Dry Run）

```bash
entradex dry-run accounts
entradex dry-run balances <accountNo>
entradex dry-run order <marketType> <symbol> <side> <orderType> <price> <quantity> [--price-stop <price>]
```

## 常见工作流程

```bash
# 1) Configure credentials
entradex config set

# 2) Send OTP
entradex auth send-otp user@example.com

# 3) Create trading token with passcode
entradex auth create-token smart_otp <passcode>

# 4) Place an order
entradex trade order STOCK VIC NB LO 15000 100 <trading-token>
```