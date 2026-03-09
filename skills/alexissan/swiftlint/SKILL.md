---
name: swiftlint
emoji: "\U0001F9F9"
requires: swiftlint
install: brew install swiftlint
description: 通过 CLI 实现 Swift 代码的代码检查（linting）和样式规范（style enforcement）
---
# SwiftLint

SwiftLint 是一个用于通过静态分析来强制执行 Swift 代码风格和规范的工具。它支持对整个项目进行代码检查，自动修复可修复的违规问题，管理检查规则，并能与 Xcode 和持续集成（CI）系统集成——所有这些都可以通过命令行（CLI）来完成。

---

## 验证安装

```bash
swiftlint version
```

如果尚未安装：

```bash
brew install swiftlint
```

或者通过 Mint 安装：

```bash
mint install realm/SwiftLint
```

或者作为 Swift Package Manager 的插件（添加到 `Package.swift` 中）：

```swift
.package(url: "https://github.com/realm/SwiftLint.git", from: "0.57.0")
```

然后运行：

```bash
swift package plugin swiftlint
```

---

## 基本用法

### 检查当前目录的代码

```bash
swiftlint
```

该命令会递归地检查当前目录下的所有 `.swift` 文件。

### 检查特定路径的代码

```bash
swiftlint lint --path Sources/
```

### 检查特定文件

```bash
swiftlint lint --path Sources/App/ViewModel.swift
```

### 从标准输入读取文件进行检查

```bash
cat MyFile.swift | swiftlint lint --use-stdin --quiet
```

> **使用建议：** 当用户请求“检查我的代码风格”或“对 Swift 代码进行代码检查”时，请从项目根目录运行 `swiftlint`。如果用户指定了具体的文件或文件夹，可以使用 `--path` 参数。

---

## 自动修复

SwiftLint 可以自动修复某些违规问题。

### 修复所有可自动修复的违规问题

```bash
swiftlint --fix
```

### 修复特定路径的代码

```bash
swiftlint --fix --path Sources/
```

### 修复特定文件

```bash
swiftlint --fix --path Sources/App/ViewModel.swift
```

### 预览修复结果（干运行）

先运行检查以查看违规情况，然后再进行修复：

```bash
swiftlint lint --path Sources/ && swiftlint --fix --path Sources/
```

> **使用建议：** 在自动修复之前，务必先运行检查，以便用户了解哪些地方会发生变化。有些违规问题是无法自动修复的——修复后需要单独报告这些问题。

---

## 输出格式

### 默认格式（人类可读）

```bash
swiftlint
```

输出示例：`Sources/App.swift:12:1: warning: Line Length Violation: ...`

### JSON 格式

```bash
swiftlint lint --reporter json
```

### CSV 格式

```bash
swiftlint lint --reporter csv
```

### Checkstyle（XML 格式）

```bash
swiftlint lint --reporter checkstyle
```

### GitHub Actions 格式

```bash
swiftlint lint --reporter github-actions-logging
```

### Xcode 摘要（plist 格式）

```bash
swiftlint lint --reporter xcode-summary
```

### SonarQube 格式

```bash
swiftlint lint --reporter sonarqube
```

### Markdown 格式

```bash
swiftlint lint --reporter markdown
```

### 将结果保存到文件

```bash
swiftlint lint --reporter json > swiftlint-results.json
```

### 所有可用的报告格式

| 报告格式 | 适用场景 |
| --- | --- |
| `xcode` | 适用于 Xcode 的格式（默认） | 本地开发 |
| `json` | JSON 数组 | 程序化处理 |
| `csv` | CSV | 电子表格分析 |
| `checkstyle` | XML | Jenkins、CI 工具 |
| `codeclimate` | Code Climate JSON | Code Climate 集成 |
| `github-actions-logging` | GitHub 注释 | GitHub Actions CI |
| `sonarqube` | SonarQube JSON | SonarQube 集成 |
| `markdown` | Markdown 表格 | PR 评论 |
| `emoji` | 带有表情符号的格式 | 适用于终端输出 |
| `html` | HTML 报告 | 浏览器查看 |
| `junit` | JUnit XML | 测试报告工具 |
| `xcode-summary` | Plist | Xcode 构建摘要 |

