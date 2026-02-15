---
name: productboard-search
description: 搜索并探索 ProductBoard 的功能、产品以及用户反馈。
user-invocable: true
homepage: https://github.com/robertoamoreno/openclaw-productboard
metadata: {"openclaw":{"emoji":"🔍"}}
---

# ProductBoard 搜索功能

您可以在 ProductBoard 工作区中搜索和探索功能、产品、组件以及客户反馈。

## 可用的工具

- `pb_search`：对所有 ProductBoard 实体进行全局搜索
- `pb_feature_list`：通过过滤器列出功能
- `pb_feature_get`：获取详细的功能信息
- `pb_feature_search`：按名称/描述搜索功能
- `pb_product_list`：列出所有产品
- `pb_product_get`：获取包含组件的产品详细信息
- `pb_product_hierarchy`：查看完整的产品/组件结构
- `pb_note_list`：列出客户反馈记录

## 搜索策略

### 查找功能

1. **按关键词**：使用 `pb_feature_search` 并输入查询词
2. **按产品**：使用 `pb_feature_list` 并设置 `productId` 过滤器
3. **按状态**：使用 `pb_feature_list` 并设置 `status` 过滤器（新创建、进行中、已发布、已归档）
4. **按组件**：使用 `pb_feature_list` 并设置 `componentId` 过滤器

### 了解工作区结构

1. 首先使用 `pb_product_hierarchy` 查看整个工作区的组织结构
2. 使用 `pb_product_get` 探索特定产品及其组件
3. 通过产品或组件过滤功能以缩小搜索范围

### 查找客户反馈

1. 使用 `pb_note_list` 查看最近的反馈记录
2. 使用 `createdFrom` 和 `createdTo` 过滤器按日期范围筛选
3. 使用 `pb_search` 并设置类型为 `note` 来查找特定的反馈

## 示例查询

**用户**：“查找与身份验证相关的所有功能”
**操作**：使用 `pb_feature_search` 并输入查询词 “authentication”

**用户**：“当前有哪些功能正在进行中？”
**操作**：使用 `pb_feature_list` 并设置 `status` 为 “in-progress”

**用户**：“显示产品结构”
**操作**：使用 `pb_product_hierarchy` 查看完整的产品结构

**用户**：“查找关于性能的客户反馈”
**操作**：使用 `pb_search` 并输入查询词 “performance” 和类型 “note”

## 提示

- 先使用 `pb_search` 进行广泛搜索，然后使用特定工具进行细化
- 在不熟悉的工作区中，先使用 `pb_product_hierarchy` 来了解结构
- 搜索不区分大小写，支持部分匹配
- 结果中包含直接链接，可快速访问 ProductBoard 页面