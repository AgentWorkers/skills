# 人员关系管理技能（People-Relationship Management Skill）

## 概述

该技能提供了一种基于图的数据存储解决方案，使用 SQLite 数据库进行持久化存储。它使 AI 代理能够创建、管理和查询人员及其之间的关系，非常适合用于构建个人客户关系管理（CRM）系统、组织结构图、导师关系网络以及协作关系映射。

## 功能

### 人员管理
- **创建人员**：添加包含详细信息（姓名、角色、关系、所属组织、性格特征、备注）的新人员。
- **读取人员信息**：检索特定人员信息或在数据库中搜索/过滤人员。
- **更新人员信息**：修改任何人员的信息。
- **删除人员**：从数据库中删除人员（相关关系也会被删除）。
- **搜索**：按姓名、角色或组织进行全文搜索。
- **过滤**：按组织或关系类型进行过滤。

### 关系管理
- **创建关系**：在人员之间建立有向关系。
- **查询关系**：获取某人的所有 incoming（进入关系）、outgoing（传出关系）或所有关系。
- **更新关系**：修改关系类型和描述。
- **删除关系**：删除特定的关系。
- **双向支持**：跟踪关系的双向性。

### 图操作
- **导出整个图**：将整个关系网络导出为 JSON 格式（包含节点和边）。
- **查看个人关系网络**：获取某人的完整关系网络视图。
- **支持自定义关系类型**：如 `reports_to`（下属向上级汇报）、`manages`（上级管理下属）等。

## 数据库架构

### 表结构

**people**
- `id`：整数类型，主键
- `name`：文本类型，非空
- `role`：文本类型
- `relation_to_me`：文本类型
- `organization`：文本类型
- `character`：文本类型
- `notes`：文本类型
- `created_at`：时间戳类型
- `updated_at`：时间戳类型

**edges**
- `id`：整数类型，主键
- `from_person_id`：整数类型（外键，引用 `people` 表的 `id`）
- `to_person_id`：整数类型（外键，引用 `people` 表的 `id`）
- `relationship_type`：文本类型，非空
- `description`：文本类型
- `created_at`：时间戳类型
- `updated_at`：时间戳类型
- `from_person_id` 和 `to_person_id` 上有唯一性约束

### 索引
- `idx_people_name`：针对 `people.name` 的索引
- `idx_edges_from`：针对 `edges.from_person_id` 的索引
- `idx_edges_to`：针对 `edges.to_person_id` 的索引

## 使用示例

### 命令行界面

```bash
# Person operations
python people_skill.py add-person "Jane Doe" --role "CTO" --org "StartupXYZ" --relation "Mentor"
python people_skill.py get-person 1
python people_skill.py search "engineer"
python people_skill.py list-people --org "StartupXYZ"
python people_skill.py update-person 1 --notes "Coffee meeting scheduled"
python people_skill.py delete-person 1

# Relationship operations
python people_skill.py add-relationship 1 2 "mentors" --description "Tech career guidance"
python people_skill.py get-relationships 1
python people_skill.py list-relationships
python people_skill.py update-relationship 1 --type "coaches"
python people_skill.py delete-relationship 1

# Graph operations
python people_skill.py get-graph
python people_skill.py get-network 1
```

### Python API

```python
from database import PeopleDatabase
from people_skill import PeopleAgent

# Initialize
agent = PeopleAgent("people.db")

# Add people
result = agent.add_person(
    name="Alice Johnson",
    role="VP Engineering",
    relation_to_me="Former colleague",
    organization="TechCorp",
    character="Strategic thinker, empathetic leader",
    notes="Worked together 2020-2022"
)
person_id = result["person_id"]

# Add relationship
agent.add_relationship(
    from_person_id=1,
    to_person_id=2,
    relationship_type="manages",
    description="Direct manager relationship"
)

# Query network
network = agent.get_person_network(person_id)
print(f"Found {network['connections_count']} connections")

# Export graph
graph = agent.get_graph()
print(f"Graph: {graph['nodes_count']} nodes, {graph['edges_count']} edges")
```

## 常见的关系类型

