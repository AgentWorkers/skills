---
name: coverage
description: 分析测试覆盖率差距。当用户提到“测试覆盖率”、“哪些部分没有被测试”、“覆盖率差距”、“缺失的测试用例”、“覆盖率报告”或“哪些内容需要测试”时，请使用此功能。
  Analyze test coverage gaps. Use when user says "test coverage",
  "what's not tested", "coverage gaps", "missing tests", "coverage report",
  or "what needs testing".
---
# 分析测试覆盖范围中的缺口

映射应用程序中所有可测试的部分，明确哪些部分已经过测试，哪些部分尚未被覆盖。

## 步骤

### 1. 绘制应用程序结构图

使用 `Explore` 子代理来整理以下内容：

**路由/页面：**
- 扫描路由定义（Next.js 的 `app/` 目录、React Router 配置、Vue Router 等）
- 列出所有用户可见的页面及其路径

**组件：**
- 识别交互式组件（表单、模态框、下拉菜单、表格）
- 记录具有复杂状态逻辑的组件

**API 端点：**
- 扫描 API 路由文件或后端控制器
- 列出所有 API 端点及其方法

**用户流程：**
- 识别关键路径：认证、结账、入职流程、核心功能
- 绘制多步骤工作流程的图谱

### 2. 统计现有测试

扫描所有 `*.spec.ts` / `*.spec.js` 文件：
- 提取哪些页面/路由被测试（通过 `page.goto()` 调用）
- 提取哪些组件被测试（通过定位器使用情况）
- 提取哪些 API 端点被模拟或实际调用
- 统计每个区域的测试数量

### 3. 生成覆盖范围矩阵

```
## Coverage Matrix

| Area | Route | Tests | Status |
|---|---|---|---|
| Auth | /login | 5 | ✅ Covered |
| Auth | /register | 0 | ❌ Missing |
| Auth | /forgot-password | 0 | ❌ Missing |
| Dashboard | /dashboard | 3 | ⚠️ Partial (no error states) |
| Settings | /settings | 0 | ❌ Missing |
| Checkout | /checkout | 8 | ✅ Covered |
```

### 4. 对缺口进行优先级排序

根据业务影响对未覆盖的部分进行排序：

1. **关键** — 认证、支付、核心功能 → 首先进行测试
2. **高** — 用户交互相关的 CRUD 操作、搜索、导航功能
3. **中等** — 设置、偏好设置、边缘情况
4. **低** — 静态页面、关于页面、服务条款

### 5. 提出测试计划

对于每个缺口，建议：
- 需要的测试数量
- 应使用的测试模板（来自 `templates/` 目录）
- 预计的工作量（简单/中等/复杂）

```
## Recommended Test Plan

### Priority 1: Critical
1. /register (4 tests) — use auth/registration template — quick
2. /forgot-password (3 tests) — use auth/password-reset template — quick

### Priority 2: High
3. /settings (4 tests) — use settings/ templates — medium
4. Dashboard error states (2 tests) — use dashboard/data-loading template — quick
```

### 6. 自动生成测试（可选）

询问用户：“是否为前 N 个缺口生成测试？[是/否/选择具体缺口]”

如果用户选择“是”，则使用推荐的模板为每个缺口调用 `/pw:generate` 命令。

## 输出结果：

- 覆盖范围矩阵（表格格式）
- 覆盖范围百分比估计
- 带有工作量估计的优先级缺口列表
- 自动生成缺失测试的选项