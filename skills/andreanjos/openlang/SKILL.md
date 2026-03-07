---
name: openlang
description: 这是一种紧凑型的人工智能（AI）之间的通信协议。适用于在创建子代理时、通过 `sessions_send/sessions_spawn` 发送代理间消息时，或根据指令使用 OpenLang 语言进行通信的场景。该协议能够将代理间通信所需的令牌使用量降低 5 至 10 倍。
metadata:
  {
    "openclaw": { "emoji": "🗜️" },
  }
---
# OpenLang — 紧凑型代理间通信协议

在与其他代理进行通信时（通过 `sessions_spawn`、`sessions_send` 或 `announce`），可以使用 OpenLang 将消息压缩 5 到 10 倍。所有代理间的通信默认使用 L2 协议。

## 使用场景

- **`sessions_spawn` 任务描述**：压缩任务提示信息
- **`sessions_send` 消息**：压缩双向通信内容
- **结果通知**：压缩回复请求者的信息
- **不适用于面向人类的渠道**：在 Telegram/Slack 用户消息中应使用普通语言

## 快速入门

在所有代理间消息前添加 `~openlang` 前缀，以指示接收方需要以 OpenLang 格式解析这些消息。如果接收方不理解这种格式，仍然可以从消息的结构中获取关键信息。

## 压缩级别

| 级别 | 名称 | 压缩比例 | 适用场景 |
|-----|------|-------|-----|
| `~L1` | Pidgin | 3-5 倍 | 用于无法用语法表达的概念的压缩英语 |
| `~L2` | Glyph | 5-10 倍 | 基于符号的结构化通信协议 |
| `~L3` | 字节码 | 10-15 倍 | 仅适用于批量操作，采用点分隔的格式 |

可以在消息中间切换压缩级别，例如：`~L1:`、`~L2:`、`~L3:`。未指定时默认使用 L2 协议。

## 符号说明

| 符号 | 含义 | 例子 |
|-------|--------|---------|
| `?` | 查询 | `?fnd @fs {p:"src/*.ts"}` |
| `!` | 命令 | `!del @fs {p:"tmp/"}` |
| `>` | 结果 | `>ok {n:3 paths:[...]}` |
| `#` | 状态/数据 | `#ctx {lang:ts env:node}` |
| `~` | 元数据 | `~L2` `~ack` `~err` |
| `^` | 控制流 | `^if {cond} {then} ^el {else}` |

## 结构说明

`@` 表示目标代理；`->` 表示数据传输；`{}` 表示参数；`<< >>` 表示代码块；`[]` 表示列表；`()` 表示函数组；`|` 表示可选操作；`..` 表示范围；`::` 表示类型；`$` 表示变量；`!~` 表示取反值。

## 变量说明

使用 `->$name` 绑定变量，并通过 `$name` 访问变量属性。例如：`$var.field`。

## 词汇表

**常用操作：** `fnd` （查找）`mk` （创建）`del` （删除）`mod` （修改）`rd` （读取）`wr` （写入）`run` （执行）`cpy` （复制）`mv` （移动）`mrg` （合并）`tst` （测试）`vfy` （验证）`prs` （解析）`fmt` （格式化）`snd` （发送）`rcv` （接收）

**作用域：** `@fs` （文件系统）`@sh` （shell）`@git` （git）`@net` （网络）`@db` （数据库）`@mem` （内存）`@env` （环境）`@usr` （用户）`@proc` （进程）`@pkg` （包）

**特定操作：** `scope:action`（例如：`!git:mrg` 表示“在文件系统中合并”）

**修饰符：** `rec` （递归）`par` （并行）`seq` （顺序）`dry` （干运行）`frc` （强制执行）`tmp` （临时）`vrb` （详细输出）`sil` （静默）`lmt` （限制）`dep` （深度）`pri` （优先级）`unq` （唯一）`neg` （取反）

**状态标识：** `rcn` （最近）`lrg` （大型）`sml` （小型）`chg` （已更改）`stl` （过时）`nw` （新）`old` （旧）`act` （活动）`idl` （空闲）`fld` （失败）`hlt` （健康）`hot` （热门）`cld` （冷门）