- `reports_to`：层级汇报关系（下属向上级汇报）
- `manages`：层级管理关系（上级管理下属）
- `works_with`：同事协作关系
- `mentors`：导师关系（导师与被指导者）
- `mentored_by`：反向导师关系（被指导者与导师）
- `friends_with`：个人友谊关系
- `knows`：泛泛之交关系
- `collaborates_with`：项目协作关系
- `introduced_by`：关系建立者

## 使用场景

### 1. 个人客户关系管理（Personal CRM）
- 跟踪专业联系人、他们的角色、所属组织以及认识他们的途径。
- 添加关于对话、会议或后续行动的备注。

```bash
python people_skill.py add-person "Sarah Chen" \
  --role "Product Director" \
  --org "InnovateCo" \
  --relation "Met at conference" \
  --notes "Interested in API collaboration, follow up Q2"
```

### 2. 组织结构图构建
- 构建和维护包含汇报关系的组织结构图。

```bash
# Add team members
python people_skill.py add-person "Mike Lead" --role "Team Lead" --org "Engineering"
python people_skill.py add-person "Dev One" --role "Engineer" --org "Engineering"
python people_skill.py add-person "Dev Two" --role "Engineer" --org "Engineering"

# Create reporting structure
python people_skill.py add-relationship 2 1 "reports_to"
python people_skill.py add-relationship 3 1 "reports_to"
```

### 3. 导师关系网络
- 跟踪导师关系和职业指导联系。

```bash
python people_skill.py add-relationship 5 3 "mentors" \
  --description "Career guidance in ML/AI"
```

### 4. 协作关系追踪
- 映射项目中的人员协作关系。

```bash
python people_skill.py add-relationship 1 2 "works_with" \
  --description "Project Phoenix collaboration"
```

### 5. 网络分析
- 分析你的职业网络，识别关键联系人。

```bash
# View someone's complete network
python people_skill.py get-network 1

# Export for visualization
python people_skill.py get-graph > network.json
```

## 高级功能

### 双向关系查询
- 系统自动处理关系的双向性。

### 级联删除
- 删除人员时，系统会自动删除所有相关关系。

### 避免重复
- 唯一性约束确保同一人员之间不会存在重复的关系。

### 搜索灵活性
- 可在多个字段上进行搜索。

## 集成示例

### 导出到可视化工具
- 将数据导出到可视化工具中。

### 从 CSV 文件导入数据
- 从 CSV 文件导入人员信息。

## 最佳实践

- **统一命名规范**：使用一致的命名规则来表示关系类型。
- **添加详细备注**：记录重要信息。
- **定期更新**：使用更新命令保持数据最新。
- **记录性格特征**：使用 `character` 字段记录人员的性格特点。
- **明确关系描述**：为关系添加描述以增加清晰度。
- **先搜索再添加**：在添加新人员之前先进行搜索，以避免重复。

## API 参考

请参阅 [people_skill.py](people_skill.py) 以获取完整的 API 文档。

### 关键类
- `PeopleDatabase`：负责底层数据库操作。
- `PeopleAgent`：提供高级接口，返回结果字典。

### 返回格式
所有代理方法返回的字典包含：
- `success`：布尔值，表示操作是否成功。
- `message`：人类可读的状态信息（在出错时提供）。
- 与操作相关的具体数据字段。

## 错误处理
- 该技能包含全面的错误处理机制：
  - 外键约束确保关系的有效性。
  - 唯一性约束防止关系重复。
  - 级联删除机制维护数据的引用完整性。
  - 命令行界面中的异常处理块提供用户友好的错误信息。

## 性能
- 使用索引实现快速查询。
- 高效处理图结构的数据遍历。
- 适用于包含数千人员的大型网络。
- SQLite 支持并发读操作。

## 未来改进方向
- 可能的扩展功能：
  - 图形化展示关系网络。
  - 查找人员之间的最短路径。
  - 计算人员的影响力/中心性。
  - 检测重复人员。
  - 支持多种格式的导出（如 GraphML、DOT）。
  - 从 LinkedIn 或联系人列表导入数据。
  - 基于时间的关联关系追踪。
  - 为关系计算信任度/影响力得分。

## 许可证
- MIT 许可证。