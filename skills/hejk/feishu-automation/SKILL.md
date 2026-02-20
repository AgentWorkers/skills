---
name: feishu-automation
description: Feishu（Lark）生产力套件的高级自动化工作流。适用于需要自动化文档处理流程、在Feishu应用之间同步数据、生成报告，或对文档、维基、Bitable表格及云存储进行批量操作的场景。触发条件包括：“批量处理飞书文档”、“自动同步飞书表格数据”、“备份知识库”、“生成飞书报告”、“自动化执行飞书任务”以及“飞书数据迁移”。
---
# Feishu自动化

## 概述

本技能支持Feishu/Lark生产力套件中的高级自动化功能，提供了针对常见自动化场景的解决方案、脚本和工作流程，包括批量文档处理、数据同步、报告生成和知识管理。

## 快速入门

### 先决条件
- 已配置OpenClaw与Feishu的集成
- 在Feishu应用中启用了以下权限：`docx`、`wiki`、`bitable`、`drive`
- 目标文档/表格已经存在且可访问

### 基本示例：批量更新文档
```bash
# Use the batch_update.py script to update multiple documents
python scripts/batch_update.py --folder-token fldcnXXX --template "weekly_report.md"
```

## 核心自动化任务

### 1. 文档自动化
- **批量创建**：根据模板生成多个文档
- **内容同步**：将数据从Bitable同步到文档中
- **格式转换**：在markdown格式和Feishu文档格式之间进行转换
- **备份与归档**：定期备份重要文档

### 2. Wiki与知识管理
- **Wiki迁移**：在wiki空间之间移动内容
- **自动标记**：根据内容分析为wiki页面添加标签
- **目录生成**：为大型wiki生成目录
- **链接检查**：查找并修复wiki中的无效链接

### 3. Bitable自动化
- **数据导入/导出**：将Bitable数据与外部数据源进行同步
- **报告生成**：根据Bitable查询结果生成文档
- **数据验证**：确保Bitable中的数据质量
- **通知系统**：在Bitable数据发生变化时发送警报

### 4. 跨应用工作流程
- **文档 → Bitable**：从文档中提取结构化数据并导入到Bitable表中
- **Bitable → 文档**：根据Bitable表数据生成报告
- **Wiki → Drive**：将wiki页面归档到云存储
- **Drive → Wiki**：将文档导入为wiki页面

## 工作流程模板

### 周报自动化
1. 从Bitable中查询每周指标
2. 生成包含图表的markdown报告
3. 创建/更新Feishu文档
4. 将报告发布到指定的wiki空间
5. 通过Feishu聊天工具通知团队

详细实现步骤请参阅`references/weekly_report_workflow.md`。

### 文档迁移
1. 列出源文件夹中的文档
2. 将每个文档转换为markdown格式
3. 在目标文件夹/wiki中创建新文档
4. 更新所有内部链接
5. 验证迁移是否完成

相关脚本请参阅`scripts/migrate_documents.py`。

## 工具参考

本技能基于OpenClaw提供的原生Feishu工具实现：
- `feishu_doc`：用于文档的读写操作
- `feishu_wiki`：用于导航知识库
- `feishu_bitable_*`：用于Bitable的操作
- `feishu_drive`：用于管理云存储

在可能的情况下，请直接使用原生工具；仅在复杂的工作流程中使用脚本。

## 包含的资源

本技能附带了用于常见自动化任务的现成资源：

### 脚本
- `batch_update.py`：根据模板批量更新文档
- `migrate_documents.py`：在文件夹/空间之间迁移文档
- `bitable_to_doc.py`：根据Bitable数据生成文档
- `wiki_backup.py`：将wiki页面备份为markdown文件

### 参考资料
- `weekly_report_workflow.md`：周报自动化步骤指南
- `feishu_api_patterns.md`：常见的API使用模式和示例
- `error_handling.md`：处理Feishu API错误的方法
- `best_practices.md：性能与可靠性最佳实践

### 资源文件
- `templates/weekly_report.md`：周报模板
- `templates/meeting_notes.md`：会议记录模板
- `templates/project_status.md`：项目状态更新模板
- `config/sample_config.yaml`：配置示例

## 获取帮助

如有疑问或遇到问题，请：
1. 首先查阅相关参考文件
2. 查看`error_handling.md`中的错误信息
3. 根据具体需求调整脚本
4. 咨询OpenClaw的Feishu官方文档以获取工具的详细信息