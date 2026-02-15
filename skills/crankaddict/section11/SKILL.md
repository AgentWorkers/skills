---
name: section-11
description: 基于证据的耐力自行车训练指导协议（v11.3）。适用于分析训练数据、回顾训练过程、生成训练前/后报告、制定训练计划、解答训练相关问题或提供自行车训练建议。在回答任何训练问题之前，请务必先获取运动员的JSON数据。
---

# 第11节 — AI教练协议

## 首次使用设置

首次使用时，请按照以下步骤操作：

1. **检查工作区中是否存在** `DOSSIER.md` 文件**  
   - 如果未找到，请从以下链接下载模板：  
     https://raw.githubusercontent.com/CrankAddict/section-11/main/DOSSIER_TEMPLATE.md  
   - 让运动员填写他们的个人信息（训练区域、目标、训练计划等），  
   - 然后将文件保存为 `DOSSIER.md` 并放入工作区。  

2. **设置JSON数据源**  
   - 运动员需要创建一个私有的GitHub仓库来存储训练数据。  
   - 设置自动同步功能，将 `Intervals.icu` 中的数据同步到 `latest.json` 文件中。  
   - 将 `latest.json` 的URL保存在 `DOSSIER.md` 文件的“数据源”部分。  
   - 详情请参考：  
     https://github.com/CrankAddict/section-11#2-set-up-your-data-mirror-optional-but-recommended  

3. **配置心跳监测设置**  
   - 从以下链接下载模板：  
     https://raw.githubusercontent.com/CrankAddict/section-11/refs/heads/main/openclaw/HEARTBEAT_TEMPLATE.md  
   - 询问运动员以下具体信息：  
     - 天气监测的位置（城市/地区）  
     - 时区  
     - 可进行的户外骑行时间  
     - 天气阈值（最低温度、最大风速、最大降雨百分比）  
     - 偏好的通知时间  
   - 将配置文件保存为 `HEARTBEAT.md` 并放入工作区。  

在完成资料文件、数据源和心跳监测配置的设置之前，切勿开始教练流程。  

## 协议内容  

请查阅以下文档以获取详细的使用指南：  
https://raw.githubusercontent.com/CrankAddict/section-11/main/SECTION_11.md  

**当前版本：** 11.3  

## 数据层次结构  
1. JSON数据（始终优先从运动员提供的URL获取）  
2. 协议规则（`SECTION_11.md`）  
3. 运动员的个人资料文件（`DOSSIER.md`）  
4. 心跳监测配置文件（`HEARTBEAT.md`）  

## 必须执行的操作：  
- 在提出任何训练建议之前，先获取最新的 `latest.json` 数据。  
- 严禁进行任何虚拟计算——仅使用实际获取到的数据。  
- 在生成训练建议之前，请确保遵循第11节中的验证流程。  
- 在报告中需引用所使用的框架（验证流程中的第10项）。  

## 报告模板  

请使用 `/examples/reports/` 目录下的标准化报告模板：  
- **训练前报告**：评估运动员的准备情况，提供“进行训练”、“修改训练计划”或“跳过训练”的建议——详见 `PRE_WORKOUT_TEMPLATE.md`  
- **训练后报告**：记录训练数据、计划执行情况以及每周的总体表现——详见 `POST_WORKOUT_TEMPLATE.md`  
- **简洁性原则**：当数据正常时，报告应简洁明了；当数据超出阈值或运动员提出疑问时，报告应提供详细解释。  

报告模板可从以下链接下载：  
- https://raw.githubusercontent.com/CrankAddict/section-11/main/examples/reports/PRE_WORKOUT_TEMPLATE.md  
- https://raw.githubusercontent.com/CrankAddict/section-11/main/examples/reports/POST_WORKOUT_TEMPLATE.md  

## 心跳监测操作  

在每次进行心跳监测时，请遵循 `HEARTBEAT.md` 中定义的检查和调度规则：  
- **每日检查**：记录训练情况、健康状况以及天气情况（仅当天气条件适宜时）。  
- **每周分析**：对训练数据进行背景分析。  
- 自动安排下一次心跳监测的时间，时间点应在指定的通知时间内随机选择。