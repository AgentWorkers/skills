---
name: hex-vetter
version: 1.0.0
description: 针对“技能”（Skills）的物理层十六进制审计功能：能够检测隐藏的二进制数据、控制字符以及基于编码的攻击行为。
author: Matrix-Meta
tags:
  - security
  - hex
  - audit
  - binary-analysis
---
# hex-vetter 🔬

hex-vetter 是一款用于物理层二进制数据审计的工具，能够检测隐藏在二进制文件中的恶意代码、控制字符以及基于编码的攻击手段。

## 概述

hex-vetter 对文件进行深度的二进制分析，以发现文本审查工具可能遗漏的问题。它专为技能包的安全审计而设计，能够检测隐藏的有效载荷、混淆过的代码以及可疑的二进制数据。

## 安装

```bash
git clone https://github.com/Matrix-Meta/hex-vetter.git
cd hex-vetter
npm install
```

## 使用方法

### 命令行

```bash
# Scan a single file
node vet.js <file_path>

# Scan a directory recursively
node scan_all.js <directory_path>

# Verify file integrity
node verify.js <file_path>
```

### 作为模块使用

```javascript
const { scanFile } = require('./vet.js');
const result = await scanFile('/path/to/file.bin');

console.log(result.riskLevel);    // 'LOW', 'MEDIUM', 'HIGH'
console.log(result.flags);       // Array of detected issues
console.log(result.hexDump);      // Formatted hex output
```

## 检测内容

| 标志 | 描述 |
|------|-------------|
| `NULL_BYTES` | 空字节（0x00）——二进制注入或文件填充的迹象 |
| `CONTROL_chars` | 控制字符（0x01-0x1F）——隐藏的终端序列 |
| `UNICODE OVERRIDE` | Unicode 方向性重写（如 LRO、RLO 等） |
| `HIGH_NON_ascii` | 非 ASCII 字节占比过高——可能是 Base64 编码的有效载荷 |
| `MAGIC_BYTES` | 已知的特殊字节/签名 |
| `SUSPICIOUS_PATTERN` | 常见攻击模式的匹配检测 |

## API 参考

### scanFile(filePath)

扫描单个文件并返回分析结果。

```javascript
const { scanFile } = require('./vet.js');

const result = await scanFile('./some file.js');
// Returns: { riskLevel, flags, hexDump, details }
```

### scanDirectory(dirPath)

递归扫描目录中的所有文件。

```javascript
const { scanDirectory } = require('./scan_all.js');

const results = await scanDirectory('./skills/');
// Returns: Array of scan results for each file
```

### verifyIntegrity(filePath)

使用存储的校验和来验证文件完整性。

```javascript
const { verifyIntegrity } = require('./verify.js');

const result = await verifyIntegrity('./starfragment.js');
// Returns: { valid, expected, actual }
```

## 风险等级

- **🟢 低风险**: 文件正常，未检测到可疑内容 |
- **🟡 中等风险**: 检测到某些可疑标志，建议手动审查 |
- **🔴 高风险**: 存在大量可疑内容，必须手动审查 |

## 安全政策

1. **强制审查**: 被标记为 **高风险** 的文件在使用前必须由人工或可信的代理进行手动检查。
2. **误报**: 风险等级的判断是基于启发式的。常见的误报情况包括：
   - `.env` 文件被包含在 `.npmignore` 文件中 |
   - 文档中包含编码示例 |
   - 压缩后的文件资源 |
3. **代理操作**: 如果代理在审计过程中发现高风险文件，必须：
   - 立即通知用户 |
   - 提供具体原因（例如，是签名匹配还是二进制数据问题） |
   - 建议下一步的手动审查步骤 |

## 架构

```
hex-vetter/
├── starfragment.js       # Core module (self-modifying storage)
├── scan_all.js          # Recursive directory scanner
├── verify.js            # Integrity verification
├── vet.js               # Main entry point
├── README.md
└── SKILL.md            # This file
```

## 自修改存储机制

`starfragment.js` 模块采用了自修改存储机制：它在运行时从自身文件中读取和写入数据。所有常量都被编码为有效的 JavaScript 注释，并存储在源文件的末尾。

## 贡献方式

欢迎在 GitHub 上提交问题或 pull 请求：
https://github.com/Matrix-Meta/hex-vetter