# slack-standup SKILL.md

## 技能简介
- 名称：slack-standup  
- 版本：1.0  
- 许可证：MIT  
- 类别：生产力 / 团队协作  

## 描述  
这是一个用于 Slack 的自动化每日站会（standup meeting）工具。它会在预定时间收集团队成员的更新信息，汇总回复内容，并将汇总结果发布到指定的频道中。  

## 商业价值  
- 问题：远程团队在安排站会时浪费时间。  
- 解决方案：通过 Slack 机器人实现异步站会。  
- 投资回报（ROI）：每位团队成员每天可节省 15–30 分钟的时间。  

## 功能  
1. `collect_standup`：提示团队成员提供每日更新内容。  
2. `aggregate_responses`：将收到的回复整理成格式化的摘要。  
3. `post_summary`：将汇总结果发布到指定的 Slack 频道。  
4. `schedule_reminder`：设置每日重复提醒。  

## 所需工具  
- Slack 机器人 API（xoxb-* 令牌）  
- Cron 定时任务  
- 文本格式化工具（Slack MRKDWN）  

## 安装步骤  
1. 执行命令：`clawhub install slack-standup`  
2. 配置 Slack 机器人的访问令牌。  
3. 设置站会时间（默认为上午 9:00）。  
4. 测试功能：`/standup test`  

## 定价方案  
- 一次性购买：25 美元  
- 订阅服务：每月 5 美元  
- 团队套餐：50 美元（最多 10 名成员）