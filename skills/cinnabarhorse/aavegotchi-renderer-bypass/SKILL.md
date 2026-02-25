---
name: aavegotchi-renderer-bypass
description: 通过从 Goldsky Base 的核心数据中提取渲染器哈希值，并向 www.aavegotchi.com 发送 POST 请求（路径为 /api(renderer/batch），来渲染 Aavegotchi 资产。当用户提供tokenId 或 inventory URL 时，或者需要确定性的哈希值以及图像文件时，可以使用此方法。
---
# AavegotchiRenderer Bypass

该工具用于从令牌数据或渲染器批量API中生成Aavegotchi资产的图像。

## 输入参数

- 可以接受`tokenId`或包含`id=<tokenId>`的库存URL作为输入。
- 默认目标链（chainId）为8453。

## 输出参数

- 返回生成的渲染器哈希值。
- 返回 `/api(renderer/batch` 的HTTP状态码。
- 将原始的批量处理结果（JSON格式）保存到磁盘。
- 如果存在，将生成的`PNG_Full` 和 `PNG_Headshot` 图像文件保存到磁盘。
- 如果存在`GLB_3DModel`，则返回其URL及可用性信息。

## 执行流程

1. 从直接输入或库存URL中提取`tokenId`。
2. 查询Goldsky Base的核心子图：
   `https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn`
3. 生成符合渲染器格式的哈希值：
   `<Collateral>-<EyeShape>-<EyeColor>-<Body>-<Face>-<Eyes>-<Head>-<LeftHand>-<RightHand>-<Pet>`
4. 发送POST请求到 `https://www.aavegotchi.com/api(renderer/batch`，参数如下：
   - `verify: true`
   - `renderTypes: ["PNG_Full", "PNG_Headshot", "GLB_3DModel"]`
5. 下载生成的`proxyUrls.PNG_Full` 和 `proxyUrls.PNG_Headshot` 文件。
6. 返回生成的哈希值、请求响应以及保存的资产文件路径。

## 使用方法

- 运行捆绑好的脚本（参见```bash
node scripts/render-gotchi-bypass.mjs --token-id 6741
```）。
- 或者直接提供库存URL（参见```bash
node scripts/render-gotchi-bypass.mjs \
  --inventory-url "https://www.aavegotchi.com/u/0x.../inventory?itemType=aavegotchis&chainId=8453&id=6741"
```）。
- 使用`--out-dir /tmp`参数指定资产文件的保存路径（默认为`/tmp`）。

## 返回格式

必须返回以下信息：

1. `tokenId`
2. 生成的哈希值
3. `/api(renderer/batch` 的HTTP状态码及原始JSON响应
4. `PNG_Full` 和 `PNG_Headshot` 图像文件的路径（或说明文件未生成的原因）
5. `GLB_3DModel` 的URL及其可用性信息（`availability.exists=false`表示文件不存在）

## 故障排除

- 如果Goldsky未返回任何Aavegotchi数据，请检查`tokenId`和目标链的配置是否正确。
- 如果请求返回400状态码，请检查眼睛部位的映射信息以及左右可穿戴物品的顺序是否正确。
- 如果`availability.exists`为`false`，请重新执行批量处理流程以触发渲染并重新获取结果。
- 如果请求返回404状态码，请检查Aavegotchi服务的部署状态是否正常。