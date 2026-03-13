#!/bin/bash
# 查询 ECS 实例脚本
# 用法：./query_ecs.sh [关键词] [地域]

KEYWORD="${1:-}"
REGION="${2:-cn-beijing}"

if [ -n "$KEYWORD" ]; then
    echo "查询包含 '$KEYWORD' 的 ECS 实例（地域：$REGION）..."
    aliyun ecs DescribeInstances --region "$REGION" | \
        jq -r '.Instances.Instance[] | select(.InstanceName | ascii_downcase | contains("'"$KEYWORD"'")) | 
        "\(.InstanceId)\t\(.InstanceName)\t\(.Status)\t\(.RegionId)\t\(.PublicIpAddress.IpAddress[0] // "无")"' | \
        column -t -s $'\t'
else
    echo "查询所有 ECS 实例（地域：$REGION）..."
    aliyun ecs DescribeInstances --region "$REGION" | \
        jq -r '.Instances.Instance[] | 
        "\(.InstanceId)\t\(.InstanceName)\t\(.Status)\t\(.RegionId)\t\(.PublicIpAddress.IpAddress[0] // "无")"' | \
        column -t -s $'\t'
fi

echo ""
echo "总计：$(aliyun ecs DescribeInstances --region "$REGION" | jq '.TotalCount') 台实例"
