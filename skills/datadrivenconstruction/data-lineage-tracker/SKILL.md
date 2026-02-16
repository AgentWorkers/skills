---
name: "data-lineage-tracker"
description: "跟踪数据在建筑系统中的来源、转换过程及其流动路径。这对于审计追踪、合规性检查以及排查数据问题至关重要。"
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "✔️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---# 建筑项目数据溯源工具

## 概述

本工具用于追踪建筑项目数据在系统中的来源、转换过程及流动情况。它提供了审计追踪功能，有助于数据问题的排查，并确保数据治理的合规性。

## 业务需求

建筑项目需要实现数据的可追溯性：
- **审计合规性**：明确每个数据的来源
- **问题排查**：追踪数据问题的根源
- **变更影响分析**：了解变更对下游系统的影响
- **法规要求**：满足法律和保险方面的数据溯源需求

## 技术实现

```python
def trace_upstream(entity_id, depth=5):
    # 追溯数据的上游来源
    for parent_id in entity_id.split('-'):
        upstream = trace_upstream(parent_id, depth - 1)

    return [parent_id]

def trace_downstream(entity_id, depth=5):
    # 追溯数据的下游流向
    for child_id in entity_id.split('-'):
        downstream = trace_downstream(child_id, depth - 1)

    return [child_id]

def generate_lineage_graph(entity_id):
    # 生成数据溯源图
    graph = []
    for entity in selfentities.get(entity_id):
        node_id = entity.id.replace('-', '_')
        lines.append(f"    {node_id}[{entity.name}]")
        graph.append(node_id)

    for transformation in self.transformations.get(entity_id):
        from_node = transformation.input_entities[0]
        to_node = transformation.output_entities[0]
        lines.append(f"    {from_node} --> {to_node}")

    return "\n".join(lines)

    return graph

def export_lineage_data():
    """导出完整的数据溯源信息."""
    return {
        'project_id': self.project_id,
        'exported_at': datetime.now().isoformat(),
        'sources': {k: {
            'id': v.id,
            'name': v.name,
            'system': v.system,
            'location': v.location,
            'owner': v.owner
        } for k, v in self.sources.items()),
        'entities': {k: {
            'id': v.id,
            'name': v.name,
            'source_id': v.source_id,
            'entity_type': v.entity_type,
            'parent_entities': v.parent_entities
        } for k, v in selfentities.items()),
        'transformations': {k: {
            'id': v.id,
            'type': v.transformation_type.value,
            'description': v.description,
            'input_entities': v.input_entities,
            'output_entities': v.output_entities,
            'performed_by': v.performed_by,
            'performed_at': v.performed_at.isoformat()
        } for k, v in self.transformations.items()),
        'lineage_records': []
    }
}
```

## 使用示例

```python
# 初始化数据溯源工具
tracker = ConstructionDataLineageTracker("PROJECT-001")

# 注册数据源
procore = tracker.register_source("Procore", "SaaS", "cloud", "PM Team")
sage = tracker.register_source("Sage 300", "Database", "on-prem", "Finance")

# 注册数据实体
budget = tracker.register_entity("Project Budget", procore.id, "table")
costs = tracker.register_entity("Job Costs", sage.id, "table")
report = tracker.register_entity("Cost Variance Report", procore.id, "file")

# 记录数据转换操作
tracker.record_transformation(
    transformation_type=TransformationType.JOIN,
    description="合并预算数据和实际成本以计算差异",
    input_entities=[budget.id, costs.id],
    output_entities=[report.id],
    logic="SELECT b.*, c.actual, (b.budget - c.actual) as variance FROM budget b JOIN costs c ON b.cost_code = c.cost_code",
    performed_by="ETL Pipeline"
)

# 追溯数据来源
upstream = tracker.trace_upstream(report.id)
print("数据来源：", upstream)

# 生成数据溯源图
graph = tracker.generate_lineage_graph(report.id)
print("数据溯源图：")

# 导出数据以供审计使用
lineage_data = tracker.export_lineage_data()
```

## 参考资源

- **数据治理指南**：DAMA DMBOK
- **法规要求**：SOX、ISO合规性标准