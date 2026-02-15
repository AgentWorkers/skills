---
name: shortcuts-generator
description: 通过创建 `.plist` 文件来生成 macOS/iOS 快捷方式。适用于需要创建快捷方式、自动化工作流程、构建 `.shortcut` 文件或生成快捷方式 `.plist` 的场景。涵盖了 1,155 个操作（427 个 WF*Actions + 728 个 AppIntents）、变量引用以及控制流。
allowed-tools: Write, Bash
---

# macOS 快捷方式生成器

生成可签名并导入到 Apple 的 Shortcuts 应用程序中的有效 `.shortcut` 文件。

## 快速入门

快捷方式是一种具有以下结构的二进制 plist 文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>WFWorkflowActions</key>
    <array>
        <!-- Actions go here -->
    </array>
    <key>WFWorkflowClientVersion</key>
    <string>2700.0.4</string>
    <key>WFWorkflowHasOutputFallback</key>
    <false/>
    <key>WFWorkflowIcon</key>
    <dict>
        <key>WFWorkflowIconGlyphNumber</key>
        <integer>59511</integer>
        <key>WFWorkflowIconStartColor</key>
        <integer>4282601983</integer>
    </dict>
    <key>WFWorkflowImportQuestions</key>
    <array/>
    <key>WFWorkflowMinimumClientVersion</key>
    <integer>900</integer>
    <key>WFWorkflowMinimumClientVersionString</key>
    <string>900</string>
    <key>WFWorkflowName</key>
    <string>My Shortcut</string>
    <key>WFWorkflowOutputContentItemClasses</key>
    <array/>
    <key>WFWorkflowTypes</key>
    <array/>
</dict>
</plist>
```

### 最简单的“Hello World”示例

```xml
<dict>
    <key>WFWorkflowActionIdentifier</key>
    <string>is.workflow.actions.gettext</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key>
        <string>A1B2C3D4-E5F6-7890-ABCD-EF1234567890</string>
        <key>WFTextActionText</key>
        <string>Hello World!</string>
    </dict>
</dict>
<dict>
    <key>WFWorkflowActionIdentifier</key>
    <string>is.workflow.actions.showresult</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>Text</key>
        <dict>
            <key>Value</key>
            <dict>
                <key>attachmentsByRange</key>
                <dict>
                    <key>{0, 1}</key>
                    <dict>
                        <key>OutputName</key>
                        <string>Text</string>
                        <key>OutputUUID</key>
                        <string>A1B2C3D4-E5F6-7890-ABCD-EF1234567890</string>
                        <key>Type</key>
                        <string>ActionOutput</string>
                    </dict>
                </dict>
                <key>string</key>
                <string>￼</string>
            </dict>
            <key>WFSerializationType</key>
            <string>WFTextTokenString</string>
        </dict>
    </dict>
