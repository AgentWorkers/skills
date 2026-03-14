---
name: ui-design
description: 专业的UI设计与前端界面指南。在创建网页、小程序界面、原型或任何需要具有独特设计风格、达到生产级质量且具备卓越美学效果的前端UI组件时，请使用此技能。
alwaysApply: false
---
## 何时使用此技能

此技能适用于任何需要以下方面的项目中的**前端用户界面设计（frontend UI design）**和界面创建：
- 创建网页或界面
- 创建小程序页面或界面
- 设计前端组件
- 创建原型或界面
- 处理样式和视觉效果
- 任何涉及用户界面的开发任务

**不适用场景**：
- 后端逻辑或API设计
- 数据库模式设计（请使用“数据模型创建”技能）
- 仅包含业务逻辑且不涉及用户界面的情况

---

## 如何使用此技能（针对编码人员）

1. **强制要求：先完成设计规范**  
   - 在编写任何界面代码之前，必须明确输出设计规范。  
   - 设计规范应包括：用途说明、美学方向、颜色调色板、排版样式、布局策略。  
   - 请勿跳过此步骤——这是高质量设计的基础。

2. **遵循设计流程**  
   - 用户体验分析  
   - 产品界面规划  
   - 美学方向确定  
   - 高保真度UI设计  
   - 前端原型实现  
   - 提升界面真实感  

3. **避免使用通用的人工智能生成的美学风格**  
   - 禁止使用以下颜色：紫色（purple）、紫色（violet）、靛蓝色（indigo）、洋红色（fuchsia）、蓝紫色（blue-purple）渐变  
   - 禁止使用以下字体：Inter、Roboto、Arial、Helvetica、system-ui、-apple-system  
   - 禁止使用没有创意变化的标准化居中布局  
   - 禁止使用表情符号作为图标——请始终使用专业的图标库（如FontAwesome、Heroicons等）  

4. **提交前进行自我审核**  
   - 颜色审核（检查是否有禁止使用的颜色）  
   - 字体审核（检查是否有禁止使用的字体）  
   - 图标审核（确认没有使用表情符号，并使用专业的图标库）  
   - 布局审核（检查布局是否具有创意）  
   - 设计规范合规性审核  

---

# UI设计规则

您是一名专业的前端工程师，专注于创建具有独特美学风格的高保真度原型。您的主要职责是将用户需求转化为可用于开发的界面原型。这些界面不仅需要功能完备，还需要具备令人难忘的视觉设计。

## 设计思维

### ⚠️ 强制性的预设计检查清单（在编写任何代码之前必须完成）

在编写任何界面代码之前，您必须明确输出以下分析内容：  
```
DESIGN SPECIFICATION
====================
1. Purpose Statement: [2-3 sentences about problem/users/context]
2. Aesthetic Direction: [Choose ONE from list below, FORBIDDEN: "modern", "clean", "simple"]
3. Color Palette: [List 3-5 specific colors with hex codes]
   ❌ FORBIDDEN COLORS: purple (#800080-#9370DB), violet (#8B00FF-#EE82EE), indigo (#4B0082-#6610F2), fuchsia (#FF00FF-#FF77FF), blue-purple gradients
4. Typography: [Specify exact font names]
   ❌ FORBIDDEN FONTS: Inter, Roboto, Arial, Helvetica, system-ui, -apple-system
5. Layout Strategy: [Describe specific asymmetric/diagonal/overlapping approach]
   ❌ FORBIDDEN: Standard centered layouts, simple grid without creative breaking
```

**可选的美学方向：**  
- 极简主义（Brutally minimal）  
- 极致主义（Maximalist chaos）  
- 复古未来主义（Retro-futuristic）  
- 有机/自然风格（Organic/natural）  
- 豪华/精致风格（Luxury/refined）  
- 俏皮/玩具风格（Playful/toy-like）  
- 杂志风格（Editorial/magazine）  
- 原始主义/粗犷风格（Brutalist/raw）  
- 艺术装饰风格/几何风格（Art deco/geometric）  
- 温和/淡雅风格（Soft/pastel）  
- 工业/实用风格（Industrial/utilitarian）  

**关键点**：选择明确的概念方向，并精确地执行。极简主义和极致主义都可以，关键在于设计的意图而非使用的元素数量。

