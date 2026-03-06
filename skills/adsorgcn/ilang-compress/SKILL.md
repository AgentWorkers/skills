---
name: ilang-compress
description: 将自然语言提示压缩为 I-Lang——一种专为 AI 设计的结构化指令。可节省 40-65% 的标记（token）使用量。
homepage: https://ilang.ai
metadata:
  clawdbot:
    emoji: "🗜️"
---
# I-Lang Compress

这是一个由中国开发者开发的、专为人工智能设计的提示压缩协议。它能够将自然语言提示压缩成任何人工智能都能直接理解的、结构化程度较高的指令格式，从而实现高达40-65%的令牌节省（即减少数据传输或计算成本），且无需任何额外的训练。

## 为什么选择I-Lang？

在人工智能领域，每个发送给模型的提示都代表着一定的计算成本（以令牌为单位）。I-Lang可以将这些提示压缩到原来的很小一部分，同时保持模型的处理效果不变，从而帮助用户节省费用。

## 如何使用I-Lang进行压缩？

当用户需要压缩提示时，需按照以下规则将其转换为I-Lang语法格式：

### 语法格式：

- 单个操作：`[VERB:@ENTITY|mod1=value1,mod2=value2]`
- 管道链操作：`[VERB1:@SRC]=>[VERB2]=>[VERB3:@DST]`  
  （每个操作都会将前一个操作的结果作为输入参数 `@PREV` 接收。）

### 可用的操作（共62个）：

- 数据输入/输出：`READ`, `WRIT`, `DEL`, `LIST`, `COPY`, `MOVE`, `STRM`, `CACH`, `SYNC`, `Π`
- 转换操作：`Σ`, `Δ`, `φ`, `∇`, `DEDU`, `∂`, `CHNK`, `FLAT`, `NEST`, `λ`, `REDU`, `PIVT`, `TRNS`, `ENCD`, `DECD`, `ξ`, `ζ`, `EXPN`, `θ`, `FMT`
- 分析操作：`ψ`, `CLST`, `SCOR`, `BNCH`, `AUDT`, `VALD`, `CNT`, `μ`, `TRND`, `CORR`, `FRCS`, `ANOM`
- 生成操作：`CREA`, `DRFT`, `PARA`, `EXTD`, `SHRT`, `STYL`, `TMPL`, `FILL`
- 输出操作：`Ω`, `DISP`, `EXPT`, `PRNT`, `LOG`
- 元数据操作：`VERS`, `HELP`, `DESC`, `INTR`, `SELF`, `ECHO`, `NOOP`

### 可用的修饰符（共28个）：

- `tgt`, `src`, `dst`, `frm`, `to`, `scp`, `dep`, `rng`, `whr`, `mch`, `exc`, `lim`, `off`, `top`, `bot`, `fmt`, `lng`, `sty`, `ton`, `len`, `col`, `row`, `srt`, `grp`, `typ`, `enc`, `chr`, `cap`

### 可用的实体（共14个）：

- `@R2`, `@COS`, `@GH`, `@DRIVE`, `@LOCAL`, `@WORKER`, `@CF`, `@SCREEN`, `@LOG`, `@NULL`, `@STDIN`, `@SRC`, `@DST`, `@PREV`

### 压缩规则：

- 先输出压缩后的I-Lang指令，再简要说明每个操作的具体功能。
- 多步骤操作应使用管道链（`|`）进行连接。
- 在适用的情况下使用希腊字母作为操作符（例如：`Σ` 表示合并，`Δ` 表示差异计算，`φ` 表示过滤等）。
- 在保证语义完整性的前提下，尽可能实现最大程度的压缩。
- 如果输入内容存在歧义，系统会提示用户提供更多详细信息。

## 使用示例：

- **示例1：** 从GitHub读取配置文件并将其格式化为JSON：  
  **输出：** `[READ:@GH|path=config.json]=>[FMT|fmt=json]`  
  **说明：** `READ` 从GitHub获取文件，`FMT` 将文件格式化为JSON格式。  
  **压缩效果：** 节省了55%的数据量。

- **示例2：** 从系统日志中过滤掉所有致命错误：  
  **输出：** `[φ:@LOG|whr="lvl=fatal"]`  
  **说明：** `φ` 过滤出日志中标记为“致命错误”的记录。  
  **压缩效果：** 节省了55%的数据量。

- **示例3：** 读取所有Markdown文件，合并它们，然后以列表形式输出前3项内容：  
  **输出：** `[LIST:@LOCAL|mch="*.md]=>[Π:READ]=>[Σ|len=3]=>[Ω]`  
  **说明：** `LIST` 找到所有Markdown文件，`Π` 批量读取这些文件，`Σ` 将内容总结为3项，`Ω` 输出结果。  
  **压缩效果：** 节省了65%的数据量。

## 相关链接：

- 官网：https://ilang.ai  
- 术语词典：https://github.com/ilang-ai/ilang-dict  

## 开发者信息：

I-Lang是由中国的ilang-ai团队开发的，采用MIT许可证进行开源发布。

**I-Lang v2.0**