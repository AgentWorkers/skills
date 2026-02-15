# 目标追踪器技能

通过设置里程碑、每日记录以及强化责任意识来跟踪长期目标。

## 所在目录
`/root/clawd/goal-tracker/`

## 命令

```bash
# Show status
/root/clawd/tracker status

# Log daily activity
/root/clawd/tracker log --trained --business --wins "Description"

# Update MRR
/root/clawd/tracker mrr 5000

# Mark milestone complete
/root/clawd/tracker milestone ironman "5km run"
/root/clawd/tracker milestone mrr_100k "first client"

# Weekly summary
/root/clawd/tracker week

# Generate HTML dashboard
/root/clawd/goal-tracker/generate-dashboard
```

## 数据文件
- `data/goals.json` - 目标定义及里程碑
- `data/daily-log.json` - 每日记录
- `index.html` - 生成的可视化仪表盘

## 与Alto的集成

### 晚间检查时
询问：“今天有进行训练吗？处理了业务相关的工作吗？”
然后记录：`tracker log --trained --business`（或 `--no-trained` 等）

### 当达成目标时
记录：`tracker log --wins "成功获得了新客户"` 

### 当MRR（每月收入）发生变化时
更新：`tracker mrr 5000`

### 当里程碑完成时
标记：`tracker milestone ironman "完成5公里跑步"` 

## 被追踪的目标

### Ironman挑战（2030年前）
里程碑：
1. 一次性跑完5公里
2. 完成短距离铁人三项比赛
3. 完成奥运会标准距离的游泳和跑步项目
4. 完成半程铁人三项（70.3公里）
5. 完成全程铁人三项

### 每月收入达到10万美元（2030年前）
里程碑：
1. 获得第一个付费客户
2. 月收入达到5000美元
3. 月收入达到1万美元
4. 月收入达到2.5万美元
5. 月收入达到5万美元
6. 月收入达到10万美元

## 每周工作流程
- 周一：制定本周计划（确定优先事项）
- 每日：晚间检查（记录训练和业务进展）
- 周五：回顾本周进展（评估并调整计划）

## 需注意的规律
- 连续3天未进行训练 = 发出提醒
- 当周收入低于50% = 检查阻碍目标实现的因素
- 里程碑日期临近 = 提高完成紧迫性