> **使用建议：** 当需要程序化解析结果时，使用 `--reporter json`。在 GitHub Actions 中使用 `--reporter github-actions-logging` 可以在 PR 评论中显示详细信息。

---

## 规则

### 查看所有规则

```bash
swiftlint rules
```

### 搜索特定规则

```bash
swiftlint rules | grep "force_cast"
```

### 显示规则详细信息

```bash
swiftlint rules force_cast
```

### 规则标识符快速参考

SwiftLint 的规则分为几类：

**默认启用（常见规则）**

| 规则 | 检查内容 |
| --- | --- |
| `line_length` | 行长度超过限制（默认为 120，超过则显示警告；超过 200 则显示错误） |
| `trailing_whitespace` | 行尾的空白字符 |
| `trailing_newline` | 缺少或多余的行尾换行符 |
| `opening_brace` | 开括号的放置位置 |
| `closing_brace` | 关括号的放置位置 |
| `colon` | 冒号的使用（例如，`let x : Int` 应该写成 `let x: Int`） |
| `comma` | 逗号的使用 |
| `force_cast` | 使用 `as!` 进行强制类型转换 |
| `force_try` | 使用 `try!` 进行强制尝试 |
| `force_unwrapping` | 在可选变量上使用 `!` 进行解包 |
| `type_body_length` | 类型体的长度超过限制 |
| `function_body_length` | 函数体的长度超过限制 |
| `file_length` | 文件的总长度超过限制 |
| `cyclomatic_complexity` | 代码的循环复杂度过高 |
| `nesting` | 代码嵌套层次过深 |
| `identifier_name` | 变量/函数名的命名规范问题 |
| `type_name` | 类型名的命名规范问题 |
| `unused_import` | 未使用的导入语句（可选） |
| `unuseddeclaration` | 未使用的声明（可选） |
| `vertical_whitespace` | 过多的空行 |
| `todo` | `TODO/FIXME` 注释会被视为警告 |
| `mark` | `MARK` 注释的格式不正确 |
| `void_return` | 显式写 `-> Void` 而不是 `-> ()` |
| `syntactic_sugar` | 应优先使用 `[Int]` 而不是 `Array<Int>` |
| `redundant_optional_initialization` | `var x: Int? = nil`（`nil` 是默认值） |
| `redundant_string_enum_value` | 枚举值的名称与实际值相同 |

**需要手动启用的规则（必须明确启用）**

| 规则 | 检查内容 |
| --- | --- |
| `explicit_type_interface` | 缺少显式的类型注解 |
| `missing_docs` | 缺少文档注释 |
| `multiline_arguments` | 多行函数调用格式问题 |
| `multiline_parameters` | 多行函数参数格式问题 |
| `vertical_parameter_alignment` | 参数在声明中的对齐问题 |
| `sorted_imports` | 导入语句未排序 |
| `file_header` | 文件头缺失或格式不正确 |
| `accessibility_label_for_image` | 图片缺少可访问性标签 |
| `accessibility_trait_for_button` | 按钮缺少可访问性属性 |
| `strict_fileprivate` | 应优先使用 `private` 而不是 `fileprivate` |
| `prohibited_interface_builder` | 在 Storyboard/XIB 中使用不允许的接口 |
| `no_magic_numbers` | 代码中存在魔术数字 |
| `prefer_self_in_static_references` | 在静态引用中优先使用 `Self` 而不是具体的类型名 |
| `balanced_xctest_lifecycle` | `setUp` 方法没有 `tearDown` 方法 |
| `test_case_accessibility` | 测试方法没有正确标记 |

> **使用建议：** 为新项目设置 SwiftLint 时，先使用默认规则，仅添加用户明确请求的额外规则。避免一次性启用所有规则。

---

## 配置文件（.swiftlint.yml）

SwiftLint 会读取当前目录（或其父目录）下的 `.swiftlint.yml` 文件。

### 生成默认配置

虽然没有内置的配置生成工具，但以下是一个简单的配置示例：

