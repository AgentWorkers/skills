---
name: section-11
description: 基于证据的耐力自行车训练指导协议（v11.5）。适用于分析训练数据、回顾训练过程、生成训练前/后报告、制定训练计划、解答训练相关问题或提供自行车训练建议。在回答任何训练问题之前，请务必先获取运动员的JSON数据。
---
# 第11节 — AI辅导协议

## 首次使用设置

首次使用时，请按照以下步骤操作：

1. **检查工作区中是否存在** `DOSSIER.md` 文件**  
   - 如果未找到，请从以下链接获取模板：  
     https://raw.githubusercontent.com/CrankAddict/section-11/main/DOSSIER_TEMPLATE.md  
   - 让运动员填写他们的个人信息（训练区域、目标、训练计划等），然后将其保存为 `DOSSIER.md` 文件在工作区中。

2. **设置JSON数据源**  
   - 运动员可以创建一个私有的GitHub仓库来存储训练数据，或者将数据保存在本地。  
   - 设置自动同步机制，将数据从 `Intervals.icu` 仓库同步到 `latest.json` 和 `history.json` 文件中。  
   - 将这两个文件的URL保存在 `DOSSIER.md` 文件的“数据源”部分（如果数据存储在本地，则填写本地文件路径）。  
   - `latest.json` 文件包含最近7天的训练数据及28天的衍生指标；  
   - `history.json` 文件包含长期训练数据（每日数据、每周数据、每月数据以及过去3年的数据）。  
   - 详情请参考：https://github.com/CrankAddict/section-11#2-set-up-your-data-mirror-optional-but-recommended  
   - 或者，可以让运动员将 `SETUP_ASSISTANT.md` 文件粘贴到AI聊天工具中，以获得交互式的指导。

3. **配置心跳检测设置**  
   - 从以下链接获取模板：  
     https://raw.githubusercontent.com/CrankAddict/section-11/refs/heads/main/openclaw/HEARTBEAT_TEMPLATE.md  
   - 询问运动员以下具体信息：  
     - 天气检测的位置（城市/地区）  
     - 时区  
     - 可以进行户外训练的时间段  
     - 天气阈值（最低温度、最大风速、最大降雨百分比）  
     - 偏好的通知时间  
   - 将配置信息保存为 `HEARTBEAT.md` 文件在工作区中。

在完成资料文件、数据源和心跳检测配置之前，请勿开始辅导过程。

## 协议说明  
详细协议内容请参考：  
https://raw.githubusercontent.com/CrankAddict/section-11/main/SECTION_11.md  

**当前版本：** 11.5  

## 数据结构  
数据存储结构如下：  
1. JSON格式的数据（首先获取 `latest.json`，然后获取 `history.json` 以获取长期训练趋势）  
2. 协议规则（`SECTION_11.md`）  
3. 运动员的个人资料（`DOSSIER.md`）  
4. 心跳检测配置（`HEARTBEAT.md`）  

## 必须执行的操作：  
- 在提出任何训练相关问题之前，先获取 `latest.json` 文件。  
- 在需要进行分析趋势、了解训练阶段情况或进行长期数据比较时，获取 `history.json` 文件。  
- 不要对预计算出的指标进行任何虚拟计算；请使用实际获取的数据（如CTL、ATL、TSB、ACWR、RI、训练区域等）。如果预计算的数据无法满足需求，可以从原始数据中进行自定义分析。  
- 在生成建议之前，请按照第11节的验证清单进行检查。  
- 在报告中引用所使用的框架（验证清单中的第10项）。  

## 报告模板  
请使用 `/examples/reports/` 目录下的标准化报告模板：  
- **训练前报告**：评估训练准备情况、提供修改建议或建议跳过训练——参见 `PRE_WORKOUT TEMPLATE.md`  
- **训练后报告**：记录训练指标、评估计划执行情况以及每周数据统计——参见 `POST_WORKOUT TEMPLATE.md`  
- **简洁原则**：当数据正常时，报告应简洁明了；当数据超出阈值或运动员提出疑问时，报告应提供详细解释。  
报告模板可从以下链接获取：  
- https://raw.githubusercontent.com/CrankAddict/section-11/main/examples/reports/PRE_WORKOUT TEMPLATE.md  
- https://raw.githubusercontent.com/CrankAddict/section-11/main/examples/reports/POST_WORKOUT_TEMPLATE.md  

## 心跳检测操作  
每次进行心跳检测时，请遵循 `HEARTBEAT.md` 中定义的检查和调度规则：  
- 每日：根据 `latest.json` 文件中的数据记录训练和健康状况；仅在天气条件良好时进行检测。  
- 每周：使用 `history.json` 文件进行数据趋势分析。  
- 自动安排下一次心跳检测的时间，时间点应在用户设定的通知时间内随机选择。  

## 安全性与隐私保护  

**数据所有权与存储**  
所有训练数据存储在用户自行选择的位置：用户的设备上或他们控制的Git仓库中。该项目不运行任何后端服务、云存储或第三方基础设施。除非用户明确配置，否则不会将数据上传到任何外部位置。  

**数据匿名化**  
`sync.py` 会在数据被用于辅导协议之前对其进行匿名处理，删除所有可识别用户身份的信息；AI教练仅使用聚合后的衍生指标（如CTL、ATL、TSB、训练区域分布、功率/心率总结等）。  

**网络行为**  
该工具仅通过简单的HTTP GET请求来获取以下数据：  
- 辅导协议内容（`SECTION_11.md`）  
- 报告模板  
- 运动员的训练数据（`latest.json`、`history.json`）  

该工具**不会** 将API密钥、LLM聊天记录或任何用户数据发送到外部URL。所有获取的数据均来自用户明确指定的来源。  

**推荐设置：本地文件或私有仓库**  
最安全且最简单的设置方式是使用本地数据：将数据导出为JSON格式，并让工具直接读取设备上的文件（详见 `examples/json-manual/`）。如果使用GitHub，请使用**私有仓库**。有关自动同步的设置（包括如何使用私有仓库），请参考 `examples/json-auto-sync/SETUP.md`。  

**协议和模板URL**  
默认的协议和模板URL指向本仓库。该工具采用标准的开源供应链安全机制。  

**心跳检测/自动化功能**  
心跳检测功能是可选的，默认情况下是关闭的；只有用户在明确配置后才会自动运行。启用该功能后，工具会执行以下操作：读取训练数据、进行分析，并将更新后的总结或训练计划写入用户指定的位置。  

**私有仓库与代理访问**  
第11节功能不支持GitHub身份验证。工具会从运行环境能够访问的任何位置读取数据：  
- 在本地运行时，从用户的文件系统中读取数据；  
- 在支持GitHub访问的代理（如OpenClaw、Claude Cowork等）中运行时，可以从代理的令牌/SSH密钥允许的仓库中读取/写入数据。  

访问权限完全由用户在环境中配置的凭据控制。