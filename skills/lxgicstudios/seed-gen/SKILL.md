---
name: seed-gen
description: 根据您的数据库模式生成逼真的数据库种子数据。当您需要看起来真实的测试数据时，可以使用这些数据。
---

# 种子数据生成（Seed Data Generation）

该工具能够生成看起来真实的数据，不再使用“test user 1”或“lorem ipsum”这样的占位符。它会根据您的数据库模式（schema）生成有实际意义的数据，包括真实的姓名、合理的电子邮件地址、准确的时间戳以及相互关联的数据记录。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-seed prisma/schema.prisma
```

## 功能介绍

- 根据您的数据库模式生成真实的数据
- 识别字段类型并生成相应的值
- 确保相关表之间的引用关系正确无误
- 生成连贯的数据结构（而非随机生成的垃圾数据）
- 输出可直接使用的种子数据脚本

## 使用示例

```bash
# Generate seed data from schema
npx ai-seed prisma/schema.prisma

# Specify number of records
npx ai-seed prisma/schema.prisma --count 50

# Target specific tables
npx ai-seed prisma/schema.prisma --tables users,posts,comments

# Output as SQL
npx ai-seed prisma/schema.prisma --format sql > seed.sql
```

## 最佳实践

- **根据实际需求选择数据类型**：例如，电子商务应用需要产品相关的数据；社交应用则需要用户交互相关的信息。
- **从小规模开始**：先生成10-20条记录以检查数据质量，再逐步扩大生成规模。
- **验证数据关系**：确保外键引用的是真实存在的记录。
- **考虑边缘情况**：添加一些空字段、已删除的用户记录或过时的日期，以便测试用户界面（UI）的响应性。

## 适用场景

- 新项目启动时需要演示数据
- 开发用户界面时需要真实的数据作为设计依据
- 测试数据库查询时需要足够的数据来观察性能问题
- 向利益相关者展示产品时需要专业且高质量的数据示例

## 该工具属于LXGIC开发工具包（LXGIC Dev Toolkit）的一部分

LXGIC Studios提供了110多种免费开发者工具，此工具属于其中之一。免费版本完全无需支付费用、注册或API密钥，只需使用npx命令即可运行。更多信息请访问：

- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，直接使用npx命令即可运行。建议使用Node.js 18及以上版本。运行时需要设置`OPENAI_API_KEY`环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-seed --help
```

## 工作原理

该工具会读取您的数据库模式以理解数据模型和表之间的关系，然后利用GPT模型生成符合领域特性的数据。生成的种子数据脚本会按照正确的插入顺序进行排列，以确保外键约束得到遵守。

## 许可协议

采用MIT许可证，永久免费。您可以自由使用该工具。

---

（注：由于提供的代码块仅为示例，实际翻译内容可能因具体工具的实现细节而有所不同。上述翻译基于代码块的格式和描述进行了相应的调整。）