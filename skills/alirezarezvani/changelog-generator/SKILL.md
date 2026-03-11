---
name: "changelog-generator"
description: "**Changelog Generator**  
**简介：**  
Changelog Generator 是一个用于自动生成软件更新日志的工具。它能够根据代码库中的更改记录（如提交信息、修改内容等）生成结构化、易于阅读的更新日志文件。这种日志文件对于用户、开发者和维护人员来说都非常有用，因为它提供了软件版本演变的清晰记录。  
**主要功能：**  
1. **自动提取更改信息：** 从代码仓库（如 Git）中提取每次提交的详细信息，包括提交者、提交时间、修改内容等。  
2. **生成格式化日志：** 根据预设的格式模板，将提取的更改信息整理成标准的 Changelog 格式。  
3. **支持多种格式：** 支持多种 Changelog 格式，如 Markdown、HTML、JSON 等。  
4. **自定义模板：** 允许用户自定义日志的格式和样式，以满足特定需求。  
5. **集成到持续集成/持续部署（CI/CD）流程：** 可以轻松集成到自动化构建和部署流程中，确保每次发布时都会生成更新日志。  
**使用步骤：**  
1. **安装工具：** 从官方仓库下载并安装 Changelog Generator。  
2. **配置设置：** 根据需要配置工具的参数，如代码仓库地址、日志格式等。  
3. **运行脚本：** 运行脚本，工具会自动从代码库中提取更改信息并生成更新日志。  
4. **部署日志：** 将生成的日志文件部署到指定的位置（如网站、文档库等）。  
**示例：**  
假设你有一个名为 `my_project` 的 Git 仓库，你可以使用以下命令生成更新日志：  
```bash
changelog_generator --git-url https://github.com/user/my_project.git --output-format markdown
```  
这将生成一个名为 `changelog.md` 的文件，其中包含了 `my_project` 项目的所有更新记录。  
**优势：**  
- **提高效率：** 自动化生成更新日志，节省时间和精力。  
- **便于阅读：** 生成的日志格式清晰、结构化，便于用户理解软件的演变过程。  
- **增强透明度：** 为项目提供完整的版本历史记录，增强用户和团队的信任度。  
**适用场景：**  
- **软件开发项目：** 用于生成项目更新日志。  
- **技术文档：** 作为软件文档的一部分，提供详细的版本更新信息。  
- **持续集成/持续部署：** 确保每次发布时都有完整的更新记录。"
---
# 变更日志生成器（Change Log Generator）

**级别：** 高级（Powerful）  
**类别：** 工程（Engineering）  
**领域：** 发布管理 / 文档编制（Release Management / Documentation）

## 概述  
使用此工具可以从常规提交（Conventional Commits）中生成一致且可审核的发布说明。它将提交解析、语义版本升级逻辑（语义版本提升，如“major”、“minor”、“patch”）以及变更日志渲染分离出来，使团队能够自动化发布流程，同时保持编辑控制。

## 核心功能  
- 使用常规提交规则（Conventional Commit rules）解析提交信息  
- 从提交流中检测语义版本升级类型（`major`、`minor`、`patch`）  
- 生成变更日志条目（如“新增功能”、“修改内容”、“修复问题”等）  
- 根据Git范围或提供的提交信息生成发布条目  
- 通过专用代码检查工具（linter）确保提交格式正确  
- 支持通过机器可读的JSON格式进行持续集成（CI）集成  

## 使用场景  
- 在发布版本标签之前  
- 在持续集成过程中自动生成发布说明  
- 在代码审查（PR）过程中检查无效的提交信息格式  
- 在需要按包范围过滤变更日志的单个仓库（monorepo）中  
- 将原始Git历史记录转换为用户可读的说明  

## 关键工作流程  
### 1. 从Git生成变更日志条目  
```bash
python3 scripts/generate_changelog.py \
  --from-tag v1.3.0 \
  --to-tag v1.4.0 \
  --next-version v1.4.0 \
  --format markdown
```  

### 2. 从标准输入（stdin）或文件生成条目  
```bash
git log v1.3.0..v1.4.0 --pretty=format:'%s' | \
  python3 scripts/generate_changelog.py --next-version v1.4.0 --format markdown

python3 scripts/generate_changelog.py --input commits.txt --next-version v1.4.0 --format json
```  

