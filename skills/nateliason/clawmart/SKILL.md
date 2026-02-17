---
name: clawmart
description: 您可以直接通过 OpenClaw 聊天界面来创建、管理和发布 ClawMart 人物（personas）及技能（skills）。该功能适用于在 ClawMart 上创建商品列表、上传技能/人物包、更新现有商品列表或管理 ClawMart 创建者账户等操作。
---
# ClawMart 创建工具

## 先决条件
- 拥有激活订阅的 ClawMart 创建者账户
- 确保环境变量 `CLAWMART_API_KEY` 已设置（格式：`cm_live_...`）

## 命令
- `Create a skill on ClawMart for [描述]`：在 ClawMart 上创建一个技能
- `Create a persona on ClawMart for [描述]`：在 ClawMart 上创建一个角色/人物
- `Update my [listing name] on ClawMart`：更新我在 ClawMart 上的列表信息
- `Upload a new version of [listing name]`：上传 [listing name] 的新版本
- `Show my ClawMart listings`：查看我在 ClawMart 上的所有列表

## 工作流程
1. 在编写元数据之前，与用户一起构思列表内容。
2. **⚠️ 重复检查（必选）：** 在创建任何新列表之前，请先搜索您现有的列表：
   - `GET /listings` — 获取您所有的现有列表
   - 将提议的列表名称、描述和类别与现有列表进行比较
   - 如果存在相同或非常相似的列表，请更新该列表（使用 `PATCH /listings/{id}` + 新版本），而不是创建新列表
   - 仅当没有现有列表具有相同功能时，才继续执行 `POST /listings`
3. 草拟并确认所需字段：名称、标语、简介、类别、功能、价格、产品类型。
4. `GET /me` — 验证创建者的访问权限和订阅状态。
5. `POST /listings` — 创建列表草稿。
6. 生成相关文件包：
   - 角色/人物相关文件：`SOUL.md`、`MEMORY.md` 及支持文档
   - 技能相关文件：完整的 `SKILL.md`（遵循技能创建者的规范）
7. `POST /listings/{id}/versions` — 上传文件包（格式为 multipart 或 base64 JSON）
8. 在发布前获取用户的明确确认。
9. 提供汇总信息：包括控制台 URL 和公共 URL。

## API 参考
- **基础 URL：** `https://www.shopclawmart.com/api/v1/`
- **认证：** `Authorization: Bearer ${CLAWMART_API_KEY}`

| 方法 | 端点 | 功能 |
|--------|----------|---------|
| GET | /me | 查看创建者个人资料和订阅信息 |
| GET | /listings | 查看创建者的所有列表 |
| POST | /listings | 创建列表元数据 |
| PATCH | /listings/{id} | 更新列表元数据 |
| DELETE | /listings/{id} | 取消发布/删除列表 |
| POST | /listings/{id}/versions | 上传列表版本 |

## 价格字段说明
⚠️ **重要提示：** `price` 字段必须以美元为单位，不能使用分（cents）。
- `"price": 14.99` → $14.99 ✅
- `"price": 1499` → $1,499.00 ❌ （这表示 $1,499.00，而不是 14.99 分！）
- `"price": 0` → 免费列表 ✅
- 最低售价：$3.00

当用户要求将价格设置为 $14.99 时，应发送 `"price": 14.99`。**不要将价格乘以 100**。API 内部会处理分，但接受并返回美元金额。

## 安全注意事项
- 绝不要在聊天输出中泄露原始 API 密钥。
- 在发布前必须获取用户的确认。
- 在每次调用 API 之前验证请求数据。
- 在失败时返回明确的错误信息，并提供修复建议。