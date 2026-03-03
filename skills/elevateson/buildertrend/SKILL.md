---
name: buildertrend
description: "通过 Browser Relay 完成 Buildertrend 的自动化流程——包含 43 个自动化脚本，涵盖销售、项目管理、财务、调度、变更请求、每日日志、需求申请（RFIs）、待办事项列表、开票和采购等功能。无需使用任何 API。"
homepage: https://github.com/elevateson/buildertrend-openclaw
metadata: { "openclaw": { "requires": { "capabilities": ["browser"] } } }
---
# Buildertrend 技能 — {{company_name}}

## 概述
Buildertrend 是 {{company_name}} 的项目管理平台。该平台**不提供 API**，所有自动化操作均通过 OpenClaw 的 Chrome 扩展程序（Browser Relay）在浏览器中完成。

> **如果是新用户？** 请参阅下面的 [设置与配置](#setup--configuration) 以开始使用。

## 工作原理
1. 用户在 Chrome 浏览器中登录 Buildertrend。
2. 用户点击 Buildertrend 选项卡上的 OpenClaw Browser Relay 工具栏图标（图标会亮起）。
3. 代理使用 `browser` 工具，并设置 `profile="chrome"` 来控制该选项卡。
4. 工作流程：**截图 → 读取数据 → 执行操作 → 验证结果**。

## 重要规则

### 在执行任何操作之前
1. **截图**——确认你处于正确的页面。
2. 检查登录界面——如果已登出，请停止操作并要求用户重新认证。
3. 等待页面完全加载。
4. 在点击之前确认目标元素的正确位置。

### 在执行操作期间
- **每次操作后都要截图**——以验证结果。
- **不要急于操作**——在操作之间适当休息。
- **先读取数据再修改**——在修改之前始终记录当前状态。
- **注意弹出窗口**——在尝试与页面交互之前，检查是否有弹出窗口。

### 出现错误时
- 立即截图。
- 报告发生的情况以及你尝试执行的操作。
- **不要盲目重试**——请寻求指导。
- 将错误截图保存到 `memory/bt-errors/` 文件夹中。

## 导航模式
*（将在第一阶段发现后填充）

## 模块参考
有关完整的模块列表和优先级，请参阅 `STRATEGYY.md`。
有关 UI 元素映射，请参阅 `buildertrend-map.json`（在发现相应模块后）。

## 工作流程手册
有关分步自动化工作流程，请参阅 `playbooks/` 目录。
有关完整的索引和交叉引用，请参阅 `playbooks/README.md`。

### 可用的工作流程手册（共 43 个）：

**销售与前期准备（6 个）：**
| 工作流程手册 | 文件 | 触发条件 |
|---|---|---|
| 潜在客户机会 | `playbooks/lead-opportunities.md` | 新潜在客户、检查销售流程、潜在客户活动 |
| 将潜在客户转化为工作机会 | `playbooks/convert-lead-to-job.md` | 潜在客户准备好转化、提案被接受 |
| 客户提案 | `playbooks/client-proposals.md` | “创建提案”、报价准备完成、发送给客户 |
| 运行报价 | `playbooks/run-estimates.md` | “生成报价”、新工作需要定价 |
| 启动项目与估算 | `playbooks/takeoff-estimating.md` | “进行项目启动”、上传计划、测量蓝图 |
| 投标包管理 | `playbooks/bid-package-management.md` | “发送投标”、“参与竞标”、比较回复 |

**客户与联系人管理（4 个）：**
| 工作流程手册 | 文件 | 触发条件 |
| 添加客户 | `playbooks/add-clients.md` | “将客户添加到工作机会中”、新客户联系人 |
| 客户门户设置 | `playbooks/client-portal-setup.md` | “设置客户门户”、配置客户访问权限 |
| 供应商入职 | `playbooks/sub-vendor-onboarding.md` | “添加新供应商”、供应商入职、中标通知 |
| 客户调查与反馈 | `playbooks/surveys-feedback.md` | “发送调查问卷”、收集客户反馈、NPS 跟踪 |

**项目管理（9 个）：**
| 工作流程手册 | 文件 | 触发条件 |
| 创建每日日志 | `playbooks/create-daily-log.md` | [项目] 的每日日志、每日提醒 |
| 日程管理 | `playbooks/schedule-management.md` | “添加到日程表中”、更新进度、发送子项目更新 |
| 管理请求信息（RFI） | `playbooks/manage-rfis.md` | “创建请求信息”、跟踪未解决的问题、跟进 |
| 待办事项与任务清单 | `playbooks/manage-todos-punchlist.md` | “创建待办事项”、“任务清单”、关闭事项跟踪 |
| 管理选择事项 | `playbooks/manage-selections.md` | “设置选择事项”、客户完成选择、预留费用 |
| 规格管理 | `playbooks/specifications-management.md` | “创建规格书”、范围文档、链接到投标文件 |
| 文档管理 | `playbooks/document-management.md` | “上传计划文件”、文件管理、共享文档 |
| 消息与沟通 | `playbooks/messaging-communications.md` | “向 [子团队] 发送消息”、检查消息、通知所有子团队成员 |
| 照片与视频管理 | `playbooks/photo-video-management.md` | “上传照片”、现场文档记录、标注、视频录制 |

**财务（12 个）：**
| 工作流程手册 | 文件 | 触发条件 |
| 收据 → 发票 | `playbooks/receipt-to-bill.md` | 成本收件箱中有新收据、用户发送收据 |
| 创建发票 | `playbooks/create-invoice.md` | 为 [项目] 创建发票、 billing cycle、财务部门批准 |
| 创建采购订单 | `playbooks/create-po.md` | 为 [供应商] 创建采购订单、投标被批准、财务部门需要采购订单 |
| 创建变更订单 | `playbooks/create-change-order.md` | 为 [项目] 创建变更订单、客户财务部门提出请求 |
| 高级变更订单 | `playbooks/manage-change-orders-advanced.md` | 复杂的变更订单、差异性采购订单、多采购订单管理 |
| 工作成本报告 | `playbooks/job-costing-report.md` | “预算情况如何？”，每周审查、会议前准备 |
| Buildertrend 与 QuickBooks Online 对账 | `playbooks/bt-qbo-reconciliation.md` | “检查 QuickBooks Online 的同步情况”、每月结算、发现差异 |
| 信用备忘录与押金 | `playbooks/credit-memos-deposits.md` | “创建押金”、“申请信用”、“保留金管理” |
| 在线支付设置 | `playbooks/online-payments-setup.md` | “设置支付方式”、配置客户/子团队的支付方式 |
| 保留金管理 | `playbooks/retainage-management.md` | “设置保留金”、释放扣款、保留金报告 |
| 报告与仪表板 | `playbooks/reporting-dashboards.md` | “运行报告”、财务审查、现金流、关键绩效指标（KPI） |

**人力与时间（1 个）：**
| 工作流程手册 | 文件 | 触发条件 |
| 计时器管理 | `playbooks/time-clock-management.md` | “[员工] 登录计时器”、批准工时表、导出工资单 |

**设置与管理员工（7 个）：**
| 工作流程手册 | 文件 | 触发条件 |
| 新工作设置 | `playbooks/new-job-setup.md` | “新工作创建”、项目启动、潜在客户转化成功 |
| 成本代码设置 | `playbooks/cost-code-setup.md` | “添加成本代码”、检查映射关系、设置 QuickBooks Online 的同步 |
| 用户与角色管理 | `playbooks/user-role-management.md` | “添加用户”、更改权限、自定义角色 |
| 管理员设置与定制 | `playbooks/admin-setup-customization.md` | 公司设置、品牌配置、功能定制 |
| Home Depot 集成 | `playbooks/home-depot-integration.md` | “连接 Home Depot 系统”、处理 Home Depot 的收据信息 |
| 模板管理 | `playbooks/template-management.md` | “创建模板”、工作/日程/报价模板 |
| 财务设置与配置 | `playbooks/financial-settings-config.md` | 税率设置、发票设置、发票审批、QuickBooks Online 同步设置 |

**集成（1 个）：**
| 工作流程手册 | 文件 | 触发条件 |
| 市场平台与集成 | `playbooks/marketplace-integrations.md` | “连接 [应用程序]”、集成状态、Zapier、Gusto 集成 |

**项目收尾（2 个）：**
| 工作流程手册 | 文件 | 触发条件 |
| 项目收尾 | `playbooks/project-closeout.md` | “项目收尾”、所有工作完成、最终付款 |
| 保修管理 | `playbooks/warranty-management.md` | “设置保修”、处理新索赔、检查索赔状态 |

**移动端（1 个）：**
| 工作流程手册 | 文件 | 触发条件 |
| 移动端工作流程 | `playbooks/mobile-workflows.md` | 移动端特定的 Buildertrend 操作、现场工作人员的操作 |

### 工作流程手册通用模式：
1. **触发条件**——用户命令、预定事件或外部输入。
2. **识别目标**——哪个项目？
3. **收集信息**——收集详细信息（通过引导式提示或自由输入）。
4. **建议操作**——提供默认选项（成本代码、供应商、金额、标签）。
5. **审核结果**——显示带有创建/编辑/取消按钮的摘要。
6. **执行操作**——在 Buildertrend 中通过 Browser Relay 执行操作（截图 → 执行操作 → 验证结果）。
7. **操作后**——记录操作、更新提醒、通知其他代理、检查 QuickBooks Online 的同步情况。

有关完整的索引和详细文档，请参阅 `playbooks/README.md`。

## 参考资料
- **bt-ui-patterns.md** — 所有 Buildertrend 表单的浏览器 Relay 交互模式：采购订单、日程表、变更订单、潜在客户信息、下拉菜单、弹出窗口、网格界面、导航（16 个部分，共 432 行）。
- **knowledge-base.md** — 完整的 Buildertrend 模块参考资料（2,349 行）。⚠️ **不要每次任务都加载整个文件**——这会占用大量屏幕空间。仅加载当前工作流程相关的部分。
- **qbo-sync-guide.md** — QuickBooks Online 集成参考指南。
- **workflows.md** — 官方的 Buildertrend 工作流程手册。
- **knowledge-base.md** — 完整的 Buildertrend 模块参考资料（2,349 行）。⚠️ **不要每次任务都加载整个文件**——根据需要搜索或仅加载相关部分。加载整个文件会占用大量屏幕空间。
- **qbo-sync-guide.md** — QuickBooks Online 集成参考指南。
- **workflows.md** — 官方的 Buildertrend 工作流程手册。

## 会话管理
- Buildertrend 会话会过期——在开始工作流程之前始终检查登录状态。
- 如果会话已过期：通知用户，不要尝试重新输入凭据。
- 所有登录/认证操作均由用户完成——代理不会直接处理凭据。

## 数据提取
从 Buildertrend 中提取数据（如预算、日程表等）时：
1. 对页面进行截图。
2. 解析页面的 aria/role 树结构以获取结构化数据。
3. 将数据格式化为清晰的输出（JSON 或 markdown 表格）。
4. 将数据存储在适当的内存文件中或传递给请求数据的代理。

## 集成
- 预算数据 → 财务代理（用于 QuickBooks Online 对账）。
- 采购订单数据 → 采购代理（用于采购流程跟踪）。
- 联系人数据 → 客户关系管理（CRM）代理（用于客户关系管理）。
- 日程表/变更订单/每日日志 → 代理（用于项目报告）。
- 文档 → Google Drive（用于归档）。

---

## 设置与配置

### 先决条件
- **OpenClaw** 版本需达到 2026.2.20 或更高版本。
- 安装了 OpenClaw 的 Chrome 扩展程序（Browser Relay）。
- 拥有 Buildertrend 账户（包含你希望自动化的模块）。
- 用户必须在 Chrome 浏览器中登录 Buildertrend。

### 第 1 步：安装该技能
将 `buildertrend/` 文件夹复制到你的 OpenClaw 工作区中的 `SKILLS/` 目录下：
```
~/.openclaw/workspace/SKILLS/buildertrend/
```

### 第 2 步：配置占位符
该技能在所有文件中使用了 `{{placeholders}}`。请将这些占位符替换为你的公司实际值：

| 占位符 | 含义 | 示例 |
|---|---|---|
| `{{company_name}}` | 你的公司名称 | Acme Construction LLC |
| `{{company_domain}}` | 你的公司域名 | acmeconstruction.com |
| `{{company_phone}}` | 公司电话号码 | 555-123-4567 |
| `{{company_prefix}}` | 发票/采购订单前缀 | ACME- |
| `{{admin_email}}` | 管理员电子邮件地址 | admin@acmeconstruction.com |
| `{{owner_name}}` | 账户所有者的全名 | Jane Smith |
| `{{team_member}}` | 其他团队成员（根据上下文替换） | John Doe |
| `{{tax_jurisdiction}}` | 你的税收管辖区名称 | CA-Los Angeles |
| `{{tax_rate}}` | 综合税率（%） | 9.5 |
| `{{state_tax}}` | 州税税率（%） | 7.25 |
| `{{city_tax}}` | 市税税率（%） | 2.25 |
| `{{jurisdiction}}` | 管辖区简称 | LA County |
| `{{project_address}}` | 示例项目地址 | 100 Main St, Suite 200 |
| `{{bookkeeper_workspace}}` | 财务代理的工作区路径 | workspace-bookkeeper |
| `{{receipt_agent_workspace}}` | 收据代理的工作区路径 | workspace-receipt-agent |
| `{{procurement_agent_workspace}}` | 采购代理的工作区路径 | workspace-procurement |

**快速替换**（从技能根目录运行）：
```bash
find . -name "*.md" -exec sed -i '' 's/{{company_name}}/Your Company/g' {} +
```
对每个占位符都使用你的实际值进行替换。

### 第 3 步：自定义项目选择按钮
许多工作流程手册包含用于选择项目的内联按钮。请将示例项目替换为你的实际项目：

**替换前：**
```
| 🏗️ Project Alpha | `primary` | `bt_co_project_1` |
| 🏗️ Project Alpha | `primary` | `bt_co_project_3` |
```

**替换后：**
```
| 🏗️ 123 Main St Office Buildout | `primary` | `bt_co_project_MAIN` |
| 🏗️ 456 Oak Ave Renovation | `primary` | `bt_co_project_OAK` |
```

### 第 4 步：配置 Browser Relay
1. 安装 OpenClaw 的 Chrome 扩展程序（Browser Relay）。
2. 在 Chrome 浏览器中登录 Buildertrend。
3. 点击 Buildertrend 选项卡上的 Browser Relay 工具栏图标（图标会亮起）。
4. 代理现在可以通过 `browser` 工具（设置 `profile="chrome"`）来控制该选项卡。

### 第 5 步：在测试项目上测试
**⚠️ 不要在实际项目中进行测试。** 先在 Buildertrend 中创建一个测试项目：
1. 在 Buildertrend 中创建一个名为 “Test Project” 的项目。
2. 运行一个简单的工作流程手册（例如 `create-daily-log.md`）。
3. 确认代理能否正确地进行截图、导航和操作。
4. 确认无误后，再在实际项目中使用。

### 多代理设置（可选）
> **只使用一个代理？** 该技能完全可以仅由一个代理执行。工作流程手册中提到了多个类型的代理（财务代理、收据代理、采购代理、CRM 代理）——**可以忽略这些内容**。当工作流程手册中提到 “通知财务代理” 时，只需跳过该步骤或自行处理。无需进行多代理设置。

如果你使用多个代理，请配置他们的工作区：
- 将 `{{bookkeeper_workspace}}` 替换为财务代理的工作区路径。
- 将 `{{receipt_agent_workspace}}` 替换为收据代理的工作区路径。
- 将 `{{procurement_agent_workspace}}` 替换为采购代理的工作区路径。
- 更新上面的 **集成** 部分，填写你的代理名称。

### 管辖区配置
税率、保留金规则和押金减免要求通过 `{{placeholders}}` 进行配置。请根据你的实际情况进行调整：
- **税率** — 将 `{{tax_rate}}` 设置为你的实际税率。
- **保留金** — 查看 `playbooks/retainage-management.md` 以了解特定管辖区的规则。
- **押金减免** — 查看 `playbooks/lien-waiver-tracking.md` 以了解当地的合规要求。