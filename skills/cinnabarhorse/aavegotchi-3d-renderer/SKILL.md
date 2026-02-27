---
name: aavegotchi-3d-renderer
description: 通过从 Goldsky Base 核心数据中提取渲染器哈希值，并向 www.aavegotchi.com 的 `/api renderer/batch` 发送 POST 请求来渲染 Aavegotchi 资产。当用户提供 `tokenId` 或 `inventory URL` 时，或者需要确定性的哈希值以及图像文件时，可以使用此方法。
---
# Aavegotchi 3D 渲染器

该工具可以从令牌数据或渲染器批量 API 中生成 Aavegotchi 资产的 3D 图像。

## 输入参数

- 可以接受 `tokenId` 或包含 `id=<tokenId>` 的库存 URL。
- 默认目标链（chainId）为 8453。

## 输出结果

- 返回生成的渲染器哈希值。
- 返回 `/api(renderer/batch` 的 HTTP 状态码。
- 将原始的批量处理 JSON 数据保存到磁盘。
- 如果可用，将 `PNG_Full` 和 `PNG_Headshot` 图像保存到磁盘。
- 如果存在 `GLB_3DModel`，则返回其可用性及对应的 URL。

## 执行流程

1. 从直接输入或库存 URL 中提取 `tokenId`。
2. 查询 Goldsky Base 的核心子图：
   `https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn`
3. 生成符合渲染器格式的哈希值：
   `<Collateral>-<EyeShape>-<EyeColor>-<Body>-<Face>-<Eyes>-<Head>-<RightHand>-<LeftHand>-<Pet>`
4. 使用以下参数发起批量渲染请求：
   ```
   POST https://www.aavegotchi.com/apirenderer/batch
   ```
   - `force: true`
   - `verify: false`
   - `renderTypes: ["PNG_Full", "PNG_Headshot", "GLB_3DModel"]
5. 持续使用 `POST /api(renderer/batch` 并设置 `verify: true`，直到所有请求的渲染类型都满足 `availability.exists=true` 条件，或者达到超时时间。
6. 仅当对应的 `availability.exists=true` 时，下载 `proxyUrls.PNG_Full` 和 `proxyUrls.PNG_Headshot` 文件。
7. 返回生成的哈希值、渲染请求的开始状态、验证结果、轮询统计信息以及保存的文件路径。

## 命令使用方式

- 运行捆绑好的脚本：
   ```bash
node scripts/render-gotchi-bypass.mjs --token-id 6741
```

- 或者直接传递库存 URL：
   ```bash
node scripts/render-gotchi-bypass.mjs \
  --inventory-url "https://www.aavegotchi.com/u/0x.../inventory?itemType=aavegotchis&chainId=8453&id=6741"
```

- 使用 `--out-dir /tmp` 参数指定输出文件路径（默认为 `/tmp`）。

## 可选的轮询控制选项

```bash
--poll-attempts 18 --poll-interval-ms 10000
```

## 返回格式

必须返回以下信息：

1. `tokenId`
2. 生成的哈希值
3. 渲染请求的开始状态、验证状态以及原始 JSON 文件的路径
4. 轮询统计信息（`pollAttempts`, `pollIntervalMs`, `renderReady`）
5. `PNG_Full` 和 `PNG_Headshot` 图像的输出路径（或未生成的原因是）
6. 如果存在 `GLB_3DModel`，则返回其可用性及对应的 URL

## 故障排除

- 如果 Goldsky 未返回任何 Aavegotchi 数据，请检查 `tokenId` 是否正确以及基础链（Base）的配置是否正确。
- 如果批量处理返回的哈希值格式为 400，需检查眼睛的映射关系以及左右可穿戴物品的顺序（`index4` 应在 `index5` 之前）。
- 如果 `availability.exists` 为 `false`，请确保在发起请求时使用了 `force:true`，并继续使用 `verify:true` 进行轮询，直到超时。
- 如果 API 返回 404 错误，请检查生产环境的部署状态。