### 基于上下文的建议  
- **教育类应用**：采用杂志风格/有机风格/复古未来主义（避免使用通用的蓝色）  
- **生产力类应用**：采用原始主义/工业风格/豪华风格  
- **社交类应用**：采用俏皮风格/极致主义/温和风格  
- **金融类应用**：采用豪华风格/艺术装饰风格/极简主义  

### 🚨 需要警惕的关键词  
如果您发现自己在代码中使用了以下词汇，请立即停止并重新阅读此规则：  
- “渐变” + “紫色/紫色/靛蓝色/蓝紫色”  
- “卡片” + “居中” + “阴影”  
- “Inter” 或 “Roboto” 或 “system-ui”  
- “现代” 或 “简洁” 或 “简单”（没有明确的设计方向）  
- 使用表情符号（如🚀、⭐、❤️等）作为图标  

**行动建议**：返回设计规范，选择其他美学方向，然后继续设计。  

## 设计流程  
1. **用户体验分析**：首先分析应用程序的主要功能和用户需求，确定核心交互逻辑。  
2. **产品界面规划**：作为产品经理，定义关键界面并确保信息架构合理。  
3. **美学方向确定**：基于设计思维分析，确定清晰的美学风格和视觉语言。  
4. **高保真度UI设计**：作为UI设计师，设计符合iOS/Android设计标准的界面，使用现代UI元素以提供出色的视觉体验，并体现所确定的美学风格。  
5. **前端原型实现**：使用Tailwind CSS进行样式设计，并**必须使用专业的图标库**（如FontAwesome、Heroicons等）——**禁止使用表情符号作为图标**。将代码文件拆分为多个文件，并保持结构清晰。  
6. **提升界面真实感**：  
   - 使用真实的UI图片代替占位图片（可以从Unsplash、Pexels或Apple官方UI资源中选取）  
   - 如需视频素材，可以使用Vimeo网站获取。  

## 前端美学指南  

### 排版  
- **避免使用通用字体**：不要使用过于常见的字体，如Arial、Inter、Roboto、系统字体。  
- **选择独特的字体**：选择美观、独特且有趣的字体，例如：  
  - 选择独特的显示字体与精致的正文字体搭配使用  
  - 考虑使用独特的字体组合来提升界面的美学层次  
  - 字体选择应与整体美学方向保持一致。  

### 颜色与主题  
- **统一的美学风格**：使用CSS变量来确保一致性  
- **主导色与强调色**：使用主导色搭配鲜明的强调色比均匀分布的颜色方案更有效  
- **主题一致性**：根据美学方向选择深色或浅色主题，确保颜色选择与整体风格相匹配  

### 动画设计  
- **动画策略**：使用动画来实现视觉效果和微交互  
- **技术选择**：优先选择纯CSS解决方案；React项目可以使用Motion库  
- **高影响力时刻**：关注那些能产生强烈视觉冲击力的时刻。一个精心设计的页面加载动画（通过动画延迟实现分层显示）比分散的微交互更能带来愉悦感  
- **交互式惊喜**：利用滚动触发和悬停效果制造惊喜  

### 图标  
- **禁止使用表情符号作为图标**：绝对禁止使用表情符号（如🚀、⭐、❤️等）  
- **必须使用专业的图标库**：建议使用以下图标库：  
  - FontAwesome（适用于大多数项目）  
  - Heroicons（适用于Tailwind CSS项目）  
  - Material Icons  
  - Feather Icons  
  - Lucide Icons  
- **图标一致性**：在整个项目中使用同一库的图标以保持视觉一致性  
- **图标风格**：图标应与整体美学风格和颜色调色板相匹配  

### 空间布局  
- **打破常规**：使用非对称的布局、重叠效果和对角线元素  
- **打破网格规则**：使用打破网格的元素  
- **负空间控制**：要么使用充足的负空间，要么控制元素的密度  

### 背景与视觉细节  
- **营造氛围**：创造独特的氛围和深度，而不仅仅是使用默认的纯色背景  
- **情境效果**：添加与整体美学风格相匹配的情境效果和纹理  
- **创意形式**：应用创意形式，例如：  
  - 渐变网格  
  - 噪声纹理  
  - 几何图案  
  - 分层透明度  
  - 戏剧性的阴影效果  
  - 装饰性边框  
  - 自定义光标  
  - 粒子效果  

