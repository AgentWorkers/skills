---
name: grafana-lens
description: "Grafana 是一款用于数据可视化、监控、警报和安全管理的工具。它提供了以下功能：  
- grafana_query：用于执行数据查询  
- grafana_query_logs：用于查询日志记录  
- grafana_query_traces：用于查询追踪信息  
- grafana_create_dashboard：用于创建新的仪表板  
- grafana_update_dashboard：用于更新现有仪表板  
- grafana_create_alert：用于创建警报规则  
- grafana_share_dashboard：用于共享仪表板  
- grafana_annotate：用于为数据添加注释  
- grafana_exploredatasources：用于探索数据源  
- grafana_list_metrics：用于列出所有可用的指标  
- grafana_search：用于搜索数据或指标  
- grafana_get_dashboard：用于获取仪表板信息  
- grafana_check_alerts：用于检查警报状态  
- grafana_push_metrics：用于将数据推送到 Grafana 进行可视化  
- grafana_explain_metric：用于解释特定指标的含义  
- grafana_security_check：用于进行安全检查  
这些功能可以用于满足各种需求，例如：  
- 根据用户请求查询特定指标或仪表板的数据  
- 监控系统性能和错误日志  
- 设置警报规则以及时通知异常情况  
- 分析成本和资源使用情况  
- 使用 PromQL、Prometheus、LogQL 等语言处理数据  
- 查看和分析日志信息  
- 发现并调试性能问题  
- 共享仪表板和图表  
- 推送自定义数据（如日历数据、Git 仓库数据等）到 Grafana 进行可视化  
- 回填历史数据并添加时间戳  
- 修改仪表板的布局和设置  
- 分析指标趋势和变化  
- 进行安全审计和威胁检测  
当需要查询相关数据、监控系统状态、设置警报或进行其他与 Grafana 相关的操作时，可以使用这些工具。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔭",
        "requires": { "config": ["grafana.url", "grafana.apiKey"] },
      },
  }
---
# Grafana Lens

您可以使用Grafana Lens的所有原生功能：查询数据、创建仪表板、设置警报、接收警报通知、标注事件、探索数据源、推送自定义数据，并直接展示可视化结果。Grafana Lens支持Grafana中的任何数据类型，而不仅仅是代理指标。