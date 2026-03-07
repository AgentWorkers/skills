---
name: grafana-lens
description: "Grafana 是一款用于数据可视化、监控、警报和安全管理的工具。它提供了以下功能：  
- grafana_query：用于执行数据查询  
- grafana_query_logs：用于查询日志记录  
- grafana_query_traces：用于查询追踪数据  
- grafana_create_dashboard：用于创建新的仪表板  
- grafana_update_dashboard：用于更新现有仪表板  
- grafana_create_alert：用于设置警报规则  
- grafana_share_dashboard：用于共享仪表板  
- grafana_annotate：用于在仪表板上添加注释  
- grafana_explore_datasources：用于探索数据源  
- grafana_list_metrics：用于列出所有可用的指标  
- grafana_search：用于搜索指标或仪表板  
- grafana_get_dashboard：用于获取仪表板信息  
- grafana_check_alerts：用于检查警报状态  
- grafana_push_metrics：用于将指标数据推送到 Grafana  
- grafana_explain_metric：用于解释指标的含义  
- grafana_security_check：用于进行安全检查  
这些功能可以帮助用户监控系统性能、分析数据、接收警报、管理成本、可视化数据，并确保系统的安全性。  
当用户需要查询指标、仪表板、监控数据、查看警报信息、了解成本消耗、使用令牌情况、执行数据可视化操作时，都可以使用相应的 Grafana 工具。此外，Grafana 还支持 PromQL、Prometheus、LogQL 等数据源，以及 Loki 和 Tempo 等日志管理系统。它还提供了丰富的工具来调试系统、共享图表、处理警报通知、推送自定义数据（如日历数据、Git 仓库数据等），并支持历史数据的回填和存储。用户还可以修改仪表板布局、添加或删除面板、调整时间范围等。"
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

您可以使用Grafana Lens的所有原生功能：查询数据、创建仪表板、设置警报、接收警报通知、标注事件、探索数据源、推送自定义数据，并直接展示可视化结果。Grafana Lens支持Grafana中的任何类型的数据，而不仅仅是代理指标。