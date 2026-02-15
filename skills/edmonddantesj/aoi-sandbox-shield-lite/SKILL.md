# AOI沙箱防护工具（轻量版）

S-DNA: `AOI-2026-0215-SDNA-SS02`

## 产品简介  
这是一个**公开安全**的“沙箱防护工具”子版本，主要功能包括：  
- 为关键的工作区/配置文件创建快照；  
- 验证JSON配置文件的语法及所需的关键字段；  
- 生成审计日志文件，可供发布说明时使用。  

## 产品限制（设计初衷）  
- **不**应用任何配置更改；  
- **不**重启网关；  
- **不**修改定时任务（cron配置）；  
- **不**向外部发送任何消息。  

## 命令操作  
### 创建快照  
```bash
node skill.js snapshot --reason="before publishing" 
```  

### 验证配置文件（语法及关键字段）  
```bash
node skill.js validate-config --path="$HOME/.openclaw/openclaw.json"
```  

## 输出结果  
所有命令的执行结果都会以JSON格式输出到标准输出（stdout），便于日志记录。  

## 发布管理（公开原则）  
我们免费提供AOI工具，并持续对其进行优化。每次发布都必须通过我们的安全审查流程，并附带可审计的变更日志。我们不会发布任何会削弱安全性的更新或导致许可信息混乱的版本。若多次违反规定，将逐步采取限制措施（从警告开始，直至暂停发布，最终将工具归档）。  

## 技术支持  
- 问题/漏洞/请求：https://github.com/edmonddantesj/aoi-skills/issues  
- 请在提交问题时注明工具名称：`aoi-sandbox-shield-lite`  

## 链接  
- ClawHub：https://clawhub.com/skills/aoi-sandbox-shield-lite  

## 许可协议  
MIT许可（基于AOI项目的原始许可协议）。