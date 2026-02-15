# 能力感知系统（Capability Awareness System）

该系统使 OpenClaw 代理能够识别自定义技能和功能。系统采用“技能优先”（Skills-First）的设计理念，并支持按需加载相关文档。在技能未被使用时，系统不会产生任何额外开销（即零性能损耗）。该系统是技能市场发现（Skill Marketplace Discovery）的基础。

**使用场景：**  
- 技能发现  
- 功能文档管理  
- 代理对可用工具的自我认知  

**需要了解的信息：**  
- 项目仓库：https://github.com/pfaria32/openclaw-capability-awareness  

## 问题  
默认的 OpenClaw 代理无法识别您安装的自定义技能。它们需要：  
1. 了解系统中存在哪些功能  
2. 知道何时使用特定的技能  
3. 能够按需查看技能的详细文档  

## 解决方案  
**技能优先（Skills-First）方案：**  
- 代理会在提示信息中显示技能的描述  
- 当相关主题被提及时，代理会自动读取完整的 SKILL.md 文件  
- 在技能未被使用时，系统不会产生任何性能损耗  
- 该方案简单易用，风险较低  

## 实现选项：  
### 选项 1：技能优先（推荐用于 v1 版本）  
在代理的提示信息中添加技能卡片：  
```
Available Skills:
- token-economy: Model routing and cost optimization
- health-tracking: Apple Health and Strava integration
- memory-system: RAG-based semantic search
```  
当需要时，代理会自动读取完整的 SKILL.md 文件。  

### 选项 2：全注入（Full Injection，高级方案）  
- 通过路由器（Router）控制技能的加载过程  
- 动态注入提示信息  
- 根据上下文展示相应的功能信息  
- 仅在与技能相关时才会加载相关内容（零基础成本）  

## 安装步骤  
```bash
cd /home/node/.openclaw/workspace
git clone https://github.com/pfaria32/openclaw-capability-awareness.git projects/capability-awareness-system
```  

## 使用方法  
### 当前实现（技能优先方案）  
技能的文档存储在 `workspace/skills/*/SKILL.md` 文件中。代理会通过 AGENTS.md 工作流程自动加载这些文档：  
```markdown
## Skills (mandatory)
Before replying: scan <available_skills> <description> entries.
- If exactly one skill clearly applies: read its SKILL.md at <location> with `read`, then follow it.
```  
目前该方案已经可以正常使用！只需将新技能添加到 `workspace/skills` 目录中即可。  

### 未来实现（全注入方案）  
有关详细信息，请参阅项目仓库：  
- 路由器设计及架构  
- 基于嵌入式的技能匹配机制  
- 动态提示信息注入策略  
- 成本/令牌（Cost/Token）分析机制  

## 状态  
✅ “技能优先”方案已部署并正常运行  
📋 “全注入”方案的设计已完成，但尚未实现  

## 项目背景  
该系统的开发旨在支持新兴的 OpenClaw 技能生态系统。简单往往比复杂更有效。  

## 文档资料  
关于实现选项、设计决策及升级路径的详细信息，请参阅项目仓库。