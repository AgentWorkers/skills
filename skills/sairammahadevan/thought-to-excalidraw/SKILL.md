---
name: pm-visualizer
description: 将产品经理的想法（包括“为什么这样做”、“具体做什么”、“如何实现”以及“用户使用流程”）可视化，并生成一个可编辑的 Excalidraw 图表。当用户要求“将产品规格可视化”、“创建产品经理用图”或“梳理产品开发思路”时，可以使用此功能。
---

# PM Visualizer 技能

该技能可以将产品经理的非结构化思维转化为结构化的 Excalidraw 可视化图表。

## 特点
- **智能布局**：自动划分“为什么（Why）”、“是什么（What）”和“如何实现（How）”三个部分，并为“用户流程（User Journey）”创建横向布局。
- **颜色编码**：通过颜色区分问题（黄色）、解决方案（绿色）、实现方式（蓝色）以及流程（红色/粉色）。
- **元素分组**：文本会正确地绑定到相应的容器中，确保它们在图表中保持一致的位置。

## 工作流程

1. **分析需求**：从用户的请求或背景信息中提取以下内容：
    *   **标题**：功能或产品的名称。
    *   **问题**：问题描述、业务目标，或“我们为什么要开发这个功能？”。
    *   **解决方案**：功能需求或具体实现细节。
    *   **实现方式**：技术实现细节、API 策略，或“我们将如何实现它？”。
    *   **用户流程**：用户操作步骤的顺序列表。

2. **准备数据**：创建一个 JSON 文件（例如 `temp_visual_data.json`），其结构如下：
    ```json
    {
      "title": "Feature Name",
      "why": ["Reason 1", "Reason 2"],
      "what": ["Feature 1", "Feature 2"],
      "how": ["Tech 1", "Tech 2"],
      "journey": ["Step 1", "Step 2", "Step 3"]
    }
    ```

3. **生成图表**：运行 Python 脚本以生成 `.excalidraw` 文件。
    ```bash
    python3 skills/pm-visualizer/scripts/layout_diagram.py temp_visual_data.json ~/Downloads/Documents/PM_Visuals/Output_Name.excalidraw
    ```
    * 确保输出目录已经存在。*

4. **清理临时文件**：删除临时生成的 JSON 输入文件。

5. **通知用户**：告知用户图表已生成，并提供输出路径。

## 示例

**用户请求：**“将新的‘使用 Google 登录’功能可视化。**原因：**减少登录流程的复杂性。**具体实现：**在登录页面上添加 Google 登录按钮。**实现方式：**使用 OAuth2 协议。**用户流程：**用户点击按钮 → 显示 Google 登录弹窗 → 重定向到仪表板。**

**操作步骤：**
1. 创建 `login_spec.json` 文件：
    ```json
    {
      "title": "Login with Google",
      "why": ["Reduce friction", "Increase conversion"],
      "what": ["Google Sign-in Button", "Profile Sync"],
      "how": ["OAuth 2.0 Flow", "Google Identity SDK"],
      "journey": ["User clicks 'Sign in with Google'", "Google permissions popup appears", "User approves access", "System verifies token", "User redirected to Dashboard"]
    }
    ```
2. 在 `~/Downloads/Documents/PM_Visuals` 目录下创建一个新的文件夹。
3. 运行以下命令生成图表：
    `python3 skills/pm-visualizer/scripts/layout_diagram.py login_spec.json ~/Downloads/Documents/PM_Visuals/Login_Spec.excalidraw`