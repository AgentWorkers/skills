---
name: fred-navigator
description: 使用 `fredapi` 导航 FRED 的分类和系列，支持带有意图识别的自然语言查询，并进行双重验证。
metadata:
  short-description: FRED navigation and lookup
---
# FRED Navigator

## 目的

提供一个可靠的工作流程，用于浏览 FRED 的类别和系列，支持以下方式：
1. 直接提供 `category_id`
2. 直接提供 `series_id`
3. 使用自然语言进行查询 → 意图识别 → 双重验证

## 输入参数

- `category_id`：FRED 类别 ID
- `series_id`：FRED 系列 ID
- `query`：自然语言请求
- `limit`：返回的候选项数量（默认为 5）
- `api_key`：仅从环境变量 `FRED_API_KEY` 中读取

## 所需资源

- `references/fred_categories_tree.json`
- `references/fred_categories_flat.json`
- 可选：`references/category_paths.json`（预先计算好的路径信息）
- 可选：`references/synonyms.json`（同义词词典）
- 辅助脚本：`scripts/fred_query.py`
- 路径构建脚本：`scripts/build_paths.py`

### 可选资源结构说明

- `references/category_paths.json` 的格式：
  - `{ "category_id": { "id": <int>, "name": "<str>", "path": "<str>" }, ... }`
- `references/synonyms.json` 的格式：
  - `{ "concept": ["alias1", "alias2", ...], ... }`

## 工作流程

### 1. 类别探索

1. 加载 `fred_categories_tree.json` 以进行分层浏览。
2. 如果用户提供了 `category_id`，验证其是否存在。
3. 如果用户提供了 `category_name`，则通过模糊匹配在 `fred_categories.flat.json` 中查找对应的类别，并返回候选结果。

### 2. 系列发现

1. 使用 `search_by_category(category_id)` 列出可用的系列。
2. 建议使用 `scripts/fred_query.py category <id>` 来获得一致的输出结果。
3. 返回的关键列包括：
   - `id`, `title`, `frequency`, `units`, `seasonal_adjustment`, `last_updated`。

### 3. 系列检索

1. 使用 `get_series(series_id)` 获取时间序列数据。
2. 使用 `get_series_info(series_id)` 获取元数据。
3. 建议使用 `scripts/fred_query.py series <id>` 和 `scripts/fred_query.py series-info <id>`。
4. 提供以下信息：
   - 数据的前几行/最后几行
   - 缺失数据的数量
   - 最新值和日期

### 4. 自然语言查询

#### 4.1 意图识别（Top-K）

1. 使用 IDE 的代理（Codex）来解析自然语言请求的意图。
2. 选择最匹配的类别。
3. 如果置信度较低，请求用户确认所选类别后再继续操作。
4. 如果有 `references/category_paths.json` 和 `references/synonyms.json`，可将其作为辅助信息使用。

#### 4.2 双重验证

**结构验证**
- 候选类别必须存在于 `fred_categories_tree.json` 中。
- 如果满足以下条件之一，则通过验证：
  - 该类别有非空的子类别（`children` 不为空）
  - 使用 `search_by_category(id)` 可找到至少 1 个系列
  - 建议使用 `scripts/fred_query.py check-category <id>` 进行快速验证

**语义验证（通过代理）**
- 将用户输入的查询与候选类别的名称或路径进行比较。
- 返回 `pass/fail` 或一个数值相关性分数。

#### 4.3 决策

- 如果结构验证和语义验证都通过，则接受该类别。
- 否则：
  - 返回前 5 个候选类别
  - 请求用户明确选择一个类别

## 错误处理

- 在不确定的情况下，始终返回前 5 个候选类别。
- 如果类别验证失败，切勿继续进行系列数据的检索。

## 注意事项

- 不要硬编码 API 密钥。
- 将大量的参考数据放在 `references/` 目录下，而不是本文件中。
- 在执行查询相关的 Python 函数时，应在沙箱环境中运行它们。

## 维护

- 要更新工作流程或规则，请编辑 `SKILL.md`。
- 要更新类别数据，请替换 `references/` 目录下的文件。
- 要改进自然语言匹配功能，请添加或编辑 `references/synonyms.json`（将关键词映射到相关术语列表）。
- 如有需要，可以重新生成预先计算好的路径信息：运行 `scripts/build_paths.py`。
- 如需添加辅助脚本，请将它们放在 `scripts/` 目录中，并在此处记录使用方法。