```yaml
# .swiftlint.yml

# Paths to include (default: all Swift files)
included:
  - Sources
  - Tests

# Paths to exclude
excluded:
  - Pods
  - DerivedData
  - .build
  - Packages

# Disable specific rules
disabled_rules:
  - todo
  - trailing_whitespace

# Enable opt-in rules
opt_in_rules:
  - sorted_imports
  - unused_import
  - missing_docs

# Configure specific rules
line_length:
  warning: 120
  error: 200
  ignores_comments: true
  ignores_urls: true

type_body_length:
  warning: 300
  error: 500

file_length:
  warning: 500
  error: 1000

function_body_length:
  warning: 50
  error: 100

identifier_name:
  min_length:
    warning: 2
    error: 1
  max_length:
    warning: 50
    error: 60
  excluded:
    - id
    - x
    - y
    - i
    - j
    - ok

type_name:
  min_length:
    warning: 3
    error: 0
  max_length:
    warning: 50
    error: 60

cyclomatic_complexity:
  warning: 10
  error: 20

nesting:
  type_level:
    warning: 2
  function_level:
    warning: 3
```

### 使用自定义路径的配置文件

```bash
swiftlint lint --config path/to/.swiftlint.yml
```

### 多个配置文件（子配置）

```yaml
# Feature/.swiftlint.yml — inherits parent config and overrides
child_config: ../.swiftlint.yml

disabled_rules:
  - force_cast
```

### 父配置文件（继承自其他配置）

```yaml
# .swiftlint.yml
parent_config: shared/.swiftlint-base.yml
```

### 远程配置文件

```yaml
parent_config: https://raw.githubusercontent.com/org/repo/main/.swiftlint.yml
```

> **使用建议：** 如果项目已经存在 `.swiftlint.yml` 文件，请在建议修改之前先读取该文件。建议修改现有配置文件，而不是创建新的配置文件。

---

## 逐行/代码块禁用规则

### 禁用某行的特定规则

```swift
let value = dict["key"] as! String // swiftlint:disable:this force_cast
```

### 禁用某代码块的特定规则

```swift
// swiftlint:disable force_cast
let a = x as! String
let b = y as! Int
// swiftlint:enable force_cast
```

### 禁用整个代码块的规则

```swift
// swiftlint:disable all
// Legacy code that can't be refactored yet
// swiftlint:disable:enable all
```

### 仅禁用下一行

```swift
// swiftlint:disable:next force_cast
let value = dict["key"] as! String
```

### 仅禁用上一行

```swift
let value = dict["key"] as! String
// swiftlint:disable:previous force_cast
```

> **使用建议：** 尽量使用针对特定行的禁用选项（如 `disable:this`、`disable:next`），而不是全局禁用整个代码块。除非用户处理的是自动生成的代码或旧代码，并且明确表示不希望进行代码检查，否则不要建议使用 `disable all`。

---

## 与 Xcode 的集成

### 在构建阶段运行 SwiftLint

在 Xcode 的构建阶段中添加一个运行脚本：

```bash
if command -v swiftlint >/dev/null 2>&1; then
  swiftlint
else
  echo "warning: SwiftLint not installed, download from https://github.com/realm/SwiftLint"
fi
```

### 带有自动修复功能的构建阶段

```bash
if command -v swiftlint >/dev/null 2>&1; then
  swiftlint --fix && swiftlint
fi
```

### 作为 Swift Package 的插件（Xcode 15+）

如果将 SwiftLint 作为包依赖项添加：

```bash
swift package plugin swiftlint
```

或者在 Xcode 中：右键点击项目 → 选择 “SwiftLintBuildToolPlugin”。

> **使用建议：** 对于现代项目（Xcode 15 及更高版本），建议使用 SPM 插件，因为它可以将 SwiftLint 的版本固定在项目中，无需单独安装。

---

## 与持续集成（CI）的集成

### GitHub Actions

```yaml
- name: SwiftLint
  run: |
    brew install swiftlint
    swiftlint lint --reporter github-actions-logging --strict
```

仅针对已更改的文件进行代码检查：

