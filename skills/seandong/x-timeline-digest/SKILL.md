---
name: x-timeline-digest
version: 1.0.2
description: 使用 bird 工具从您的个人时间线以及您关注的用户的时间线中构建去重后的摘要数据。生成的摘要数据将用于后续的上游传输。
homepage: https://github.com/seandong
metadata: {"openclaw":{"emoji":"🐦","requires":{"bins":["bird"]}}}
---# x-timeline-digest  
## 概述  
该技能使用 `bird` 工具读取 X/Twitter 时间线，并生成一份高质量的内容摘要。  
**数据来源**：  
- **“For You” 时间线**  
- **关注者时间线**  

**功能**：  
1. 获取最新的推文  
2. 采用增量式过滤方式（避免重复处理）  
3. 去重（基于推文 ID 和文本内容的相似度）  
4. 对推文进行排序和筛选  
5. 生成中文摘要  
6. 输出结构化的数据（格式化后的 JSON 数据）  

> 数据的传递方式（通过 Telegram、电子邮件等）不在本技能的范围内处理；  
> 具体的通知方式由上游的 OpenClaw 工作流程决定。  

---  
## 配置  
所有配置信息均从 `skills.entries["x-timeline-digest"].config` 文件中读取。  

### 配置字段  
| 名称          | 类型        | 默认值    | 描述                                      |  
|---------------|------------|---------|-----------------------------------------|  
| intervalHours    | number      | 6        | 时间间隔（以小时为单位）                          |  
| fetchLimitForYou   | number      | 100       | 从 “For You” 时间线获取的推文数量                |  
| fetchLimitFollowing | number      | 60       | 从关注者时间线获取的推文数量                |  
| maxItemsPerDigest | number      | 25       | 每份摘要中包含的推文数量                        |  
| similarityThreshold | number      | 0.9       | 推文内容相似度的阈值                          |  
| statePath       | string      | ~/.openclaw/state/x-timeline-digest.json | 状态文件路径                          |  

---  
## 依赖项  
- 必须安装 `bird` 并确保它已添加到系统的 `PATH` 环境变量中；  
- `bird` 必须已通过 cookie 进行身份验证；  
- 该技能仅支持只读操作（即无法修改原始数据）。  

## 使用方法  

### 1. 基本用法（原始 JSON 格式）  
运行该脚本以获取去重后的 JSON 数据：  
```bash
node skills/x-timeline-digest/digest.js
```  

### 2. 高级用法（推荐）  
若需生成分类、摘要化且经过内容过滤的摘要：  
1. 运行脚本：`node skills/x-timeline-digest/digest.js > digest.json`  
2. 查看提示模板：`read skills/x-timeline-digest/PROMPT.md`  
3. 将 `digest.json` 的内容通过 LLM（大型语言模型）进行处理（将 `{{JSON_DATA}}` 替换为实际数据）。  

*注：脚本在输出 JSON 数据前会自动过滤掉广告、无用的内容。*  

## 使用 `bird` 的命令  
- 查看 “For You” 时间线：`bird home -n <N> --json`  
- 查看关注者时间线：`bird home --following -n <N> --json`  

---  
## 状态管理  
系统会将处理结果保存到 `statePath` 指定的文件中。  
**状态文件结构示例**：  
```json  
{
  "lastRunAt": "2026-02-01T00:00:00+08:00",  
  "sentTweetIds": {
    "123456789": "2026-02-01T00:00:00+08:00"
  }  
}  
```  
**规则说明**：  
- 已经被记录在 `sentTweetIds` 中的推文不得再次被处理；  
- 成功执行后：  
  - 更新 `lastRunAt` 的时间戳；  
  - 将新处理的推文 ID 添加到 `sentTweetIds` 中；  
  - 推文 ID 会被保留至少 30 天。  

## 处理流程：  
1. 从 “For You” 时间线和关注者时间线中获取推文；  
2. 根据 `lastRunAt` 的时间戳进行增量式过滤；  
3. 通过推文 ID 进行彻底去重；  
4. 根据文本内容的相似度合并重复的推文；  
5. 对推文进行排序，并限制每份摘要中的推文数量（`maxItemsPerDigest`）；  
6. **生成中文摘要**（使用 `PROMPT.md` 模板和 LLM 进行分类和内容处理）：  
  - 分类：🤖 AI 与技术、💰 加密与市场、💡 洞察、🗞️ 其他  
  - 语言：简体中文  
  - 格式：[作者](URL): 摘要  
  - 过滤内容：去除广告和低质量信息  

## 输出结果  
该技能返回一个 JSON 对象，包含以下内容：  
```json  
{
  "window": {
    "start": "2026-02-01T00:00:00+08:00",
    "end": "2026-02-01T06:00:00+08:00",
    "intervalHours": 6
  },
  "counts": {
    "forYouFetched": 100,
    "followingFetched": 60,
    "afterIncremental": 34,
    "afterDedup": 26,
    "final": 20
  },
  "digestText": "中文摘要内容",
  "items": [
    {
      "id": "123456",
      "author": "@handle",
      "createdAt": "2026-02-01T02:15:00+08:00",
      "text": "推文内容",
      "url": "https://x.com/handle/status/123456",
      "sources": ["following"]
    }
  ]
}  
```