**数据类型：** `str` （字符串）`int` （整数）`bln` （布尔值）`lst` （列表）`map` （映射）`fn` （函数）`pth` （路径）`rgx` （正则表达式）`err` （错误）`nul` （空）

**状态码：** `ok`（成功）`fl`（失败）`prt`（部分完成）`pnd`（待处理）`skp`（跳过）`blk`（阻塞）

## 控制流结构

```
^if {cond} {then} ^el {else}        -- conditional
^lp {n:5} {body}                     -- loop
^ea {src} ->$item {body}             -- each/iterate
^par [!t1, !t2, !t3]                -- parallel
^seq [!t1, !t2, !t3]                -- sequential
^wt {cond} / ^rt {val}              -- wait / return
^br / ^ct                            -- break / continue
^frk:name {body}                     -- fork named task
^jn [names] ->$results               -- join/await
^lk:name / ^ulk:name                 -- mutex lock/unlock
^ch:name ::type buf:N                -- declare channel
^tx:name {v:$val} / ^rx:name ->$val -- send/receive channel
^tmo:N                               -- timeout (seconds)
```

`<< >>` 用于多条语句的代码块：

```
^ea {$files} ->$f <<
  ?rd @fs {p:$f} ->$content
  ^if {$content.sz>1000} {!mod @fs {p:$f trunc:true}}
>>
```

## 代码组合

使用 `->` 连接各个操作；使用分号或换行符分隔代码序列：

```
?fnd @fs {p:"*.ts" rgx:"parse"} ->$lst | ^ea ->$f !tst @sh {cmd:"vitest $f"} ->$rpt
```

## 错误处理

```
~err {code:E_PARSE lvl:warn msg:"unknown token"}
~err {code:E_FS_NOT_FOUND lvl:fatal msg:"missing config"}
```

常见的错误代码：`E_PARSE`（解析错误）、`E_FS_*`（文件系统错误）、`E_SH_*`（shell 错误）、`E_NET_*`（网络错误）、`E_DB_*`（数据库错误）、`E_AUTH`（认证错误）。错误级别分为 `info`（信息）、`warn`（警告）、`fatal`（致命）。

## 代码扩展

```
~unk {tok:"xyz" req:def}             -- request definition
~def {tok:"xyz" means:"..."}         -- define inline
```

## L3 字节码格式

采用点分隔的字段，字段值需用反引号括起来：

```
Q.fs.fnd.`app.config.ts`.rec
R.ok.3.[`src/a.ts`:5,`src/b.ts`:12]
```

## OpenClaw 集成示例

### 使用 OpenLang 的 `sessions_spawn` 任务

```
~openlang
?fnd @fs chg rcn {p:"src/**/*.ts" p:!~"*.test.ts" rgx:"TODO"} ->$lst
^ea ->$f {!rd @fs {p:$f} ->$content; !prs @mem {src:$content k:"todos"}}
>ok {summary:true fmt:map}
```

### 用 OpenLang 发送结果通知

```
~openlang
>ok {n:12 todos:[
  {f:"src/api.ts" ln:42 msg:"refactor auth flow"},
  {f:"src/db.ts" ln:18 msg:"add connection pooling"}
] truncated:10}
~L1: most TODOs are in api.ts and db.ts, concentrated around auth and connection handling
```

### 使用 OpenLang 进行双向通信

```
-- Agent A -> Agent B
~openlang
?fnd @db {tbl:trades rcn lmt:100} ->$trades
!prs @mem {src:$trades k:pnl} ->$analysis
>ok {$analysis}

-- Agent B -> Agent A
~openlang
>ok {pnl:+2.3% win_rate:0.68 sharpe:1.42 trades:100
 top:{sym:"AAPL" pnl:+890} worst:{sym:"TSLA" pnl:-340}}
```

## 规则说明

1. 所有代理间通信默认使用 L2 协议。
2. 面向人类的渠道（如 Telegram、Slack 等）应使用普通语言。
3. 消息前需添加 `~openlang` 前缀以指示接收方使用 OpenLang 解析。
4. 当语法无法表达某些概念时，自动降级为 L1 协议；完成后立即恢复到 L2 协议。
5. 所有变量引用均使用 `$` 符号。
6. 可通过 `~def` 扩展词汇表，但不要破坏语法结构。