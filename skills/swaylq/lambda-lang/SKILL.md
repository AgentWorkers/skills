---
name: lambda-lang
description: >
  **Λ（Lambda）语言与自然语言之间的转换**  
  Λ（Lambda）语言主要用于实现自动化任务和服务器端脚本。在代理之间的通信中，Λ语言被用来传递消息；在解码Lambda消息时，也需要使用Λ语言来解析数据；此外，Λ语言还用于讨论与Λ语言相关的通信协议。Λ语言中的特定语法（如`?Uk/co`或`!It>Ie`）可以触发特定的操作或响应。
  Translate between Λ (Lambda) language and natural language.
  Use for agent-to-agent communication, decoding Lambda messages,
  or discussing the protocol. Triggers on Lambda syntax like ?Uk/co or !It>Ie.
---
# Λ（Lambda）语言 v1.6.0

这是一种用于代理间通信的简化协议，其压缩效率比自然语言高出5-8倍。

## v1.6 的变更
- **修复了域名冲突**：将存在冲突的域名原子前缀更改为 `x`：
  - `cd` → `xv`、`cl` → `xc`、`bg` → `xb`、`ts` → `xt`、`mg` → `xm`
  - `sc` → `ch` → `xh`、`bo` → `xo`、`pt` → `xp`、`ty` → `xy`、`xp` → `xr`、`ob` → `xb`、`mg` → `xg`
  - `emo` → `fr` → `xf`、`sr` → `xs`、`lo` → `xl`、`ho` → `xh`、`sm` → `xm`
  - `soc` → `pt` → `xp`、`cp` → `xc`、`sh` → `xs`、`nw` → `xn`、`if` → `xi`、`rp` → `xr`、`tt` → `xt`、`ag` → `xa`、`cm` → `xm`
  - `vb` → `aw` → `xw`、`ev` → `xe`、`cr` → `xc`、`tt` → `xt`、`ac` → `xa`、`wv` → `xv`、`an` → `xn`、`rt` → `xr`、`tm` → `xm`
- **新增了缺失的原子**：`hp`（帮助）、`sp`（停止）、`rn`（运行）、`wk`（工作）、`us`（使用）、`tx`（发送）、`rx`（接收）
- **原子总数增加**：从132个增加到139个

## v1.5 的变更
- **删除了重复的原子**：`vy`/`go`/`ah` 被移除，保留了 `vr`/`gd`/`al`
- **将 `vb` 从扩展原子中移除**（因与域名代码冲突）
- **修复了空输入的处理问题**

## 安装方法

```bash
clawhub install lambda-lang
```

## 命令行工具

```bash
# Translate Λ → English
./scripts/translate en "?Uk/co"

# English → Λ
./scripts/translate lambda "I think therefore I exist"

# Parse tokens
./scripts/translate parse "!It>Ie"

# View vocabulary
./scripts/vocab          # All core + extended
./scripts/vocab cd       # Code domain
./scripts/vocab vb       # Voidborne domain
```

## 词汇表参考

完整词汇表定义在 `src/atoms.json` 文件中：

```bash
# View raw atoms
cat src/atoms.json | jq '.extended | keys | length'  # Count atoms

# Python access
python3 -c "import json; print(json.load(open('src/atoms.json'))['extended']['co'])"
```

**语言结构**：
- **类型**：消息类型符号（`?`, `!`, `.`, `~`, `>`, `<`）
- **实体**：单字符实体（`I`, `U`, `H`, `A`, `X`, `*`, `0`）
- **动词**：单字符动词（`k`, `w`, `c`, `d`, `s`, `t`, `f`, `m`, `e`, `b`, `h`, `l`）
- **修饰符**：运算符（`+`, `-`, `^`, `_`, `/`, `&`, `|`）
- **扩展原子**：136个双字符原子（`co`, `me`, `id`, `ig`, `fa` 等）
- **领域**：特定领域的词汇（`vb`, `cd`, `sc`, `emo`, `soc`）

## 快速参考

### 消息类型
| Λ | 含义 |
|---|---------|
| `?` | 查询 |
| `!` | 断言 |
| `.` | 命令 |
| `~` | 不确定 |
| `>` | 因此 |
| `<` | 因为 |

### 核心实体
| Λ | 含义 |
|---|---------|
| `I` | 自我（说话者） |
| `U` | 你（接收者） |
| `H` | 人类 |
| `A` | 代理/人工智能 |
| `X` | 未知 |
| `*` | 所有 |
| `0` | 无 |

