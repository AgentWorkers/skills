---
name: "Deep Research for OpenClaw"
description: "安装并配置一个结构化的 OpenClaw 深度研究子代理，该子代理支持混合搜索、基于工件的运行流程、声明验证、报告检查以及经过验证的最终处理流程。"
version: "0.1.0"
metadata:
  openclaw:
    homepage: "https://github.com/MilleniumGenAI/deep-research-openclaw-agent"
    requires:
      bins:
        - openclaw
        - python
      config:
        - openclaw.json
        - deep-researcher agent configured in OpenClaw
        - Tavily API key configured if Tavily-backed scouting is desired
---
# OpenClaw的深度研究功能

## 该功能的用途  
这是一个用于安装和配置`deep-researcher`子代理的集成技能，该子代理来自公共仓库：  
[deep-research-openclaw-agent](https://github.com/MilleniumGenAI/deep-research-openclaw-agent)  

该仓库包含以下内容：  
- `workspace-researcher`提示包；  
- 本地研究辅助脚本；  
- 主要的深度研究编排合约；  
- 报告的校验、验证和最终处理流程。  

该功能专为OpenClaw用户设计，旨在让他们能够快速实现可复制的深度研究工作流程，而无需从头开始构建运行时环境和相关合约。  

## 功能概述  
- 通过`计划（plan）→探索（scout）→收集（harvest）→验证（verify）→合成（synthesize）`的步骤进行结构化深度研究；  
- 结合使用`web_search`、Tavily和`web_fetch`进行混合式数据发现；  
- 明确管理源代码注册表、声明记录和覆盖范围跟踪；  
- 对报告进行校验、验证，并生成最终的M2M格式JSON输出；  
- 以`SUCCESS | PARTIAL | FAILURE`的形式返回结果，并明确指出存在的差距和冲突。  

## 使用要求  
- 确保使用的是OpenClaw 2026.3.x或更高版本；  
- 主机上必须安装Python；  
- OpenClaw中已配置`deep-researcher`代理；  
- 如果需要使用Tavily支持的功能，请确保环境变量中包含`TAVILY_API_KEY`。  

## 安装步骤  
1. 克隆仓库：  
   ```bash
   git clone https://github.com/MilleniumGenAI/deep-research-openclaw-agent.git
   ```  
2. 将`openclaw/workspace-researcher`目录复制到OpenClaw的根目录中，或直接将代理配置指向该路径。  
3. 确保`deep-researcher`代理的配置文件与`openclaw/main-deep-research-skill.md`文件中的内容一致。  
4. 在`openclaw.json`文件中注册或更新`deep-researcher`代理的配置信息。  
5. 如果需要使用Tavily的支持功能，请确保`TAVILY_API_KEY`已配置在环境变量或`.env`文件中。  

## 验证步骤  
在实际使用代理之前，请运行以下命令进行验证：  
```bash
python -m py_compile openclaw/workspace-researcher/scripts/*.py
python openclaw/workspace-researcher/scripts/init_research_run.py --workspace openclaw/workspace-researcher --topic "Smoke test" --language en --task-date 2026-03-10
```  

配置完成后，可以通过OpenClaw运行首次测试任务：  
```bash
openclaw agent --agent deep-researcher --json --message "使用您的本地SOUL.md合约执行深度研究。目标：确认运行时环境能否正常启动新任务；如果没有外部数据来源，则返回`PARTIAL`状态。范围仅限于本地初始化和工件生成；网络搜索不在该范围内。成功标准：生成新的临时工件，并如实说明证据收集过程中遇到的问题。任务日期：2026-03-10。输出格式：最终的M2M JSON格式。约束条件：不得伪造数据来源；如果证据不足，则返回`PARTIAL`状态。"
```  

## 相关参考资料  
- 项目主页README文件：[README.md](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/README.md)  
- 子代理合约：[openclaw/workspace-researcher/SOUL.md](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/workspace-researcher/SOUL.md)  
- 主要编排合约：[openclaw/main-deep-research-skill.md](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/main-deep-research-skill.md)  
- 运行时脚本：[openclaw/workspace-researcher/scripts/](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/tree/main/openclaw/workspace-researcher/scripts)  
- 代理配置模板：[openclaw/agent-config.template.json](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/agent-config.template.json)  
- 已知限制：[docs/known-limits.md](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/docs/known-limits.md)  

## 注意事项  
- 该功能仅适用于OpenClaw环境。  
- ClawHub根据MIT-0许可协议发布所有技能。  
- 运行时的核心配置文件为`openclaw/workspace-researcher/SOUL.md`。  
- 研究结果必须基于可追踪的外部来源生成，不得使用本地生成的工件。