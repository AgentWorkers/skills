---
name: ares-business-registry
description: 查询捷克ARES商业注册信息，支持按ICO代码或名称进行查询；支持人类可读的文本（human-readable text）、JSON格式或原始数据（raw data）两种输出方式；支持重试机制；同时支持对法律文件内容的解码（legal-form decoding）。
---
# ARES商业注册系统（捷克）

请使用`scripts/ares_client.py`来查询ICO信息并进行商业实体搜索。

## 工作目录

- 从工作区根目录开始：
  - `python3 skills/ares-business-registry/scripts/ares_client.py ...`
- 从`skills/ares-business-registry`目录开始：
  - `python3 scripts/ares_client.py ...`

## 命令

推荐通过以下方式运行脚本：
- `./ares ico <ico>`
- `./ares name "名称" [--nace 代码 ...] [--city 城市] [--limit 数量] [--offset 偏移量] [--pick 索引]`

该脚本还支持以下命令：
- `python3 scripts/ares_client.py search --name "名称" ...`
- `python3 scripts/ares_client.py search --nace 代码 [代码 ...] ...`
- `python3 scripts/ares_client.py search --name "名称" --nace 代码 ...`（同时使用名称和NACE代码进行搜索）

## 输出格式

- 默认格式：易于阅读的摘要
- `--json`：标准化JSON格式的输出（包含固定字段）
- `--raw`：原始的ARES数据格式

## 示例

```bash
# ICO lookup
python3 scripts/ares_client.py ico 27604977
python3 scripts/ares_client.py ico 27604977 --json
python3 scripts/ares_client.py ico 27604977 --raw

# Search by name
python3 scripts/ares_client.py search --name Google
python3 scripts/ares_client.py search --name Google --limit 3 --json
python3 scripts/ares_client.py search --name Google --city Praha --limit 10 --offset 0
python3 scripts/ares_client.py search --name Google --limit 3 --pick 1

# Search by NACE code (CZ-NACE, exactly 5 digits)
python3 scripts/ares_client.py search --nace 47710 --limit 10            # all clothing retailers
python3 scripts/ares_client.py search --nace 47710 --city Praha --json    # clothing retailers in Praha
python3 scripts/ares_client.py search --nace 47710 47910 --limit 5        # clothing retail + mail order

# Combined: name + NACE (AND filter)
python3 scripts/ares_client.py search --name sport --nace 47710 --json    # "sport" in clothing retail
```

## 标准化JSON格式的输出示例

- **ICO信息输出**：
  - `{ "subject": { "name": "ICO名称", "ico": "ICO文件路径", "dic": "数据创建日期", "address": "企业地址", "codes": "企业所属行业代码", "decoded": "解码后的数据" } }`
- **搜索结果输出**：
  - `{ "query": "搜索条件", "total": "搜索结果总数", "items": "匹配的实体数量", "picked?": "是否选择了特定实体?" }`
  - `query`字段包含：`name`（可选）、`city`（可选）、`nace`（可选的代码数组）、`limit`、`offset`
  - `dic`字段可能为空。
  - `datumVzniku`字段可能为空。

## 错误信息（仅适用于`--json`选项）

```json
{
  "error": {
    "code": "validation_error | ares_error | network_error",
    "message": "Human readable message",
    "status": 429,
    "details": {}
  }
}
```

## 验证规则与退出状态

- **ICO信息**：必须包含8位数字以及一个mod11校验和。
- **搜索请求**：至少需要提供`--name`（长度大于等于3个字符）或`--nace`参数；两者可以同时提供。
- **NACE代码**：每个代码必须为5位数字（符合CZ-NACE格式，例如`47710`）；允许多个代码（用空格分隔）。
- **`--limit`参数**：默认值为10，最大值为100。
- **`--offset`参数**：必须大于等于0。
- **退出状态码**：
  - `0`：操作成功
  - `1`：验证失败
  - `2`：ARES服务器返回错误响应
  - `3`：网络问题或超时

## 缓存与数据解码

- 企业法律形式数据（`PravniForma`）通过POST请求`/ciselniky-nazevniky/vyhledat`获取。
- 缓存文件路径：`skills/ares-business-registry/.cache/pravni_forma.json`
- 缓存有效期：24小时
- 如果缓存文件过期或不可用，系统会使用内存中的数据作为备用。
- 缓存中的代码对应关系如下：
  - `112`：s.r.o.（小型零售企业）
  - `121`：a.s.（有限责任公司）
  - `141`：z.s.（大型零售企业）
  - `701`：个体经营者（OSVČ）
  - `301`：股份有限公司（s.p.）
  - `331`：合伙企业（p.o.）

## NACE代码搜索

- 使用`--nace`参数时，系统会将`czNace`代码发送到ARES的过滤接口。
- 代码必须为5位数字（符合CZ-NACE_2025格式）；允许多个代码（用空格分隔），ARES会返回符合任意一个代码的实体。
- 当同时使用`--name`参数时，两个过滤条件会以AND逻辑进行匹配（实体必须同时满足名称和NACE代码的条件）。
- 仅使用`--nace`参数的搜索也是支持的，可用于浏览某一行业的所有企业。
- 常见的电子商务相关NACE代码示例：
  - `47710`：服装零售
  - `47910`：邮购或网上零售
  - `47410`：计算机和软件零售
  - `47750`：化妆品和卫生用品零售
  - `46420`：服装和鞋类批发
- 完整的CZ-NACE代码列表：https://www.czso.cz/csu/czso/klasifikace_ekonomickych_cinnosti_cz_nace

## 城市过滤限制

- `--city`参数用于匹配`sidlo.nazevObce`（结构化过滤条件）。
- ARES服务器仅进行尽力匹配；实际返回的记录可能不在指定的城市范围内。

## 重试机制与速率限制

- HTTP请求超时时间：连接5秒，读取数据20秒。
- 对于临时性的错误（如`429/502/503/504`状态码），系统会尝试重试。
- 重试间隔时间：1秒、2秒、4秒。
- 如果提供了`Retry-After`参数，系统会按照该参数进行重试。