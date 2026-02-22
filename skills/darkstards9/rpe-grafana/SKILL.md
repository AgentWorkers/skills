---
name: rpe-grafana
description: "**从 Grafana 仪表板中读取当前值，而无需了解底层的查询语句。**  
**适用场景：** 当被询问 Grafana 仪表板中显示的数值（如传感器读数、指标数据、统计信息）时。  
**操作方式：** 通过仪表板和面板的名称进行导航，无需使用 PromQL 或 SQL 语句。  
**不适用场景：** 用于向 Grafana 写入数据、执行管理操作或直接执行原始查询语句。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "env": ["GRAFANA_URL", "GRAFANA_USER", "GRAFANA_PASSWORD"] },
        "install":
          [
            {
              "id": "config",
              "kind": "config",
              "label": "Configure Grafana credentials in openclaw.json",
            },
          ],
      },
  }
---
# Grafana 技能

无需编写查询语句，即可从任何 Grafana 仪表板中读取当前值。该插件通过仪表板和面板名称进行导航，提取面板的现有查询配置，并返回一个简洁的摘要——无需了解 PromQL、SQL 或数据源的相关知识。

支持与任何 Grafana 数据源（Prometheus、InfluxDB、MySQL 等）配合使用。

## 适用场景

✅ **在以下情况下使用此技能：**
- 当被问及某个在 Grafana 仪表板中可见的值时
- 列出可用的仪表板或面板
- 根据面板名称检索指标的当前值或最近值

## 不适用场景

❌ **请勿在以下情况下使用此技能：**
- 编写、修改或创建仪表板 → 使用 Grafana 用户界面
- 进行管理操作（用户管理、数据源配置、警报设置） → 直接使用 Grafana API
- 需要运行没有对应面板的自定义查询

## 设置方法

将以下代码添加到您的 `openclaw.json` 文件中：

```json
{
  "plugins": {
    "entries": {
      "rpe-grafana": {
        "enabled": true,
        "config": {
          "url": "http://your-grafana:3000",
          "user": "your-username",
          "password": "your-password"
        }
      }
    }
  }
}
```

或者设置环境变量：
- `GRAFANA_URL` - Grafana 的基础 URL
- `GRAFANA_USER` - 用户名
- `GRAFANA_PASSWORD` - 密码或 API 密钥

## 工具

### `grafana_list_dashboards`

列出所有可用的仪表板。

**参数：** 无

**返回值：`[{ uid, title }]`

### `grafana_list_panels`

列出某个仪表板中的所有面板。

**参数：**
- `dashboard_uid`（必需）- 来自 `grafana_list_dashboards` 的仪表板 UID

**返回值：`[{ id, title }]`

### `grafana_query_panel`

读取特定面板的当前数据。从仪表板中获取面板的查询配置，并通过 Grafana 的数据源 API 执行该查询——无需了解查询语言的相关知识。

**参数：**
- `dashboard_uid`（必需）- 仪表板 UID
- `panel_id`（必需）- 来自 `grafana_list_panels` 的面板 ID
- `from`（可选）- 时间范围的起始时间（默认：`now-1h`）
- `to`（可选）- 时间范围的结束时间（默认：`now`）

**返回值：`[{ refId, name, lastValue, unit }]`

## 典型工作流程

1. 使用 `grafana_list_dashboards` 查找仪表板 UID
2. 使用 `grafana_list_panels` 根据名称查找面板 ID
3. 使用 `grafana_query_panel` 获取当前值

## 注意事项

- 需要具有读取权限的 Grafana 用户（Viewer 角色即可）
- 仪表板 UID 是稳定的标识符；面板 ID 在同一仪表板内是唯一的
- 行式面板会自动扁平化显示