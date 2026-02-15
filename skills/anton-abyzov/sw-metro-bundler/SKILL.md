---
name: metro-bundler
description: Metro Bundler 的配置、优化及故障排除方法。适用于处理打包错误（如 “无法解析模块”）或缓存问题。
---

# Metro Bundler 专家

在 React Native 的 Metro Bundler 方面拥有全面的专业知识，包括配置、优化、自定义转换器、缓存策略以及解决常见的打包问题。

## 我的专长

### Metro 基础知识

**什么是 Metro？**
- React Native 的 JavaScript 打包工具
- 负责转换和打包 JavaScript 模块
- 管理资源文件（如图片、字体等）
- 提供快速的开发环境刷新功能
- 生成用于调试的源代码映射文件（source maps）

**关键概念**
- **转换器（Transformer）**：将源代码（TypeScript、JSX）转换为 JavaScript
- **解析器（Resolver）**：在文件系统中查找模块
- **序列化器（Serializer）**：将多个模块合并成打包文件
- **缓存（Cache）**：加快后续构建的速度

### Metro 配置

**基本的 `metro.config.js` 文件**
```javascript
const { getDefaultConfig } = require('expo/metro-config');

/** @type {import('expo/metro-config').MetroConfig} */
const config = getDefaultConfig(__dirname);

module.exports = config;
```

**自定义配置**
```javascript
const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

const defaultConfig = getDefaultConfig(__dirname);

const config = {
  transformer: {
    // Enable Babel transformer
    babelTransformerPath: require.resolve('react-native-svg-transformer'),

    // Source map options
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: true,
      },
    }),
  },

  resolver: {
    // Custom asset extensions
    assetExts: defaultConfig.resolver.assetExts.filter(ext => ext !== 'svg'),

    // Custom source extensions
    sourceExts: [...defaultConfig.resolver.sourceExts, 'svg', 'cjs'],

    // Node module resolution
    nodeModulesPaths: [
      './node_modules',
      '../../node_modules',  // For monorepos
    ],

    // Custom platform-specific extensions
    platforms: ['ios', 'android', 'native'],
  },

  server: {
    // Custom port
    port: 8081,

    // Enhanced logging
    enhanceMiddleware: (middleware) => {
      return (req, res, next) => {
        console.log(`Metro request: ${req.url}`);
        return middleware(req, res, next);
      };
    },
  },

  watchFolders: [
    // Watch external folders (monorepos)
    path.resolve(__dirname, '..', 'shared-library'),
  ],

  resetCache: true,  // Reset cache on start (dev only)
};

module.exports = mergeConfig(defaultConfig, config);
```

### 优化策略

**内联依赖项（Inline Dependencies）**
```javascript
// metro.config.js
module.exports = {
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        inlineRequires: true,  // Lazy load modules (faster startup)
      },
    }),
  },
};

// Before (eager loading)
import UserProfile from './UserProfile';
import Settings from './Settings';

function App() {
  return (
    <View>
      {showProfile ? <UserProfile /> : <Settings />}
    </View>
  );
}

// After inline requires (lazy loading)
function App() {
  return (
    <View>
      {showProfile ?
        <require('./UserProfile').default /> :
        <require('./Settings').default />
      }
    </View>
  );
}
```

**打包文件分割（实验性功能）**
```javascript
// metro.config.js
module.exports = {
  serializer: {
    createModuleIdFactory: () => {
      // Generate stable module IDs for better caching
      return (path) => {
        return require('crypto')
          .createHash('sha1')
          .update(path)
          .digest('hex')
          .substring(0, 8);
      };
    },
  },
};
```

**资源文件优化**
```javascript
// metro.config.js
module.exports = {
  transformer: {
    // Minify assets
    minifierPath: require.resolve('metro-minify-terser'),
    minifierConfig: {
      compress: {
        drop_console: true,  // Remove console.log in production
        drop_debugger: true,
      },
      output: {
        comments: false,
      },
    },
  },

  resolver: {
    // Optimize asset resolution
    assetExts: [
      'png', 'jpg', 'jpeg', 'gif', 'webp',  // Images
      'mp3', 'wav', 'm4a', 'aac',           // Audio
      'mp4', 'mov',                          // Video
      'ttf', 'otf', 'woff', 'woff2',        // Fonts
    ],
  },
};
```

### 自定义转换器

**SVG 转换器（SVG Transformer）**
```bash
# Install
npm install react-native-svg react-native-svg-transformer

# metro.config.js
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

config.transformer = {
  ...config.transformer,
  babelTransformerPath: require.resolve('react-native-svg-transformer'),
};

config.resolver = {
  ...config.resolver,
  assetExts: config.resolver.assetExts.filter(ext => ext !== 'svg'),
  sourceExts: [...config.resolver.sourceExts, 'svg'],
};

module.exports = config;
```

**多文件扩展名处理（Multiple File Extensions）**
```javascript
// metro.config.js
module.exports = {
  resolver: {
    // Add .web.js, .native.js for platform-specific code
    sourceExts: ['js', 'json', 'ts', 'tsx', 'jsx', 'web.js', 'native.js'],

    // Custom resolution logic
    resolveRequest: (context, moduleName, platform) => {
      if (moduleName === 'my-module') {
        // Custom module resolution
        return {
          filePath: '/custom/path/to/module.js',
          type: 'sourceFile',
        };
      }

      return context.resolveRequest(context, moduleName, platform);
    },
  },
};
```

### 缓存策略

