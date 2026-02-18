---
name: garmin-tracker
description: 根据2026年2月1日的固定数据结构，从Garmin网站获取活动（activities）和训练计划（training plan）数据，并重新生成并维护garmin_tracking.json文件。
metadata: { "openclaw": { "requires": { "bins": ["node", "python3"] } } }
---
# Garmin Tracker

当用户请求同步、重建或验证位于 `garmin_tracking.json`（工作区根目录下）中的Garmin训练数据时，请使用此技能。

## 运行时前提条件

- 在执行此技能的运行环境中，必须具备 `playwright-core`。  
- 如果出现 `MODULE_NOT_FOUND: playwright-core` 的错误，请在当前工作区中安装它：

```bash
npm install playwright-core
```

## 使用范围

- 该技能的应用范围较为有限：主要用于Garmin跑步者/用户的训练数据管理（包括训练历史记录汇总和即将进行的训练计划）。  
- 以下内容不在其使用范围内：  
  - 深度遥测数据抓取（如GPS路线信息、分段数据、步频/功率/海拔等原始数据）；  
  - 营养数据工作流管理或外部工作流的集成。  

## 硬性规则

- 训练数据的开始日期固定为 `2026-02-01`。  
- 必须保留以下顶级字段：`lastUpdate`、`planName`、`currentWeek`、`summary`、`history`、`upcoming`、`recurring_activities`。  
- 字段 `summary.to` 的值必须始终为当前日期（格式为 `YYYY-MM-DD`）。  
- 训练数据的格式必须符合以下规范：  
  - `type`  
  - `distanceKm`  
  - `durationSec`  
  - `avgPaceSecPerKm`  
  - `avgHrBpm`  
  - `calories`  
  - `sourceId`  

## 浏览器操作流程（Garmin）

1. 打开Garmin活动列表页面，收集自 `2026-02-01` 以来的所有训练活动。  
2. 打开Garmin训练计划页面（路径为 `/app/training-plan`），并更新 `currentWeek` 和 `upcoming` 的数据。  
3. 数据提取过程中仅保留活动列表/表格相关字段，禁止抓取GPS数据、分段数据或步频/功率等详细信息。  
4. 如果浏览器操作失败，请先尝试以下内置恢复步骤（切换标签页 -> 重新聚焦页面 -> 重新获取数据），然后再采取进一步措施。  

## 会话/身份验证机制

- 用户需在OpenClaw使用的浏览器配置中登录Garmin账户。  
- 如果Garmin页面显示用户已登出，需让用户重新登录后再执行操作。  
- 请勿将用户凭据存储在技能相关文件中。  

## 身份验证顺序（优先级）

请按照以下顺序进行身份验证：  
1. 使用浏览器已保存的登录会话（优先选择）；  
2. 在受控浏览器/配置中手动登录；  
3. 仅当浏览器登录失败或用户明确拒绝登录时，才使用备用凭据进行登录。  

`sync_training_plan.mjs` 支持以下身份验证选项：  
- `--auth-source auto`（默认值）：使用浏览器已保存的登录会话；如果用户已登出且凭据可用，则尝试使用凭据登录。  
- `--auth-source browser`：禁止使用凭据，强制用户手动登录。  
- `--auth-source credentials`：要求用户提供凭据并直接进行登录。  

## 用户身份验证指导

如果用户未登录，请按照以下步骤进行引导：  
1. 在受控浏览器配置中手动登录：  
  `https://connect.garmin.com/signin/` → `https://connect.garmin.com/app/training-plan` → 重新执行同步操作。  
2. 如果浏览器登录失败，请求用户提供凭据并使用凭据登录。  

**注意事项：**  
- 身份验证策略（优先使用浏览器会话还是凭据）可由操作员根据具体环境进行配置。  
- 在使用容器化浏览器环境的场景中，可通过配置的 `noVNC/VNC` 端点完成登录。  
- 在主机浏览器模式下，用户需直接在OpenClaw配置的主机浏览器中登录。  

## 备用凭据登录方式

如果浏览器登录失败，可以使用备用凭据进行登录：  
1. 仅请求用户提供必要的登录信息（用户名/电子邮件及2FA验证码）。  
2. 仅将凭据用于登录操作，登录完成后立即将其从内存或上下文中清除。  
3. 绝不要将凭据保存到 `MEMORY.md`、`garmin_tracking.json`、日志文件或技能相关文件中。  
4. 登录成功后，继续按照常规流程执行操作。  

## 数据重建流程  

1. 读取当前的 `garmin_tracking.json` 文件。  
2. 保留 `planName` 和 `recurring_activities` 字段。  
3. 从Garmin活动数据中重建 `history` 部分（仅包括自 `2026-02-01` 以来的数据）。  
4. 根据重建后的 `history` 数据重新计算 `summary`。  
5. 将 `summary.to` 设置为当前日期，将 `lastUpdate` 设置为当前时间戳。  

## 本地验证/数据一致性检查脚本  

使用随技能提供的脚本进行数据格式规范化和汇总信息的重新计算：  

```bash
python3 {baseDir}/scripts/reconcile_tracking.py --file garmin_tracking.json --write
```  
（用于检查数据格式是否正确）  

## 训练计划同步脚本  

使用随技能提供的脚本从Garmin训练计划中更新 `currentWeek` 和 `upcoming` 数据：  

```bash
node {baseDir}/scripts/sync_training_plan.mjs --file garmin_tracking.json --write
```  
（用于从Garmin训练计划中获取最新数据）  

**备用凭据登录示例（最后手段）：**  
```bash
node {baseDir}/scripts/sync_training_plan.mjs \
  --auth-source credentials \
  --garmin-email "user@example.com" \
  --garmin-password "***" \
  --file garmin_tracking.json \
  --write
```  
（用于在无法使用浏览器登录时提供凭据登录方式）  

## CDP数据源配置优先级：  

- `--cdp-url`：用户可指定具体的CDP数据源地址。  
- 通过 `--config` 参数从OpenClaw配置文件中读取默认的CDP数据源地址（格式为 `browser.defaultProfile` → `browser.profiles.<profile>.cdpUrl`）。  
- 在无法使用指定数据源时，使用脚本默认的CDP端点（`http://127.0.0.1:<port>`）。  

**配置示例：**  
```bash
node {baseDir}/scripts/sync_training_plan.mjs --config data/config/openclaw.json --url "https://connect.garmin.com/app/training-plan" --file garmin_tracking.json --write
```  
（用于演示如何配置CDP数据源）  

## 最小化解析器测试  

运行相关的解析器测试用例：  
```bash
node --test {baseDir}/scripts/__tests__/training_plan_parser.test.mjs
```  
（用于确保数据解析的正确性）  

## 最终检查：  

- 确保文件为有效的JSON格式。  
- 确保文件中不存在 `nutritionLog` 字段。  
- 确保 `history` 数组中的每个活动记录格式正确。  
- 确保 `summary.to` 的值与当前日期一致。