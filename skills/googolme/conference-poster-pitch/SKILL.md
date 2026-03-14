---
name: conference-poster-pitch
description: 为会议海报生成一个简短的宣传语（“电梯演讲”风格）。
version: 1.0.0
category: Present
tags: []
author: AIPOCH
license: MIT
status: Draft
risk_level: Medium
skill_type: Tool/Script
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-06'
---
# 会议海报推介脚本

生成适用于学术海报展示的简短推介语（“电梯演讲”格式）。

## 参数

| 参数            | 类型        | 默认值    | 是否必填 | 说明                                      |
|------------------|-----------|---------|---------|-----------------------------------------|
| `--poster-title`, `-t` | 字符串      | -        | 是        | 海报标题                                      |
| `--duration`, `-d` | 整数       | 60       | 否        | 推介语时长（30秒、60秒或180秒）                         |

## 使用方法

```bash
# Generate 60-second pitch
python scripts/main.py --poster-title "CRISPR Therapy for Sickle Cell Disease" --duration 60

# Generate quick 30-second pitch
python scripts/main.py --poster-title "Novel Biomarkers in Cancer" --duration 30

# Generate detailed 3-minute pitch
python scripts/main.py --poster-title "AI in Drug Discovery" --duration 180
```

## 输出结果

- 适用于30秒、60秒和3分钟推介的脚本
- 结构化的推介语格式
- 可直接用于实际演示的文本

## 风险评估

| 风险指标            | 评估结果    | 风险等级   |
|------------------|-----------|---------|
| 代码执行          | 在本地执行Python/R脚本 | 中等      |
| 网络访问          | 无外部API调用    | 低        |
| 文件系统访问          | 读取输入文件、写入输出文件 | 中等      |
| 指令篡改          | 遵循标准提示指南   | 低        |
| 数据泄露          | 输出文件保存在工作区   | 低        |

## 安全检查清单

- [ ] 无硬编码的凭据或API密钥
- [ ] 无未经授权的文件系统访问
- [ ] 输出内容不包含敏感信息
- [ ] 有防止提示注入的安全机制
- [ ] 输入文件路径经过验证（防止路径遍历攻击）
- [ ] 输出目录限制在工作区内
- [ ] 脚本在沙箱环境中执行
- [ ] 错误信息经过处理（不显示堆栈跟踪）
- [ ] 依赖项经过审核

## 先决条件

无需额外的Python包。

## 评估标准

### 成功指标

- [ ] 脚本能成功执行主要功能
- [ ] 输出内容符合质量标准
- [ ] 能妥善处理边缘情况
- [ ] 性能表现可接受

### 测试用例

1. **基本功能**：标准输入 → 预期输出
2. **边缘情况**：无效输入 → 良好的错误处理
3. **性能**：处理大型数据集时 → 处理时间可接受

## 生命周期状态

- **当前阶段**：草案阶段
- **下一次审查日期**：2026-03-06
- **已知问题**：无
- **计划中的改进**：
  - 性能优化
  - 支持更多功能