**缓存管理**
```bash
# Clear Metro cache
npx react-native start --reset-cache
npm start -- --reset-cache  # Expo

# Or manually
rm -rf $TMPDIR/react-*
rm -rf $TMPDIR/metro-*

# Clear watchman cache
watchman watch-del-all

# Clear all caches (nuclear option)
npm run clear  # If configured in package.json
```

**缓存配置**
```javascript
// metro.config.js
const path = require('path');

module.exports = {
  cacheStores: [
    // Custom cache directory
    {
      get: (key) => {
        const cachePath = path.join(__dirname, '.metro-cache', key);
        // Implement custom cache retrieval
      },
      set: (key, value) => {
        const cachePath = path.join(__dirname, '.metro-cache', key);
        // Implement custom cache storage
      },
    },
  ],

  // Reset cache on config changes
  resetCache: process.env.RESET_CACHE === 'true',
};
```

### 单一仓库（Monorepo）设置

**工作区配置（Workspaces Configuration）**
```javascript
// metro.config.js (in app directory)
const path = require('path');
const { getDefaultConfig } = require('@react-native/metro-config');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

const config = getDefaultConfig(projectRoot);

// Watch workspace directories
config.watchFolders = [workspaceRoot];

// Resolve modules from workspace
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
];

// Avoid hoisting issues
config.resolver.disableHierarchicalLookup = false;

module.exports = config;
```

**符号链接处理（Symlink Handling）**
```javascript
// metro.config.js
module.exports = {
  resolver: {
    // Enable symlink support
    unstable_enableSymlinks: true,

    // Resolve symlinked packages
    resolveRequest: (context, moduleName, platform) => {
      const resolution = context.resolveRequest(context, moduleName, platform);

      if (resolution && resolution.type === 'sourceFile') {
        // Resolve real path for symlinks
        const realPath = require('fs').realpathSync(resolution.filePath);
        return {
          ...resolution,
          filePath: realPath,
        };
      }

      return resolution;
    },
  },
};
```

### 常见问题及解决方法

- **“无法解析模块”（“Unable to resolve module”）**
- **“端口 8081 已被占用”（“Port 8081 already in use”）**
- **“类型错误：Module AppRegistry 未注册为可调用模块”（“Invariant Violation: Module AppRegistry is not a registered callable module”）**
- **“转换错误：... 语法错误”（“TransformError: ... SyntaxError”）**

## 何时需要我的帮助

当您遇到以下问题时，请联系我：
- 需要配置 Metro Bundler
- 需要自定义转换器（如处理 SVG、图片等资源）
- 需要优化打包文件的大小和启动时间
- 需要设置使用 Metro 的单一仓库（monorepo）
- 需要解决 “无法解析模块” 的错误
- 需要有效清除 Metro 缓存
- 需要配置源代码映射文件
- 需要处理特定平台的文件解析问题
- 需要调试打包性能
- 需要自定义资源文件的处理方式
- 需要解决端口冲突（如端口 8081 的占用问题）
- 需要处理单一仓库中的符号链接问题

## 必备命令

### 开发阶段（Development）
```bash
# Start Metro bundler
npx react-native start

# Start with cache cleared
npx react-native start --reset-cache

# Start with custom port
npx react-native start --port 8082

# Start with verbose logging
npx react-native start --verbose

# Expo dev server
npx expo start

# Expo with cache cleared
npx expo start -c
```

### 调试阶段（Debugging）
```bash
# Check Metro status
curl http://localhost:8081/status

# Get bundle (for debugging)
curl http://localhost:8081/index.bundle?platform=ios > bundle.js

# Check source map
curl http://localhost:8081/index.map?platform=ios > bundle.map

# List all modules in bundle
curl http://localhost:8081/index.bundle?platform=ios&dev=false&minify=false
```

### 缓存管理（Cache Management）
```bash
# Clear Metro cache
rm -rf $TMPDIR/react-*
rm -rf $TMPDIR/metro-*

# Clear watchman
watchman watch-del-all

# Clear all (comprehensive)
npm run clear  # Custom script
# Or manually:
rm -rf $TMPDIR/react-*
rm -rf $TMPDIR/metro-*
watchman watch-del-all
rm -rf node_modules
npm install
```

## 专业技巧与建议

- **1. 打包文件分析（Bundle Analysis）**：分析打包文件的大小以寻找优化机会
- **2. 环境特定配置（Environment-Specific Configuration）**：根据不同环境进行相应的配置调整
- **3. 自定义资源文件处理流程（Custom Asset Pipeline）**：定制资源文件的处理方式
- **4. 预加载重要模块（Preloading Heavy Modules）**：提高应用程序的启动速度
- **5. 提升开发性能（Improving Development Performance）**：优化开发过程中的性能表现

## 与 SpecWeave 的集成

- **配置管理（Configuration Management）**：在 `docs/internal/architecture/` 目录中记录 Metro 的配置信息
- **跟踪打包文件大小的变化**：监控每次代码更新后的打包文件大小
- **将打包优化纳入任务管理（Include Bundling Optimization in Tasks）**：将打包优化步骤纳入项目任务流程

**性能监控（Performance Monitoring）**
- **设置打包文件大小的阈值**：设定合理的打包文件大小上限
- **跟踪启动时间的改进**：记录应用程序启动时间的优化情况
- **记录优化策略**：详细记录所采用的优化方法

**故障排除（Troubleshooting）**
- **维护故障排除指南**：整理针对 Metro 常见问题的解决方案
- **记录缓存清除步骤**：提供有效的缓存清除方法
- **跟踪打包错误**：在代码更新报告中记录打包过程中出现的错误信息