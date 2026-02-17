---
name: s3-bulk-upload
description: 将多个文件上传到 S3，并通过文件名的首字母前缀实现自动分类和组织。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
      bins:
        - aws
    primaryEnv: AWS_ACCESS_KEY_ID
    emoji: "\U0001F4E6"
    install:
      - kind: brew
        formula: awscli
        bins: [aws]
---
# S3批量上传

使用文件名的第一个字符作为前缀，将文件自动组织并上传到S3（例如：`a/apple.txt`、`b/banana.txt`、`0-9/123.txt`）。

## 快速入门

使用随附的脚本进行批量上传：

```bash
# Basic upload
./s3-bulk-upload.sh ./files my-bucket

# Dry run to preview
./s3-bulk-upload.sh ./files my-bucket --dry-run

# Use sync mode (faster for many files)
./s3-bulk-upload.sh ./files my-bucket --sync

# With storage class
./s3-bulk-upload.sh ./files my-bucket --storage-class STANDARD_IA
```

## 先决条件

确认AWS凭据已配置：

```bash
aws sts get-caller-identity
```

如果配置失败，请确保`AWS_ACCESS_KEY_ID`和`AWS_SECRET_ACCESS_KEY`已设置，或通过`aws configure`进行配置。

## 文件组织逻辑

文件按照文件名的第一个字符进行分类：

| 文件名的第一个字符 | 前缀            |
|-----------------|-------------------|
| `a-z`     | 小写字母（例如：`a/`、`b/`）     |
| `A-Z`     | 小写字母（例如：`a/`、`b/`）     |
| `0-9`     | `0-9/`             |
| 其他       | `_other/`           |

## 单个文件上传

使用自动前缀上传单个文件：

```bash
FILE="example.txt"
BUCKET="my-bucket"

# Compute prefix from first character
FIRST_CHAR=$(echo "${FILE}" | cut -c1 | tr '[:upper:]' '[:lower:]')
if [[ "$FIRST_CHAR" =~ [a-z] ]]; then
  PREFIX="$FIRST_CHAR"
elif [[ "$FIRST_CHAR" =~ [0-9] ]]; then
  PREFIX="0-9"
else
  PREFIX="_other"
fi

aws s3 cp "$FILE" "s3://${BUCKET}/${PREFIX}/${FILE}"
```

## 批量上传

从指定目录上传所有文件：

```bash
SOURCE_DIR="./files"
BUCKET="my-bucket"

for FILE in "$SOURCE_DIR"/*; do
  [ -f "$FILE" ] || continue
  BASENAME=$(basename "$FILE")
  FIRST_CHAR=$(echo "$BASENAME" | cut -c1 | tr '[:upper:]' '[:lower:]')

  if [[ "$FIRST_CHAR" =~ [a-z] ]]; then
    PREFIX="$FIRST_CHAR"
  elif [[ "$FIRST_CHAR" =~ [0-9] ]]; then
    PREFIX="0-9"
  else
    PREFIX="_other"
  fi

  aws s3 cp "$FILE" "s3://${BUCKET}/${PREFIX}/${BASENAME}"
done
```

## 高效的批量同步

对于大型文件上传，可以先使用符号链接将文件分阶段上传，然后再使用`aws s3 sync`完成同步：

```bash
SOURCE_DIR="./files"
STAGING_DIR="./staging"
BUCKET="my-bucket"

# Create staging directory with prefix structure
rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR"

for FILE in "$SOURCE_DIR"/*; do
  [ -f "$FILE" ] || continue
  BASENAME=$(basename "$FILE")
  FIRST_CHAR=$(echo "$BASENAME" | cut -c1 | tr '[:upper:]' '[:lower:]')

  if [[ "$FIRST_CHAR" =~ [a-z] ]]; then
    PREFIX="$FIRST_CHAR"
  elif [[ "$FIRST_CHAR" =~ [0-9] ]]; then
    PREFIX="0-9"
  else
    PREFIX="_other"
  fi

  mkdir -p "$STAGING_DIR/$PREFIX"
  ln -s "$(realpath "$FILE")" "$STAGING_DIR/$PREFIX/$BASENAME"
done

# Sync entire staging directory to S3
aws s3 sync "$STAGING_DIR" "s3://${BUCKET}/"

# Clean up
rm -rf "$STAGING_DIR"
```

## 验证

按前缀列出文件：

```bash
BUCKET="my-bucket"
PREFIX="a"

aws s3 ls "s3://${BUCKET}/${PREFIX}/" --recursive
```

生成所有上传文件的清单：

```bash
BUCKET="my-bucket"

aws s3 ls "s3://${BUCKET}/" --recursive | awk '{print $4}'
```

统计每个前缀下的文件数量：

```bash
BUCKET="my-bucket"

for PREFIX in {a..z} 0-9 _other; do
  COUNT=$(aws s3 ls "s3://${BUCKET}/${PREFIX}/" --recursive 2>/dev/null | wc -l | tr -d ' ')
  [ "$COUNT" -gt 0 ] && echo "$PREFIX: $COUNT files"
done
```

## 错误处理

常见问题及解决方法：

| 错误              | 原因                | 解决方案                |
|------------------|------------------|----------------------|
| `AccessDenied`       | 权限不足            | 确保IAM策略中包含`s3:PutObject`权限     |
| `NoSuchBucket`       | 不存在的桶             | 创建桶或检查桶名是否正确           |
| `InvalidAccessKeyId`    | 凭据错误              | 核对`AWS_ACCESS_KEY_ID`是否正确       |
| `ExpiredToken`      | 会话令牌过期            | 刷新凭据或重新认证             |

在批量上传前测试桶的访问权限：

```bash
BUCKET="my-bucket"
echo "test" | aws s3 cp - "s3://${BUCKET}/_test_access.txt" && \
  aws s3 rm "s3://${BUCKET}/_test_access.txt" && \
  echo "Bucket access OK"
```

## 存储类

通过选择合适的存储类来优化成本：

```bash
# Standard (default)
aws s3 cp file.txt s3://bucket/prefix/file.txt

# Infrequent Access (cheaper storage, retrieval fee)
aws s3 cp file.txt s3://bucket/prefix/file.txt --storage-class STANDARD_IA

# Glacier Instant Retrieval (archive with fast access)
aws s3 cp file.txt s3://bucket/prefix/file.txt --storage-class GLACIER_IR

# Intelligent Tiering (auto-optimize based on access patterns)
aws s3 cp file.txt s3://bucket/prefix/file.txt --storage-class INTELLIGENT_TIERING
```

在批量上传命令中添加`--storage-class`参数，以优化对不经常访问的文件的存储成本。