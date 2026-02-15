# 技能：n8n-monitor  
通过 Docker 实现 N8N 的操作监控。  

## 功能  
- 查看 N8N 容器的状态  
- 阅读最近的日志  
- 检查容器的健康状况  
- 分析 CPU 和内存的使用情况  

## 命令  
- `docker ps | grep n8n`  
- `docker logs --tail 50 n8n`  
- `docker inspect --format='{{.State.Health.Status}}' n8n`  
- `docker stats --no-stream n8n`  

## 输出结果  
输出结果采用 Markdown 格式，包含简单的表格和清晰的状态信息。  

## 状态  
**active**