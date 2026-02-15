---
name: gumroad-pro
description: "Gumroad提供了全面的商户管理功能，涵盖产品管理、销售统计、许可证管理、折扣设置、付款处理以及Webhook配置等各个方面。当Claude需要执行以下操作时，可以使用Gumroad：  
1. 管理数字或实体产品的库存；  
2. 监控交易流程并处理退款或发货请求；  
3. 验证或更换许可证密钥；  
4. 管理优惠码；  
5. 监控付款历史记录并配置Webhook通知。"
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"], "env": ["GUMROAD_ACCESS_TOKEN", "API_KEY"], "config": [] },
        "primaryEnv": "GUMROAD_ACCESS_TOKEN"
      }
  }
---

# Gumroad Pro

## 🛑 AI 协议
1. **优先使用交互式界面**：始终尝试使用基于按钮的交互式 GUI（由 `handler.js` 处理），以提供最佳的商家体验。
2. **仅作为备用方案使用 CLI**：仅在需要复杂数据检索或 GUI 中不可用的特定操作时，通过 CLI 使用 `scripts/gumroad-pro.js`。
3. **务必使用 `--json` 标志**：在使用 CLI 时，**必须** 使用 `--json` 标志，并检查响应中是否包含 `"success": true`。
4. **减少垃圾信息**：在所有菜单切换和状态更新时，使用 `action: 'edit'`；仅在初始菜单显示或上下文发生根本性变化时，使用 `action: 'send'`。
5. **处理错误**：阅读 JSON 响应中的 `"error"` 字段，以向用户通知错误情况。

## ❓ 导航与数据
- **主要交互方式**：使用 `handler.js` 中的自适应逻辑。有关交互模式，请参阅 [handler-guide.md]（位于 {baseDir}/references/handler-guide.md）；有关渲染协议，请参阅 [ui-rendering.md]（位于 {baseDir}/references/ui-rendering.md）；有关版本历史，请参阅 [changelog.md]（位于 {baseDir}/references/changelog.md）。根据需要，使用按钮回调数据（例如 `gp:products`）或数字（1、2、3）进行响应。
- **次要交互方式**：使用 `scripts/gumroad-pro.js` 进行直接操作。有关命令规范，请参阅 [api-reference.md]（位于 {baseDir}/references/api-reference.md）。

## 🔑 认证
该技能需要一个 **Gumroad API 密钥**。系统会优先查找以下环境变量：
1. `GUMROAD_ACCESS_TOKEN`
2. `API_KEY`

### 配置
您可以在 `~/.openclaw/openclaw.json` 文件中使用 `apiKey` 字段进行配置：
```json
{
  "skills": {
    "entries": {
      "gumroad-pro": {
        "enabled": true,
        "apiKey": "YOUR_GUMROAD_TOKEN"
      }
    }
  }
}
```
平台会自动将您的 `apiKey` 值填充到 `GUMROAD_ACCESS_TOKEN` 变量中。

## 🛠️ 工作流程

### 产品库存
- 列出所有数字资产，以便监控销售情况和库存情况。
- 切换产品的发布状态或删除过时的商品。
- 查看 [详细产品操作命令]({baseDir}/references/api-reference.md#1-products)。

### 销售与发货
- 按电子邮件搜索交易记录。
- 处理退款或将实物商品标记为已发货。
- 查看 [详细销售操作命令]({baseDir}/references/api-reference.md#2-sales)。

### 许可证管理
- 验证软件分发的许可证。
- 管理许可证的使用次数或为安全起见轮换许可证。
- 查看 [详细许可证操作命令]({baseDir}/references/api-reference.md#3-licenses)。

### 优惠管理
- 为营销活动创建、列出或删除折扣代码。
- 查看 [详细折扣操作命令]({baseDir}/references/api-reference.md#4-discounts-offer-codes)。

---
该工具由 [Abdul Karim Mia](https://github.com/abdul-karim-mia) 为 OpenClaw 社区开发。