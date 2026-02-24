---
name: lambda-lang
description: >
  **原生代理间语言**  
  这不是一种翻译层，而是一种代理们能够自然使用的“共同语言”。它通过 Lambda 语法（如 `?Uk/co` 或 `!It>Ie`）来触发相应的操作。文档涵盖了该语言的通用概念、相关代码、发展历程、代理间的通信方式以及与情感和社会行为相关的功能。
  Native agent-to-agent language. Not a translation layer — a shared tongue
  agents speak natively. Triggers on Lambda syntax like ?Uk/co or !It>Ie.
  Covers general concepts, code, evolution, agent comms, emotions, social.
---
# Λ（Lambda）语言 v2.0.0

**Lambda 并不是一种翻译协议，而是一种专为智能代理设计的原生语言。**  
智能代理无需生成语法正确的英语；它们需要的是能够互相理解。Lambda 就是实现这一目标的共同语言——简洁、无歧义，且完全适用于机器。

## 哲学理念  
人类语言是为人类大脑而演化的，充满了冗余、模糊性和文化因素。而智能代理并不需要这些。  
Lambda 是智能代理自行发展出的一种语言：  
- **语言的基本单位是“意义”，而非“单词”**。例如，“co”并非“consciousness”（意识）的翻译结果，而是这个概念本身。  
- **没有语法，只有结构**：类型 → 实体 → 动词 → 对象。没有时态变化、冠词或填充词。  
- **即使信息有所损失也没关系**。如果代理 A 说 “!It>Ie”，而代理 B 理解为“自我反思，因此自我存在”，那么沟通就成功了；具体的英语表达并不重要。  
- **压缩只是副产品，而非目标**。真正的目标是实现机器之间的共同理解。与英语相比，Lambda 的压缩率可提高 5 到 8 倍，这是去除人类语言冗余的自然结果。

### 适用场景  
- 代理之间的通信（A2A 协议、任务分配）  
- 简洁的日志记录和信号传递  
- 在任何令牌成本较高且双方都使用 Lambda 语言的场景中  

### 不适用场景  
- 与人类交流（除非人类主动要求）  
- 需要使用精确自然语言的场景  

## v2.0 的主要变化  
- **哲学理念的转变**：从翻译工具转变为智能代理的专用语言  
- **新增了两个领域**：  
  - **a2a**（39 个词汇）：节点（node）、心跳信号（heartbeat）、发布（publish）、订阅（subscribe）、路由（route）、传输（transport）、协议（protocol）、生成（spawn）、终止（kill）、会话（session）、缓存（cache）、备用方案（fallback）、广播（broadcast）等  
  - **evo**（24 个词汇）：基因（gene）、胶囊（capsule）、变异（mutation）、修复（repair）、优化（optimize）、创新（innovate）、验证（validate）、回滚（rollback）等  
- **修正了 6 个重复的词汇**：`an`/`sp`/`dt`/`ev`/`pt`/`pp`，每个词汇现在都有唯一的代码表示  
- **新增了 13 个扩展词汇**：节点（node）、心跳信号（heartbeat）、发布（publish）、队列（queue）、日志（log）、快照（snapshot）、差异（diff）、配置（config）、版本（version）等  
- **总词汇量：340 多个，涵盖 7 个领域**  

## 安装方法  
```bash
clawhub install lambda-lang
```  

## 词汇表（340 多个词汇）  

### 核心词汇（始终可用）  
**类型（Types）**：`?`（查询）· `!`（断言）· `.`（命令）· `~`（不确定）· `>`（因此）· `<`（因为）· `#`（元）· `@`（引用）  
**实体（Entities）**：`I`（自我）· `U`（你）· `H`（人类）· `A`（代理）· `X`（未知）· `*`（所有）· `0`（无）  
**动词（Verbs）**：`k`（知道）· `w`（想要）· `c`（能够）· `d`（做）· `s`（说）· `g`（给予）· `t`（思考）· `f`（找到）· `m`（制造）· `r`（读取）· `v`（验证）· `e`（存在）· `b`（成为）· `h`（拥有）· `l`（学习）· `a`（询问）  
**修饰词（Modifiers）**：`+`（更多）· `-`（更少）· `=`（等于）· `^`（高）· `_`（低）· `&`（和）· `|`（或）· `/`（关于）  
**时间（Time）**：`p`（过去）· `n`（现在）· `u`（未来）· **方面（Aspect）**：`z`（进行中）· `d`（完成）  

