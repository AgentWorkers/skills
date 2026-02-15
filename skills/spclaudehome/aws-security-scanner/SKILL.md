---
name: aws-security-scanner
description: 扫描 AWS 账户中的安全配置错误和漏洞。适用于用户要求审计 AWS 安全性、检查配置错误、查找暴露的 S3 存储桶、审查 IAM 策略、检查安全组、审计 CloudTrail 或执行 AWS 安全检查的场景。涵盖 S3、IAM、EC2、RDS、CloudTrail 以及常见的 CIS 基准测试。
---

# AWS Security Scanner

使用 AWS CLI 对 AWS 基础设施进行安全检查。

## 前提条件

- 已配置 AWS CLI（通过 `aws configure` 或分配 IAM 角色）
- 具备访问被扫描资源的权限

## 快速扫描

### S3 存储桶安全
```bash
# Find public buckets
aws s3api list-buckets --query 'Buckets[].Name' --output text | tr '\t' '\n' | while read bucket; do
  acl=$(aws s3api get-bucket-acl --bucket "$bucket" 2>/dev/null)
  policy=$(aws s3api get-bucket-policy --bucket "$bucket" 2>/dev/null)
  public_access=$(aws s3api get-public-access-block --bucket "$bucket" 2>/dev/null)
  echo "=== $bucket ==="
  echo "$acl" | grep -q "AllUsers\|AuthenticatedUsers" && echo "⚠️ PUBLIC ACL"
  echo "$policy" | grep -q '"Principal":"\*"' && echo "⚠️ PUBLIC POLICY"
  echo "$public_access" | grep -q "false" && echo "⚠️ Public access not fully blocked"
done
```

### IAM 安全问题
```bash
# Users without MFA
aws iam generate-credential-report && sleep 5
aws iam get-credential-report --query 'Content' --output text | base64 -d | grep -E "^[^,]+,.*,false" | cut -d',' -f1

# Overly permissive policies (Admin access)
aws iam list-policies --scope Local --query 'Policies[].Arn' --output text | tr '\t' '\n' | while read arn; do
  version=$(aws iam get-policy --policy-arn "$arn" --query 'Policy.DefaultVersionId' --output text)
  aws iam get-policy-version --policy-arn "$arn" --version-id "$version" --query 'PolicyVersion.Document' | grep -q '"Action":"\*".*"Resource":"\*"' && echo "⚠️ Admin policy: $arn"
done

# Access keys older than 90 days
aws iam list-users --query 'Users[].UserName' --output text | tr '\t' '\n' | while read user; do
  aws iam list-access-keys --user-name "$user" --query "AccessKeyMetadata[?CreateDate<='$(date -d '-90 days' +%Y-%m-%d)'].{User:UserName,KeyId:AccessKeyId,Created:CreateDate}" --output table
done
```

### 安全组
```bash
# Open to world (0.0.0.0/0)
aws ec2 describe-security-groups --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].{ID:GroupId,Name:GroupName,VPC:VpcId}' --output table

# SSH open to world
aws ec2 describe-security-groups --filters "Name=ip-permission.from-port,Values=22" "Name=ip-permission.cidr,Values=0.0.0.0/0" --query 'SecurityGroups[].{ID:GroupId,Name:GroupName}' --output table

# RDP open to world  
aws ec2 describe-security-groups --filters "Name=ip-permission.from-port,Values=3389" "Name=ip-permission.cidr,Values=0.0.0.0/0" --query 'SecurityGroups[].{ID:GroupId,Name:GroupName}' --output table
```

### CloudTrail 状态
```bash
# Check if CloudTrail is enabled in all regions
aws cloudtrail describe-trails --query 'trailList[].{Name:Name,IsMultiRegion:IsMultiRegionTrail,LogValidation:LogFileValidationEnabled,S3Bucket:S3BucketName}' --output table

# Check for trails without log validation
aws cloudtrail describe-trails --query 'trailList[?LogFileValidationEnabled==`false`].Name' --output text
```

### RDS 安全
```bash
# Publicly accessible RDS instances
aws rds describe-db-instances --query 'DBInstances[?PubliclyAccessible==`true`].{ID:DBInstanceIdentifier,Engine:Engine,Endpoint:Endpoint.Address}' --output table

# Unencrypted RDS instances
aws rds describe-db-instances --query 'DBInstances[?StorageEncrypted==`false`].{ID:DBInstanceIdentifier,Engine:Engine}' --output table
```

### EBS 加密
```bash
# Unencrypted EBS volumes
aws ec2 describe-volumes --query 'Volumes[?Encrypted==`false`].{ID:VolumeId,Size:Size,State:State}' --output table
```

## 完整审计报告

运行全面扫描并生成 Markdown 格式的报告：
```bash
echo "# AWS Security Audit Report"
echo "Generated: $(date)"
echo ""
echo "## S3 Buckets"
# ... run S3 checks
echo ""
echo "## IAM"  
# ... run IAM checks
echo ""
echo "## Security Groups"
# ... run SG checks
# etc.
```

## 问题严重性等级

| 问题 | 严重性 |
|-------|----------|
| S3 存储桶公开访问 | 🔴 严重 |
| SSH/RDP 对外开放 | 🔴 严重 |
| 未启用多因素认证（MFA）的 IAM 用户 | 🟠 高风险 |
| 未禁用的管理员策略 | 🟠 高风险 |
| 未启用的 CloudTrail | 🟠 高风险 |
| RDS 可公开访问 | 🟠 高风险 |
| 未加密的 EBS/RDS 数据 | 🟡 中等风险 |
| 访问密钥过期时间超过 90 天 | 🟡 中等风险 |

## CIS 标准检查

为了符合 CIS AWS 基础标准的合规性要求，请检查以下内容：
- 1.1：避免使用 root 账户
- 1.2：为 root 账户启用多因素认证（MFA）
- 1.3：禁用未使用的凭据
- 2.1：启用 CloudTrail
- 2.2：验证日志文件
- 4.1：没有任何安全组允许 0.0.0.0/0 访问端口 22
- 4.2：没有任何安全组允许 0.0.0.0 访问端口 3389

## 自动化

如需定期执行扫描，可以使用 AWS Config Rules 或设置 cron 任务：
```bash
0 6 * * * /path/to/aws-security-scan.sh | mail -s "Daily AWS Audit" security@company.com
```