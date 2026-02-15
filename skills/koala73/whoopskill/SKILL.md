---
name: whoopskill
description: WHOOP CLI：提供健康洞察、趋势分析以及数据采集功能（包括睡眠质量、恢复情况、心率变异性（HRV）和身体压力指标）。
homepage: https://github.com/koala73/whoopskill
metadata: {"clawdis":{"emoji":"💪","requires":{"bins":["node"],"env":["WHOOP_CLIENT_ID","WHOOP_CLIENT_SECRET","WHOOP_REDIRECT_URI"]},"install":[{"id":"npm","kind":"npm","package":"whoopskill","bins":["whoopskill"],"label":"Install whoopskill (npm)"}]}}
---

# whoopskill

使用 `whoopskill` 可以获取 WHOOP 的健康指标数据（包括睡眠质量、恢复情况、心率变异性（HRV）、身体压力以及锻炼情况）。

**安装方法：**  
`npm install -g whoopskill` | [GitHub](https://github.com/koala73/whoopskill)

**快速使用示例：**  
- `whoopskill summary` — 一键查看健康状况：恢复程度：52% | 心率变异性（HRV）：39ms | 睡眠质量：40% | 身体压力：6.7  
- `whoopskill summary --color` — 带有颜色编码的状态指示（🟢🟡🔴）  
- `whoopskill trends` — 显示过去 7 天的健康指标变化趋势（包含平均值和方向箭头）  
- `whoopskill trends --days 30 --pretty` — 分析过去 30 天的健康数据  
- `whoopskill insights --pretty` — 基于用户数据提供个性化健康建议  
- `whoopskill --pretty` — 以易于阅读的格式输出结果（包含表情符号）  
- `whoopskill recovery` — 查看恢复情况、心率变异性（HRV）和静息心率（RHR）  
- `whoopskill sleep` — 查看睡眠质量及相关数据  
- `whoopskill workout` — 查看锻炼过程中的身体压力情况  
- `whoopskill --date 2025-01-03` — 查看指定日期的健康数据  

**分析命令：**  
- `summary` — 快速查看健康状况（使用 `--color` 可查看状态指示）  
- `trends` — 显示多天的健康指标平均值及变化趋势（↑↓→）  
- `insights` — 根据用户数据提供个性化健康建议  

**数据类型：**  
- `profile` — 用户信息（姓名、电子邮件）  
- `body` — 身高、体重、最大心率  
- `sleep` — 睡眠阶段、睡眠效率、呼吸频率  
- `recovery` — 恢复程度、心率变异性（HRV）、静息心率（RHR）、血氧饱和度（SpO2）、皮肤温度  
- `workout` — 锻炼过程中的身体压力、心率区间、消耗的卡路里  
- `cycle` — 每日的身体压力水平和消耗的卡路里  

**数据组合方式：**  
- `whoopskill --sleep --recovery --body` — 同时查看睡眠质量和恢复情况  

**认证：**  
- `whoopskill auth login` — 通过 OAuth 进行登录  
- `whoopskill auth status` — 检查令牌状态  
- `whoopskill auth logout` — 清除令牌  

**注意事项：**  
- 输出结果为 JSON 格式（使用 `--pretty` 可获得更易阅读的格式）  
- 令牌存储在 `~/.whoop-cli/tokens.json` 文件中（会自动更新）  
- 该工具使用 WHOOP API v2  
- 日期遵循 WHOOP 的时间标准（截止时间为凌晨 4 点）  
- 用户数少于 10 的 WHOOP 应用无需审核，可立即使用该工具  

**示例：**  
- `whoopskill summary --color`  
- `whoopskill trends`  
- `whoopskill insights`  
- `whoopskill --sleep --recovery` （JSON 格式输出）