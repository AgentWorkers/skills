---
name: solo-cli
description: 通过 CLI 或 TUI 监控并操作 SOLO.ro 会计平台（包括汇总信息、收入、支出、待处理任务、电子发票以及公司相关数据）。当用户需要查看其会计数据、发票、支出或电子发票文件时，可以使用这些工具；同时，也可以将这些需求转换为安全的 `solo-cli` 命令来执行相应的操作。
---

# SOLO CLI

## 概述
使用 `solo-cli` 通过命令行界面或交互式 TUI 访问 SOLO.ro 财务平台的数据。

## 安装
如果 `solo-cli` 命令不可用，请通过 Homebrew 进行安装：
```bash
brew install rursache/tap/solo-cli
```

## 默认设置与安全性
- 配置文件位置：`~/.config/solo-cli/config.json`（首次运行时创建）
- 使用 `--config` 或 `-c` 指定自定义配置文件路径
- 凭据存储在本地；永远不会作为命令参数传递
- 会话 cookie 会被缓存到 `~/.config/solo-cli/cookies.json` 中，以便后续登录更快

## 快速入门
- 配置：编辑 `~/.config/solo-cli/config.json` 文件，设置用户名和密码
- 查看账户概要：`solo-cli summary`
- 查看年度概要：`solo-cli summary 2025`
- 查看收入：`solo-cli revenues`
- 查看支出：`solo-cli expenses`
- 查看待处理任务：`solo-cli queue`
- 生成电子发票：`solo-cli efactura`
- 查看公司信息：`solo-cli company`
- 上传文件：`solo-cli upload file.pdf`
- 删除待处理任务：`solo-cli queue delete <ID>`
- 启动 TUI：`solo-cli`（不带参数）
- 运行演示模式：`solo-cli demo`

## 配置
配置文件结构：
```json
{
  "username": "your_email@solo.ro",
  "password": "your_password",
  "company_id": "12345",
  "page_size": 100,
  "user_agent": "Mozilla/5.0 ..."
}
```

| 字段 | 是否必填 | 描述 |
|-------|----------|-------------|
| username | 是 | SOLO.ro 的登录邮箱 |
| password | 是 | SOLO.ro 的密码 |
| company_id | 否 | 用于显示公司信息的公司 ID（可在 /settings#!/company 的“网络”标签页中找到） |
| page_size | 否 | 每页显示的条目数量（默认：100） |
| user_agent | 否 | 自定义的 HTTP 用户代理字符串 |

## 命令

### `summary [year]`
查看一年的账户概要。
```bash
solo-cli summary          # Current year
solo-cli summary 2025     # Specific year
```
输出：年份、收入、支出、税款

### `revenues`
列出所有收入发票。
```bash
solo-cli revenues
solo-cli rev              # Alias
```
输出：发票代码、金额、货币、支付状态、客户名称

### `expenses`
列出所有支出记录。
```bash
solo-cli expenses
solo-cli exp              # Alias
```
输出：金额、货币、支出类别、供应商名称

### `queue`
列出待处理的支出任务或删除它们。
```bash
solo-cli queue            # List queue
solo-cli q                # Alias
solo-cli queue delete 123 # Delete item by ID
solo-cli q del 123        # Alias
```
输出：任务名称、待处理天数、逾期状态（包含任务 ID）

### `efactura`
列出所有电子发票记录。
```bash
solo-cli efactura
solo-cli ei               # Alias
```
输出：序列号、金额、货币、日期、收方名称

### `company`
查看公司信息。
```bash
solo-cli company
```
输出：公司名称、CUI（公司唯一标识符）、注册号码、地址

### `upload <file>`
上传支出文件（PDF 或图片）。
```bash
solo-cli upload invoice.pdf
solo-cli up invoice.pdf   # Alias
```
输出：上传状态和确认信息

### `demo`
使用模拟数据启动 TUI 模式（用于截图或测试，不进行 API 调用）。
```bash
solo-cli demo
```

### `tui`
启动交互式 TUI 模式（未输入命令时默认使用）。
```bash
solo-cli tui
solo-cli                  # Same as above
```

## 全局选项
| 选项 | 简写 | 描述 |
|--------|-------|-------------|
| --config | -c | 自定义配置文件的路径 |
| --help | -h | 显示帮助信息 |
| --version | -v | 显示版本信息 |

## 示例
```bash
# Basic usage
solo-cli summary
solo-cli revenues

# Custom config
solo-cli -c ~/work-config.json summary

# Pipe to grep
solo-cli expenses | grep -i "food"

# View specific year
solo-cli summary 2024

# Upload a document
solo-cli upload invoice.pdf

# Delete a queued item
solo-cli queue delete 123456
```

## 认证流程
1. 启动时，从 `~/.config/solo-cli/cookies.json` 中加载 cookie
2. 通过测试 API 调用验证 cookie 的有效性
3. 如果有效，则使用缓存的会话信息
4. 如果 cookie 无效或缺失，则使用配置文件中的凭据登录
5. 为下一次会话保存新的 cookie

## 故障排除
- **“凭证缺失”**：在 `config.json` 中填写正确的 SOLO.ro 用户名和密码
- **“认证失败”**：检查凭证是否正确
- **“配置文件中的 JSON 格式错误”**：修复 `config.json` 中的语法错误
- **公司信息未显示**：在配置文件中添加 `company_id`（可选字段）