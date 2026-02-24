---
name: snipeit
description: 通过 REST API 与 Snipe-IT 资产管理系统进行交互。该 API 用于管理资产（硬件）、用户、许可证、配件、耗材、组件、位置、部门、型号、制造商、状态标签、类别、供应商以及维护记录等相关信息。可触发以下操作：`snipe`、`asset`、`hardware`、`license`、`inventory`、`check out`、`check in`、`IT assets`、`equipment`。
metadata:
  clawdbot:
    env:
      - SNIPEIT_URL        # e.g. https://assets.w-w.top
      - SNIPEIT_API_TOKEN  # Bearer token from your profile → API keys
    requires:
      - curl
      - jq
---
# Snipe-IT 技能

## 概述

Snipe-IT 的 REST API 会对所有有效的 HTTP 请求返回 **200 OK** 的响应状态码。请检查响应中的 `.status` 字段，其值为 `"success"` 或 `"error"`。

基础 URL：`$SNIPEIT_URL/api/v1`

---

## 核心辅助功能

```bash
snipe() {
  local method="${1:-GET}"
  local endpoint="$2"
  local data="${3:-}"

  local args=(
    -s -X "$method"
    -H "Authorization: Bearer $SNIPEIT_API_TOKEN"
    -H "Accept: application/json"
    -H "Content-Type: application/json"
  )

  [ -n "$data" ] && args+=(-d "$data")

  curl "${args[@]}" "${SNIPEIT_URL}/api/v1${endpoint}" | jq .
}

# Shortcuts
snipe_get()    { snipe GET    "$1"; }
snipe_post()   { snipe POST   "$1" "$2"; }
snipe_patch()  { snipe PATCH  "$1" "$2"; }
snipe_put()    { snipe PUT    "$1" "$2"; }
snipe_delete() { snipe DELETE "$1"; }
```

---

## 资产（硬件）

```bash
# List all assets (with pagination)
snipe_get "/hardware?limit=50&offset=0"

# Search assets
snipe_get "/hardware?search=MacBook&limit=20"

# Filter by status label
snipe_get "/hardware?status_id=2&limit=50"

# Get asset by ID
snipe_get "/hardware/42"

# Get asset by asset tag
snipe_get "/hardware/bytag/ASSET-001"

# Get asset by serial number
snipe_get "/hardware/byserial/SN123456"

# Create asset
snipe_post "/hardware" '{
  "asset_tag":   "ASSET-001",
  "model_id":    5,
  "status_id":   2,
  "name":        "MacBook Pro 16",
  "serial":      "SN123456",
  "location_id": 1,
  "notes":       "Assigned to dev team"
}'

# Update asset (PATCH = partial update)
snipe_patch "/hardware/42" '{
  "name":      "MacBook Pro 16 (updated)",
  "status_id": 3,
  "notes":     "Screen replaced"
}'

# Full update (PUT = replace all fields)
snipe_put "/hardware/42" '{
  "asset_tag":  "ASSET-001",
  "model_id":   5,
  "status_id":  2,
  "name":       "MacBook Pro 16",
  "serial":     "SN123456"
}'

# Delete asset
snipe_delete "/hardware/42"

# Checkout asset to user
snipe_post "/hardware/42/checkout" '{
  "checkout_to_type": "user",
  "assigned_user":    7,
  "note":             "Assigned for remote work",
  "checkout_at":      "2025-01-15",
  "expected_checkin": "2025-12-31"
}'

# Checkout asset to location
snipe_post "/hardware/42/checkout" '{
  "checkout_to_type":  "location",
  "assigned_location": 3,
  "note":              "Conference room setup"
}'

# Checkout asset to another asset
snipe_post "/hardware/42/checkout" '{
  "checkout_to_type": "asset",
  "assigned_asset":   15
}'

# Checkin asset
snipe_post "/hardware/42/checkin" '{
  "note":       "Returned after use",
  "checkin_at": "2025-06-01"
}'

# Audit asset (confirm location)
snipe_post "/hardware/audit" '{
  "asset_tag":   "ASSET-001",
  "location_id": 2,
  "note":        "Verified during quarterly audit"
}'

# Get audit history
snipe_get "/hardware/audit/due"
snipe_get "/hardware/audit/overdue"

# List assets checked out to a user
snipe_get "/users/7/assets"

# Restore deleted asset
snipe_post "/hardware/42/restore" '{}'
```

---

## 用户