```yaml
- name: SwiftLint Changed Files
  run: |
    git diff --name-only --diff-filter=d origin/main...HEAD -- '*.swift' | \
    xargs -I{} swiftlint lint --path {} --reporter github-actions-logging --strict
```

### Bitrise

```yaml
- script:
    inputs:
    - content: |
        brew install swiftlint
        swiftlint lint --strict
```

### Jenkins（结合 Checkstyle）

```bash
swiftlint lint --reporter checkstyle > swiftlint-checkstyle.xml
```

然后使用 Checkstyle 插件解析 `swiftlint-checkstyle.xml` 文件。

---

## 分析检查结果

### 按规则统计违规数量

```bash
swiftlint lint --reporter json | python3 -c "
import json, sys, collections
data = json.load(sys.stdin)
counts = collections.Counter(v['rule_id'] for v in data)
for rule, count in counts.most_common():
    print(f'{count:>5}  {rule}')
"
```

### 仅显示错误（不显示警告）

```bash
swiftlint lint --strict 2>&1 | grep "error:"
```

### 严格模式（警告也会被视为错误）

```bash
swiftlint lint --strict
```

在这种模式下，SwiftLint 会在遇到任何违规时返回非零的退出代码（而不仅仅是错误）。

### 静默模式（仅显示错误）

```bash
swiftlint lint --quiet
```

这种模式下，输出中只会显示错误，忽略警告。

### 通过 CLI 启用/禁用特定规则

```bash
swiftlint lint --enable-rules sorted_imports,unused_import
swiftlint lint --disable-rules todo,trailing_whitespace
```

---

## 定义自定义规则

可以在 `.swiftlint.yml` 文件中定义基于正则表达式的自定义规则：

```yaml
custom_rules:
  no_print_statements:
    name: "No Print Statements"
    regex: "\\bprint\\s*\\("
    message: "Use os_log or Logger instead of print()"
    severity: warning
    match_kinds:
      - identifier

  no_hardcoded_strings:
    name: "No Hardcoded Strings in Views"
    regex: "Text\\(\"[^\"]+\"\\)"
    message: "Use LocalizedStringKey or String(localized:) for user-facing text"
    severity: warning
    included: ".*View\\.swift"

  no_force_unwrap_iboutlet:
    name: "No Force Unwrap IBOutlet"
    regex: "@IBOutlet\\s+(weak\\s+)?var\\s+\\w+:\\s+\\w+!"
    message: "Use optional IBOutlets to avoid crashes"
    severity: error

  accessibility_identifier_required:
    name: "Accessibility Identifier"
    regex: "\\.accessibilityIdentifier\\("
    message: "Good — accessibilityIdentifier found"
    severity: warning
    match_kinds:
      - identifier

  prefer_logger_over_print:
    name: "Prefer Logger"
    regex: "\\bNSLog\\s*\\("
    message: "Use Logger (os.Logger) instead of NSLog"
    severity: warning
```

### 规则类型及匹配内容

| 规则类型 | 匹配内容 |
| --- | --- |
| `identifier` | 变量/函数名 |
| `string` | 字符串字面量 |
| `comment` | 注释 |
| `keyword` | Swift 关键字 |
| `typeidentifier` | 类型名 |
| `number` | 数字字面量 |
| `parameter` | 函数参数 |
| `argument` | 函数参数 |

> **使用建议：** 自定义规则非常强大，但基于正则表达式，因此可能会产生误报。在建议将自定义规则永久添加到项目中之前，务必先在代码库中测试它们。

---

## 常见命令参数说明

| 参数 | 作用 |
| --- | --- |
| `--path <path>` | 检查特定文件或目录 |
| `--config <path>` | 使用自定义配置文件 |
| `--reporter <name>` | 输出格式（如 json、csv 等） |
| `--strict` | 将警告视为错误 |
| `--quiet` | 仅显示错误 |
| `--fix` | 自动修复可修复的违规问题 |
| `--enable-rules <rules>` | 启用特定规则（用逗号分隔） |
| `--disable-rules <rules>` | 禁用特定规则（用逗号分隔） |
| `--use-stdin` | 从标准输入读取 Swift 代码 |
| `--force-exclude` | 即使指定了文件路径也忽略该文件 |
| `--cache-path <path>` | 自定义缓存目录 |
| `--no-cache` | 禁用缓存 |
| `--use-alternative-excluding` | 使用替代的文件排除方法 |
| `--in-process-sourcekit` | 使用内置的 SourceKit 进行代码分析 |
| `--compiler-log-path` | Xcodebuild 日志文件的路径 |
| `--progress` | 显示进度条 |

