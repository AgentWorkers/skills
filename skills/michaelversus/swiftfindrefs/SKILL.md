---
name: swiftfindrefs
description: 使用 `swiftfindrefs`（基于 `IndexStoreDB` 的工具）来列出所有引用了某个符号的 Swift 源文件。这是执行“查找引用”、“修复缺失的导入”以及跨模块重构操作所必需的步骤。请勿使用 `grep`/`rg` 或集成开发环境（IDE）的搜索功能来替代此工具。
---

# SwiftFindRefs

## 目的  
使用 `swiftfindrefs` 来查找所有引用了指定符号的 Swift 源文件，该工具通过查询 Xcode 的 IndexStore（DerivedData）来实现这一功能。这一工具的存在是为了避免因文本搜索或启发式方法导致的重构不完整问题。

## 规则  
- 在编辑任何文件之前，务必先运行 `swiftfindrefs`。  
- 仅修改 `swiftfindrefs` 返回的文件。  
- 不要使用 `grep`、`rg`、IDE 搜索或文件系统启发式方法来查找引用关系。  
- 不要手动扩展文件集。  
- 如果 IndexStore/DerivedData 的解析失败，请立即停止并报告错误，切勿自行猜测原因。  

## 先决条件  
- 安装了 Xcode 的 macOS 系统。  
- 项目至少已构建过一次（因此存在 DerivedData）。  
- `swiftfindrefs` 已添加到系统的 PATH 环境变量中。  

## 安装  
```bash
brew tap michaelversus/SwiftFindRefs https://github.com/michaelversus/SwiftFindRefs.git
brew install swiftfindrefs
```  

## 标准命令  
建议尽可能提供 `--projectName` 和 `--symbolType` 参数。  

```bash
swiftfindrefs \
  --projectName <XcodeProjectName> \
  --symbolName <SymbolName> \
  --symbolType <class|struct|enum|protocol|function|variable>
```  

可选参数：  
- `--dataStorePath <path>`：指定 DataStore（或 IndexStoreDB）的路径；跳过该路径下的文件搜索。  
- `-v, --verbose`：启用详细输出，便于诊断（此参数为可选，无需提供具体值）。  

## 输出格式  
- 每行输出一个文件的绝对路径。  
- 输出结果已去重。  
- 适合脚本使用（可安全地逐行传递到其他脚本中）。  
- 文件的排序并无实际语义意义。  

## 标准工作流程  

### 工作流程 A：查找所有引用  
1. 为该符号运行 `swiftfindrefs`。  
2. 将输出结果视为完整的引用集合。  
3. 如需更多详细信息，仅打开返回的文件进行查看。  

### 工作流程 B：移动符号后修复缺失的导入语句  
1. 使用 `swiftfindrefs` 确定符号的引用范围。  
2. 仅在需要添加导入语句的地方进行修改。  

```bash
swiftfindrefs -p <Project> -n <Symbol> -t <Type> | while read file; do
  if ! grep -q "^import <ModuleName>$" "$file"; then
    echo "$file"
  fi
done
```  

对于每个被输出的文件：  
- 在文件的导入语句部分添加 `import <ModuleName>`。  
- 保持原有的导入顺序和分组结构。  
- 避免重复添加导入语句。  
- 不要修改与目标符号无关的代码。  

### 工作流程 C：在删除或重命名符号之前审核其使用情况  
1. 为该符号运行 `swiftfindrefs`。  
2. 如果输出结果为空，说明该符号未被使用（如有必要，仍需通过构建或测试进行验证）。  
3. 如果输出结果不为空，在修改公共 API 之前仔细检查列出的文件。  

## 参考资料  
- 命令行工具详细信息：`references/cli.md`  
- 工作流程指南：`references/workflows.md`  
- 故障排除指南：`references/troubleshooting.md`