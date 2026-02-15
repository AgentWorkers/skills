# 技能健康监控器

该工具会扫描技能目录，检查其结构是否符合规范以及是否存在环境依赖关系。  
当您怀疑某个技能存在问题（如文件损坏、元数据缺失），或需要审计工作空间时，可以使用该工具。

## 使用方法  
```bash
node skills/skill-health-monitor/index.js
```

## 主要功能  
- 检查是否存在 `SKILL.md` 文件（技能文档）  
- 检查是否存在 `package.json` 或 `index.js` 文件（技能的入口文件）  
- **依赖关系检查：** 验证 `SKILL.md` 文件中声明的环境变量是否真实存在  
- 显示技能的总数、正常运行的技能数量以及存在问题的技能数量  
- 生成 `health_report.json` 和 `dependency_report.json` 文件，以便后续程序化使用