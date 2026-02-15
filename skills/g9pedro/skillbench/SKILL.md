---
name: skillbench
description: **跟踪技能版本、评估性能、比较改进情况，并获取自我提升的反馈。** 该系统可与 TaskTime 和 ClawVault 集成使用。
metadata:
  openclaw:
    requires:
      bins: [skillbench]
    install:
      - id: node
        kind: node
        package: "@versatly/skillbench"
        bins: [skillbench]
        label: Install SkillBench CLI (npm)
---

# skillbench：AI代理的自我提升技能管理系统

**该系统用于跟踪技能版本、评估性能、比较改进情况，并为后续的优化提供依据。**

**属于[ClawVault](https://clawvault.dev)生态系统的一部分** | [tasktime](https://clawhub.com/skills/tasktime) | [ClawHub](https://clawhub.com)  

## 安装  
```bash
npm install -g @versatly/skillbench
```  

## 主要功能循环  
```
1. Use a skill    → skillbench use github@1.0.0
2. Do the task    → tt start "Create PR" && ... && tt stop
3. Record result  → skillbench record "Create PR" --success
4. Check scores   → skillbench score github
5. Improve skill  → Update skill, bump version
6. Repeat         → Compare v1.0.0 vs v1.1.0
```  

## 命令  
### 跟踪技能进度  
```bash
skillbench use github@1.2.0            # Set active skill version
skillbench skills                       # List tracked skills + signals
```  

### 记录基准测试结果  
```bash
# Auto-pulls duration from tasktime
skillbench record "Create PR" --success

# Manual duration
skillbench record "Create PR" --duration 45s --success

# Record failures
skillbench record "Create PR" --fail --error-type "auth-error"
```  

### 评分与比较  
```bash
skillbench score                        # All skills with grades
skillbench score github                 # Single skill
skillbench compare github@1.0.0 github@1.1.0
```  

### 导出数据与查看仪表盘  
```bash
skillbench export --format markdown
skillbench export --format json
skillbench dashboard                    # Generate HTML dashboard
skillbench dashboard --open             # Generate and open in browser
```  

### 自动化测试  
```bash
skillbench test tasktime@1.1.0          # Run smoke test
skillbench test tasktime@1.1.0 --suite full  # Run named suite
skillbench test tasktime@1.1.0 --dry-run     # Test without recording
```  

### 数据同步  
```bash
skillbench sync --clawhub               # Import installed skills
skillbench sync --vault                 # Sync to ClawVault
skillbench sync --all                   # Everything
```  

### 系统健康状况监控  
```bash
skillbench health                       # Overall health report with alerts
skillbench watch --once                 # Run all test suites once
skillbench watch --interval 300         # Continuous monitoring every 5 min
```  

### 数据分析与改进方案  
```bash
skillbench improve                      # Get suggestions for weakest skill
skillbench improve github               # Improvement plan for specific skill
skillbench trend tasktime --days 30     # Performance trend over time
skillbench leaderboard                  # Compare agents (multi-agent setups)
skillbench schedule --interval 60       # Generate cron config for auto-testing
```  

### 基线设定与性能退化检测  
```bash
skillbench baseline tasktime --set      # Set baseline from current performance
skillbench baseline --list              # List all baselines
skillbench baseline --check             # Check all baselines (CI-friendly, exits 1 if failing)
skillbench baseline tasktime --remove   # Remove a baseline
```  

### 集成持续集成/持续部署（CI/CD）流程  
```bash
skillbench ci                           # Run all tests + baseline checks
skillbench ci --json                    # JSON output for automation
skillbench badge                        # Generate shields.io badges for README
```  

可复制 `examples/github-action.yml` 文件以快速搭建适用于 GitHub Actions 的工作流程。  

## 评分系统  
| 评分等级 | 分数 | 含义 |
|-------|-------|---------|
| 🏆 A+ | 95-100 | 顶级表现 |
| ✅ A | 85-94 | 优秀 |
| 👍 B | 70-84 | 良好 |
| ⚠️ C | 50-69 | 需改进 |
| ❌ D | <50 | 功能故障 |

评分依据：成功率（40%）、平均耗时（30%）、稳定性（20%）以及性能趋势（10%）。  

## 与 tasktime 的集成  
当省略 `--duration` 参数时，skillbench 会自动从 [tasktime](https://clawhub.com/skills/tasktime) 获取数据：  
```bash
tt start "Create PR" -c git
# ... do work ...
tt stop
skillbench record --success   # Duration auto-pulled
```  

## 与 ClawVault 的集成  
所有基准测试结果会自动同步到 [ClawVault](https://clawvault.dev)。  

## 改进提示  
`skillbench` 会显示以下状态提示：  
- ⚠️ **需要改进**：成功率低于 70%  
- 🕐 **数据过期**：超过 7 天未更新基准测试结果  
- ↘️ **性能下降**：技能表现随时间恶化  

## 相关工具/服务  
- [ClawVault](https://clawvault.dev)：AI 代理的内存管理系统  
- [tasktime](https://clawhub.com/skills/tasktime)：任务计时工具（命令行界面）  
- [ClawHub](https://clawhub.com)：技能交易平台