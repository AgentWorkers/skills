---
name: Pandas
slug: pandas
version: 1.0.0
homepage: https://clawic.com/skills/pandas
description: 使用高效的模式来分析、转换和清洗 DataFrame，支持过滤、分组、合并以及数据透视（pivoting）等操作。
metadata: {"clawdbot":{"emoji":"🐼","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请创建 `~/pandas/` 目录，并阅读 `setup.md` 以完成初始化配置。用户偏好设置存储在 `~/pandas/memory.md` 文件中，用户可以随时查看或修改该文件。

## 使用场景

当用户需要使用 Python 处理表格数据时，可以使用该工具。该工具能够执行 DataFrame 操作、数据清洗、数据聚合、数据合并、数据透视以及数据导出等功能。

## 架构

数据存储在 `~/pandas/` 目录下。具体数据结构请参考 `memory-template.md` 文件。

```
~/pandas/
├── memory.md     # User preferences and common patterns
└── snippets/     # Saved code patterns (optional)
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 数据存储模板 | `memory-template.md` |

## 核心规则

### 1. 使用向量化操作
- **严禁** 使用 `for` 循环遍历 DataFrame 的每一行
- **仅在不存在向量化替代方法时** 使用 `.apply()` 方法
- **优先选择 `df['col'].str.method()` 而不是 `apply(lambda x: x.method())`  

### 2. 通过链式方法提升代码可读性
```python
# Good: method chaining
result = (df
    .query('age > 30')
    .groupby('city')
    .agg({'salary': 'mean'})
    .reset_index())

# Bad: intermediate variables everywhere
filtered = df[df['age'] > 30]
grouped = filtered.groupby('city')
result = grouped.agg({'salary': 'mean'}).reset_index()
```

### 3. 明确处理缺失数据
- 在进行分析之前，务必检查 `df.isna().sum()` 的结果
- 选择合适的处理策略：`dropna()`、`fillna()` 或数据插值
- 在删除缺失值之前，务必记录缺失值产生的原因

### 4. 对于重复出现的字符串，使用分类数据类型（Categorical）
```python
# Memory savings for columns with few unique values
df['status'] = df['status'].astype('category')
df['country'] = df['country'].astype('category')
```

### 5. 在合并数据时进行验证
```python
# Always specify how and validate
result = pd.merge(
    df1, df2,
    on='id',
    how='left',
    validate='m:1'  # Many-to-one: catch unexpected duplicates
)
```

### 6. 对于复杂的过滤条件，优先使用 `query()` 方法
```python
# Readable
df.query('age > 30 and city == "NYC" and salary < 100000')

# Hard to read
df[(df['age'] > 30) & (df['city'] == 'NYC') & (df['salary'] < 100000)]
```

### 7. 在适当的情况下设置索引
```python
# Faster lookups, cleaner merges
df = df.set_index('user_id')
user_data = df.loc[12345]  # O(1) lookup
```

## 常见错误与注意事项

- **设置警告（SettingWithCopyWarning）**：使用 `.loc[]` 进行数据赋值，例如：`df.loc[mask, 'col'] = value`
- **循环效率低下**：将 `iterrows()` 替换为向量化操作或 `.apply()` 方法
- **内存溢出**：在读取 CSV 文件时指定数据类型，例如：`pd.read_csv(f, dtype={'id': 'int32')`
- **数据丢失**：在合并数据前后检查数据集的行数，例如：`print(f"合并前：{len(df1)}, 合并后：{len(result)})`
- **索引混乱**：在 `groupby()` 操作后使用 `reset_index()` 以获得清晰的 DataFrame 结构
- **链式索引操作**：`df['a']['b']` 可能会无声地失败，应使用 `df.loc[:, ['a', 'b']]` 来获取数据

## 安全性与隐私

**数据存储**：
- 用户偏好设置存储在 `~/pandas/memory.md` 文件中
- 所有 DataFrame 操作均在本地执行
- 无数据会被发送到外部

**该工具不执行以下操作：**
- 无数据上传至任何外部服务
- 无权限访问 `~/pandas/` 目录之外的文件
- 未经明确指示，不会修改原始数据文件

**用户控制**：
- 可以查看存储的偏好设置：`cat ~/pandas/memory.md`
- 可以清除所有数据：`rm -rf ~/pandas/`

## 相关技能

如果用户需要，可以通过 `clawhub install <slug>` 安装以下相关工具：
- `data-analysis`：通用数据分析工具
- `csv`：CSV 文件处理工具
- `sql`：数据库查询工具
- `excel-xlsx`：Excel 文件操作工具

## 反馈建议

- 如果该工具对你有帮助，请在 ClawHub 上给它打星（star）：`clawhub star pandas`
- 保持工具的最新状态：`clawhub sync`