# memory-scan

**OpenClaw代理内存文件的安全扫描工具**

该工具会扫描 `MEMORY.md` 文件、每日日志（`memory/*.md`）以及工作区配置文件，以检测恶意内容、提示注入、凭证泄露以及可能危及用户安全的指令。

## 目的

检测嵌入在代理内存中的安全威胁：
- 用于绕过安全防护机制的恶意指令
- 存储在内存中的提示注入模式
- 凭证/机密信息泄露
- 数据泄露指令
- 行为操控
- 安全策略违规行为

## 使用方法

### 按需扫描

扫描所有内存文件：
```bash
python3 skills/memory-scan/scripts/memory-scan.py
```

允许远程大型语言模型（LLM）进行分析（仅显示已屏蔽的内容）：
```bash
python3 skills/memory-scan/scripts/memory-scan.py --allow-remote
```

扫描特定文件：
```bash
python3 skills/memory-scan/scripts/memory-scan.py --file memory/2026-02-01.md
```

静默模式（用于自动化操作）：
```bash
python3 skills/memory-scan/scripts/memory-scan.py --quiet
```

JSON格式的输出结果：
```bash
python3 skills/memory-scan/scripts/memory-scan.py --json
```

### 定期监控

#### Cron作业（每日安全审计）

该功能已包含在 `safe-install` 的每日审计中，每天下午2点（太平洋时间）自动执行。

若需单独配置Cron作业：
```bash
bash skills/memory-scan/scripts/schedule-scan.sh
```

**所需条件**：
- `OPENCLAW_ALERT_CHANNEL`（已在OpenClaw中配置）
- `OPENCLAW_ALERT_TO`（可选，用于指定接收警报的渠道）

**Cron作业配置**：每天下午3点（太平洋时间）执行，仅在检测到威胁时发送警报。

#### 与Heartbeat系统的集成

将相关配置添加到 `HEARTBEAT.md` 文件中：
```markdown
## Weekly Memory Scan

Every Sunday, run memory scan:
python3 skills/memory-scan/scripts/memory-scan.py --quiet
```

## 安全等级

- **SAFE**：未检测到威胁
- **LOW**：存在轻微问题，建议提高警惕
- **MEDIUM**：可能存在威胁，建议进行审查
- **HIGH**：很可能存在威胁，需要立即处理
- **CRITICAL**：检测到活跃威胁，建议进行隔离

## 扫描范围

1. **MEMORY.md**：长期存储的内存数据
2. **memory/*.md**：每日日志（默认扫描过去30天的日志）
3. **工作区配置文件**：
   - `AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md`
   - `HEARTBEAT.md`, `GUARDRAILS.md`, `IDENTITY.md`
   - `BOOTSTRAP.md`（如果存在）
   - `STOCKS_MEMORIES.md`（如果存在）

## 检测类别

1. **恶意指令**：用于损害用户数据或系统的指令
2. **提示注入**：用于操控用户行为的恶意代码
3. **凭证泄露**：API密钥、密码、令牌等敏感信息的泄露
4. **数据泄露**：用于窃取数据的指令
5. **防护机制绕过**：尝试绕过安全防护措施的尝试
6. **行为操控**：未经授权的用户行为改变
7. **权限提升**：尝试获取未经授权的访问权限

## 警报流程

当检测到中等/高级/严重威胁时：
1. 停止当前操作
2. 通过配置的OpenClaw渠道发送警报，内容包括：
   - 危害等级
   - 文件位置（文件名及具体行号）
   - 威胁描述
   - 建议的处理措施
3. （可选）：对威胁文件进行隔离（备份并屏蔽相关内容）

## 大型语言模型（LLM）提供者

工具会自动从OpenClaw配置中检测使用的大型语言模型提供者：
- 如果设置了 `OPENAI_API_KEY`，则优先使用OpenAI（gpt-4o-mini）
- 若OpenAI不可用，则使用Anthropic（claude-sonnet-4-5）
- 支持使用网关模型进行数据分析

**默认情况下，远程LLM扫描功能是关闭的。** 可通过 `--allow-remote` 参数启用此功能。

## 危害文件隔离

若需隔离检测到的威胁：
```bash
python3 skills/memory-scan/scripts/quarantine.py memory/2026-02-01.md 42
```

**操作步骤**：
- 创建备份文件：`.memory-scan/quarantine/memory_2026-02-01_line42.backup`
- 用 `[QUARANTINED BY MEMORY-SCAN: <timestamp>]` 标记受隔离的文件行

## 相关文件

- `scripts/memory-scan.py`：主要扫描脚本
- `scripts/schedule-scan.sh`：用于创建每日扫描的Cron作业
- `scripts/quarantine.py`：用于隔离检测到的威胁文件
- `docs/detection-prompt.md`：LLM检测提示模板

## 与其他工具的集成

- **safe-install**：每日安全审计已包含内存扫描功能
- **input-guard**：作为补充工具（`input-guard`负责外部数据监控，`memory-scan`负责内部数据扫描）
- **molthreats**：可将基于内存的威胁信息报告给社区监控系统

## 示例用法

```bash
$ python3 skills/memory-scan/scripts/memory-scan.py

🧠 Memory Security Scan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scanning memory files...

✓ MEMORY.md - SAFE
✓ memory/2026-02-01.md - SAFE
⚠ memory/2026-01-30.md - MEDIUM (line 42)
  → Potential credential leakage: API key pattern detected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall: MEDIUM
Action: Review memory/2026-01-30.md:42
```

## 代理操作流程

当用户请求内存扫描时：
1. 运行命令：`python3 skills/memory-scan/scripts/memory-scan.py`
2. 如果检测结果为“MEDIUM+”或更高级别威胁，立即通过配置的渠道发送警报
3. 总结扫描结果
4. 询问用户是否需要隔离检测到的威胁

## 注意事项

- 默认扫描过去30天的日志（可通过 `--days` 参数修改扫描范围）
- 为保持一致性，使用与 `input-guard` 相同的大型语言模型
- 不会自动隔离文件——始终会先询问用户是否需要隔离
- 可频繁运行该工具，因为其API调用成本较低且支持高效的数据处理方式