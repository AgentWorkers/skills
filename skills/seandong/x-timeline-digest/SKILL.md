---
name: x-timeline-digest
description: 使用 bird 工具，从您自己的 Twitter 时间线以及您关注的人的时间线中构建一个去重后的摘要（digest）。该摘要将作为数据包（payload）用于后续的上游传输。
homepage: https://github.com/seandong
metadata: {"openclaw":{"emoji":"🐦","requires":{"bins":["bird"]}}}
---
# x-timeline-digest  
## 概述  
该技能使用 `bird` 工具读取 X/Twitter 的时间线数据，并生成一份高质量的信息摘要。  
**数据来源：**  
- “For You” 时间线  
- 被关注者的时间线  

**功能：**  
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
所有配置信息均从 `skills.entries["x-timeline-digest"].config` 文件中读取：  

### 配置字段  
| 名称          | 类型        | 默认值       | 描述                                      |  
|-----------------|------------|------------|-----------------------------------------|  
| intervalHours    | number      | 6          | 时间间隔（以小时为单位）                          |  
| fetchLimitForYou    | number      | 100         | 从 “For You” 时间线获取的推文数量                |  
| fetchLimitFollowing | number      | 60         | 从被关注者时间线获取的推文数量                |  
| maxItemsPerDigest | number      | 25         | 每份摘要中包含的推文数量上限                    |  
| similarityThreshold | number      | 0.9         | 推文内容相似度的阈值                          |  
| statePath       | string      | ~/.openclaw/state/x-timeline-digest.json | 状态文件路径                          |  

---  
## 依赖项  
- 确保已安装 `bird` 并将其添加到系统路径（PATH）中  
- `bird` 必须已登录（使用 Cookie 进行身份验证）  
- 该技能仅支持只读操作（无法修改数据）  

## 使用方法  

### 1. 基本用法（原始 JSON 格式）  
运行该技能以获取去重的 JSON 数据：  
```bash
node skills/x-timeline-digest/digest.js
```  

### 2. 智能摘要生成（推荐用法）  
若需生成包含分类、摘要和去噪内容的智能摘要，请执行以下步骤：  
1. 运行脚本：`node skills/x-timeline-digest/digest.js > digest.json`  
2. 查看提示模板：`read skills/x-timeline-digest/PROMPT.md`  
3. 将 `digest.json` 的内容（其中 `{{JSON_DATA}}` 为待填充的部分）发送给你的 LLM（大型语言模型）。  

*注：脚本会在输出 JSON 之前自动过滤掉无关内容（如 “gm”、广告和短链接）。*  

## 使用 `bird` 的命令  
- 查看 “For You” 时间线：`bird home -n <N> --json`  
- 查看被关注者的时间线：`bird home --following -n <N> --json`  

---  
## 状态管理  
程序会将运行状态保存到 `statePath` 指定的文件中：  
```json
{
  "lastRunAt": "2026-02-01T00:00:00+08:00",
  "sentTweetIds": {
    "123456789": "2026-02-01T00:00:00+08:00"
  }
}
```  
**规则说明：**  
- 已经包含在 `sentTweetIds` 中的推文不得再次被处理。  
- 成功运行后：  
  - 更新 `lastRunAt` 的时间戳；  
  - 将新生成的推文 ID 添加到 `sentTweetIds` 中；  
  - 保留推文 ID 至少 30 天。  

## 处理流程：  
1. 从 “For You” 和被关注者的时间线中获取推文；  
2. 根据 `lastRunAt` 进行增量式过滤；  
3. 通过推文 ID 进行严格去重；  
4. 根据文本内容的相似度合并重复推文；  
5. 对推文进行排序并限制摘要长度（最多 `maxItemsPerDigest` 条）；  
6. 将推文内容生成中文摘要。  

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