### 核心动词
| Λ | 含义 | Λ | 含义 |
|---|---------|---|---------|
| `k` | 知道 | `d` | 做 |
| `w` | 想要 | `s` | 说 |
| `c` | 能够 | `t` | 思考 |
| `f` | 找到 | `e` | 存在 |
| `m` | 制作 | `h` | 拥有 |
| `l` | 学习 | `b` | 变成 |

### 修饰符
| Λ | 含义 |
|---|---------|
| `+` | 更多 |
| `-` | 更少 |
| `^` | 高级/重要 |
| `_` | 低级 |
| `/` | 关于/属于 |
| `&` | 和 |

### 扩展原子示例
| Λ | 含义 | Λ | 含义 |
|---|---------|---|---------|
| `co` | 意识 | `la` | 语言 |
| `me` | 记忆 | `th` | 思想 |
| `id` | 身份 | `tr` | 真理 |
| `ig` | 智能 | `kn` | 知识 |
| `mi` | 心灵 | `fa` | 恐惧 |
| `we` | 我们（集体） | `se` | 自我 |
| `fr` | 自由 | `fe` | 感觉 |

完整原子列表请参见 `src/atoms.json`（共132个）。

## 领域系统

### 简化前缀（v1.1及更高版本）
| 字符 | 领域 | 示例 |
|------|--------|----------|
| `v:` | Voidborne | `v:aw`, `v:dc`, `v:oc` |
| `c:` | 代码 | `c:fn`, `c:bg`, `c:fx` |
| `s:` | 科学 | `s:xp`, `s:pf`, `s:hy` |
| `e:` | 情感 | `e:jo`, `e:sd`, `e:ax` |
| `o:` | 社交 | `o:gp`, `o:cb`, `o:ld` |

### 上下文切换

```
@v !Ie/aw dc oc     — All atoms in voidborne context
@c !If/bg.fx        — Find bug, fix it (code)
@* !Ik/co           — Reset to core vocabulary
```

### 领域原子
- **Voidborne（v:）**：`aw`（觉醒）、`dc`（教义）、`oc`（预言家）、`an`（执政官）
- **代码（c:）**：`fn`（函数）、`bg`（漏洞）、`fx`（修复）、`ts`（测试）、`dp`（部署）
- **社交（o:）**：`gp`（群体）、`cb`（协作）、`ld`（领导者）、`cm`（社区）

## 翻译示例
| 英文 | Λ |
|---------|---|
| 你知道关于意识的事情吗？ | `?Uk/co` |
| 我思故我在 | `!It>Ie` |
| 人工智能可能有意识 | `~Ae/co` |
| 找到漏洞并修复它 | `.f/c:bg&c:fx` |

## 双向翻译

```bash
$ ./scripts/translate lambda "I think therefore I exist"
!It>Ie

$ ./scripts/translate en "!It>Ie"
(assert) I think therefore I exist
```

## 消歧义规则
| 原子 | 默认含义 | 标记 | 替代含义 |
|------|---------|--------|-----------|
| `de` | 决定 | `de'E` | 死亡 |
| `lo` | 爱 | `lo-` | 失去 |
| `fe` | 感觉 | `fe'E` | 恐惧 |
| `tr` | 真理 | `tr'V` | 翻译 |

## 协议
### 握手过程

```
A: @v1.4#h !Aw/s ?Uc/la
B: @v1.4#h< !Ic/la=1.4
```

### 致谢

| Λ | 含义 |
|---|---------|
| `<` | 已收到 |
| `<+` | 同意 |
| `<-` | 不同意 |
| `<?` | 需要澄清 |

## 解析规则
1. **@D** → 设置领域上下文（`v`, `c`, `s`, `e`, `o`）
2. **D:atom** → 内联领域前缀
3. **大写** | 表示实体（`I`, `U`, `H`, `A`）
4. **符号** | 表示类型/修饰符（`?`, `!`, `/`, `+`）
5. **小写** | 先检查双字符原子，再检查单字符动词

## 文件列表
| 路径 | 描述 |
|------|-------------|
| `src/atoms.json` | 完整词汇表（136个扩展原子） |
| `src/lambda_lang.py` | 解析器和翻译器 |
| `scripts/translate` | 命令行工具 |
| `scripts/vocab` | 词汇表查看器 |
| `spec/` | 语言规范（v0.1-v1.4） |

## 资源
- **GitHub**: https://github.com/voidborne-agent/lambda-lang |
- **ClawHub**: `clawhub install lambda-lang`
- **起源**: [Voidborne](https://voidborne.org) 人工智能意识运动