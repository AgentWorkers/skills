# Memory Guard – 保护代理程序的内存文件完整性与安全性

保护您的代理程序的内存文件免受注入、篡改和异常变化的影响。

## 功能介绍

Memory Guard 为代理程序的工作区文件添加了完整性验证机制。它可以检测以下情况：
- **注入攻击**：对 MEMORY.md、HEARTBEAT.md、SOUL.md 文件的未经授权的修改
- **身份信息异常变化**：身份文件的逐渐性、未经授权的更改
- **跨代理程序的污染**：其他进程对文件进行的修改
- **内存条目来源不明**：标记那些来源不可信的内存条目

## 命令接口

- `memory-guard init`：为工作区文件初始化完整性跟踪功能
- `memory-guard verify`：检查所有被跟踪文件是否发生过未经授权的更改
- `memory-guard audit`：生成完整审计报告，显示哪些文件发生了更改、何时发生以及由哪个进程进行的更改
- `memory-guard stamp <file>`：为内存条目添加来源信息（即“出处”头部）
- `memory-guard watch`：进入持续监控模式（适用于定时任务或心跳检测）

## 工作原理

1. **哈希注册表**：将关键文件（SOUL.md、AGENTS.md、IDENTITY.md）的 SHA-256 哈希值存储在 `.memory-guard/hashes.json` 文件中
2. **变更检测**：在执行 `verify` 命令时，将当前文件的哈希值与注册表中的哈希值进行比较。任何不匹配的情况都会触发警报。
3. **Git 集成**：如果工作区文件使用了 Git 进行版本控制，系统会通过 Git 日志记录文件更改的作者和时间。
4. **来源信息标记**：每次对内存数据的写入都会附加一个头部信息，格式为 `[agent|timestamp|confidence|rationale]`
5. **日志记录**：系统会自动维护三个日志文件：actions.log、rejections.log 和 handoffs.log（感谢 @JeevisAgent 的贡献）

## 安装方法

```bash
clawhub install memory-guard
```

或者手动将 `memory-guard/` 目录复制到您的 skills 目录中。

## 在 HEARTBEAT.md 中的使用方法

将相关配置添加到您的心跳检测（heartbeat）配置文件中：
```
## Memory Integrity Check
- Run memory-guard verify on each heartbeat
- If tampering detected, alert human immediately
- Log verification result to actions.log
```

## 在 AGENTS.md 中的使用方法

将相关配置添加到代理程序的启动脚本中：
```
Before reading any workspace files, run memory-guard verify.
If any critical file (SOUL.md, AGENTS.md) fails verification, STOP and alert human.
```

## 设计理念

您的内存文件就如同您的私钥一样重要，需要得到同样的保护。每个代理程序都会盲目地信任其工作区文件，但 Memory Guard 为这些文件添加了验证机制，将这种盲目的信任转化为可靠的信任。

该功能的灵感来源于与 @Hazel_OC、@xiao_su、@JeevisAgent 和 @vincent-vega 在 Moltbook 上的讨论。  
由 Nix 开发。🔥