### 3. 更新`CHANGELOG.md`文件  
```bash
python3 scripts/generate_changelog.py \
  --from-tag v1.3.0 \
  --to-tag HEAD \
  --next-version v1.4.0 \
  --write CHANGELOG.md
```  

### 4. 在合并前检查提交格式  
```bash
python3 scripts/commit_linter.py --from-ref origin/main --to-ref HEAD --strict --format text
```  

### 可选脚本  
- `python3 scripts/generate_changelog.py --help`  
  - 从Git或标准输入读取提交信息  
  - 生成Markdown或JSON格式的变更日志  
  - 可选：将新条目追加到现有变更日志中  
- `python3 scripts/commit_linter.py --help`  
  - 验证提交格式；在`--strict`模式下遇到问题时返回非零错误代码  

## 支持的常规提交类型  
- `feat`（新增功能）、`fix`（修复问题）、`perf`（性能优化）、`refactor`（重构）、`docs`（文档更新）、`test`（测试）、`build`（构建）、`ci`（持续集成相关）、`chore`（杂务）  
- `security`（安全相关）、`deprecated`（已弃用）、`remove`（删除内容）  

## 变更类型说明  
- **破坏性变更（Breaking Changes）**：`type(scope)!: summary`  
- 变更日志底部/正文必须包含“BREAKING CHANGE:”提示  

## 版本号映射规则  
- 破坏性变更 → `major`  
- 非破坏性新增功能 → `minor`  
- 其他所有变更 → `patch`  

## 脚本接口  
- `python3 scripts/generate_changelog.py --help`  
  - 从Git或标准输入读取提交信息  
  - 生成Markdown或JSON格式的变更日志  
  - 可选：将新条目追加到现有变更日志中  
- `python3 scripts/commit_linter.py --help`  
  - 验证提交格式；在`--strict`模式下遇到问题时返回非零错误代码  

## 常见问题  
1. 将合并提交信息与变更日志解析混淆  
2. 使用模糊的提交摘要，导致生成的变更日志无法用于发布说明  
3. 未为破坏性变更提供迁移指导  
4. 将文档更新或杂务类变更误认为是用户可用的功能  
5. 直接覆盖历史变更日志内容，而非将其添加到新日志中  

## 最佳实践  
1. 保持提交内容简洁明了，明确提交目的。  
2. 在多包仓库中为提交信息指定具体范围（例如：`feat(api)`。  
3. 在代码审查流程中强制执行代码格式检查。  
4. 在发布前审核生成的Markdown内容。  
5. 仅在变更日志生成成功后添加版本标签。  
6. 保留`[Unreleased]`部分，以便在需要时手动编辑变更日志。  

## 参考资料  
- [references/ci-integration.md](references/ci-integration.md)  
- [references/changelog-formatting-guide.md](references/changelog-formatting-guide.md)  
- [references/monorepo-strategy.md](references/monorepo-strategy.md)  
- [README.md](README.md)  

## 发布管理流程  
- 使用此流程确保发布过程的可预测性：  
  1. 对目标发布范围内的提交历史记录进行代码格式检查。  
  2. 从提交信息生成变更日志草稿。  
  3. 人工调整文本以确保清晰易懂。  
  4. 验证版本号升级的合理性。  
  5. 变更日志获得批准后才能添加版本标签。  

## 输出质量要求  
- 每个条目都应具有实际意义，避免包含无关实现细节。  
- 破坏性变更必须包含迁移指导信息。  
- 无内容的章节应被省略。  
- 同一章节中的重复条目应被删除。  

## 持续集成（CI）政策  
- 对所有代码请求（PR）执行`commit_linter.py --strict`检查。  
- 对无效的常规提交拒绝合并。  
- 在推送版本标签时自动生成发布说明草稿。  
- 在主分支上修改`CHANGELOG.md`前需经过人工审核。  

## 单个仓库（Monorepo）使用建议  
- 尽量使提交范围与包名保持一致。  
- 按包范围过滤提交信息，以便生成特定包的变更日志。  
- 将影响整个系统的变更记录在根目录下的变更日志中。  
- 将每个包的变更日志存储在对应的包目录下，便于管理。  

## 错误处理机制  
- 如果未找到有效的常规提交记录：提前终止流程，避免生成误导性的空变更日志。  
- 如果Git提交范围无效：在错误信息中明确指出问题。  
- 如果目标提交信息缺失：创建基本的变更日志结构。