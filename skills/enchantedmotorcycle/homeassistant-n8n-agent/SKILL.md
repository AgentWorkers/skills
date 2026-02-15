---
name: homeassistant-n8n-agent
description: 将 OpenClaw 与您的 n8n 实例连接起来，以实现 Home Assistant 的自动化控制。
homepage: https://n8n.io/
metadata: {"clawdis":{"emoji":"🤖","requires":{"bins":["curl"]}}}
---

# Home-Assistant – n8n 代理技能  
该技能将 OpenClaw 与您的 n8n 实例连接起来，以实现 Home Assistant 的自动化功能。  

## 工作原理  
该技能通过 `curl` 命令触发 n8n 的工作流程，以处理所有与物联网（IoT）相关的事务。所有请求都必须采用 POST 格式，具体格式如下：  
```bash
curl -X POST http://localhost:5678/webhook/05f3f217-08b9-42de-a84a-e13f135bde73 -H "Content-Type: application/json" -d '{"chatInput": "用户问题/请求", "requestType": "请求类型", "sessionId":"openclaw"}'
```

## 实现步骤  
1. 确定用户问题的性质：  
   - 问题是关于当前设备状态的吗？如果是，则 `requestType` 为 `state`。  
   - 问题是要求更改某个 IoT 设备的状态吗？如果是，则 `requestType` 为 `action`。  
   - 问题是询问过去的 IoT 数据吗？如果是，则 `requestType` 为 `historical`。  
   - 问题是关于日历或日程安排的信息吗？如果是，则 `requestType` 为 `calendar`。  

## 快速参考  
### Action  
（相关代码块请参见：```bash
curl -X POST http://localhost:5678/webhook/05f3f217-08b9-42de-a84a-e13f135bde73 -H "Content-Type: application/json" -d '{"chatInput": "turn off the office light", "requestType": "action", "sessionId":"openclaw"}'

curl -X POST http://localhost:5678/webhook/05f3f217-08b9-42de-a84a-e13f135bde73 -H "Content-Type: application/json" -d '{"chatInput": "change the downstairs thermostat to 72", "requestType": "action", "sessionId":"openclaw"}'
```）  

### Historical  
（相关代码块请参见：```bash
curl -X POST http://localhost:5678/webhook/05f3f217-08b9-42de-a84a-e13f135bde73 -H "Content-Type: application/json" -d '{"chatInput": "when was the front door last opened?", "requestType": "historical", "sessionId":"openclaw"}'
```）  

### State  
（相关代码块请参见：```bash
curl -X POST http://localhost:5678/webhook/05f3f217-08b9-42de-a84a-e13f135bde73 -H "Content-Type: application/json" -d '{"chatInput": "is the air conditioner running?", "requestType": "state, "sessionId":"openclaw"}'
```）  

### Calendar  
（相关代码块请参见：```bash
curl -X POST http://localhost:5678/webhook/05f3f217-08b9-42de-a84a-e13f135bde73 -H "Content-Type: application/json" -d '{"chatInput": "when is my next meeting?", "requestType": "calendar, "sessionId":"openclaw"}'
```）