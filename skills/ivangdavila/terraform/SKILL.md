---
name: Terraform
description: 避免常见的 Terraform 错误：状态损坏（state corruption）、`count` 与 `for_each` 的误用、生命周期管理中的陷阱（lifecycle traps），以及依赖关系的排序问题。
metadata: {"clawdbot":{"emoji":"🟪","requires":{"bins":["terraform"]},"os":["linux","darwin","win32"]}}
---

## 状态管理  
- 如果本地状态损坏或丢失，应使用远程后端（如 S3、GCS 或 Terraform Cloud）进行恢复。  
- 当多人同时操作时，应使用 DynamoDB 或类似工具来实现状态锁定机制。  
- 绝不要手动编辑状态数据，应使用 `terraform state mv`、`rm` 或 `import` 命令进行操作。  
- 如果状态文件中包含明文形式的敏感信息，必须对这些信息进行加密处理，并限制访问权限。  

## `count` 与 `for_each` 的区别  
- `count` 通过索引来计数元素；删除第一个元素会导致所有索引重新排序，从而需要重新计算总数。  
- `for_each` 通过键来遍历元素；删除某个元素不会影响其他元素的计数结果。  
- 不可以在同一资源上同时使用 `count` 和 `for_each`，必须选择其中一种方法。  
- 使用 `for_each` 时，需要先对数据结构进行转换（例如使用 `toset()` 将列表转换为集合）。  

## 生命周期规则  
- `prevent_destroy = true`：防止资源被意外删除；如果要删除资源，必须先取消该规则。  
- `create_before_destroy = true`：确保新资源在旧资源被删除之前创建，从而实现零停机时间。  
- `ignore_changes`：用于忽略外部对状态的修改（例如通过 `ignore_changes = [tags]` 可忽略某些标签引起的状态变化）。  
- `replace_triggered_by`：当资源依赖关系发生变化时，会触发资源的重新生成。  

## 依赖关系管理  
- 依赖关系可以通过引用自动建立（例如 `aws_instance.foo.id`）。  
- 对于配置文件中未明确指定的依赖关系，可以使用 `depends_on` 来声明它们（例如 `depends_on = [aws_iam_role.x, aws_iam_policy.y]`）。  
- 数据源会在规划阶段被执行；如果资源还不存在，执行数据源操作可能会导致失败。  

## 数据源  
- 数据源用于读取现有资源的信息，不会创建新的资源。  
- 数据源在规划阶段被执行；因此相关资源必须已经存在。  
- 如果依赖关系不明确或规划失败，应使用 `depends_on` 来明确指定依赖关系。  
- 可以考虑使用资源的输出结果作为数据源，这样会更加清晰明了。  

## 模块管理  
- 可以固定模块的版本（例如 `source = "org/name/aws?version=1.2.3"`）。  
- 使用 `terraform init -upgrade` 可以更新模块版本，但不会自动进行版本升级。  
- 模块的输出结果必须明确指定；外部代码无法直接访问模块的内部资源。  
- 嵌套模块的输出结果需要被上层模块引用；每个模块都需要输出结果。  

## 变量管理  
- 变量没有默认类型，需要明确指定类型（例如 `type = string`、`list(string)`、`map(object {...})`）。  
- 可以设置变量为敏感信息（`sensitive = true`），这样这些变量不会显示在输出结果中，但仍会保存在状态文件中。  
- 使用 `validation` 块来定义变量的约束条件，并设置自定义错误信息。  
- 变量默认为可空（`nullable = false`），但如果需要禁止空值，需要明确指定。  

## 常见错误  
- 使用 `terraform destroy` 会永久删除资源，无法恢复；请谨慎使用该命令。  
- 规划阶段成功并不意味着应用阶段也会成功；应用过程中可能会遇到 API 错误、配额限制或权限问题。  
- 重命名资源相当于先删除再创建；应使用 `moved` 块或 `terraform state mv` 来处理资源迁移。  
- 不同环境应使用不同的状态文件或后端。  
- 除非必要，否则应避免使用 `provisioners`；优先考虑使用 `cloud-init`、`user_data` 或其他配置管理工具。  

## 导入资源  
- `terraform import aws_instance.foo i-1234` 用于将现有资源导入状态文件。  
- `import` 命令不会自动生成配置文件；需要手动编写相应的资源配置。  
- 从 Terraform 1.5 开始，可以使用 `import` 块在配置文件中声明性地导入资源。  
- 导入资源后需要重新执行规划阶段以验证配置是否正确；如果配置无误，规划阶段不应显示任何变化。