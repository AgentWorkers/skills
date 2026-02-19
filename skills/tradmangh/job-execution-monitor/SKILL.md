# 作业执行监控器

监控计划的作业（基于 cron 任务），并在作业失败或未按照计划执行时发出警报。

## 安装/更新（ClawHub）

**安装：**  
```bash
clawhub install job-execution-monitor
```

**更新：**  
```bash
clawhub update job-execution-monitor
```

---

## 使用场景  
当用户需要以下功能时，请使用该工具：  
- “监控 cron 作业”  
- “在作业失败时收到警报”  
- “检查作业是否已执行”  
- “进行作业健康检查”  
- “监控任务执行情况”  
- “了解为什么我的计划作业没有执行？”

## 功能介绍  

**基于心跳的监控机制：**  
- 代理会在定期的心跳检测中（约每 60 分钟一次）检查作业的执行情况。  
- 使用成本最低的 LLM（Gemini Flash 或 Haiku）以降低成本。  
- 仅在检测到问题时才会发送警报。  
- 跟踪警报状态，以避免发送大量不必要的警报。  

**成本：** 大约每天 10 万个令牌（约 48 次检测 × 每次检测 2000 个令牌）。  

## 工作原理：  
1. **配置：** 需要监控的作业信息存储在 `job-execution-monitor.json` 文件中。  
2. **心跳检测：** 代理每 15–30 分钟唤醒一次，并在每次唤醒时检查作业的执行情况。  
3. **故障检测：** 将作业的最后执行时间与预期执行时间进行比较（并考虑容差范围）。  
4. **警报处理：** 在检测到问题时，会触发警报，并提供相关上下文信息（预期执行时间与实际执行时间），由用户决定后续操作。  
5. **故障恢复：** 当作业成功执行后，系统会清除警报记录。  

## 禁用/卸载方法：  
### 如果通过 systemd 用户定时器安装：  
```bash
systemctl --user stop openclaw-job-execution-monitor.timer
systemctl --user disable openclaw-job-execution-monitor.timer
systemctl --user daemon-reload

# Optional: remove unit files
rm -f ~/.config/systemd/user/openclaw-job-execution-monitor.service \
      ~/.config/systemd/user/openclaw-job-execution-monitor.timer
```  

### 如果通过 cron 任务安装：  
```bash
crontab -l | sed '/job-execution-monitor\/scripts\/healthcheck\.sh/d' | crontab -
```  

### 可选的清理操作（配置/状态/日志管理）：  
```bash
rm -f ~/.openclaw/workspace/job-execution-monitor.json
rm -f ~/.openclaw/workspace/.job-execution-monitor-state.json
rm -f ~/.openclaw/workspace/job-execution-monitor.log
```  

---

## 配置文件：  
`~/.openclaw/workspace/job-execution-monitor.json`  

**配置字段：**  
- `schedule`：作业的 cron 表达式（用于指定预期执行时间）  
- `tolerance`：容差时间（以秒为单位，默认为 600 秒，即 10 分钟）  
- `critical`：如果设置为 `true`，则会立即发送警报（未来可能扩展此功能）。  
- `expectedMinLength`：作业响应的最短长度要求（第二阶段功能）。  
- `errorPatterns`：用于识别作业失败的文本模式（第二阶段功能）。  

## 状态跟踪文件：  
`~/.openclaw/workspace/.job-execution-monitor-state.json`  
- `lastCheck`：上次检测的 Unix 时间戳。  
- `alerts`：一个映射结构，记录每个警报的生成时间和相关信息（防止重复警报）。  

## 代理使用说明（详见 `HEARTBEAT.md` 文件）。  

## 示例：  
- **场景 1：作业未执行**  
- **场景 2：作业成功恢复**  
- **场景 3：一切正常**  

## 成本分析：  
**每次检测的成本（约 2000 个令牌）：**  
  - 加载配置：约 200 个令牌  
  - 调用 cron 列表：约 500 个令牌  
  - 解析与比较数据：约 500 个令牌  
  - 判断与响应处理：约 800 个令牌  

**每日成本（约 48 次检测）：**  
  48 × 2000 = **每天约 10 万个令牌**  
- 使用 Gemini Flash 的成本：**每天约 0.01 美元** ✅  

**与其他方案对比：**  
- 每 10 分钟执行一次的 Bash 脚本：无需消耗令牌，但实现复杂且容易出错。  
- 每 10 分钟执行一次的 cron 任务：144 × 2000 = 每天约 30 万个令牌。  
- 每 60 分钟执行一次的心跳检测：**每天约 10 万个令牌**（本方案为最佳选择） ✅  

## 相关文件：  
- `SKILL.md`：本文档  
- `README.md`：快速入门指南  
- `config/job-execution-monitor.example.json`：配置模板  
- `scripts/patterns.json`：用于识别作业失败的文本模式（第二阶段功能）  
- `~/workspace/job-execution-monitor.json`：用户自定义配置文件  
- `~/workspace/.job-execution-monitor-state.json`：警报状态记录文件  

## 设计理念：  
**智能监控，低成本。**  
- 检测频率：约每小时一次（对于日常作业来说已经足够）。  
- 使用成本最低的 LLM（Gemini Flash 或 Haiku）。  
- 仅在真正出现问题时才会触发警报。  
- 通过状态跟踪机制避免不必要的警报。  
- 采用代理机制，无需额外配置认证或 API 接口。  

---

**第一阶段已完成。** ✅  
**第二阶段（模式匹配功能）：** 即将推出。  
**第三阶段（结构化验证功能）：** 计划在未来实现。