---
name: open-ontologies
version: "0.5.1"
description: 使用39种以上的MCP工具进行AI原生的本体工程开发，这些工具基于内存中的Oxigraph三元组存储系统。通过“生成-验证-迭代”的循环来构建、验证、查询和管理RDF/OWL本体。该技术适用于构建本体、知识图谱、RDF数据、SPARQL查询、BORO/4D建模、SHACL验证、临床术语映射，以及采用Terraform风格的本体生命周期管理。
tags:
  - ontology
  - rdf
  - owl
  - sparql
  - knowledge-graph
  - semantic-web
  - mcp
  - oxigraph
  - shacl
  - boro
metadata:
  openclaw:
    requires:
      mcp:
        - name: open-ontologies
          description: >
            Oxigraph-backed MCP server providing all onto_* tools.
            Install: cargo install open-ontologies OR download binary from
            https://github.com/fabio-rovai/open-ontologies/releases
          config:
            command: open-ontologies
            args: ["serve"]
      bins:
        - open-ontologies
    network:
      - description: "onto_pull fetches ontologies from remote URLs or SPARQL endpoints (user-provided URLs only)"
        direction: outbound
        optional: true
      - description: "onto_push sends triples to a user-specified SPARQL endpoint"
        direction: outbound
        optional: true
    notes: >
      All processing is local by default. The in-memory Oxigraph triple store runs inside the
      MCP server process -- no database, no JVM, no external services required.
      Network access is only used by onto_pull and onto_push when the user explicitly provides
      a remote URL or SPARQL endpoint. onto_monitor alerts are logged locally to stdout;
      no external notification services are contacted. No credentials or API keys are needed
      for core functionality.
---
# 开放本体工程（Open Ontologies）

这是一种基于人工智能的本体工程方法，可以直接生成OWL/RDF格式的本体，使用MCP工具进行验证，并通过类似Terraform的生命周期管理框架进行迭代优化。

## 先决条件

使用该功能需要**Open Ontologies MCP服务器**，该服务器提供了`onto_*`系列工具。

