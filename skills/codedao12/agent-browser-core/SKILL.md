---
name: agent-browser-core
description: OpenClaw 技能适用于代理-浏览器命令行界面（Agent-Browser CLI），该界面基于 Rust 开发，并提供 Node.js 作为备用方案。该技能支持基于 AI 的 Web 自动化功能，包括快照（snapshots）、引用（refs）以及结构化命令（structured commands）的支持。
---

# Agent Browser Skill（核心功能）

## 目的  
提供一个高级的、可投入生产环境的脚本集（playbook），用于通过命令行界面（CLI）和结构化命令来自动化网页任务。

## 适用场景  
- 需要对AI代理进行确定性自动化操作。  
- 希望获得包含引用信息（refs）的简洁快照以及JSON格式的输出结果。  
- 偏好使用快速响应的CLI，并且支持Node.js作为备用方案。  

## 不适用场景  
- 需要完整的SDK或自定义JavaScript集成。  
- 需要处理大量文件上传或复杂的媒体处理流程。  

## 快速入门指南  
- 阅读`references/agent-browser-overview.md`以了解安装方法、架构及核心概念。  
- 阅读`references/agent-browser-command-map.md`以了解命令类别及参数设置。  
- 阅读`references/agent-browser-safety.md`以了解高风险操作控制规则及安全模式设置。  
- 阅读`references/agent-browser-workflows.md`以了解推荐的自动化工作流程。  
- 阅读`references/agent-browser-troubleshooting.md`以了解常见问题及解决方法。  

## 必需条件  
- 已安装agent-browser CLI及相应的浏览器运行环境。  
- 需要处理的目标URL及工作流程步骤。  
- 如果需要身份验证，请配置相应的会话或用户策略。  

## 预期输出  
- 明确的命令执行顺序及自动化操作的约束条件。  

## 操作注意事项  
- 在执行操作前先生成快照；操作完成后再次生成快照以记录DOM变化。  
- 使用`--json`选项生成便于机器解析的JSON格式输出。  
- 在执行任何操作前，请确保等待相关资源加载完成并检查其状态。  
- 操作完成后，请关闭相关标签页或会话以释放系统资源。  

## 安全模式默认设置  
- 未经明确批准，严禁使用`eval`、`--allow-file-access`、自定义的`--executable-path`或任意`--args`参数。  
- 除非任务有特殊要求，否则避免使用`network route`、设置凭据或修改cookie/存储内容。  
- 允许访问的域名应经过严格审核；禁止访问本地主机或私有网络内的目标地址。  

## 安全性提示  
- 将访问令牌和凭据视为敏感信息，严格保密处理。  
- 除非确实必要，否则禁止使用`--allow-file-access`选项。