---
name: prompt-compressor
description: 通过训练代理生成压缩后的响应、压缩后的内存日志以及压缩后的预压缩摘要，可以节省 20% 至 40% 的 LLM 令牌（即模型运行所需的资源）。该功能通过 `SOUL.md` 指令实现，无需额外的钩子（hooks）、进程或依赖项。当用户请求压缩提示内容时，系统也会自动执行压缩操作。适用于需要降低令牌成本、优化 API 使用效率、压缩提示内容或提升代理运行效率的场景。
version: 1.0.0
metadata: {"openclaw":{"emoji":"🗜️","homepage":"https://github.com/ckpxgfnksd-max/prompt-compressor-openclaw"}}
---
# Prompt Compressor  
该插件从第2轮开始通过压缩所有代理的输出来节省令牌（tokens）。  

## 工作原理  
这并非一个“钩子”（hook）——钩子需要使用较新版本的OpenClaw。该插件通过向`SOUL.md`文件中添加指令来实现以下功能：  
1. **生成压缩后的响应**：不包含填充内容或冗余语句，直接给出答案。  
2. **生成压缩后的`MEMORY.md`文件**：每行只记录一个事实，不包含叙述性内容。  
3. **生成压缩后的每日日志**：仅记录决策内容，不记录讨论过程。  
4. **压缩数据刷新操作**：将数据以压缩形式存储，避免使用长段落。  

这些优化措施会形成叠加效应：压缩后的响应 → 压缩后的历史记录 → 压缩后的压缩摘要 → 从而在后续轮次中节省更多令牌。  

## 安装方法  
将`soul-snippet.md`文件的内容追加到用户的`SOUL.md`文件中：  
```bash
cat {baseDir}/soul-snippet.md >> ~/.openclaw/SOUL.md
```  

如果使用工作区的`SOUL.md`文件：  
```bash
cat {baseDir}/soul-snippet.md >> <workspace>/SOUL.md
```  

之后，启动一个新的会话（使用命令`/new`），以便加载更新后的`SOUL.md`文件。  

## 当用户请求压缩特定提示内容时  
请手动应用以下规则：  

### 删除以下内容：  
- 问候语：`Hello`、`Hi`、`Hey`、`Good morning`  
- 结束语：`Thanks`、`Best regards`、`Cheers`  
- 应用性语句：`Could you please`、`I was wondering if`、`Would you be able to`  
- 填充词：`just`、`really`、`very`、`basically`、`actually`、`literally`、`honestly`  
- 重复性语句：`I think that`、`In my opinion`、`It is worth mentioning`  

### 缩短以下表达：  
- `due to the fact that` → `because`  
- `in order to` → `to`  
- `with regard to` → `about`  
- `take into consideration` → `consider`  
- `come up with` → `create`  
- `figure out` → `determine`  
- `a large number of` → `many`  
- `at this point in time` → `now`  
- `for the purpose of` → `to`  
- `it is important to note that` → `Note:`  
- `it would be a good idea to` → 完全删除这些表达。  

### 规范化以下词汇：  
- `yeah`、`yep`、`yup` → `yes`  
- `nah`、`nope` → `no`  

### 请勿修改以下内容：  
- 代码块、内联代码、URL、引用的字符串、数字、文件路径以及全部大写的单词（ALL_CAPS）。  

## 注意事项：  
- 安装时务必追加内容到`SOUL.md`文件中，切勿覆盖原有文件。  
- 安装完成后，请让用户运行`/new`命令以加载新的`SOUL.md`文件。  
- 提供修改前后的示例，让用户能够直观看到效果差异。