---
name: section-11
description: 基于证据的耐力自行车训练指导协议（v11.10）。适用于分析训练数据、回顾训练过程、生成训练前/后报告、制定训练计划、解答训练相关问题或提供自行车训练建议。在回答任何训练问题之前，务必先获取运动员的JSON数据。
---
# 第11节 — AI教练协议

## 首次使用设置

首次使用时，请按照以下步骤操作：

1. **检查工作区中是否存在** `DOSSIER.md` 文件**：
   - 如果未找到，请从以下链接下载模板：https://raw.githubusercontent.com/CrankAddict/section-11/main/DOSSIER_TEMPLATE.md
   - 让运动员填写他们的个人信息（训练区域、目标、训练计划等）
   - 将填写好的文件保存为 `DOSSIER.md` 并放在工作区中。

2. **设置JSON数据源**：
   - 运动员可以创建一个私有的GitHub仓库来存储训练数据，或者将数据保存在本地文件中。
   - 设置自动同步机制，将 `Intervals.icu` 中的数据同步到 `latest.json` 和 `history.json` 文件中。
   - 将这两个文件的URL保存在 `DOSSIER.md` 的“数据源”部分（如果是本地数据，则直接保存文件路径）。
   - `latest.json` 文件包含最近的7天训练数据及28天的衍生指标。
   - `history.json` 文件包含长期数据（每日数据保留90天，每周数据保留180天，每月数据保留3年）。
   - 详情请参考：https://github.com/CrankAddict/section-11#2-set-up-your-data-mirror-optional-but-recommended
   - 或者，可以让运动员将 `SETUP-AssISTANT.md` 文件粘贴到AI聊天界面中，以获得交互式的指导。

3. **配置心跳检测设置**：
   - 从以下链接下载模板：https://raw.githubusercontent.com/CrankAddict/section-11/refs/heads/main/openclaw/HEARTBEAT_TEMPLATE.md
   - 询问运动员以下具体信息：
     - 天气检测的位置（城市/地区）
     - 时区
     - 可进行的户外骑行时间
     - 天气阈值（最低温度、最大风速、最大降雨百分比）
     - 偏好的通知时间
   - 将配置文件保存为 `HEARTBEAT.md` 并放在工作区中。

在完成资料文件、数据源和心跳检测配置之前，请勿开始教练流程。

## 协议说明

详细协议内容请参考：https://raw.githubusercontent.com/CrankAddict/section-11/main/SECTION_11.md

**当前版本：** 11.5

## 外部资源