**安装方式：** 使用`cargo install open-ontologies`命令进行安装，或从[GitHub仓库](https://github.com/fabio-rovai/open-ontologies/releases)下载最新版本。

**MCP配置**（需添加到`.mcp.json`文件或Claude配置文件中）：
```json
{
  "mcpServers": {
    "open-ontologies": {
      "command": "open-ontologies",
      "args": ["serve"]
    }
  }
}
```

**无需登录凭证。**所有处理操作都在内存中的Oxigraph三元组存储库中本地完成。网络访问仅在明确调用`onto_pull`（获取远程本体）或`onto_push`（发送到SPARQL端点）时使用。监控警报信息（`onto_monitor`）仅记录到标准输出（stdout）。

## 核心工作流程

在构建或修改本体时，请遵循以下工作流程。根据具体需求选择合适的工具并按顺序执行操作，因为这个流程并非固定不变。

### 1. 生成本体
- 理解领域需求（自然语言描述、能力要求、方法论约束等）
- 直接生成Turtle/OWL格式的本体——Claude支持OWL、RDF、BORO和4D建模格式
- 对于复杂的方法论，需要提供相关背景文档或约束条件

### 2. 验证并加载本体
- 调用`onto_validate`验证生成的Turtle格式本体；如果验证失败，修复语法错误后重新验证
- 调用`onto_load`将本体加载到Oxigraph三元组存储库中
- 调用`onto_stats`检查类数量、属性数量是否符合预期

### 3. 核实本体结构
- 调用`onto_lint`检查是否存在缺失的标签、注释、领域信息或范围定义；修复发现问题
- 使用SPARQL调用`onto_query`验证本体结构（如类、子类层次结构等是否符合预期）
- 如果存在参考本体，调用`onto_diff`进行对比分析

### 4. 迭代优化
- 如果任何步骤发现问题，修复相关内容并重新开始整个流程
- 重复上述步骤，直到验证通过、统计结果正确、代码检查无错误且SPARQL查询返回预期结果

### 5. 保存本体
- 调用`onto_save`将最终生成的本体保存为.ttl文件
- 调用`onto_version`保存一个可回滚的版本快照

## 本体生命周期管理（Terraform风格）

对于生产环境中的动态演化本体，可按照以下步骤进行管理：
1. **规划**：使用`onto_plan`查看新增/删除的类、影响范围及风险评分；使用`onto_lock`保护重要的IRI（Identifier Resources）。
2. **执行**：使用`onto_enforce`根据规则集（如`generic`、`boro`、`value_partition`）检查设计模式的合规性。
3. **应用更改**：使用`onto_apply`（模式为`safe`或`migrate`）应用修改；`migrate`模式可用于添加owl:equivalentClass等关联关系。
4. **监控**：使用`onto_monitor`运行SPARQL监控任务，并设置阈值警报；如果系统被阻塞，可使用`onto_monitor_clear`清除阻塞状态。
5. **版本跟踪**：使用`onto_drift`比较不同版本的本体，并自动调整评估权重。

## 数据扩展流程

在将本体应用于外部数据时，可执行以下操作：
1. `onto_map`：根据数据模式和已加载的本体生成映射配置
2. `onto_ingest`：将结构化数据（CSV、JSON、NDJSON、XML、YAML、XLSX、Parquet等）解析为RDF格式
3. `onto_shacl`：使用SHACL规范验证数据格式（如基数、数据类型、类等）
4. `onto_reason`：执行RDFS或OWL-RL推理，生成新的三元组
- 或者直接使用`onto_extend`完成整个流程：数据导入、SHACL验证、推理一体化

## 临床术语支持

针对医疗健康领域的本体，提供以下辅助工具：
- `onto_crosswalk`：查找ICD-10、SNOMED CT和MeSH之间的映射关系
- `onto_enrich`：添加skos:exactMatch三元组，将类与临床代码关联起来
- `onto_validate_clinical`：检查类标签是否符合临床术语标准

## 本体对齐

用于对齐两个本体：
- `onto_align`：使用6个权重指标检测潜在的对齐候选项（如equivalentClass、exactMatch、subClassOf等）
- `onto_align_feedback`：接受或拒绝对齐结果，以自动调整权重值

## 工具参考

| 工具 | 使用场景 |
| ---- | ----------- |
| `onto_validate` | 生成或修改本体后进行验证 |
| `onto_load` | 验证通过后加载本体到存储库 |
| `onto_stats` | 加载完成后检查数据统计信息 |
| `onto_lint` | 检查是否存在缺失的标签或领域信息 |
| `onto_query` | 验证本体结构并回答相关问题 |
| `onto_diff` | 与参考本体或旧版本进行对比 |
| `onto_save` | 将本体保存到文件 |
| `onto_convert` | 在不同格式之间转换本体（如Turtle、N-Triples、RDF/XML等） |
| `onto_clear` | 在加载新本体前清空存储库 |
| `onto_pull` | 从远程URL或SPARQL端点获取本体 |
| `onto_push` | 将本体发布到SPARQL端点 |
| `onto_import` | 解析并加载owl:imports关联关系 |
| `onto_version` | 保存版本快照 |
| `onto_history` | 查看所有保存的版本信息 |
| `onto_rollback` | 恢复到之前的版本 |
| `onto_ingest` | 将结构化数据解析为RDF并加载到存储库 |
| `onto_map` | 根据数据模式生成映射配置 |
| `onto_shacl` | 使用SHACL规范验证数据 |
| `onto_reason` | 执行RDFS或OWL-RL推理 |
| `onto_extend` | 完整的流程：数据导入、SHACL验证、推理 |
| `onto_plan` | 显示新增/删除的类及影响范围 |
| `onto_apply` | 以安全模式或迁移模式应用更改 |
| `onto_lock` | 保护重要IRI不被删除 |
| `onto_drift` | 比较不同版本的本体并自动调整权重 |
| `onto_enforce` | 检查设计模式的合规性 |
| `onto_monitor` | 运行SPARQL监控任务并设置警报 |
| `onto_monitor_clear` | 清除阻塞状态 |
| `onto_crosswalk` | 查找ICD-10、SNOMED、MeSH之间的临床术语映射 |
| `onto_enrich` | 添加skos:exactMatch三元组以关联临床代码 |
| `onto_validate_clinical` | 检查类标签是否符合临床术语标准 |
| `onto_align` | 检测两个本体之间的对齐关系 |
| `onto_align_feedback` | 接受或拒绝对齐结果以调整权重 |
| `onto_lineage` | 查看整个流程的执行历史 |
| `onto_lint_feedback` | 处理代码检查中发现的问题 |
| `onto_enforce_feedback` | 接受或拒绝违规操作，以便进行后续优化 |

## 使用示例

### 从零开始构建一个披萨本体
```
Build me a pizza ontology with classes for Pizza, PizzaBase (ThinAndCrispy, DeepPan),
PizzaTopping (Mozzarella, Tomato, Pepperoni, Mushroom), and properties hasBase, hasTopping.
Include rdfs:labels and rdfs:comments on everything. Validate and run competency queries
to check I can ask "what toppings does a Margherita have?"
```

### 加载并查询现有本体
```
Load the ontology from https://www.w3.org/TR/owl-guide/wine.rdf, show me stats,
lint it, and run a SPARQL query to find all subclasses of Wine.
```

### 安全地演化本体
```
I need to add a new class "GlutenFreePizza" as a subclass of Pizza with a restriction
that hasBase only GlutenFreeBase. Plan the change, enforce against generic rules,
and apply in safe mode.
```

### 将CSV数据导入知识图谱
```
I have a CSV of employees with columns: name, department, role, start_date.
Map it to the loaded HR ontology and ingest it. Then validate with SHACL shapes
and run inference to materialize department hierarchies.
```

### 对齐两个本体
```
Load schema.org and my company ontology. Run onto_align to find equivalentClass
and exactMatch candidates. I'll review and give feedback to calibrate the weights.
```

## 关键原则

根据前一步工具的输出结果动态决定下一步的操作。如果`onto_validate`验证失败，需修复错误后重试；如果`onto_stats`显示数据统计错误，需重新生成本体；如果`onto_lint`发现缺失标签，需补充相应内容。MCP工具各自独立执行特定任务，而Claude负责整个流程的协调管理。