</dict>
```

## 核心概念

### 1. 动作（Actions）
每个动作都包含以下内容：
- **标识符（Identifier）**：`isworkflow.actions.<name>`（例如，`isworkflow.actions.showresult`）
- **参数（Parameters）**：在 `WFWorkflowActionParameters` 中定义的特定于动作的配置
- **UUID（UUID）**：用于引用此动作输出的唯一标识符

### 2. 变量引用（Variable References）
要使用上一个动作的输出：
1. 源动作需要一个 `UUID` 参数
2. 在 `attachmentsByRange` 字典中使用 `OutputUUID` 来引用该输出
3. 在需要插入变量的字符串中使用 `￼`（U+FFFC）作为占位符
4. 将 `WFSerializationType` 设置为 `WFTextTokenString`

### 3. 控制流（Control Flow）
控制流动作（如重复、条件判断、菜单操作）使用以下内容：
- **分组标识符（GroupingIdentifier）**：用于链接开始/中间/结束动作的 UUID
- **WFControlFlowMode**：0=开始，1=中间（其他/分支），2=结束

## 常见动作快速参考

| 动作 | 标识符 | 关键参数 |
|--------|------------|----------------|
| 显示文本 | `isworkflow.actions.gettext` | `WFTextActionText` |
| 显示结果 | `isworkflow.actions.showresult` | `Text` |
| 请求输入 | `isworkflow.actions.ask` | `WFAskActionPrompt`, `WFInputType` |
| 使用 AI 模型 | `isworkflow.actions.askllm` | `WFLLMPrompt`, `WFLLMModel`, `WFGenerativeResultType` |
| 评论 | `isworkflow.actions.comment` | `WFCommentActionText` |
| URL | `isworkflow.actions.url` | `WFURLActionURL` |
| 下载 URL 内容 | `isworkflow.actions.downloadurl` | `WFURL`, `WFHTTPMethod` |
| 获取天气信息 | `isworkflow.actions.weather.currentconditions` | （无需参数） |
| 打开应用程序 | `isworkflow.actions.openapp` | `WFAppIdentifier` |
| 打开 URL | `isworkflow.actions.openurl` | `WFInput` |
| 弹出警告 | `isworkflow.actions.alert` | `WFAlertActionTitle`, `WFAlertActionMessage` |
| 发送通知 | `isworkflow.actionsnotification` | `WFNotificationActionTitle`, `WFNotificationActionBody` |
| 设置变量 | `isworkflow.actions.setvariable` | `WFVariableName`, `WFInput` |
| 获取变量值 | `isworkflow.actions.getvariable` | `WFVariable` |
| 输入数字 | `isworkflow.actions.number` | `WFNumberActionNumber` |
| 列出项目 | `isworkflow.actions.list` | `WFItems` |
| 创建字典 | `isworkflow.actions.dictionary` | `WFItems` |
| 重复执行（指定次数） | `isworkflow.actions.repeat.count` | `WFRepeatCount`, `GroupingIdentifier`, `WFControlFlowMode` |
| 逐个重复执行 | `isworkflow.actions.repeat.each` | `WFInput`, `GroupingIdentifier`, `WFControlFlowMode` |
| 条件判断 | `isworkflow.actions.conditional` | `WFInput`, `WFCondition`, `GroupingIdentifier`, `WFControlFlowMode` |
| 从菜单中选择 | `isworkflow.actions.choosefrommenu` | `WFMenuPrompt`, `WFMenuItems`, `GroupingIdentifier`, `WFControlFlowMode` |
| 查找照片 | `isworkflow.actions.filter.photos` | `WFContentItemFilter`（详见 FILTERS.md） |
| 删除照片 | `isworkflow.actions.deletephotos` | `photos`（**注意**：此处不需要 `WFInput` 参数！）

## 详细参考文档

有关完整文档，请参阅：
- [PLIST_FORMAT.md](PLIST_FORMAT.md) - 完整的 plist 结构
- [ACTIONS.md](ACTIONS.md) - 所有 427 个 WF*Action 的标识符和参数
- [APPINTENTS.md](APPINTENTS.md) - 所有 728 个 AppIntent 动作
- [PARAMETER_TYPES.md](PARAMETER_TYPES.md) - 所有参数类型和序列化格式
- [VARIABLES.md](VARIABLES.md) - 变量引用系统
- [CONTROL_FLOW.md](CONTROL_FLOW.md) - 重复、条件判断、菜单操作的模式
- [FILTERS.md](FILTERS.md) - 用于查找/过滤动作的内容过滤器（照片、文件等）
- [EXAMPLES.md](EXAMPLES.md) - 完整的示例代码

## 快捷方式的签名

在导入之前，必须对快捷方式文件进行签名。可以使用 macOS 的 `shortcuts` 命令行工具来完成签名：

```bash
# Sign for anyone to use
shortcuts sign --mode anyone --input MyShortcut.shortcut --output MyShortcut_signed.shortcut

# Sign for people who know you
shortcuts sign --mode people-who-know-me --input MyShortcut.shortcut --output MyShortcut_signed.shortcut
```

签名流程如下：
1. 将 plist 文件以 XML 格式写入 `.shortcut` 文件中
2. 运行 `shortcuts sign` 命令添加加密签名（签名文件大小会增加约 19KB）
3. 签名后的文件即可导入到 Shortcuts.app 中

## 创建快捷方式的步骤：
1. **定义动作**：指定快捷方式的功能
2. **生成 UUID**：每个产生输出的动作都需要一个唯一的 UUID
3. **构建动作数组**：为每个动作创建包含标识符和参数的字典
4. **建立变量引用**：使用 `OutputUUID` 将输出与输入关联起来
5. **封装成 plist 文件**：添加包含图标、名称和版本的根结构
6. **保存文件**：将文件保存为 `.shortcut` 格式（XML 或其他格式均可）
7. **签名**：运行 `shortcuts sign` 命令使文件可导入

## 重要规则：
1. **UUID 必须为大写**：格式为 `A1B2C3D4-E5F6-7890-ABCD-EF1234567890`
2. **WFControlFlowMode 必须是整数**：使用 `<integer>0</integer>` 而不是 `<string>0</string>`
3. **范围键的格式**：使用 `{position, length}`，例如 `{0, 1}` 表示获取第一个字符
4. **占位符字符**：使用 `￼`（U+FFFC）来标记变量插入的位置
5. **控制流需要匹配的结束动作**：每个重复/条件判断/菜单操作都需要一个具有相同 `GroupingIdentifier` 的结束动作