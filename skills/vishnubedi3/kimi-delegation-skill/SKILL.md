---
name: kimi-delegation-skill
description: 将所有的推理和代码生成任务委托给基于 HuggingFace Transformers 的 KIMI（KIMMY）因果语言模型。当代理程序绝对不能自行进行推理或编写代码时，应使用此技能，而是将所有任务代理给基于 KIMI 的模型来处理。
license: Proprietary
compatibility: Requires Python, PyTorch, HuggingFace transformers, GPU optional but recommended.
allowed-tools: Python(Read Write)
metadata:
  author: internal
  version: "1.0"
---
## 目的

此技能遵循严格的委托模型：主要代理（agent）没有任何推理或代码编写的权限。所有用户任务都会被转发给通过 Transformers 加载的 KIMI（KIMMY）模型进行处理。代理仅充当任务调度者（dispatcher）的角色。

## 激活条件

在以下情况下激活此技能：
- 代理不得独立进行推理；
- 所有的规划、推理和代码生成工作必须由 KIMI/KIMMY 模型完成；
- 需要将任务委托给外部因果语言模型（causal LM）进行处理。

## 执行步骤

1. 使用有效的本地或远程模型路径初始化 `KIMISkill`；
2. 使用 `Qwen3Coder` 对 `KIMISkill` 实例进行封装；
3. 对于每个用户输入的提示（prompt），调用 `Qwen3Coder.handle_prompt` 方法；
4. 将用户输入的提示原样转发给 KIMMY；
5. KIMMY 生成完整的响应；
6. 去除提示中的辅助信息（scaffolding），并将生成的响应作为最终输出返回。

**参考文件：**
- `scripts/kimi_skill.py`
- `scripts/qwen3_coder.py`

## 输入与输出

**输入：**  
一个原始的用户任务字符串。

**输出：**  
一个字典，包含以下内容：
- `author`：始终为 `"KIMMY"`；
- `content`：生成的响应内容，其中不包含任何提示辅助信息。

## 失败模式与边缘情况

- 模型路径无效或无法访问：初始化失败；
- 内存（VRAM）不足：模型可能切换到 CPU 进行处理，或者无法成功加载；
- 任务过于复杂（长度过长），可能导致上下文限制被超出；
- 如果生成过程失败，不允许代理尝试自行进行推理。

代理不得尝试通过自行推理来恢复任务执行。

## 参考资料

技术细节和架构原理请参阅：
- `references/REFERENCE.md`