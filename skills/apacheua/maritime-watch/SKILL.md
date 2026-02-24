# maritime-watch

## 描述

这是一个用于监控Chornomorsk港口状态和安全的技能。它从多种来源收集数据，包括天气报告、船舶跟踪服务和新闻推送，以提供港口运营状况和潜在风险的全面视图。该技能设计有抗API速率限制的能力，并通过交叉验证来自多个来源的数据来避免信息错误。

## 输入参数

*   `port`: 需要监控的港口名称（默认值：Chornomorsk）。

## 输出结果

返回一个JSON对象，包含以下信息：

*   `weather`: 港口的当前天气状况（经过交叉验证）。
*   `vessels`: 目前在港口内或正在接近港口的船舶列表（经过交叉验证）。
*   `security`: 港口的安全状况（例如警报、警告等）（经过交叉验证）。
*   `news`: 与港口相关的最新新闻。

## 使用方法

只需使用`port`参数调用该技能即可：

```
maritime-watch port=Chornomorsk
```

## 示例

```json
{
  "weather": {
    "temperature": 10,
    "conditions": "Cloudy"
  },
  "vessels": [
    {
      "name": "MV Example",
      "status": "Arrived"
    }
  ],
  "security": {
    "status": "Normal"
  },
  "news": [
    {
      "title": "Port expansion project announced",
      "url": "https://example.com/news"
    }
  ]
}
```