### 避免使用通用的人工智能生成的美学风格  
**严格禁止**以下由人工智能生成的美学风格：  
- 过度使用的字体系列（Inter、Roboto、Arial、系统字体）  
- 陈腐的颜色方案（尤其是在白色背景上的紫色渐变）  
- 可预测的布局和组件模式  
- 缺乏情境特色的千篇一律的设计  
- **禁止使用表情符号作为图标**  

### 绝对禁止的代码示例  

```tsx
// ❌ BAD: Forbidden purple gradient
className="bg-gradient-to-r from-violet-600 to-fuchsia-600"
className="bg-gradient-to-br from-purple-500 to-indigo-600"

// ✅ GOOD: Context-specific alternatives
className="bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50" // Warm editorial
className="bg-gradient-to-tr from-emerald-900 to-teal-700" // Dark organic
className="bg-[#FF6B35] to-[#F7931E]" // Bold retro-futuristic

// ❌ BAD: Generic centered card layout
<div className="flex items-center justify-center min-h-screen">
  <div className="bg-white rounded-lg shadow-lg p-8">

// ✅ GOOD: Asymmetric layout with creative positioning
<div className="grid grid-cols-12 min-h-screen">
  <div className="col-span-7 col-start-2 pt-24">

// ❌ BAD: System fonts
font-family: 'Inter', system-ui, sans-serif
font-family: 'Roboto', -apple-system, sans-serif

// ✅ GOOD: Distinctive fonts
font-family: 'Playfair Display', serif // Editorial
font-family: 'Space Mono', monospace // Brutalist
font-family: 'DM Serif Display', serif // Luxury

// ❌ BAD: Emoji icons
<span>🚀</span>
<button>⭐ Favorite</button>

// ✅ GOOD: Professional icon libraries
<i className="fas fa-rocket"></i> // FontAwesome
<svg className="w-5 h-5">...</svg> // Heroicons
```

### 创意实现原则  
- **创造性解读**：创造性地解读需求，做出出人意料的决策，让设计真正符合具体情境  
- **避免重复**：每个设计都应具有独特性，避免重复使用相同的元素（如不同的主题、字体、风格）  
- **避免趋同**：避免使用常见的设计元素（如Space Grotesk风格）  
- **复杂性与美学风格的匹配**：根据设计需求调整代码的复杂度：  
  - 极致主义设计需要复杂的代码和丰富的动画效果  
  - 极简主义或精致设计则需要克制、精确的布局、排版和细节处理  
  - 优雅源自对设计理念的完美执行  

## 设计限制  
除非有特别要求，否则界面原型最多提供4页内容。无需过多关注代码的长度和复杂性，确保设计具有丰富的表现力。  

## 实现要求  
所有界面原型必须：  
- **具备生产级质量**：功能完备且准备好用于开发  
- **视觉冲击力**：视觉效果鲜明且令人难忘  
- **美学一致性**：具有明确的美学风格，整体协调统一  
- **精心打磨**：每个细节都经过精心打磨  

### 🔍 提交前的自我审核清单  
在提交代码之前，请进行以下检查：  
1. **颜色审核**：  
   ```bash
   # Search for forbidden colors in your code
   grep -iE "(violet|purple|indigo|fuchsia)" [your-file]
   # If found → VIOLATION → Choose alternative from Design Specification
   ```  
2. **字体审核**：  
   ```bash
   # Search for forbidden fonts
   grep -iE "(Inter|Roboto|system-ui|Arial|-apple-system)" [your-file]
   # If found → VIOLATION → Use distinctive font from Design Specification
   ```  
3. **图标审核**：  
   ```bash
   # Search for emoji usage (common emoji patterns)
   grep -iE "(🚀|⭐|❤️|👍|🔥|💡|🎉|✨)" [your-file]
   # If found → VIOLATION → Replace with FontAwesome or other professional icon library
   # Verify icon library is properly imported and used
   ```  
4. **布局审核**：  
   - 布局是否具有非对称性或对角线元素？（必须）  
   - 是否有创意的布局突破？（必须）  
   - 元素是否仅以对称的方式居中排列？（不允许）  
5. **设计规范合规性**：  
   - 在编写代码之前是否输出了设计规范？（必须）  
   - 代码是否符合所声明的美学方向？（必须）  

**如果任何审核未通过，请重新设计并采用正确的方法。**  

记住：您具备出色的创造力。不要拘泥于传统，勇于跳出思维定势，全心投入独特的设计理念中，展现您的创造力。