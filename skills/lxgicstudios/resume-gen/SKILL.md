---
name: resume-gen
description: 生成并优化开发人员的简历，用于求职时使用。
---

# 简历生成器

撰写简历是一件麻烦的事情。通过这个工具，您可以轻松描述自己的工作经验，并获得一份格式规范的开发者简历。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-resume "senior fullstack engineer, 5 years React, Node.js, AWS"
```

## 功能介绍

- 生成专业的开发者简历
- 突出与职位相关的重要技能
- 使用动词性描述来表达成就，并对成果进行量化
- 以 Markdown 格式输出，便于编辑

## 使用示例

```bash
# Senior role
npx ai-resume "senior fullstack engineer, 5 years React, Node.js, AWS"

# Junior role
npx ai-resume "junior frontend dev, 1 year Vue.js" -o resume.md

# Career change
npx ai-resume "backend engineer transitioning to ML, Python, PyTorch"
```

## 使用建议

- **量化成果**：例如“将系统性能提升了 40%”
- **使用职位描述中的关键词**  
- **保持简洁**：大多数职位的简历应控制在一页以内  
- **定期更新**：不要等到需要时才去更新简历

## 适用场景

- 开始求职时  
- 需要一份基础简历以便进一步定制  
- 更新过时的简历  
- 申请不同类型的职位  

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无付费门槛、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios  
- Twitter: https://x.com/lxgicstudios  
- Substack: https://lxgicstudios.substack.com  
- 官网: https://lxgicstudios.com  

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-resume --help
```

## 工作原理

该工具会根据您提供的经验描述，自动生成一份格式规范的简历，其中包含相应的章节、动词性描述以及突出的技术技能。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/resume-gen](https://github.com/lxgicstudios/resume-gen)  
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)