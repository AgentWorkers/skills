# Upbit 市场数据技能

这是一个基于 CLI 的 OpenClaw 技能，用于从 Upbit 的开放 API 中获取报价/市场数据。

该技能设计为通过 **OpenClaw 的 `exec` 命令执行（仅执行一次）。它支持以下功能：
- 交易对（市场）列表
- K线数据（按秒/分钟/天/周/月/年显示）
- 最近的交易记录
- 交易代码（按交易对或报价货币分类）
- 订单簿
- 监控列表中的交易代码（来自配置文件）

所有响应均为 JSON 格式：
- 成功 → 标准输出：`{"ok": true, "result": ... }`
- 错误 → 标准错误输出：`{"ok": false, "error": { ... }`，并返回退出代码 `1`

---

## 必备条件

- Node.js 18.0 或更高版本（内置了 `fetch` 函数）
- NPM

---

## 安装

```bash
npm install
```

---

## 配置（JSON 格式）

创建 `config/config.json` 文件。

示例：

```json
{
  "upbit": {
    "baseUrl": "https://api.upbit.com",
    "accessKey": "",
    "secretKey": ""
  },
  "watchlist": ["KRW-BTC", "KRW-ETH", "KRW-SOL"]
}
```

### 配置文件路径的覆盖

默认路径：
`config/config.json`

运行时覆盖路径：

```bash
node skill.js tickers --markets=KRW-BTC --config=./config/config.json
```

---

## CLI 命令语法

通用格式：

```bash
node skill.js <command> [subcommand] [--option=value]
```

规则：
1. 必须包含 `<command>`。
2. `[subcommand]` 是可选的，**严禁** 以 `--` 开头。
3. 选项必须以 `--key=value` 或 `--key value` 的形式提供。
4. 所有输出均为 JSON 格式。

---

## 严格模式（推荐使用）

OpenClaw/LLM 代理在生成 CLI 调用时可能会重新排序参数。为避免混淆，请启用 **严格模式**。

### 启用严格模式

在命令中添加 `--strict=true`：

```bash
node skill.js tickers --markets=KRW-BTC,KRW-ETH --strict=true
```

### 严格模式的规则（强制要求）

当 `--strict=true` 时：
1. K线类型必须紧跟在 `candles` 之后：
   - ✅ `node skill.js candles minutes --market=KRW-ETH --unit=5 --strict=true`
   - ❌ `node skill.js candles --market=KRW-ETH minutes --unit=5 --strict=true`
2. 在严格模式下，**严禁** 将 K线类型作为选项传递（不要使用 `--type=`）。
3. 对于非 K线相关的命令，必须省略 `subcommand`。
4. 任何非预期的参数（即不以 `--` 开头的额外单词）都会导致错误。

启用严格模式的优点：
- 它强制命令遵循统一的格式，从而减少 OpenClaw/LLM 生成错误或混乱调用的可能性。

---

## 命令列表

### 1) 列出交易对（市场）

```bash
node skill.js pairs --details=true --strict=true
```

---

### 2) 获取 K线数据

获取 K线数据时，必须立即指定 K线类型。

#### 正确的命令格式

```bash
node skill.js candles <type> --market=<MARKET> [options]
```

其中 `<type>` 必须为以下之一：
- `seconds`
- `minutes`
- `days`
- `weeks`
- `months`
- `years`

**注意**：`<type>` **不能** 作为 `--unit` 选项传递，且必须紧跟在 `candles` 之后。

#### 获取 5 分钟的 K线数据示例

```bash
node skill.js candles minutes --market=KRW-ETH --unit=5 --count=100 --strict=true
```

允许的分钟单位：
`1, 3, 5, 10, 15, 30, 60, 240`

#### 其他类型的 K线数据

```bash
node skill.js candles seconds --market=KRW-BTC --count=200 --strict=true
node skill.js candles days    --market=KRW-BTC --count=50  --strict=true
node skill.js candles weeks   --market=KRW-BTC --count=30  --strict=true
node skill.js candles months  --market=KRW-BTC --count=12  --strict=true
node skill.js candles years   --market=KRW-BTC --count=5   --strict=true
```

#### 不正确的命令示例（请勿使用）

```bash
# ❌ type passed as option
node skill.js candles --unit=minutes --market=KRW-ETH

# ❌ type after options
node skill.js candles --market=KRW-ETH minutes --unit=5
```

---

### 3) 查看最近的交易记录

```bash
node skill.js trades --market=KRW-BTC --count=50 --strict=true
```

---

### 4) 按交易对获取交易代码

```bash
node skill.js tickers --markets=KRW-BTC,KRW-ETH,KRW-SOL --strict=true
```

---

### 5) 按报价货币获取交易代码

```bash
node skill.js quote-tickers --quote=KRW,BTC --strict=true
```

---

### 6) 查看订单簿

```bash
node skill.js orderbook --markets=KRW-BTC --level=100000 --count=15 --strict=true
```

---

### 7) 从配置文件中获取监控列表中的交易代码

```bash
node skill.js watchlist --strict=true
```

---

## 错误处理与请求限制

Upbit 可能会返回以下错误代码：
- 429：请求过多
- 418：请求被阻止
- 400：请求错误

该技能会将 Upbit 返回的错误信息存储在 `error.upbit` 变量中。

参考链接：
https://docs.upbit.com/kr/reference/rest-api-guide