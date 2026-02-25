---
name: aavegotchi-3d-renderer
description: 通过从 Goldsky Base 的核心数据中提取渲染器哈希值，并向 www.aavegotchi.com 的 `/api(renderer/batch` 发送 POST 请求来渲染 Aavegotchi 资产。当用户提供 `tokenId` 或 `inventory URL` 时，或者需要确定性的哈希值以及图像文件时，可以使用此方法。
---
# Aavegotchi 3D 渲染器

该工具能够根据令牌数据或库存 URL（格式为 `id=<tokenId>`）来渲染 Aavegotchi 资产。

## 输入参数

- 可以输入 `tokenId` 或包含 `id=<tokenId>` 的库存 URL。
- 默认目标链（chainId）为 8453。

## 输出参数

- 返回生成的渲染器哈希值。
- 返回 `/apirenderer/batch` 的 HTTP 状态码。
- 将原始的批量处理 JSON 数据保存到磁盘。
- 如果可用，将 `PNG_Full` 和 `PNG_Headshot` 文件也保存到磁盘。
- 如果存在 `GLB_3DModel`，则返回其 URL 及可用性信息。

## 执行流程

1. 从直接输入或库存 URL 中提取 `tokenId`。
2. 查询 Goldsky Base 的核心子图：
   `https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn`
3. 生成符合渲染器格式的哈希值：
   `<Collateral>-<EyeShape>-<EyeColor>-<Body>-<Face>-<Eyes>-<Head>-<RightHand>-<LeftHand>-<Pet>`
4. 发送 POST 请求到 `https://www.aavegotchi.com/api renderer/batch`，参数如下：
   - `verify: true`
   - `renderTypes: ["PNG_Full", "PNG_Headshot", "GLB_3DModel"]`
5. 下载生成的图像文件（`proxyUrls.PNG_Full` 和 `proxyUrls.PNG_Headshot`）。
6. 返回生成的哈希值、请求响应结果以及保存的资产文件路径。

## 使用方法

- 运行捆绑好的脚本：
   ```bash
node scripts/render-gotchi-bypass.mjs --token-id 6741
```

- 或者直接提供库存 URL：
   ```bash
node scripts/render-gotchi-bypass.mjs \
  --inventory-url "https://www.aavegotchi.com/u/0x.../inventory?itemType=aavegotchis&chainId=8453&id=6741"
```

- 使用 `--out-dir /tmp` 参数来指定资产文件的保存路径（默认为 `/tmp`）。

## 返回格式

必须返回以下信息：

1. `tokenId`
2. 生成的哈希值
3. `/apirenderer/batch` 的请求状态码及原始 JSON 数据
4. `PNG_Full` 和 `PNG_Headshot` 文件的路径（或说明文件未生成的缘由）
5. `GLB_3DModel` 的 URL 及其可用性信息（`availability.exists=false` 表示文件不存在）

## 故障排除

- 如果 Goldsky 未返回任何 Aavegotchi 资产信息，请检查 `tokenId` 是否正确。
- 如果请求返回状态码 `400`，请检查眼睛部位的映射关系以及右手/左手的显示顺序（应为 `index4` 先于 `index5`）。
- 如果 `availability.exists` 为 `false`，请重新执行批量处理请求以触发渲染并重新检查结果。
- 如果请求端点返回 `404`，请检查 Aavegotchi 服务的部署状态。