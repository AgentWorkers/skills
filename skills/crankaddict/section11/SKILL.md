---
name: section-11
description: 基于证据的耐力自行车训练指导协议（v11.5）。适用于分析训练数据、回顾训练过程、生成训练前/后报告、制定训练计划、解答训练相关问题或提供自行车训练建议。在回答任何训练问题之前，请务必先获取运动员的JSON数据。
---
# 第11节 — AI辅导协议

## 首次使用设置

首次使用时，请按照以下步骤操作：

1. **检查工作区中是否存在DOSSIER.md文件**：
   - 如果未找到，请从以下链接获取模板：https://raw.githubusercontent.com/CrankAddict/section-11/main/DOSSIER_TEMPLATE.md
   - 让运动员填写他们的个人信息（训练区域、目标、训练计划等）
   - 将填写好的文件保存为DOSSIER.md，并放在工作区中。

2. **设置JSON数据源**：
   - 运动员可以创建一个私有的GitHub仓库来存储训练数据，或者将数据保存在本地文件中。
   - 设置自动同步机制，将数据从`Intervals.icu`同步到`latest.json`和`history.json`文件中。
   - 将这两个文件的URL保存在DOSSIER.md的“Data Source”部分（如果数据保存在本地，则填写本地文件路径）：
     - `latest.json`：包含最近7天的训练数据及28天的衍生指标
     - `history.json`：包含长期训练数据（每日数据、每周数据、每月数据及过去3年的数据）
   - 详情请参考：https://github.com/CrankAddict/section-11#2-set-up-your-data-mirror-optional-but-recommended
   - 或者，可以让运动员将`SETUP_ASSISTANT.md`粘贴到AI聊天界面中，以获得交互式的设置指导。

3. **配置心跳检测设置**：
   - 从以下链接获取模板：https://raw.githubusercontent.com/CrankAddict/section-11/refs/heads/main/openclaw/HEARTBEAT_TEMPLATE.md
   - 询问运动员以下具体信息：
     - 天气检测的位置（城市/地区）
     - 时区
     - 可以进行户外训练的时间段
     - 天气阈值（最低温度、最大风速、最大降雨百分比）
     - 偏好的通知时间
   - 将配置文件保存为HEARTBEAT.md，并放在工作区中。

在完成资料文件、数据源和心跳检测配置之前，切勿开始辅导流程。

## 协议说明

详细协议内容请参考：https://raw.githubusercontent.com/CrankAddict/section-11/main/SECTION_11.md

**当前版本：** 11.5

## 外部资源

本技能所引用的所有外部文件（`sync.py`、`SECTION_11.md`、模板文件、设置指南等）都存储在开源仓库[CrankAddict/section-11](https://github.com/CrankAddict/section-11)中，您可以前往那里查看这些文件。

## 数据结构

数据存储结构如下：
1. JSON数据（首先获取`latest.json`文件，然后根据需要获取`history.json`文件以获取长期训练趋势）
2. 协议规则（`SECTION_11.md`文件）
3. 运动员的个人资料文件（DOSSIER.md）
4. 心跳检测配置文件（HEARTBEAT.md）

## 必需的操作：
- 在提出任何训练相关问题之前，必须先获取`latest.json`文件。
- 当需要进行趋势分析、阶段评估或长期数据比较时，需要获取`history.json`文件。
- 不要对预计算出的指标进行任何虚拟计算——请使用实际获取到的数据（如CTL、ATL、TSB、ACWR、RI、训练区域等）。如果预计算的数据无法满足需求，可以基于原始数据进行自定义分析。
- 在生成建议之前，请按照第11节的验证清单进行检查。
- 在报告中引用所使用的框架（请参考清单中的第10项）。

## 报告模板

请使用`/examples/reports/`目录下的标准化报告模板：
- **训练前报告**：评估运动员的准备情况，提供“进行训练”、“修改训练计划”或“跳过训练”的建议——请参考`PRE_WORKOUT_TEMPLATE.md`
- **训练后报告**：记录训练期间的各项指标、计划执行情况以及每周的总体数据——请参考`POST_WORKOUT_TEMPLATE.md`
- **简洁性原则**：当数据正常时，报告应简洁明了；当数据超出阈值或运动员提出疑问时，报告应提供详细解释。

报告模板的获取地址：
- https://raw.githubusercontent.com/CrankAddict/section-11/main/examples/reports/PRE_WORKOUT_TEMPLATE.md
- https://raw.githubusercontent.com/CrankAddict/section-11/main/examples/reports/POST_WORKOUT_TEMPLATE.md

## 心跳检测机制

在每次进行心跳检测时，请遵循`HEARTBEAT.md`中定义的检查和调度规则：
- 每日：根据`latest.json`文件记录训练和健康状况，仅在天气条件适宜时进行天气检查
- 每周：使用`history.json`文件进行数据趋势分析
- 自动安排下一次心跳检测的时间，时间点在用户设定的通知时间内随机选择

## 安全性与隐私

**数据所有权与存储**

所有训练数据均由用户自行决定存储位置：可以存储在用户的设备上，或者存储在他们控制的Git仓库中。该项目不使用任何后端服务、云存储或第三方基础设施。除非用户明确配置，否则不会将数据上传到任何外部位置。

本技能会从用户配置的JSON数据源（`DOSSIER.md`和`HEARTBEAT.md`）中读取数据，并仅在工作区中更新这些文件。

**数据匿名化**

`sync.py`脚本（存储在源代码仓库中）负责对原始训练数据进行匿名化处理。本技能本身不执行匿名化操作。AI辅导系统仅使用经过汇总和计算后的指标（如CTL、ATL、TSB、训练区域分布、功率/心率总结等）。

**网络行为**

本技能通过简单的HTTP GET请求获取以下数据：
- 辅导协议内容（`SECTION_11.md`）
- 报告模板（来自同一仓库）
- 运动员的训练数据（`latest.json`、`history.json`）

本技能**不会**将API密钥、LLM聊天记录或任何用户数据发送到外部URL。所有获取的数据都来自用户明确指定的来源。

**推荐设置：本地文件或私有仓库**

最安全且最简单的设置方式是使用本地数据：将数据导出为JSON格式，然后让技能直接读取设备上的文件（请参考`examples/json-manual/`）。如果使用GitHub，请使用私有仓库。有关自动同步设置的详细信息，请参考`examples/json-auto-sync/SETUP.md`（包括如何使用私有仓库）。

**协议和模板文件的URL**

默认的协议和模板文件URL指向本开源仓库。该系统的安全机制遵循标准的开源供应链安全规范。

**心跳检测/自动化**

心跳检测功能是可选的，默认情况下是关闭的。只有当用户明确启用后，系统才会自动执行相关操作，主要包括读取训练数据、进行分析，并将更新后的总结或训练计划写入用户指定的位置。

**私有仓库与代理访问**

第11节功能不支持GitHub身份验证。系统会从运行环境能够访问的任何位置读取数据：
- 在本地运行时：从用户的文件系统中读取数据
- 在支持GitHub访问的代理（如OpenClaw、Claude Cowork等）中运行时：可以读取/写入代理的权限范围内的仓库

所有访问权限完全由用户在环境中配置的凭据控制。