---
name: basecred
description: **通过 BaseCred SDK 获取链上声誉信息（适用于 Ethos、Talent Protocol、Farcaster/Neynar）**  
当用户需要查询任意 0x 地址的钱包声誉、开发者评分、创作者评分、Ethos 信誉度或 Farcaster 账户质量时，可以使用此功能。该 SDK 支持从多个来源统一获取用户信息，并能够展示信息的层级结构及更新时间。
---

# BaseCred — 在链上查询用户声誉

## 先决条件

1. **已在工作区安装相关包**：`npm i basecred-sdk`
2. **API密钥** 已配置在工作区的 `.env` 文件中：
   ```
   TALENT_PROTOCOL_API_KEY=<key>
   NEYNAR_API_KEY=<key>          # optional — enables Farcaster scoring
   ```
   Ethos Network 不需要 API 密钥。

## 快速工作流程

1. 从工作区运行查询脚本：
   ```bash
   node /path/to/skills/basecred/scripts/query.mjs <0x-address>
   ```
   该脚本会自动查找 `node_modules/basecred-sdk` 和 `.env` 文件（从当前工作目录开始搜索）。请确保当前工作目录指向正确的工作区。

2. 解析 JSON 输出结果，并以用户可理解的方式展示结果。可以使用 `references/output-schema.md` 中的等级表将原始分数转换为人类可读的等级。

## 展示结果

清晰地总结以下三个方面的信息：

- **Ethos**：分数、信誉等级、用户评价 sentiment（情感倾向）以及获得的担保数量。如果 `hasNegativeReviews` 为 `true`，则标明存在负面评价。
- **Talent Protocol**：构建者的分数/等级以及创作者的分数/等级。请注意其验证状态。
- **Farcaster**：质量分数（0–1）以及是否达到最低标准。
- **活跃度**：分为“最近活跃”、“已过时”或“处于休眠状态”。如果数据已过时或处于休眠状态，请予以说明。

**重点关注的关键指标**：
- 在 Ethos 平台上，如果获得 0 个担保，则说明该用户信誉极佳；而对于处于休眠状态的 Talent 用户，则需要重新激活其账户以提升信誉。
- 对于 Farcaster 用户，需要关注其质量分数以及是否达到最低标准。

## 参考资料

- **输出格式及等级表**：`references/output-schema.md` — 当需要将分数转换为等级或理解响应结构时，请参考此文件。