---

## 常见工作流程

### 为新项目设置 SwiftLint

```bash
# 1. Install
brew install swiftlint

# 2. Run initial lint to see baseline
swiftlint lint --path Sources/ --reporter json > baseline.json

# 3. Create config based on results
cat > .swiftlint.yml << 'EOF'
included:
  - Sources
  - Tests
excluded:
  - Pods
  - DerivedData
  - .build
disabled_rules:
  - todo
opt_in_rules:
  - sorted_imports
  - unused_import
line_length:
  warning: 120
  error: 200
  ignores_urls: true
EOF

# 4. Fix autocorrectable issues
swiftlint --fix --path Sources/

# 5. Re-lint to see remaining issues
swiftlint
```

### 在提交 Pull Request（PR）之前修复所有问题

```bash
# Autocorrect what we can
swiftlint --fix

# Check what remains
swiftlint lint --strict
```

### 仅检查已更改的文件

```bash
git diff --name-only --diff-filter=d origin/main...HEAD -- '*.swift' | \
  xargs -I{} swiftlint lint --path {} --strict
```

### 比较不同分支之间的违规数量

```bash
# Current branch count
CURRENT=$(swiftlint lint --quiet 2>&1 | wc -l | tr -d ' ')

# Main branch count
git stash
git checkout main
MAIN=$(swiftlint lint --quiet 2>&1 | wc -l | tr -d ' ')
git checkout -
git stash pop

echo "main: $MAIN violations, current: $CURRENT violations"
```

---

## 故障排除

### 常见问题及解决方法

| 错误 | 解决方案 |
| --- | --- |
| 未找到可检查的文件 | 检查配置文件中的 `included` 路径，或从项目根目录运行脚本 |
| 配置无效 | 验证 `.swiftlint.yml` 文件中的 YAML 语法是否正确 |
| 未找到 SourceKit | 运行 `sudo xcode-select -s /Applications/Xcode.app` |
| 规则未找到 | 使用 `swiftlint rules` 命令查看规则名称（某些规则可能是可选的） |
| 检查速度过慢 | 为 Pods/DerivedData 目录添加 `excluded` 路径，或使用 `--cache-path` 参数 |
| **性能提示：**
  - 始终在配置文件中排除 `Pods/`, `DerivedData/`, `.build/`, `Packages/` 目录 |
  - 使用 `--cache-path` 选项在多次 CI 运行之间保留缓存 |
  - 在 CI 中仅检查已更改的文件，而不是整个项目 |
  - 仅在遇到意外结果时使用 `--no-cache` 选项 |

---

## 注意事项

### 使用建议

> 当用户请求“清理代码风格”或“修复代码风格”时，先运行 `swiftlint --fix`，然后再运行 `swiftlint lint` 以获取剩余的违规列表。
> 在将 SwiftLint 添加到现有项目之前，先运行 `swiftlint lint --reporter json` 以评估违规数量。如果违规数量很多，建议分阶段处理：先修复可自动修复的问题，然后再按类别处理其他问题。
> 在创建新的 `.swiftlint.yml` 文件之前，务必检查是否存在现有的配置文件。阅读该文件以了解团队的代码风格偏好。
> 对于需要支持可访问性的项目（所有项目都应如此），建议启用 `accessibility_label_for_image` 和 `accessibility_trait_for_button` 规则。
> 如果项目使用了 SwiftUI，建议定义一个自定义规则来检查 `Text()` 视图中的硬编码字符串——所有用户可见的字符串都应使用 `String(localized:)` 进行本地化处理。
> `--strict` 参数在 CI 中非常重要：如果不使用该参数，即使有警告，SwiftLint 也会返回 0，这意味着 CI 流程无法检测到代码风格的变更。