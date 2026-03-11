# Windows 文件搜索技巧

**技巧描述：**  
本技巧利用 Everything 命令行工具（es.exe）为 Windows 系统提供强大的文件搜索功能，支持快速高效地在整个文件系统中查找文件和文件夹。

## 概述  
该技巧通过调用 Everything 搜索引擎的命令行接口，在 Windows 平台上实现高级文件搜索操作。es.exe 具有极快的搜索速度，非常适合根据各种条件定位文件和文件夹。

## 错误处理  
在执行命令时，如果返回 `Error 8`，该技巧会自动尝试再次执行命令，并添加 `-instance=1.5a` 参数以确保与 Everything 1.5a 版本兼容。  

**如果添加 `-instance=1.5a` 参数后错误仍然存在：**  
这表明您的系统中未正确安装或配置 es.exe 命令行工具。请按照以下步骤操作：  

1. **下载并安装 Everything：**  
   - 访问 Everything 官方网站：https://www.voidtools.com/downloads/  
   - 下载并安装最新版本的 Everything  
   - 确保在安装过程中选择了“ES Command Line Tool”选项。  

**直接下载链接：**  
   - Everything 1.4.1（稳定版本）：  
     - 便携版 ZIP 文件：https://www.voidtools.com/Everything-1.4.1.1032.x64.zip  
     - 安装程序：https://www.voidtools.com/Everything-1.4.1.1032.x64-Setup.exe  
   - Everything 1.5.0a（包含 es.exe 的 Alpha 版本）：  
     - 便携版 ZIP 文件：https://www.voidtools.com/Everything-1.5.0.1404a.x64.zip  
     - 安装程序：https://www.voidtools.com/Everything-1.5.0.1404a.x64-Setup.exe  

2. **配置系统 PATH（选择以下方法之一）：**  
   - **方法 A：将 es.exe 目录添加到系统 PATH：**  
     - 找到 es.exe 文件（通常位于 `C:\Program Files\Everything\`）  
     - 将该目录添加到系统的 PATH 环境变量中  
     - 重新启动终端或命令提示符以使更改生效。  
   - **方法 B：将 es.exe 复制到系统目录：**  
     - 将 es.exe 文件复制到 Windows 系统目录（通常是 `C:\Windows`）。  

3. **验证安装：**  
   - 打开新的命令提示符  
   - 输入 `es -version` 以确认工具是否可用  
   - 输入 `es -get-everything-version` 或 `es -instance=1.5a -get-everything-version` 以确认 Everything.exe 是否可用  
   - 如果成功，您应该能看到 es 命令和 Everything.exe 的版本信息。  

## 核心功能  

### 1. 基本搜索语法  
```  
es [选项] 搜索词  
```  

### 2. 常见搜索选项  

**文件过滤：**  
- `-p`：匹配完整路径（包括文件夹名称）  
- `-w`：仅匹配完整单词  
- `-n <数量>`：限制结果数量  
- `-path <路径>`：在指定路径内搜索  
- `/ad`：仅显示目录  
- `/a-d`：仅显示文件（排除目录）  

**示例：** `es -path "C:\Users" -n 10 *.pdf`  

### 3. 排序和显示  
**排序选项：**  
- `-s`：按完整路径排序  
- `-sort name`：按文件名排序（支持 `size`、`extension`、`date-modified` 等）  
- 使用 `-` 前缀表示降序排序（例如：`-sort -date-modified`）  

**格式化输出：**  
```  
es -name -size -date-modified -path 搜索词  
```  

### 4. 高级功能  

**数据导出：**  
- `-csv`：将结果导出为 CSV 格式  
- `-export-csv "文件名.csv"`：导出到指定的 CSV 文件  
- `-no-header`：在导出时省略标题行  

**文件夹大小计算：**  
- `-get-folder-size <文件名>`：计算文件夹大小  
- `-get-total-size`：计算搜索结果的总大小  

**搜索词高亮显示：**  
- `-highlight`：在结果中高亮显示匹配的文本  
- `-highlight-color 0x0c`：设置高亮颜色  

## 使用示例  

**示例 1：查找最近修改的 Word 文档**  
```  
es -path "C:\\" -sort -date-modified -n 5 -name -size -date-modified *.docx  
```  

**示例 2：将隐藏文件列表导出到 CSV 文件**  
```  
es -path "C:\\" /ah -export-csv "hidden_files.csv" -no-header  
```  

## 注意事项：**  
- **平台：** 仅适用于 Windows  
- **工具：** Everything 命令行工具（es.exe）  
- **兼容性：** 支持 Everything 1.4.1.950 及更高版本  
- **通配符：** 支持 `*`（任意字符）和 `?`（单个字符）  
- **引号使用：** 对包含空格的路径或搜索词使用双引号。