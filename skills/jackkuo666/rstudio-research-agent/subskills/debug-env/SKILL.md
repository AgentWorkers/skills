---
name: debug-r-env
description: 检查是否缺少 R 包，解决库冲突，验证 R 版本的兼容性，并针对环境问题提出解决方案。
---
# 调试R环境

这是一项专门用于排查和解决R环境问题的子技能，包括包缺失、版本冲突以及配置问题等。

## 概述

该子技能用于诊断并解决常见的R环境问题，这些问题可能导致脚本无法正常运行。它会分析R的安装情况、包的依赖关系以及系统配置。

当用户需要执行以下操作时，可以使用该子技能：
- 检查是否安装了所需的包
- 解决包版本冲突
- 修复“找不到包”的错误
- 验证R版本的兼容性
- 调试库路径问题
- 排查编译失败的原因

---

## 该子技能的功能

当被调用时，该子技能将执行以下操作：
1. **分析R环境**：
   - 检查R的版本和平台
   - 列出已安装的包及其版本
   - 检查库路径
   - 验证包的依赖关系
2. **识别缺失的包**：
   - 扫描脚本中的`library()`和`require()`调用
   - 检查Bioconductor包
   - 检测GitHub上的包依赖关系
   - 识别版本不匹配的问题
3. **诊断冲突**：
   - 查找包被其他包覆盖的情况
   - 识别不兼容的版本
   - 确定系统依赖关系
   - 检查编译所需的条件
4. **提供解决方案**：
   - 生成安装命令
   - 建议更新包版本
   - 推荐重新初始化`renv`环境
   - 提供故障排除步骤

---

## 用户示例请求：
- “我的R脚本显示‘找不到包’”
- “检查是否安装了用于RNA-seq分析的所有包”
- “修复我的R环境——ggplot2无法加载”
- “为什么DESeq2会报错？”
- “调试我项目中的包依赖关系”
- “安装我分析所需的所有包”

---

## 诊断检查：
### 环境扫描
```r
# R version and platform
version
R.version.string

# Library paths
.libPaths()

# Installed packages
installed.packages()[,c("Package", "Version")]

# Package conflicts
sessionInfo()
conflicts()
```

### 缺失包检测
```r
# Scan scripts for library() calls
grep("library\\(|require\\(", scripts, value = TRUE)

# Check if packages are installed
is_installed <- function(pkg) {
  require(pkg, quietly = TRUE, character.only = TRUE)
}
```

### 依赖关系解决
```r
# Check package dependencies
tools::package_dependencies()

# Verify installation
packageVersion("ggplot2")

# Check for updates
old.packages()
```

---

## 常见问题及解决方案：
| 问题 | 诊断 | 解决方案 |
|------|-------|---------|
| “没有名为‘pkgname’的包” | 包未安装 | `install.packages("pkgname")` |
| 未找到Bioconductor包 | Bioconductor未配置 | `BiocManager::install("pkgname")` |
| 包被其他包覆盖 | 命名空间冲突 | 显式使用`library(pkgname)` |
| 编译错误 | 缺少系统依赖库 | 安装系统构建工具 |
| 版本不匹配 | 该包需要更高版本的R | 更新R或使用旧版本包 |
| `renv`初始化失败 | `renv.lock`文件损坏 | 删除并重新生成`renv.lock` |

---

## 安装命令生成器

根据不同的包来源，该子技能会生成相应的安装命令：
### CRAN包
```r
install.packages("package_name")
```

### Bioconductor包
```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("package_name")
```

### GitHub包
```r
remotes::install_github("username/package")
# or
devtools::install_github("username/package")
```

### 多个包
```r
packages <- c("tidyverse", "ggplot2", "dplyr")
install.packages(packages)
```

---

## 特定分析领域的包列表：
### 差异表达分析：
- DESeq2
- edgeR
- limma
- EnhancedVolcano
- pheatmap

### 统计建模：
- lme4
- broom
- car
- emmeans
- multcomp

### 数据可视化：
- ggplot2
- patchwork
- scales
- cowplot
- viridis

### 生物信息学：
- Biostrings
- GenomicRanges
- biomaRt
- AnnotationDbi

---

## 参数：
| 参数 | 描述 | 默认值 |
|------|---------|---------|
| `script_path` | 需要分析的R脚本路径 | 当前目录 |
| `required_packages` | 需要验证的包列表 | 从脚本中自动检测 |
| `check_bioc` | 检查Bioconductor包 | `true` |
| `check_updates` | 检查是否有可用更新 | `false` |
| `fix_issues` | 尝试安装缺失的包 | `false` |

---

## 诊断报告示例：
```
=== R Environment Diagnostic Report ===

R Version: 4.3.2 (2023-10-31)
Platform: x86_64-pc-linux-gnu
Library Path: /home/user/R/x86_64-pc-linux-gnu-library/4.3

--- Installed Packages ---
tidyverse    2.0.0  ✓
ggplot2      3.4.4  ✓
dplyr        1.1.3  ✓

--- Missing Packages ---
DESeq2       ✗     (Bioconductor required)
EnhancedVolcano ✗   (CRAN)
pheatmap     ✗     (CRAN)

--- Installation Commands ---
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("DESeq2")
install.packages(c("EnhancedVolcano", "pheatmap"))

--- Warnings ---
- R 4.3.2 detected; some packages may require R >= 4.4.0
- renv not initialized; consider running renv::init()
```

---

## 注意事项：
- 始终会检查CRAN和Bioconductor两个包源
- 如果项目中存在`renv.lock`文件，则会尊重其设置
- 生成的安装命令是安全的（运行前请仔细核对）
- 会检测编译所需的系统依赖关系
- 会检查包之间的命名空间冲突

---

## 相关子技能：
- **create-project**：设置具有正确环境的新项目
- **run-analysis**：在修复环境问题后执行脚本