---
name: arrivelah
description: 用于查询下一班到达您目的地的公交车的单字触发词
homepage: https://github.com/abhay/arrivelah
metadata: {"clawdbot":{"emoji":"🚌","requires":{"bins":["curl","jq"]},"tags":["singapore","transport","bus"]}}
---
# ArriveLah - 新加坡公交车到站信息查询

只需输入一个关键词，即可获取下一班公交车的到站信息。

## 使用方法

```
bus
```

返回结果：下一班前往您预设目的地的公交车及其到站时间。

## 配置设置

请编辑 `config.json` 文件以配置以下参数：
- `defaultStop`：您常用的公交车站代码（例如：“10051”）
- `defaultService`：您常用的公交车线路编号（例如：“120”）
- `destination`：您常去的目的地（用于显示）

## API 接口

该工具使用免费的 Arrivelah2 API（https://arrivelah2.busrouter.sg/）进行数据查询，无需 API 密钥。

## 示例输出

```
🚌 Bus 120 → Home
⏰ Next: 2 min (Seats available)
📍 From: Blk 149 Jalan Bukit Merah
```