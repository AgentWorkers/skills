---
name: struct-offset-analyzer
description: 通过读取代码，静态分析 C 结构体成员的偏移量，从而计算出内存布局。
---
# struct-offset-analyzer

该工具可静态分析C语言结构体成员的内存偏移量，无需运行任何代码。

## 使用场景

- 在逆向工程过程中定位结构体成员
- 在调试过程中确认内存布局
- 在安全研究中分析数据结构
- 在二进制分析中理解结构体字段的位置

## 工作流程

### 1. 定位结构体定义

```bash
# 搜索结构体定义
grep -n "struct xxx_st" **/*.h
grep -n "typedef struct" **/*.h
```

### 2. 收集类型信息

查找所有成员类型的定义：
- 嵌套结构体
- 枚举类型
- `typedef` 别名
- 常量定义（例如：`#define EVP_MAX_MD_SIZE 64`）

### 3. 计算对齐规则

| 类型 | 大小（64位） | 对齐要求 |
|------|---------------|----------------------|
| `char`/`unsigned char` | 1 | 1 |
| `short` | 2 | 2 |
| `int`/`uint32_t` | 4 | 4 |
| `long`/`size_t`/`pointer` | 8 | 8 |
| `unsigned char[N]` | `N` | 1（无需填充） |
| `enum` | 通常为4 | 4 |
| `struct` | 取决于成员类型 | 对齐到最大成员的大小 |

**关键规则**：
- 成员偏移量必须是其大小的整数倍
- `unsigned char` 数组是1字节对齐的，**无需填充**；
- 整个结构体的大小对齐到其最大成员的大小；
- 填充字节也会计入偏移量中。

### 4. 输出偏移量表

使用十六进制表示偏移量，格式如下：

```plaintext
| 偏移量（0x） | 成员 | 类型 | 大小 |
|------------|--------|------|------|
| 0x00 | field1 | `int` | 4 |
| 0x04 | *(padding)* | - | 4 |
| 0x08 | field2 | `void *` | 8 |
```

## 常见搜索模式

```bash
# 查找结构体成员定义
grep -n "struct xxx_st" **/*.h`

# 查找类型定义
grep -n "typedef.*XXX" **/*.h`

# 查找常量定义
grep -n "#define.*SIZE" **/*.h`

# 查找枚举定义
grep -n "typedef enum" **/*.h`
```

## 示例：OpenSSL的`ssl_st`结构体分析

以分析`client_app_traffic_secret`成员的偏移量为例：

1. 定位结构体定义：`ssl/ssl_local.h:1068`
2. 查找常量定义：`EVP_MAX_MD_SIZE = 64`（位于`include/openssl/evp.h:19`）
3. 计算结构体布局，注意`unsigned char`数组无需填充
4. 结果：偏移量为0x33c（828字节）

## 注意事项

- 确认目标平台（32位或64位）
- 注意条件编译指令（`#ifdef`）可能会影响结构体布局
- 检查`#pragma pack`指令，因为它们可能会改变对齐方式
- 联合体（union）成员共享相同的偏移量