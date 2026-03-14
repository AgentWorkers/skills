---
name: edge-router
description: 将 AI 代理的计算任务路由到成本最低且可行的后端。支持本地推理（Ollama）、云 GPU（Vast.ai）和量子硬件（Wukong 72Q）。当代理需要决定在哪里运行任务、优化计算成本、检查后端可用性，或在边缘/云/量子基础设施之间执行工作负载时，可以使用该功能。
---
# 边缘路由器（Edge Router）

该路由器会将任务路由到最便宜的后端服务：  
- 本地（免费）  
- 云GPU（0.01美元/次）  
- 量子计算服务（0.10美元/次）。  

## API  

基础地址：`https://edge-router.gpupulse.dev/api/v1`（或 `localhost:3825`）  

### 路由设置（Route Settings）  
```bash
curl -X POST "$BASE/route" -H "Content-Type: application/json" \
  -d '{"task_type": "inference"}'
```  

### 任务执行（Task Execution）  
```bash
curl -X POST "$BASE/execute" -H "Content-Type: application/json" \
  -d '{"task_type": "inference", "payload": {"model": "llama3.2:1b", "prompt": "hello"}}'
```  

### 任务类型（Task Types）  
- `inference`：优先使用本地计算资源，若本地不可用则切换到云服务  
- `training`：使用云GPU进行训练  
- `quantum`：使用Wukong 72Q量子计算平台  
- `auto`：自动选择最便宜的后端服务  

### 其他功能（Other Features）  
- `GET /backends`：获取所有后端服务的列表及状态信息  
- `GET /stats`：查看路由统计数据  
- `GET /health`：进行系统健康检查