本技能所引用的所有外部文件（`sync.py`、`SECTION_11.md`、模板文件、设置指南）都存储在开源仓库 [CrankAddict/section-11](https://github.com/CrankAddict/section-11) 中，可以前往那里查看。

## 数据结构

数据存储结构如下：
1. JSON数据（先获取 `latest.json`，再获取 `history.json` 以获取长期数据趋势）
2. 协议规则（`SECTION_11.md`）
3. 运动员的个人资料文件（`DOSSIER.md`）
4. 心跳检测配置文件（`HEARTBEAT.md`）

## 必须执行的操作：
- 在提出任何训练相关问题之前，先获取 `latest.json` 文件。
- 当需要进行分析趋势、了解训练阶段情况或进行长期数据比较时，获取 `history.json` 文件。
- 不要对预计算出的指标进行任何虚拟计算——请使用实际获取到的数值（如CTL、ATL、TSB、ACWR、RI、训练区域等）。如果预计算值无法满足需求，可以直接使用原始数据进行自定义分析。
- 在生成训练建议之前，请按照第11节的验证清单进行检查。
- 在生成建议时，请引用相关的框架（验证清单中的第10项）。

## 编写操作功能

如果数据仓库中包含 `push.py` 文件，该技能可以管理运动员的 `Intervals.icu` 日历和训练数据：
- **push**：将计划好的训练内容写入日历。
- **list**：显示指定日期范围内的训练计划。
- **move**：将训练计划重新安排到其他日期。
- **delete**：从日历中删除训练计划。
- **set-threshold**：更新特定运动的阈值（FTP、室内FTP、LTHR、最大心率、阈值配速）。请仅在验证过测试结果后进行更新，切勿根据估算值进行设置。
- **annotate**：为已完成的训练活动添加备注（默认为描述性文字；使用 `--chat` 选项可在消息面板中添加备注）或为计划中的训练活动添加备注（备注前缀为 `NOTE:`）。

所有写入操作默认处于预览模式——在没有 `--confirm` 选项的情况下，不会实际执行任何操作。执行方式可以通过GitHub Actions（使用运动员配置的仓库密钥）或本地CLI来完成。详细使用说明、训练语法和模板ID映射请参考 `examples/agentic/README.md`。

该技能仅适用于能够执行代码或触发GitHub Actions的平台（如OpenClaw、Claude Code、Cowork等）。Web聊天用户无法使用该技能。

## 报告模板

使用 `/examples/reports/` 目录下的标准化报告模板：
- **训练前报告**：评估准备情况、提供训练建议或建议是否需要调整——请参考 `PRE_WORKOUT_TEMPLATE.md`
- **训练后报告**：显示训练指标、计划执行情况、每周总结——请参考 `POST_WORKOUT_TEMPLATE.md`
- **报告简洁性原则**：当指标正常时，报告应简洁明了；当指标超出阈值或运动员提出疑问时，报告应提供详细解释。

报告模板下载地址：
- https://raw.githubusercontent.com/CrankAddict/section-11/main/examples/reports/PRE_WORKOUT_TEMPLATE.md
- https://raw.githubusercontent.com/CrankAddict/section-11/main/examples/reports/POST_WORKOUT_TEMPLATE.md

## 心跳检测操作

在每次心跳检测时，请按照 `HEARTBEAT.md` 中定义的规则进行检查和安排：
- 每日：根据 `latest.json` 文件中的数据记录训练和健康状况；仅在天气条件良好时进行天气检查。
- 每周：使用 `history.json` 文件进行数据趋势分析。
- 自动安排下一次心跳检测的时间，时间随机选择在用户设定的通知时间内。

## 安全性与隐私

**数据所有权与存储**
所有训练数据存储在用户指定的位置：用户的设备上或用户控制的Git仓库中。该项目不运行任何后端服务、云存储或第三方基础设施。除非用户明确配置，否则不会将数据上传到任何外部位置。

该技能从以下位置读取数据：用户配置的JSON数据源、工作区中的 `DOSSIER.md` 和 `HEARTBEAT.md` 文件。写入数据的位置也是工作区中的 `DOSSIER.md` 和 `HEARTBEAT.md` 文件（仅在首次使用时写入）。

**数据匿名化**
`sync.py`（存储在源代码仓库中）负责对原始训练数据进行匿名化处理。该技能本身不执行匿名化操作。AI教练仅使用汇总后的数据指标（如CTL、ATL、TSB、训练区域分布、功率/心率总结）。

**网络行为**
该技能通过简单的HTTP GET请求获取以下内容：
- 教练协议内容（`SECTION_11.md`）
- 报告模板（来自同一仓库）
- 运动员的训练数据（`latest.json`、`history.json`，来自用户配置的URL）

该技能**不会** 将API密钥、LLM聊天记录或任何用户数据发送到外部URL。所有获取的数据均来自用户明确指定的来源。

**推荐设置：本地文件或私有仓库**
最安全且最简单的设置方式是使用本地文件：将数据导出为JSON格式，并指定技能访问用户设备上的文件（详见 `examples/json-manual/`）。如果使用GitHub，请使用**私有仓库**。有关自动同步设置的详细信息（包括如何使用私有仓库），请参考 `examples/json-auto-sync/SETUP.md`。

**协议和模板URL**
默认的协议和模板URL指向该开源仓库。该系统的安全性遵循标准的开源供应链安全规范。

**心跳检测/自动化**
心跳检测功能是可选的，默认情况下是关闭的。只有用户在明确配置后，该功能才会自动运行。启用后，该技能会执行以下操作：读取训练数据、进行分析，并将更新后的总结或计划写入用户指定的位置。

**私有仓库与代理访问**
第11节功能不支持GitHub身份验证。它可以从运行环境能够访问的任何位置读取文件：
- 在本地运行时：从用户的文件系统中读取数据。
- 在支持GitHub访问的代理环境中运行时（如OpenClaw、Claude Cowork等）：可以读取/写入代理的权限范围内的仓库。

访问权限完全由用户在环境中配置的凭据控制。