---
name: acp-loop
description: 使用间隔时间或 Cron 表达式来安排 AI 代理提示的重复执行。适用于用户需要定期运行提示、按计划自动执行代理任务或设置重复工作流程的情况。触发方式包括：“schedule prompt”、“run every”、“cron”、“recurring”、“periodic”、“interval”、“loop prompt”。
---
# acp-loop：循环提示调度器  
用于按固定间隔或cron计划表运行AI代理提示。  

## 适用场景  
当用户需要：  
- 在固定时间间隔内重复运行提示；  
- 为代理任务设置cron风格的调度；  
- 自动化重复性的AI工作流程；  
- 询问关于提示的调度、循环或定期执行的相关问题时，可以使用此工具。  

## 安装  
```bash
npm install -g acp-loop
```  

## 快速入门  

### 定时模式  
按固定间隔运行提示：  
```bash
# Every 5 minutes
acp-loop --interval 5m "check logs for errors"

# Every 30 seconds, stop after 10 iterations
acp-loop --interval 30s --max 10 "quick health check"

# Every hour, timeout after 8 hours
acp-loop --interval 1h --timeout 8h "hourly report"
```  

### Cron模式  
根据cron计划表运行提示：  
```bash
# Daily at 3am
acp-loop --cron "0 3 * * *" "nightly cleanup"

# Every Monday at 9am
acp-loop --cron "0 9 * * 1" "weekly standup summary"

# Every 5 minutes (cron style)
acp-loop --cron "*/5 * * * *" "monitor status"
```  

## 选项参考  
| 选项          | 描述                                      | 示例                                        |  
|------------------|-----------------------------------------|-----------------------------------------|  
| `--interval <时长>`    | 固定间隔（30秒、5分钟、1小时）                         | `--interval 5m`                                   |  
| `--cron <表达式>`    | Cron表达式                                    | `--cron "0 9 * * *"`                               |  
| `--agent <名称>`     | 使用的代理（默认：codex）                             | `--agent claude`                                   |  
| `--max <次数>`     | 最大迭代次数                                      | `--max 10`                                      |  
| `--timeout <时长>`    | 最大总运行时间                                  | `--timeout 2h`                                   |  
| `--until <字符串>`    | 当输出包含指定内容时停止                          | `--until "DONE"`                                   |  
| `--quiet`       | 最小化输出显示                                | `--quiet`                                   |  

## 常见用法模式  
- **条件停止**：  
```bash
# Run until task reports completion
acp-loop --interval 1m --until "All tests passed" "run test suite"
```  
- **有限次运行**：  
```bash
# Run exactly 5 times
acp-loop --interval 10s --max 5 "check deployment status"
```  
- **定时执行**：  
```bash
# Run for max 1 hour
acp-loop --interval 5m --timeout 1h "monitor build"
```  
- **每日定时任务**：  
```bash
# Every day at midnight
acp-loop --cron "0 0 * * *" "generate daily report"
```  
- **使用不同代理**：  
```bash
# Use Claude instead of Codex
acp-loop --interval 10m --agent claude "review code changes"

# Use Gemini CLI
acp-loop --interval 5m --agent gemini-cli "check status"
```  

## 重要说明：  
1. **互斥性**：只能选择使用`--interval`或`--cron`，不能同时使用。  
2. **Cron库**：采用`croner`库（在笔记本电脑的睡眠/唤醒模式下表现更稳定）。  
3. **停止循环**：按Ctrl+C键可终止循环。  
4. **代理支持**：兼容所有ACP兼容的代理（如codex、claude、gemini-cli）。  

## 选择acp-loop的理由：  
- Claude Code内置的`/loop`命令存在缺陷；  
- 支持所有ACP兼容的代理；  
- 提供完善的Cron表达式支持；  
- 在笔记本电脑的睡眠/唤醒模式下运行更稳定。  

## 资源链接：  
- GitHub：https://github.com/femto/acp-loop  
- npm：https://www.npmjs.com/package/acp-loop