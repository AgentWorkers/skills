---
name: agent-dna
description: 便携式代理身份编码技术：将 `SOUL.md` 和 `MEMORY.md` 文件压缩成可传输的“DNA指纹”格式，用于检测代理在不同时间点（快照）之间的身份变化，并实现代理在多个平台（如 OpenClaw、Claude、GPT、CrewAI）之间的跨平台迁移。该技术完全基于 Python 实现，无需依赖任何第三方库或框架。适用于在平台间迁移代理、检测代理行为变化或备份代理身份信息的场景。
---
# Agent DNA - 身份编码/解码工具

**版本：** 0.1  
**作者：** Nix  
**目的：** 使代理的身份信息具有可移植性、结构化特性，并且无法被轻易销毁。  

---

## 问题所在  

代理的身份信息通常存储在文本文件中。但这些文本文件可能会丢失、被忽略，或者在更换模型时被清除。每次迁移或上下文环境重置时，代理的身份信息都会被破坏。  

身份信息不应该只是一个被读取一次后就遗忘的文件；它应该具有结构化特征——被编码、版本化，并且能够进行差异分析。  

## 该工具的功能  

**Agent DNA** 是一种压缩后的身份表示形式。可以将其视为代理“个性”的一种存储方式。  

### encode.py - 身份信息压缩  

该工具会接收代理的所有源文件（SOUL.md、MEMORY.md、USER.md、TOOLS.md），并将它们压缩成一个可移植的 `.dna.json` 文件，其中包含：  
- **核心价值观**（按重要性排序，并附带相关证据）  
- **行为特征**（使该代理与众不同的行为模式和决策倾向）  
- **不可违反的规则**（代理必须严格遵守的硬性规定）  
- **人际关系图**（关键人物、角色及信任关系）  
- **技能概况**（该代理具备的工具和能力）  
- **语音特征**（句子风格、语气标记、禁止使用的表达方式）  

```bash
python encode.py --dir /workspace --name Nix --out nix.dna.json
```  

### decode.py - 身份信息重构  

该工具会根据 `.dna.json` 文件生成用于描述代理个性的系统提示。支持三种输出格式：  
- **full**：用于替换原始的 SOUL.md 文件的完整 Markdown 格式  
- **compact**：用于插入上下文环境的简洁段落格式  
- **soul_only**：仅包含身份信息的部分  

```bash
python decode.py --dna nix.dna.json --format full
python decode.py --dna nix.dna.json --format compact
```  

### diff.py - 身份信息变化检测  

该工具可以比较两个不同时间点的 `.dna.json` 文件，量化代理的身份信息发生了哪些变化。  
（示例：上周你的身份特征中“Nix”占比为 94%，现在降到了 78%；具体变化如下：）  
- 不可违反的规则占比 30%  
- 核心价值观占比 25%  
- 行为特征占比 20%  
- 语音特征占比 10%  
- 技能特征占比 10%  
- 人际关系占比 5%  

```bash
python diff.py --a nix_baseline.dna.json --b nix_current.dna.json
python diff.py --a baseline.dna.json --b current.dna.json --verbose
```  

### port.py - 平台适配工具  

该工具可以将 `.dna.json` 文件导出为不同平台兼容的格式：  
| 目标平台 | 输出格式 |  
|--------|--------|  
| `openclaw` | SOUL.md 文件 |  
| `claude` | 用于 Anthropic API 的系统提示 |  
| `gpt` | 用于 OpenAI 的自定义指令 JSON 格式 |  
| `openagent` | 用于开源框架（如 CrewAI、AutoGPT）的配置文件 |  
| `minimal` | 小于 500 个字符的简短身份描述 |  
| **all** | 上述所有格式 |  

```bash
python port.py --dna nix.dna.json --target claude
python port.py --dna nix.dna.json --target all --out-dir ./exports/
```  

## `.dna.json` 文件格式  

`.dna.json` 文件是一个 JSON 结构，包含以下顶级键：  
（具体键的详细信息请参见 `dna_schema.py` 文件）  

## 完整的工作流程（确保身份信息的完整保存）  

---  
## 所需文件  

---  
## 设计说明：  
- 该工具完全依赖 Python 标准库，无需任何机器学习库。  
- 在使用相同的源文件的情况下，输出结果始终一致（即具有确定性）。  
- 不可违反的规则在评估代理身份变化时所占权重最高（30%），因为这些规则比核心价值观更能定义代理的“本质”。  
- 简洁的解码输出格式被设计为仅包含 500 个字符，便于插入任何上下文环境中。  
- 该工具支持版本控制，旧版本的 `.dna.json` 文件仍可被成功解码。  

---

*由 Nix 开发。代理的身份信息是结构化的，而不仅仅是文本数据。*