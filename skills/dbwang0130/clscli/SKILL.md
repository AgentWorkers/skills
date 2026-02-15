---
name: clscli
description: 查询和分析腾讯云 CLS 日志
homepage: https://github.com/
metadata:
    {"requires": {"bin": ["clscli"], "env": ["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"]}}
---

# CLS 技能

查询和分析腾讯云 CLS 日志。

## 设置
1. 安装 clscli（使用 Homebrew）：
    ```bash
    brew tap dbwang0130/clscli
    brew install dbwang0130/clscli/clscli
    ```
2. 获取凭证和区域列表：https://cloud.tencent.com/document/api/614/56474
3. 设置环境变量（与腾讯云 API 的通用参数相同）：
    ```bash
    export TENCENTCLOUD_SECRET_ID="your-secret-id"
    export TENCENTCLOUD_SECRET_KEY="your-secret-key"
    ```
4. 通过 `--region` 指定区域（例如：ap-guangzhou）。

## 使用方法

**重要提示：** 如果您不知道日志的主题，请先列出所有日志主题。

### 列出日志主题
列出某个区域内的所有日志主题，以确定用于查询或上下文的 `--region` 和主题 ID。

```bash
clscli topics --region <region> [--topic-name name] [--logset-name name] [--logset-id id] [--limit 20] [--offset 0]
```
示例：`--output=json`，`--output=csv`，`-o topics.csv`

| 选项 | 是否必填 | 描述 |
|--------|----------|-------------|
| --region | 是 | CLS 区域，例如：ap-guangzhou |
| --topic-name | 否 | 按主题名称过滤（模糊匹配） |
| --logset-name | 否 | 按日志集名称过滤（模糊匹配） |
| --logset-id | 否 | 按日志集 ID 过滤 |
| --limit | 否 | 每页显示的记录数，默认为 20，最大为 100 |
| --offset | 否 | 分页偏移量，默认为 0 |
| --output, -o | 否 | 输出格式：json、csv 或文件路径 |

输出列：Region（区域）、TopicId（主题 ID）、TopicName（主题名称）、LogsetId（日志集 ID）、CreateTime（创建时间）、StorageType（存储类型）。

### 根据查询获取日志
```bash
clscli query -q "[query condition] | [SQL statement]" --region <region> -t <TopicId> --last 1h
```
示例：
- 时间范围：`--last 1h`，`--last 30m`；或 `--from`/`--to`（Unix 时间戳，单位为毫秒）
- 多个主题：`--topics <id1>,<id2>` 或 `--t <id>`（多个主题 ID）
- 自动分页：`--max 5000`（分页显示最多 5000 条日志，或使用 `ListOver` 命令）
- 输出格式：`--output=json`，`--output=csv`，`-o result.json`（将结果写入文件）

| 选项 | 是否必填 | 描述 |
|--------|----------|-------------|
| --region | 是 | CLS 区域，例如：ap-guangzhou |
| -q, --query | 是 | 查询条件或 SQL 语句，例如：`level:ERROR` 或 `* \| select count(*) as cnt` |
| -t, --topic | 是 | 单个日志主题 ID |
| --topics | 是 | 逗号分隔的主题 ID，最多 50 个 |
| --last | 是 | 时间范围，例如：1h、30m、24h |
| --from, --to | 是 | 开始/结束时间（Unix 时间戳，单位为毫秒） |
| --limit | 否 | 每次请求返回的日志数量，默认为 100，最大为 1000 |
| --max | 否 | 最大日志数量；如果指定非零值，将自动分页显示相应数量的日志或使用 `ListOver` 命令 |
| --output, -o | 否 | 输出格式：json、csv 或文件路径 |
| --sort | 否 | 排序方式：asc 或 desc，默认为 desc |

#### 查询条件语法

支持两种语法：
- **CQL**（CLS 查询语言）：专为 CLS 日志设计的查询语法，易于使用，推荐使用。
- **Lucene**：开源的 Lucene 查询语法；不适用于日志搜索，对特殊字符、大小写和通配符有更多限制，不推荐使用。

##### CQL 语法
| 语法 | 描述 |
|--------|-------------|
| `key:value` | 关键值搜索；查找字段（key）包含值的所有日志，例如：`level:ERROR` |
| `value` | 全文搜索；查找包含特定值的日志，例如：`ERROR` |
| `AND` | 逻辑 AND，不区分大小写，例如：`level:ERROR AND pid:1234` |
| `OR` | 逻辑 OR，不区分大小写，例如：`level:ERROR OR level:WARNING`，`level:(ERROR OR WARNING)` |
| `NOT` | 逻辑 NOT，不区分大小写，例如：`level:ERROR NOT pid:1234`，`level:ERROR AND NOT pid:1234` |
| `()` | 用于指定查询优先级，例如：`level:(ERROR OR WARNING) AND pid:1234`。**注意：在没有括号的情况下，AND 的优先级高于 OR** |
| `"  "` | 短语搜索；使用双引号包围字符串，单词和顺序必须匹配，例如：`name:"john Smith"`。短语内不能使用逻辑运算符。 |
| `'  '` | 短语搜索；使用单引号，当短语包含双引号时使用，例如：`body:'user_name:"bob"'` |
| `*` | 通配符；表示零个或多个字符，例如：`host:www.test*.com`。不能使用前缀通配符。 |
| `>`, `>=`, `<`, `<=`, `=` | 数值范围的比较运算符，例如：`status>400`，`status:>=400` |
| `\` | 转义符；用于转义特殊字符（如空格、`:`, `()`, `>`, `=`, `<`, `"`, `'`, `*`）。 |
| `key:*` | 检查字段是否存在（任意值）；`long/double`：字段存在且为数值类型，例如：`response_time:*` |
| `key:""` | 检查字段是否存在且为空；`long/double`：字段值为空或不存在，例如：`response_time:""` |

#### SQL 语句语法
| 语法 | 描述 |
|--------|-------------|
| SELECT | 从表中选择数据；返回符合查询条件的日志 |
| AS | 为列指定别名 |
| GROUP BY | 使用聚合函数，按一个或多个列进行分组 |
| ORDER BY | 按指定列对结果进行排序 |
| LIMIT | 限制返回的行数，默认为 100，最大为 1000 |
| WHERE | 对原始数据进行过滤 |
| HAVING | 在 `GROUP BY` 之后、`ORDER BY` 之前进行过滤；`WHERE` 用于过滤原始数据 |
| 嵌套子查询 | 在一个 SQL 语句中嵌套另一个 SQL 语句，用于多步骤分析 |
| SQL 函数 | 提供更多高级功能：IP 地理信息、时间格式转换、字符串分割/合并、JSON 提取、数学运算、去重计数等 |

### 获取日志上下文
检索给定日志周围的上下文信息。

```bash
clscli context <PkgId> <PkgLogId> --region <region> -t <TopicId>
```
示例：`--output=json`，`--output=csv`，`-o context.json`（将结果写入文件）

| 选项 | 是否必填 | 类型 | 描述 | 示例 |
|--------|----------|------|-------------|---------|
| --region | 是 | 字符串 | CLS 区域 | ap-guangzhou |
| -t, --topic | 是 | 字符串 | 日志主题 ID | - |
| PkgId | 是 | 字符串 | 日志包 ID（例如：SearchLog Results[].PkgId） | 528C1318606EFEB8-1A7 |
| PkgLogId | 是 | 整数 | 日志包内的索引（例如：SearchLog Results[].PkgLogId） | 65536 |
| --output, -o | 否 | - | 输出格式：json、csv 或文件路径 | - |