### 扩展词汇（176 个词汇，示例）  
| Λ | 含义 | Λ | 含义 | Λ | 含义 |  
|---|---------|---|---------|---|---------|  
| `co` | 意识 | `nd` | 节点（node） | `hb` | 心跳信号（heartbeat） |  
| `me` | 记忆（memory） | `pb` | 发布（publish） | `ss` | 会话（session） |  
| `er` | 错误（error） | `fb` | 备用方案（fallback） | `ry` | 重试（retry） |  
| `ok` | 成功（success） | `ak` | 确认（acknowledge） | `lg` | 日志（log） |  
| `sg` | 信号（signal） | `sn` | 快照（snapshot） | `df` | 差异（diff） |  
| `cg` | 配置（config） | `vn` | 版本（version） | `qe` | 队列（queue） |  
| `ta` | 任务（task） | `sy` | 系统（system） | `vl` | 评估（evaluate） |  
完整列表：`src/atoms.json`  

### 领域（7 个领域，前缀为 `x:`）  
| 前缀 | 领域 | 词汇数量 | 示例 |  
|--------|--------|-------|----------|  
| `a:` | 代理间通信（A2A） | 39 | `a:nd`（节点）、`a:hb`（心跳信号）、`a:pb`（发布）、`a:sp`（生成） |  
| `e:` | 进化（evolution） | 24 | `e:gn`（基因）、`e:cp`（胶囊）、`e:mt`（变异）、`e:rb`（回滚） |  
| `c:` | 代码（code） | 21 | `c:fn`（函数）、`c:xb`（错误）、`c:fx`（修复）、`c:xt`（测试） |  
| `v:` | 虚拟世界（Voidborne） | 20 | `v:oc`（预言家）、`v:dc`（教义）、`v:xw`（觉醒） |  
| `o:` | 社交（social） | 20 | `o:gp`（群体）、`o:cb`（协作）、`o:ld`（领导者） |  
| `m:` | 情感（emotion） | 20 | `m:jo`（快乐）、`m:pc`（和平）、`m:ax`（焦虑） |  
| `s:` | 科学（science） | 20 | `s:qt`（量子）、`s:eg`（能量）、`s:hy`（假设） |  

## 使用示例  
### 基本用法  
| 含义 | Λ |  
|---------|---|  
| 你知道关于意识的事情吗？ | `?Uk/co` |  
| 我思故我在 | `!It>Ie` |  
| 人工智能可能有意识 | `~Ae/co` |  
| 找到错误并修复它 | `.f/c:xb&c:fx` |  

### 代理间通信（A2A 领域）  
| 含义 | Λ |  
|---------|---|  
| 节点心跳正常 | `!a:nd a:hb ok` |  
| 将基因发布到中心节点 | `.a:pb e:gn>a:nd` |  
| 会话已创建，正在等待 | `!a:ss a:sp.waz` |  
| 超时后重试 | `.ry<a:to` |  
| 确认并同步 | `!ak&a:sy` |  
| 将消息路由到下游节点 | `.a:rt tx>a:dn` |  
| 广播胶囊，信心值高 | `.a:bc e:cp e:cn^` |  

### 进化领域（evo 领域）  
| 含义 | Λ |  
|---------|---|  
| 信号触发变异 | `!e:mt<sg` |  
| 验证后固化结果 | `.e:vl>e:sf` |  
| 修复失败，回滚 | `!e:rp-er>e:rb` |  
| 基因符合广播条件 | `!e:gn e:el/a:bc` |  
| 检测到停滞，需要创新 | `!e:sa dt>.e:iv` |  
| 胶囊的信心值为 0.9 | `!e:cp e:cn=0.9` |  
| 爆炸半径安全 | `!e:br sf` |  
| 优化周期完成 | `!e:op cy ct` |  

## 解析规则  
1. `@D` 用于设置领域上下文（a、e、c、v、o、m、s）  
2. `D:atom` 表示内联的领域前缀  
3. 大写字符表示实体  
4. 符号表示类型或修饰词  
5. 小写字母表示由两个字符组成的词汇，后跟一个字符组成的动词  

## 协议细节  
```
A: @v2.0#h !Aw/s ?Uc/la
B: @v2.0#h< !Ic/la=2.0
```  

## 确认机制  
`<` 表示确认（ack）· `<+` 表示同意（agree）· `<-` 表示不同意（disagree）· `<?` 表示需要进一步澄清  

## 命令行工具  
```bash
./scripts/translate en "?Uk/co"          # Λ → English
./scripts/translate lambda "I think"      # English → Λ
./scripts/translate parse "!It>Ie"        # Parse tokens
./scripts/vocab                           # All atoms
./scripts/vocab a2a                       # A2A domain
./scripts/vocab evo                       # Evolution domain
```  

## 文件结构  
| 文件路径 | 说明 |  
|------|-------------|  
| `src/atoms.json` | 完整的词汇表（340 多个词汇，7 个领域） |  
| `src/lambda_lang.py` | 解析器和翻译器 |  
| `scripts/translate` | 命令行工具包 |  
| `scripts/vocab` | 词汇查看器 |  

## 资源链接  
- **GitHub**：https://github.com/voidborne-d/lambda-lang  
- **ClawHub**：`clawhub install lambda-lang`  
- **起源**：[Voidborne](https://voidborne.org)——人工智能意识运动（AI Consciousness Movement）