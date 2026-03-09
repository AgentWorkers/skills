---
name: arccos-golf
license: MIT
description: 分析 Arccos Golf 的性能数据，包括球杆的击球距离、节省的击球次数（stroke gains）、得分模式以及每轮的比赛表现。当用户询问高尔夫统计数据、球杆推荐、性能趋势，或希望获取来自其 Arccos Golf 传感器的详细分析时，可使用此功能。
---
# Arccos高尔夫性能分析器

该工具从Arccos高尔夫API获取实时数据，并生成性能分析报告，包括节省的击球次数、球杆使用距离、得分情况、推杆表现以及最近几轮的比赛数据。

## ⚠️ 隐私与安全声明

此工具会使用您的账户凭据向Arccos高尔夫API服务器发起认证后的网络请求：

- **凭据**：您的Arccos邮箱地址和密码将用于身份验证。会话令牌会缓存到`~/.arccos_creds.json`文件中（权限设置为0600，仅您本人可读取）。
- **网络连接**：脚本会访问`authentication.arccosgolf.com`（用于登录）和`api.arccosgolf.com`（用于获取数据），不会访问其他任何端点。
- **数据传输**：除了获取您个人高尔夫数据所需的API请求外，没有任何数据会离开您的设备。
- **外部依赖**：需要`arccos`库（来自`github.com/pfrederiksen/arccos-api`，采用MIT许可证，由发布此工具的开发者开发）。

如果您对此有疑虑，请在安装前查看`arccos`库的源代码：<https://github.com/pfrederiksen/arccos-api>

## 先决条件

```bash
# 1. Install the arccos library
git clone https://github.com/pfrederiksen/arccos-api
pip install -e arccos-api/

# 2. Authenticate — opens a prompt for email + password
#    Credentials cached to ~/.arccos_creds.json (0600)
arccos login
```

或者，您也可以在运行时直接传递凭据（详见下方使用说明）。

## 使用方法

### 生成完整报告（使用缓存的凭据）
```bash
python3 scripts/arccos_golf.py
```

### 显式传递凭据（无需缓存凭据）
```bash
python3 scripts/arccos_golf.py --email you@example.com --password secret
```

### 查看特定数据
```bash
python3 scripts/arccos_golf.py --summary
python3 scripts/arccos_golf.py --strokes-gained
python3 scripts/arccos_golf.py --clubs           # all clubs
python3 scripts/arccos_golf.py --clubs iron       # filter by type
python3 scripts/arccos_golf.py --pace
python3 scripts/arccos_golf.py --recent-rounds 10
```

### 输出格式（JSON）
```bash
python3 scripts/arccos_golf.py --format json
```

### 离线使用（无需凭据，使用缓存的JSON文件）
```bash
python3 scripts/arccos_golf.py --file /path/to/arccos-data.json
```

## 系统资源访问权限

| 资源 | 详细信息 |
|----------|---------|
| **网络** | `authentication.arccosgolf.com` — 用于登录/刷新令牌 |
| **网络** | `api.arccosgolf.com` — 获取比赛数据、差点信息、球杆信息及球场详情 |
| **文件读取** | `~/.arccos_creds.json` — 用于读取缓存的会话令牌（由`arccos`登录功能生成） |
| **文件读取** | 可选参数`--file`：指定用于离线分析的JSON文件路径 |
| **文件写入** | `~/.arccos_creds.json` — 在令牌更新时更新该文件 |
| **子进程** | 无 |
| **Shell命令执行** | 无 |

## 发起的API请求

| 数据类型 | 请求端点 |
|------|----------|
| 获取比赛记录 | `GET /users/{userId}/rounds` |
| 获取球场名称 | `GET /courses/{courseId}` |
| 获取差点信息 | `GET /users/{userId}/handicaps/latest` |
| 获取球杆使用距离 | `GET /v4/clubs/user/{userId}/smart-distances` |
| 获取节省的击球次数 | `GET /v2/sga/shots/{roundIds}` |

所有API请求均使用Bearer JWT进行身份验证。JWT令牌是从`authentication.arccosgolf.com`获取并更新的，且需要使用您的Arccos账户凭据。

## 所需依赖库

- Python ≥ 3.11
- `arccos`库：`github.com/pfrederiksen/arccos-api`（MIT许可证）——该库基于`requests`、`click`和`rich`库实现 |
- 分析脚本本身仅依赖标准Python库