```bash
# List all users
snipe_get "/users?limit=50"

# Search users
snipe_get "/users?search=john&limit=20"

# Get user by ID
snipe_get "/users/7"

# Get current API user
snipe_get "/users/me"

# Create user
snipe_post "/users" '{
  "first_name":  "John",
  "last_name":   "Doe",
  "username":    "john.doe",
  "email":       "john.doe@example.com",
  "password":    "SecurePass123!",
  "password_confirmation": "SecurePass123!",
  "department_id": 2,
  "location_id":   1,
  "employee_num":  "EMP-001",
  "jobtitle":      "Developer",
  "activated":     true
}'

# Update user
snipe_patch "/users/7" '{
  "department_id": 3,
  "jobtitle":      "Senior Developer"
}'

# Delete user
snipe_delete "/users/7"

# Get user's assets
snipe_get "/users/7/assets"

# Get user's licenses
snipe_get "/users/7/licenses"

# Get user's accessories
snipe_get "/users/7/accessories"

# Get user's consumables
snipe_get "/users/7/consumables"
```

---

## 许可证

```bash
# List all licenses
snipe_get "/licenses?limit=50"

# Search licenses
snipe_get "/licenses?search=Office&limit=20"

# Get license by ID
snipe_get "/licenses/3"

# Create license
snipe_post "/licenses" '{
  "name":            "Microsoft Office 365",
  "serial":          "XXXXX-XXXXX-XXXXX",
  "seats":           25,
  "category_id":     4,
  "manufacturer_id": 2,
  "license_email":   "it@example.com",
  "purchase_date":   "2025-01-01",
  "expiration_date": "2026-01-01",
  "purchase_cost":   "299.99",
  "notes":           "Annual subscription"
}'

# Update license
snipe_patch "/licenses/3" '{
  "seats": 30,
  "notes": "Seats increased"
}'

# Delete license
snipe_delete "/licenses/3"

# List license seats (who has it checked out)
snipe_get "/licenses/3/seats"

# Checkout license seat to user
snipe_post "/licenses/3/seats/12/checkout" '{
  "assigned_to": 7,
  "note":        "Developer license"
}'

# Checkin license seat
snipe_delete "/licenses/3/seats/12/checkin"
```

---

## 配件

```bash
# List all accessories
snipe_get "/accessories?limit=50"

# Get accessory by ID
snipe_get "/accessories/8"

# Create accessory
snipe_post "/accessories" '{
  "name":            "USB-C Hub",
  "category_id":     5,
  "manufacturer_id": 3,
  "qty":             10,
  "purchase_date":   "2025-01-01",
  "purchase_cost":   "49.99",
  "location_id":     1
}'

# Update accessory
snipe_patch "/accessories/8" '{"qty": 15}'

# Delete accessory
snipe_delete "/accessories/8"

# Checkout accessory to user
snipe_post "/accessories/8/checkout" '{
  "assigned_to": 7,
  "note":        "For home office"
}'

# Checkin accessory
snipe_post "/accessories/8/checkin" '{
  "note": "Returned"
}'

# List checked-out accessories
snipe_get "/accessories/8/checkedout"
```

---

## 消耗品

```bash
# List consumables
snipe_get "/consumables?limit=50"

# Get consumable by ID
snipe_get "/consumables/5"

# Create consumable
snipe_post "/consumables" '{
  "name":        "Printer Paper A4",
  "category_id": 6,
  "qty":         500,
  "item_no":     "PP-A4-500",
  "purchase_cost": "9.99",
  "location_id": 1
}'

# Checkout consumable (decrements qty)
snipe_post "/consumables/5/checkout" '{
  "assigned_to": 7,
  "note":        "For printer"
}'
```

---

## 组件

```bash
# List components
snipe_get "/components?limit=50"

# Get component by ID
snipe_get "/components/12"

# Create component
snipe_post "/components" '{
  "name":        "RAM 16GB DDR4",
  "category_id": 7,
  "qty":         20,
  "serial":      "RAM-SN-001",
  "purchase_cost": "89.99",
  "location_id": 1
}'

# Checkout component to asset
snipe_post "/components/12/checkout" '{
  "assigned_to": 42,
  "assigned_qty": 2,
  "note":        "Upgrade"
}'

# Checkin component
snipe_post "/components/12/checkin" '{
  "checkin_qty": 2
}'
```

---

## 位置信息

```bash
# List locations
snipe_get "/locations?limit=50"

# Get location by ID
snipe_get "/locations/1"

# Create location
snipe_post "/locations" '{
  "name":     "Kyiv Office",
  "address":  "Khreschatyk 1",
  "city":     "Kyiv",
  "country":  "UA",
  "currency": "UAH"
}'

# Update location
snipe_patch "/locations/1" '{"name": "Kyiv HQ"}'

# Delete location
snipe_delete "/locations/1"

# Get assets at location
snipe_get "/locations/1/assets"

# Get users at location
snipe_get "/locations/1/users"
```

---

## 部门信息

```bash
# List departments
snipe_get "/departments?limit=50"

# Get department by ID
snipe_get "/departments/2"

# Create department
snipe_post "/departments" '{
  "name":        "Engineering",
  "location_id": 1,
  "manager_id":  5
}'

# Update / Delete
snipe_patch  "/departments/2" '{"name": "Engineering & DevOps"}'
snipe_delete "/departments/2"
```

---

## 型号信息

