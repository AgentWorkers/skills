# Content Machine

这是一个自动化内容生成系统，能够发现热门话题并将其发布到社交媒体上。该系统利用人工智能（AI）进行内容研究、撰写和发布计划的管理。

## 功能介绍

- 监控来自多个来源的热门趋势
- 使用AI生成引人入胜的内容
- 安排内容发布时间并发布到相应的社交媒体平台
- 监测系统性能并进行优化

## 安装要求

### 先决条件

1. **OpenAI API Key** 或 **Anthropic API Key** – 用于内容生成
2. **Postiz API Key** – 用于将内容发布到社交媒体平台
3. （可选）特定平台的API（如Twitter、LinkedIn等）

### 环境变量

```bash
export OPENAI_API_KEY="your_openai_key"
export POSTIZ_API_KEY="your_postiz_key"
```

### 安装步骤

```bash
pip install requests openai
```

## 使用方法

### 运行内容生成

```bash
python content-machine.py --niche tech --platforms twitter,linkedin --count 5
```

### 配置数据源

编辑 `config/sources.json` 文件，添加以下内容：
- RSS源
- 新闻API
- 社交媒体趋势数据源

### 设置发布计划

```bash
python content-machine.py --schedule "9am,12pm,6pm"
```

## 配置文件

- `config/content.json` – 内容模板
- `config/schedule.json` – 发布时间表
- `config/platforms.json` – 平台设置

## 主要特性

- 支持多平台发布（Twitter、LinkedIn、Instagram、TikTok）
- 内容模板和病毒性评分功能
- 自动生成标签
- 为帖子生成图片
- 提供性能分析功能

## 成本

成本取决于AI的使用情况：
- OpenAI：每条帖子约0.001美元
- 图片生成：每条帖子约0.01美元（如需要生成图片）