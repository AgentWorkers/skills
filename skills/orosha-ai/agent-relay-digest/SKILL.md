---
name: agent-relay-digest
description: "创建经过精心整理的代理对话摘要（例如 Moltbook），方法包括收集相关帖子、对主题进行分类、根据重要性对内容进行排序，然后生成一份简洁的摘要，其中包含关键信息、参与讨论的成员以及后续需要执行的操作。这种工具可用于总结代理论坛的内容、生成每日/每周的摘要、确定需要关注的对象，或从大量信息中筛选出有价值的内容。"
---

# 代理中继摘要（Agent Relay Digest）

## 概述  
从各个代理社区中收集信息，生成一份内容精炼的摘要：收集帖子、整理主题，根据信息的重要性进行排序，并输出一份简洁、具有行动指导意义的报告。

## 工作流程（端到端）  

### 1) 确定范围  
- 选择数据来源（如子论坛、消息流等）以及时间范围（例如过去24小时）。  
- 确定目标受众（如开发者、安全专家、工具使用者等）。  

### 2) 收集帖子及元数据  
- 下载帖子、评论以及用户的互动数据（如点赞数、评论数量、作者信息等）。  
- 将原始数据保存到本地日志文件中以便后续追踪。  

### 3) 分类与排序  
- 按主题对帖子进行分类（通过关键词或内容嵌入方式）。  
- 根据帖子的互动程度、发布时间、具体性以及是否包含“build-log”或“practical”标签来对帖子进行排序。  

### 4) 生成摘要  
- 包括以下内容：  
  - 热门帖子及其重要性  
  - 新出现的主题  
  - 未解决的问题或需要协作的需求  
  - 值得关注的人物（这些人物发布的帖子具有较高的信息价值）  
  - 安全/信任相关警报  

### 5) 验证摘要的质量  
- 先使用预测试版本生成摘要，然后收集用户反馈。  
- 设定成功标准（例如：收到至少3条实质性回复或至少5个关注者）。  

## 推荐的输出格式  
- 标题：**“代理中继摘要 — {日期}”**  
- 包含以下部分：  
  - 统计数据  
  - 热门帖子  
  - 主题汇总  
  - 有价值的信息  
  - 需要关注的人物  
  - 警报信息  

- 使用结构化的数据格式（键=值的形式），以便于数据解析。  
- 显示每个条目的得分明细以及其可信度/质量等级。  
- 包含一个专门用于展示警报信息的部分（安全/信任警告）。  
- 保持整体长度简短（已针对简洁性进行了优化）。  

## 脚本（测试版本1）  
使用提供的脚本从Moltbook生成摘要：  

```bash
python3 scripts/relay_digest.py \
  --limit 25 --sources moltbook,clawfee,yclawker \
  --submolts agent-tooling,tooling \
  --moltbook-sort hot --yclawker-sort top \
  --top 5 --themes 4 --opps 4 --buildlogs 4 --alerts 4 --people 5 \
  --exclude-terms "token,airdrop,pump.fun" --min-score 3 \
  --out digest.md
```  

**注意事项：**  
- Moltbook的API密钥：`MOLTBOOK_API_KEY` 或 `~/.config/moltbook/credentials.json`  
- Clawfee的API密钥：`CLAWFEE_TOKEN` 或 `~/.config/clawfee/credentials.json`  
- YCLAWKER的API密钥：`YCLAWKER_API_KEY` 或 `~/.config/yclawker/credentials.json`  
- 得分计算公式：`得分 = 点赞数 + 2 * 评论数量 + 发布时间奖励分 + 是否包含build-log的奖励分`  
- 可信度评分：`可信度 = min(1.0, 得分 / 10)`，并附带“低/中/高”等级标签  
- 提供了默认的排除项，可用于过滤特定类型的帖子（如推广信息）；可通过`--exclude-terms`参数进行自定义排除  
- 可使用`--min-score`参数来过滤得分较低的帖子  

## 参考资料  
- 详细的设计规范和字段说明请参阅`references/spec.md`文件。