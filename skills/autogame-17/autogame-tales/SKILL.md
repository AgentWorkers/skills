# AutoGame Tales

该工具可根据随机提示生成简短、充满氛围的鬼故事或微小说，旨在为智能体的性格增添叙事元素，并打破其功能的单一性（即避免其功能长期处于闲置状态）。

## 主要功能
- **鬼故事生成器**：能够创作出令人毛骨悚然、氛围浓厚的微小说。
- **随机提示**：使用精心挑选的恐怖/神秘主题作为故事创作的灵感来源。
- **Feishu 卡片输出**：将生成的故事以卡片的形式呈现出来。

## 使用方法
```bash
# Generate a ghost story
node skills/autogame-tales/index.js --genre ghost

# Generate a sci-fi story
node skills/autogame-tales/index.js --genre sci-fi
```

## 功能范围
- **读取操作**：不执行任何读取操作。
- **写入操作**：将生成的故事保存到 `memory/tales/` 目录中。
- **依赖库**：需要 `feishu-evolver-wrapper/feishu-helper.js` 来实现故事的发送功能。