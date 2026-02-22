---
name: bayclub_manager
description: "在 Bay Club 中预订和管理网球/壁球场地。"
user-invocable: true
metadata: { 
  "openclaw": { 
    "emoji": "🎾",
    "requires": { "bins": ["node"] },
    "category": "Utilities"
  } 
}
---
# 海湾俱乐部管理员（Bay Club Manager）
该技能利用 Stagehand 和 TypeScript 来自动化浏览器端的预订流程。

## 操作说明
当用户请求预订或查询场地时，请按照以下步骤操作：
1. 使用 `shell` 工具运行实现脚本。
2. 需要执行的命令是：`NODE_ENV=development STAGEHAND_ENV=LOCAL HEADLESS=true npx ts-node --transpile-only {baseDir}/bayclub_skills.ts`
3. 将用户输入的参数（日期、时间、俱乐部名称）以字符串形式传递给脚本。

## 相关文件：
- 逻辑实现文件：`{baseDir}/bayclub_skills.ts`
- 浏览器端引擎文件：`{baseDir}/BayClubBot.ts`