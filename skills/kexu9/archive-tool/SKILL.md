---
name: archive-tool
description: Extract and create archive files (zip, rar, 7z, tar, gz). Use when: (1) Extracting zip/rar/7z files, (2) Creating zip archives, (3) Viewing archive contents, (4) Batch extracting files.
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "📦"
    homepage: https://github.com/KeXu9/archive-skill
---

# Archive Skill

该工具用于提取文件并创建压缩文件（如 zip、tar、tar.gz、gz 等格式），在缺少相应工具时（如 rar、7z）会使用系统自带的解压/压缩工具。

## 安装

```bash
# Optional (for rar/7z support)
brew install unar p7zip
```

## 功能

- ✅ 提取文件：支持 zip、tar、tar.gz、tgz、gz 格式
- ⚠️ 提取文件：支持 rar、7z 格式（需安装相应的解压工具）
- ✅ 创建压缩文件：支持 zip、tar、tar.gz 格式
- ✅ 查看压缩文件内容

## 使用方法

### 提取文件

```bash
python archive.py extract file.zip
python archive.py extract file.zip -o ./output
python archive.py extract file.rar --password secret
python archive.py extract "*.zip"  # Batch
```

### 创建压缩文件

```bash
python archive.py create output.zip ./folder
python archive.py create output.tar ./folder
python archive.py create output.tar.gz ./folder
```

### 查看压缩文件内容

```bash
python archive.py list file.zip
```

## 支持的格式

| 格式 | 是否支持提取 | 是否支持创建 | 是否使用 Python 标准库 |
|--------|-----------|-----------|-------------|
| zip | ✅ | ✅ | ✅ |
| tar | ✅ | ✅ | ✅ |
| tar.gz/tgz | ✅ | ✅ | ✅ |
| gz | ✅ | ❌ | ✅ |
| rar | ⚠️ | ❌ | - |
| 7z | ⚠️ | ❌ | - |

⚠️ 表示需要安装额外的系统工具（unar、p7zip）才能支持解压 rar 和 7z 格式的文件。