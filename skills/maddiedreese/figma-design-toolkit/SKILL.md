---
name: figma
description: 专业的Figma设计分析与资产导出工具：用于提取设计数据、以多种格式导出设计资产、审核可访问性合规性、分析设计系统以及生成全面的设计文档。该工具支持对Figma文件进行只读分析，并具备强大的导出和报告功能。
---

# Figma 设计分析与导出

这是一个专为设计系统分析、资产导出及全面设计审计而设计的专业级 Figma 集成工具。

## 核心功能

### 1. 文件操作与分析
- **文件检查**：获取任何 Figma 文件的完整 JSON 表示形式
- **组件提取**：列出所有组件、样式及设计元素
- **资产导出**：批量导出帧、组件或特定节点为 PNG/SVG/PDF 格式
- **版本管理**：访问特定文件版本及分支信息

**示例用法：**
- “从该设计系统文件中导出所有组件”
- “获取这些特定帧的 JSON 数据”
- “显示该文件中使用的所有颜色和字体”

### 2. 设计系统管理
- **样式审计**：分析颜色使用情况、字体一致性及间距模式
- **组件分析**：识别未使用的组件并测量使用频率
- **品牌合规性检查**：检查文件是否符合品牌指南
- **设计元素提取**：从 Figma 样式中生成 CSS/JSON 格式的设计元素

**示例用法：**
- “审计此设计系统是否存在可访问性问题”
- “从这些 Figma 样式中生成 CSS 自定义属性”
- “查找我们组件库中的所有不一致之处”

### 3. 批量资产导出
- **多格式导出**：将资产导出为 PNG、SVG、PDF 或 WEBP 格式
- **平台特定尺寸处理**：为 iOS/Android 生成 @1x、@2x、@3x 格式的资产
- **有序输出**：按格式或平台自动组织文件
- **客户端交付包**：包含完整文档的交付包

**示例用法：**
- “将所有组件导出为 PNG 和 SVG 格式”
- “为移动应用开发生成完整的资产包”
- “创建包含所有营销资产的客户端交付文件”

### 4. 可访问性及质量分析
- **对比度检查**：验证 WCAG 颜色对比度要求
- **字体大小分析**：确保字体大小可读
- **交互元素尺寸检查**：检查触控目标是否符合要求
- **焦点状态验证**：验证键盘导航模式

**示例用法：**
- “检查此设计的 WCAG AA 合规性”
- “分析移动设备的触控目标”
- “为该应用设计生成可访问性报告”

## 快速入门

### 认证设置
```bash
# Set your Figma access token
export FIGMA_ACCESS_TOKEN="your-token-here"

# Or store in .env file
echo "FIGMA_ACCESS_TOKEN=your-token" >> .env
```

### 基本操作
```bash
# Get file information and structure
python scripts/figma_client.py get-file "your-file-key"

# Export frames as images
python scripts/export_manager.py export-frames "file-key" --formats png,svg

# Analyze design system consistency
python scripts/style_auditor.py audit-file "file-key" --generate-html

# Check accessibility compliance
python scripts/accessibility_checker.py "file-key" --level AA --format html
```

## 工作流程模式

### 设计系统审计流程
1. **提取文件数据** → 获取组件、样式及结构
2. **分析一致性** → 检查样式差异及未使用的元素
3. **生成报告** → 创建详细的发现结果和建议
4. **手动实施** → 根据发现结果指导设计改进

### 资产导出流程
1. **确定导出目标** → 指定要导出的帧、组件或节点
2. **配置导出设置** → 设置格式、尺寸及命名规则
3. **批量处理** → 同时导出多个资产
4. **组织输出** → 按格式或平台整理文件

### 分析与文档流程
1. **提取设计数据** → 提取组件、样式及设计元素
2. **审计合规性** → 检查可访问性和品牌一致性
3. **生成文档** → 创建样式指南和组件规范
4. **导出交付物** → 将资产打包以供开发或客户端使用

## 资源

### 脚本
- `figma_client.py`：完整的 Figma API 包装器，支持所有 REST 端点
- `export_manager.py`：支持多种格式和尺寸的专业资产导出工具
- `style_auditor.py**：设计系统分析及品牌一致性检查工具
- `accessibility_checker.py**：全面的 WCAG 合规性验证及报告工具

### 参考资料
- `figma-api-reference.md`：完整的 API 文档及示例
- `design-patterns.md`：UI 模式和组件最佳实践
- `accessibility-guidelines.md`：WCAG 合规性要求
- `export-formats.md`：资产导出选项及规范

### 资产文件
- `templates/design-system/`：预构建的组件库模板
- `templates/brand-kits/`：标准品牌指南结构
- `templates/wireframes/`：常见的布局模式和流程

## 集成示例

### 与开发工作流程的集成
```bash
# Generate design tokens for CSS
python scripts/export_manager.py export-tokens "file-key" --format css

# Create component documentation
python scripts/figma_client.py document-components "file-key" --output docs/
```

### 与品牌管理的集成
```bash
# Audit brand compliance in designs
python scripts/style_auditor.py audit-file "file-key" --brand-colors "#FF0000,#00FF00,#0000FF"

# Extract current brand colors for analysis
python scripts/figma_client.py extract-colors "file-key" --output brand-colors.json
```

### 与客户端交付物的集成
```bash
# Generate client presentation assets
python scripts/export_manager.py client-package "file-key" --template presentation

# Create development handoff assets
python scripts/export_manager.py dev-handoff "file-key" --include-specs
```

## 限制与范围

### 仅读操作
该工具通过 REST API 提供对 Figma 文件的 **仅读访问** 功能。它可以：
- ✅ 提取数据、组件和样式
- ✅ 以多种格式导出资产
- ✅ 分析和审计设计文件
- ✅ 生成全面报告

### 无法实现的功能
- ❌ **修改现有文件**（颜色、文本、组件）
- ❌ **创建新的设计或组件**
- ❌ **批量更新** 多个文件
- ❌ **实时协作** 功能

如需修改文件，您需要使用插件 API 开发一个 Figma 插件。

## 技术特性

### API 速率限制
内置速率限制和重试逻辑，以优雅地处理 Figma API 的限制。

### 错误处理
提供全面的错误处理机制，包括详细的日志记录和恢复建议。

### 多格式支持
支持将资产导出为 PNG、SVG、PDF 和 WEBP 格式，并支持平台特定的尺寸设置。