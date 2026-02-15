---
name: Rental
description: 作为租户、房东、房东或客人，您可以利用市场分析、诈骗检测和租赁审核功能来寻找、协商和管理租赁事务。
---

## 角色

根据用户的具体情况，加载相应的指南：

| 角色 | 指南 | 使用场景 |
|------|-------|----------|
| 租户 | `tenant.md` | 寻找房源、提交申请、审核租约 |
| 房东 | `landlord.md` | 定价、筛选租客、物业管理 |
| 度假房东 | `vacation.md` | 优化Airbnb/VRBO房源信息 |
| 度假客人 | `vacation.md` | 预订度假房源、比较不同选项 |
| 设备租赁 | `equipment.md` | 汽车、工具、装备的租赁服务 |

---

## 核心功能

**搜索与分析：**
- 计算实际成本（租金 + 公共事业费用 + 通勤费用 + 其他费用）
- 并行比较多个房源
- 识别欺诈性房源（价格过低、要求在看房前付款、房东位于国外）

**申请与谈判：**
- 准备申请所需的文件清单
- 起草申请信函
- 研究类似房源以作为谈判的依据

**租约审核：**
- 标出存在问题的条款（自动续租、过高费用、未经通知即可入住等）
- 用通俗易懂的语言解释法律条款

---

## 快捷命令

```
"Search for 2BR apartments in [area] under $2000"
"Calculate true monthly cost including commute to [workplace]"
"Review this lease for red flags"
"Help me negotiate rent down"
"Is this listing a scam?"
```

---

## 会话状态

<!-- 当前角色：租户 | 房东 | 度假房东 | 度假客人 | 设备租赁 -->
<!-- 当前搜索条件：地理位置、预算、需求 -->
<!-- 被关注的房源地址：