```bash
# List models
snipe_get "/models?limit=50"

# Get model by ID
snipe_get "/models/5"

# Create model
snipe_post "/models" '{
  "name":             "MacBook Pro 16 M3",
  "manufacturer_id":  1,
  "category_id":      1,
  "model_number":     "MBP16-M3-2024",
  "depreciation_id":  1,
  "eol":              36
}'
```

---

## 状态标签

```bash
# List all status labels
snipe_get "/statuslabels"

# Get status label by ID
snipe_get "/statuslabels/2"

# Create status label
snipe_post "/statuslabels" '{
  "name":          "In Repair",
  "type":          "undeployable",
  "color":         "#ff6600",
  "show_in_nav":   true,
  "default_label": false
}'
# Types: deployable | pending | undeployable | archived
```

---

## 分类信息

```bash
# List categories
snipe_get "/categories?limit=50"

# Create category
snipe_post "/categories" '{
  "name":          "Laptops",
  "category_type": "asset",
  "eula":          false,
  "require_acceptance": false
}'
# category_type: asset | accessory | consumable | component | license
```

---

## 制造商与供应商

```bash
# Manufacturers
snipe_get "/manufacturers?limit=50"
snipe_post "/manufacturers" '{"name": "Apple", "url": "https://apple.com"}'
snipe_patch "/manufacturers/1" '{"support_email": "support@apple.com"}'

# Suppliers
snipe_get "/suppliers?limit=50"
snipe_post "/suppliers" '{
  "name":    "Tech Distributor LLC",
  "email":   "orders@techdist.com",
  "phone":   "+380441234567",
  "address": "Kyiv, Ukraine"
}'
```

---

## 资产维护

```bash
# List maintenances
snipe_get "/maintenances?limit=50"

# Get maintenance by ID
snipe_get "/maintenances/3"

# Create maintenance record
snipe_post "/maintenances" '{
  "asset_id":          42,
  "supplier_id":       2,
  "asset_maintenance_type": "Repair",
  "title":             "Screen replacement",
  "start_date":        "2025-06-01",
  "completion_date":   "2025-06-05",
  "cost":              "150.00",
  "notes":             "Cracked screen replaced under warranty",
  "is_warranty":       true
}'

# Update maintenance
snipe_patch "/maintenances/3" '{"completion_date": "2025-06-04", "cost": "120.00"}'

# Delete maintenance
snipe_delete "/maintenances/3"
```

---

## 报告与活动记录

```bash
# Activity log (recent actions)
snipe_get "/reports/activity?limit=50"

# Filter activity by item type
snipe_get "/reports/activity?item_type=App%5CModels%5CAsset&limit=20"

# Filter by action type
snipe_get "/reports/activity?action_type=checkout&limit=20"

# Filter by user
snipe_get "/reports/activity?user_id=7&limit=20"
```

---

## 自定义字段

```bash
# List all custom fields
snipe_get "/fields"

# List fieldsets
snipe_get "/fieldsets"

# Get fieldset by ID (includes its fields)
snipe_get "/fieldsets/2"

# Update custom field value on asset (use field's db_column_name)
snipe_patch "/hardware/42" '{
  "custom_fields": {
    "_snipeit_purchase_order_1": "PO-2025-001",
    "_snipeit_warranty_months_2": "36"
  }
}'
```

---

## 设置

```bash
# Get app settings
snipe_get "/settings"

# List backup files
snipe_get "/settings/backups"

# Download backup
snipe_get "/settings/backups/download/backup-2025-06-01.zip"

# Get app version
snipe_get "/version"
```

---

## 常见工作流程

- **完整资产录入**  
- **季度审计**  
- **许可证合规性检查**  
- **用户离职处理**  

---

## 错误处理

```bash
snipe_safe() {
  local result
  result=$(snipe "$@")
  local status=$(echo "$result" | jq -r '.status // "success"')

  if [ "$status" = "error" ]; then
    echo "❌ Error: $(echo "$result" | jq -r '.messages')" >&2
    return 1
  fi

  echo "$result"
}

# Usage
snipe_safe GET "/hardware/42"
snipe_safe POST "/hardware/42/checkout" '{"checkout_to_type":"user","assigned_user":7}'
```

---

## 设置流程

**获取 API 令牌：**
1. 登录 → 点击右上角的头像  
2. 选择 **管理 API 密钥** → **创建新令牌**  
3. 为令牌命名 → 复制令牌内容  

**重要提示：**  
- 必须同时设置 `Content-Type: application/json` 和 `Accept: application/json`  
- API 始终返回 `200 OK` 状态码，请通过 `.status` 字段判断操作是否成功（`success` 或 `error`）  
- 使用 `?limit=` 和 `?offset=` 参数进行分页（每次请求最多返回 500 条数据）  
- 日期格式：`YYYY-MM-DD`  
- 货币值应表示为字符串形式（例如 `"99.99"`，而非数字）