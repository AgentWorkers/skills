# MSP 工具包技能

**描述：**  
这套工具包专为 IT 管理服务提供商（MSP）的工作流程设计，包含用于 Azure/M365 审计、NPU 监控以及系统健康检查的核心工具。

**元数据：**  
```json
{
  "clawdbot": {
    "emoji": "🔧",
    "os": ["linux"]
  }
}
```

## 核心功能  
- `msp-dashboard.py`：用于每日监控 Azure/M365 系统的运行状态。  
- `healthcheck`：执行防火墙、SSH 以及系统更新相关的审计操作。  
- `nuc-reset.sh`：用于重启 NPU（Network Processing Unit）的脚本。  

## 安装步骤  
```bash
npm install clawhub
clawhub publish /home/cc/.openclaw/workspace/skills/msp-toolkit
```