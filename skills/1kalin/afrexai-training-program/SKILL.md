# 员工培训计划构建器

该工具可针对任何职位、部门或合规要求，构建结构化的培训计划。能够生成课程大纲、培训时间表、评估标准以及培训完成情况的跟踪记录。

## 使用场景
- 为新员工提供与职位相关的入职培训
- 推行合规性培训（如SOC 2、HIPAA、GDPR、OSHA等）
- 对团队进行新工具或新流程的技能提升培训
- 制定领导力发展计划
- 创建认证准备路径

## 使用步骤

当需要构建培训计划时，请收集以下信息：
1. **培训对象**：哪些员工需要接受培训？
2. **培训目标**：培训结束后，员工应掌握哪些知识或技能？
3. **培训时长**：整个培训计划持续多长时间？
4. **培训形式**：是自主学习、讲师指导还是混合式学习？

随后，系统将生成以下内容：

### 培训计划结构
```
PROGRAM: [Name]
AUDIENCE: [Role/team]
DURATION: [X weeks]
FORMAT: [Self-paced / Instructor-led / Blended]

MODULE 1: [Topic]
- Learning objectives (3-5 measurable outcomes)
- Content outline (topics, subtopics)
- Activities (hands-on exercises, case studies)
- Assessment (quiz, practical demo, project)
- Time estimate: X hours
- Resources needed: [tools, access, materials]

MODULE 2: [Topic]
...
```

### 评估框架
对于每个培训模块，需定义以下评估方式：
- **知识测试**：通过率至少为70%
- **实践评估**：要求学员完成演示或项目任务
- **能力评估**：针对每个技能领域，采用1-5分的评分标准

### 培训完成情况跟踪
```
| Employee | Module 1 | Module 2 | Module 3 | Overall | Status |
|----------|----------|----------|----------|---------|--------|
| Name     | ✅ 92%   | ✅ 88%   | 🔄 In Progress | 60% | On Track |
```

### 合规性培训要求
如果培训与合规性相关，还需包括以下内容：
- 相关法规要求的具体条款
- 重新认证的频率
- 文档/记录的保存期限
- 审计追踪的格式

### 培训投资回报率（ROI）指标
通过以下指标评估培训效果：
- **从培训开始到员工能够独立工作的时间**  
- **错误率的变化**（培训前后的对比）
- **员工留存率**：根据LinkedIn 2024年的数据，投资培训的员工在公司中的留存率更高  
- **每位员工的培训成本**：培训总成本除以参与人数

## 使用建议
- 将每个培训模块拆分为45-60分钟的单元，以适应员工的注意力持续时间  
- 每个模块至少包含一个实践练习  
- 建立反馈机制（在每个模块结束后进行调查）  
- 制作“快速参考卡”以提供培训后的支持  
- 安排30天的后续评估，以评估培训内容的掌握情况

## 可用资源
- 适用于10个行业的完整培训资料包：https://afrexai-cto.github.io/context-packs/  
- 用于计算AI自动化投资回报率的工具：https://afrexai-cto.github.io/ai-revenue-calculator/  
- 代理设置向导：https://afrexai-cto.github.io/agent-setup/