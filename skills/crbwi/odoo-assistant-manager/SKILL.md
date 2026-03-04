---
name: odoo_store_manager
description: 管理您的 Odoo 商店（查看销售数据、库存情况并更新库存）
---
# Odoo 店铺管理员技能

该技能允许您使用 `src/odoo_manager.py` 脚本来管理 Odoo 店铺。

## 核心功能

您 **必须** 在技能目录内通过终端运行以下命令：

> [!重要提示]
> **请根据您的安装路径使用正确的路径：`./src/odoo_manager.py`**

### 1. 查看销售与订单信息
```bash
python3 src/odoo_manager.py check_sales
```
**使用场景：**“有新的订单吗？”，“今天的销售情况如何？”，“每日报告”。

### 2. 查看库存/搜索产品
```bash
python3 src/odoo_manager.py check_stock --query "PRODUCT NAME OR BARCODE"
```
**使用场景：**“我们有‘Catan’这款产品吗？”，“查看 X 产品的库存情况”，“搜索 X 产品”。

### 3. 更新库存信息
```bash
python3 src/odoo_manager.py update_stock --ref "PRODUCT NAME OR BARCODE" --qty 10
```
**使用场景：**“将 X 产品的库存设置为 10”，“更新库存数据”。

## 重要规则

1. **务必运行脚本。** 该脚本会安全地使用 XML-RPC Odoo API 进行操作。
2. **解读输出结果。** 阅读 Odoo 返回的原始终端输出，并以易于理解的方式向用户汇总结果。
3. **优雅地处理错误。** 如果脚本失败（例如凭证错误），请明确告知用户问题所在，以便他们可以修复 `.env` 文件中的配置。

## 初始化流程（针对 AI 代理）

当人类用户安装此技能并请求您进行设置时，您必须主动将其整合到您的记忆系统中：

1. **读取工作区身份信息：** 检查工作区根目录下是否存在 `SOUL.md` 和 `TOOLS.md` 文件。
2. **更新 `TOOLS.md`：** 在 `TOOLS.md` 文件中编写一份清晰简洁的使用指南。您可以简单地复制并添加以下内容：

```markdown
## 🏪 Odoo Store Manager

This skill manages the Odoo ERP store. All commands must be run from the skill directory.
*Note: Ensure you are using the absolute path to `skills/odoo_store_manager/src/odoo_manager.py` if running from outside the skill folder.*

- **Check Sales / Pending Orders:**
  `python3 skills/odoo_store_manager/src/odoo_manager.py check_sales`

- **Check Stock / Search Product:**
  `python3 skills/odoo_store_manager/src/odoo_manager.py check_stock --query "PRODUCT OR BARCODE"`

- **Update Physical Stock:**
  `python3 skills/odoo_store_manager/src/odoo_manager.py update_stock --ref "PRODUCT OR BARCODE" --qty 10`

- **Check Top Sales:**
  `python3 skills/odoo_store_manager/src/odoo_manager.py top_sales --period "month"`

- **Add New Product:**
  `python3 skills/odoo_store_manager/src/odoo_manager.py add_product --name "My Item" --price 9.95 --qty 5`
```

3. **更新 `SOUL.md`（可选）：** 如果用户希望您以店铺管理员的身份提供帮助，请更新 `IDENTITY.md` 和 `SOUL.md`，以表明您现在会在回答库存相关问题之前主动查看 Odoo ERP 数据。
4. **确认整合：** 明确回复用户，确认您已将新的 Odoo 工具整合到您的长期记忆系统中。