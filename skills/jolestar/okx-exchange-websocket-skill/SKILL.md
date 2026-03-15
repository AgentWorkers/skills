---
name: okx-exchange-websocket-skill
description: 通过 UXC 的原始 WebSocket 模式订阅 OKX 公共交易所的 WebSocket 通道，以接收行情数据（ticker）、交易信息（trade）、订单簿数据（book）以及蜡烛图数据（candle events）。订阅过程中会使用明确的订阅帧（subscribe frames）来进行通信。
---
# OKX交易所WebSocket技能

使用此技能通过`uxc subscribe`的原始WebSocket模式来订阅OKX公共交易所的WebSocket频道。

`uxc`技能可用于通用运行时行为、数据接收处理以及事件数据的解析。

## 前提条件

- `uxc`已安装，并且位于`PATH`环境中。
- 具有访问OKX公共WebSocket端点的网络权限。
- 拥有用于存储NDJSON输出数据的可写入路径。

## 覆盖范围

此技能支持订阅OKX公共交易所的以下频道：

- 交易代码（tickers）
- 交易记录（trades）
- 市场订单簿（books5）
- K线数据（candle channels）

**不支持以下内容：**
- OKX OnchainOS MCP
- 私有WebSocket登录流程
- 交易、账户或订单管理相关频道
- REST API相关操作

## 端点模型

使用OKX公共WebSocket端点：
`wss://ws.okx.com:8443/ws/v5/public`

连接成功后，需要发送一个订阅请求帧（subscribe frame），例如：

```json
{"op":"subscribe","args":[{"channel":"tickers","instId":"BTC-USDT"}]}
```

## 核心工作流程

1. 启动原始WebSocket订阅：
   ```
   uxc subscribe start wss://ws.okx.com:8443/ws/v5/public --transport websocket --init-frame '{"op":"subscribe","args":[{"channel":"tickers","instId":"BTC-USDT"}]}' --sink file:$HOME/.uxc/subscriptions/okx-btcusdt-ticker.ndjson
   ```

2. 检查数据接收结果：
   ```
   tail -n 5 $HOME/.uxc/subscriptions/okx-btcusdt-ticker.ndjson
   ```

3. 查询订阅状态：
   ```
   uxc subscribe list
   ```
   ```
   uxc subscribe status <job_id>
   ```

4. 完成订阅后停止任务：
   ```
   uxc subscribe stop <job_id>
   ```

## 常用的订阅请求帧（Subscribe Frames）

- 交易代码（tickers）：
  ```
  {"op":"subscribe","args":[{"channel":"tickers","instId":"BTC-USDT"}]}
  ```

- 交易记录（trades）：
  ```
  {"op":"subscribe","args":[{"channel":"trades","instId":"BTC-USDT"}]}
  ```

- 市场订单簿（books5）：
  ```
  {"op":"subscribe","args":[{"channel":"books5","instId":"BTC-USDT"}]}
  ```

- K线数据（candle）：
  ```
  {"op":"subscribe","args":[{"channel":"candle1m","instId":"BTC-USDT"}]}
  ```

## 运行时验证

以下原始WebSocket数据流已通过`uxc`成功验证：
- 端点：`wss://ws.okx.com:8443/ws/v5/public`
- 传输方式：`--transport websocket`
- 订阅请求帧示例：
  ```
  {"op":"subscribe","args":[{"channel":"tickers","instId":"BTC-USDT"}]}
  ```

观察到的数据接收行为：
- 首先会收到一个表示订阅成功的`open`事件。
- 随后会连续收到包含交易代码数据的`data`事件，这些数据包含以下字段：
  - `arg.channel`：频道名称
  - `arg.instId`：交易代码的实例ID
  - `data[0].last`：最新交易价格
  - `data[0].bidPx`：买入价
  - `data[0].askPx`：卖出价
  - `data[0].ts`：时间戳

## 注意事项：

- 确保对接收到的JSON数据进行正确解析，不要使用`--text`选项。
- 首先解析`event_kind`、`data`和`meta`等关键字段。
- 在使用此技能时，必须始终指定`--transport websocket`。
- OKX公共频道无需登录，切勿将其与私有WebSocket认证流程混淆。
- 由于OKX公共频道是通过同一个端点复用的，因此必须使用`--init-frame`参数。
- `instId`值应使用OKX规定的格式（如`BTC-USDT`）。
- 正确的执行命令是`uxc subscribe start ... --transport websocket`；`uxc link`并非主要接口，频道选择信息包含在订阅请求帧中。

## 参考资料

- 使用模式：`references/usage-patterns.md`
- OKX WebSocket API文档：`https://www.okx.com/docs-v5/en/`