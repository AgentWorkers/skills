---
name: haskell
description: >
  **高级Haskell开发技能**  
  涵盖类型驱动设计、GHC扩展、Cabal/Stack/Nix构建工具、性能优化、测试以及现代Haskell库生态系统。适用于任何Haskell编程、调试或架构相关任务。
---
# Haskell 开发指南

## 核心理念

1. **类型即设计** — 将非法状态设置为不可表示的状态。如果类型检查器接受了某种状态，那么它应该是正确的。
2. **默认情况下保持代码的“纯净性”** — 侧效应在类型系统中是明确规定的。`IO` 是一种特性，而不是负担。
3. **优先使用组合而非继承** — 创建小型、可组合的函数；使用类型类来实现特定的多态性。
4. **惰性作为工具** — 惰性使得抽象更加优雅，但需要警惕内存泄漏的问题。
5. **先确保正确性，再考虑性能** — 先编写正确的代码，再进行性能分析，最后进行优化。
6. **保持简单** — 纯净性和强类型（大致遵循 Haskell2010 的规范）已经提供了 Haskell 的大部分价值。除非绝对必要，否则避免使用更高级的语言特性。

## 项目设置

### Cabal（推荐与 Nix 一起使用）

```bash
mkdir my-project && cd my-project
cabal init --interactive
```

最小的 `my-project.cabal` 文件内容：
```cabal
cabal-version: 3.0
name:          my-project
version:       0.1.0.0
build-type:    Simple

common warnings
    ghc-options: -Wall -Werror -Wcompat -Widentities
                 -Wincomplete-record-updates
                 -Wincomplete-uni-patterns
                 -Wpartial-fields
                 -Wredundant-constraints

library
    import:           warnings
    exposed-modules:  MyProject
    build-depends:    base >= 4.17 && < 5
                    , text
                    , containers
                    , aeson
    hs-source-dirs:   src
    default-language:  Haskell2010
    default-extensions:
        DeriveGeneric
        DerivingStrategies
        LambdaCase
        ScopedTypeVariables

executable my-project
    import:           warnings
    main-is:          Main.hs
    build-depends:    base, my-project
    hs-source-dirs:   app
    default-language: Haskell2010

test-suite tests
    import:           warnings
    type:             exitcode-stdio-1.0
    main-is:          Main.hs
    build-depends:    base, my-project, hspec, QuickCheck
    hs-source-dirs:   test
    default-language: Haskell2010
```

## 项目结构

```
my-project/
├── exe/
│   └── Main.hs              # Executable entry point (thin — delegates to library)
├── src/
│   ├── MyProject.hs          # Public API (re-exports)
│   ├── MyProject/
│   │   ├── Types.hs          # Core domain types
│   │   ├── App.hs            # Application monad, config
│   │   ├── DB.hs             # Database layer
│   │   ├── API.hs            # HTTP/API layer
│   │   └── Internal/         # Not exported — implementation details
│   │       └── Utils.hs
├── test/
│   ├── Main.hs
│   └── MyProject/
│       ├── TypesSpec.hs
│       └── DBSpec.hs
├── my-project.cabal
├── cabal.project             # Multi-package config, source-repository-packages
```

## 必需的 GHC 扩展

### 通过 `.cabal` 文件中的 `default-extensions` 始终启用这些扩展
```haskell
DeriveGeneric           -- Derives Generic
DerivingStrategies      -- Explicit: deriving stock, newtype, anyclass, via
LambdaCase              -- \case { ... } instead of \x -> case x of ...
ScopedTypeVariables     -- forall a. ... lets you reference 'a' in where clauses
```

### 在需要时自由使用这些扩展
```haskell
BangPatterns
DeriveDataTypeable
DeriveFunctor
DeriveGeneric               -- Generic instances for aeson, etc.
DerivingVia                 -- Derive via newtype coercion
DuplicateRecordFields       -- Same field name in different records
ExistentialQuantification   -- Hide type variables
FlexibleContexts            -- Relax context restrictions
FlexibleInstances           -- Relax instance head restrictions
FunctionalDependencies      -- fundeps for MPTC
GeneralizedNewtypeDeriving  -- Derive through newtypes
MultiParamTypeClasses       -- Typeclasses with multiple params
NumericUnderscores          -- More readable number syntax
OverloadedRecordDot         -- record.field syntax (GHC 9.2+)
OverloadedStrings           -- String literals as Text/ByteString
RankNTypes                  -- Higher-rank polymorphism (forall inside arrows)
RecordWildCards             -- Controversial but can be used effectively
```

### 除非有明显的价值，否则避免使用这些扩展
```haskell
TemplateHaskell         -- Metaprogramming (aeson TH, lens TH). Slows compilation.
GADTs                   -- Generalized algebraic data types
TypeFamilies            -- Type-level functions
DataKinds               -- Promote data constructors to types
ConstraintKinds         -- Alias constraint sets
UndecidableInstances    -- Sometimes needed for MTL/type families. Understand why.
TypeOperators           -- type a :+: b. Servant uses heavily.
AllowAmbiguousTypes     -- Pair with TypeApplications for type-level dispatch.
```

## 类型驱动开发

### 使用类型名称作为作用域访问器以避免名称冲突
```
data User = User
  { _user_firstName :: String
  , _user_email :: String
  } deriving (Eq,Ord,Show,Read,Generic)
```

### 将非法状态设置为不可表示的状态
```haskell
-- BAD: stringly-typed
data User = User { _user_role :: String, _user_email :: String }

-- GOOD: types encode constraints
data Role = Admin | Editor | Viewer
  deriving stock (Show, Eq, Ord)

newtype Email = Email { _unEmail :: Text }  -- smart constructor validates

mkEmail :: Text -> Either EmailError Email
mkEmail t
  | "@" `T.isInfixOf` t = Right (Email t)
  | otherwise = Left InvalidEmail

data User = User
  { _user_role  :: !Role
  , _user_email :: !Email
  }
```

### 用于状态机的“幻影类型”（Phantom Types）
```haskell
data Draft
data Published

data Article (s :: Type) = Article
  { articleTitle   :: !Text
  , articleContent :: !Text
  }

publish :: Article Draft -> Article Published
publish (Article t c) = Article t c

-- Only published articles can be shared
share :: Article Published -> IO ()
share = ...
```

### 为安全性设计的新类型（Newtypes）
```haskell
newtype UserId    = UserId    { unUserId    :: Int64 } deriving newtype (Eq, Ord, Show, FromJSON, ToJSON)
newtype ProductId = ProductId { unProductId :: Int64 } deriving newtype (Eq, Ord, Show, FromJSON, ToJSON)

-- Now you can't accidentally pass a ProductId where UserId is expected
getUser :: UserId -> IO User
```

## 错误处理

```haskell
-- Pure errors: Either
parseConfig :: Text -> Either ConfigError Config

-- App-level errors: ExceptT or MonadError
class Monad m => MonadError e m where
  throwError :: e -> m a
  catchError :: m a -> (e -> m a) -> m a

-- The ReaderT pattern (simple, composable)
newtype App a = App { unApp :: ReaderT AppEnv IO a }
  deriving newtype (Functor, Applicative, Monad, MonadIO, MonadReader AppEnv)

data AppError
  = NotFound Text
  | Unauthorized
  | ValidationError [Text]
  deriving stock (Show)

-- Throw with exceptions in IO, catch at boundaries
throwIO :: Exception e => e -> IO a
catch   :: Exception e => IO a -> (e -> IO a) -> IO a

-- RULE: Use Either for expected failures, exceptions for unexpected/IO failures.
-- Never use error/undefined in library code.
```

## 常见模式

### ReaderT 模式
```haskell
data AppEnv = AppEnv
  { appDbPool   :: !Pool Connection
  , appLogger   :: !Logger
  , appConfig   :: !Config
  }

newtype App a = App (ReaderT AppEnv IO a)
  deriving newtype (Functor, Applicative, Monad, MonadIO, MonadReader AppEnv)

runApp :: AppEnv -> App a -> IO a
runApp env (App m) = runReaderT m env

-- Use Has-pattern for granular access:
class Has field env where
  obtain :: env -> field

instance Has (Pool Connection) AppEnv where
  obtain = appDbPool

grabPool :: (MonadReader env m, Has (Pool Connection) env) => m (Pool Connection)
grabPool = asks obtain
```

### Optics（lens/optics）
```haskell
-- With OverloadedRecordDot (GHC 9.2+), often you don't need lens for simple access.
-- Use lens/optics for: nested updates, traversals, prisms for sum types.

-- lens: view, set, over
view _1 (1, 2)       -- 1
set _1 10 (1, 2)     -- (10, 2)
over _1 (+1) (1, 2)  -- (2, 2)

-- Compose with (.)
view (config . database . host) appEnv
over (users . each . name) T.toUpper myData
```

## 测试

### HSpec — 测试框架
```haskell
-- test/MyProject/TypesSpec.hs
module MyProject.TypesSpec (spec) where

import Test.Hspec
import MyProject.Types

spec :: Spec
spec = do
  describe "mkEmail" $ do
    it "accepts valid emails" $
      mkEmail "user@example.com" `shouldBe` Right (Email "user@example.com")

    it "rejects invalid emails" $
      mkEmail "invalid" `shouldSatisfy` isLeft
```

### QuickCheck — 属性测试
```haskell
import Test.QuickCheck

prop_reverseReverse :: [Int] -> Bool
prop_reverseReverse xs = reverse (reverse xs) == xs

-- Generate domain types:
instance Arbitrary Email where
  arbitrary = do
    user   <- listOf1 (elements ['a'..'z'])
    domain <- listOf1 (elements ['a'..'z'])
    pure $ Email $ T.pack $ user <> "@" <> domain <> ".com"
```

## 性能优化

### 严格性
```haskell
-- Strict fields in data types (almost always want this):
data Config = Config
  { configHost :: !Text       -- strict (bang pattern in field)
  , configPort :: !Int
  }

-- BangPatterns in let bindings:
{-# LANGUAGE BangPatterns #-}
let !result = expensiveComputation

-- Use Text, not String. Always.
-- Use ByteString for binary data.
-- Use Vector for indexed access, [] for sequential processing.
-- Use HashMap/HashSet for large unordered collections.
-- Use Map/Set for ordered collections or when Ord is available.
```

### 性能分析
```bash
# Build with profiling
cabal build --enable-profiling

# Run with heap profiling
./my-project +RTS -hc -p -RTS

# Time profiling report
./my-project +RTS -p -RTS
# Generates my-project.prof

# Heap profile visualization
hp2ps -c my-project.hp
```

### 常见的内存泄漏问题
```haskell
-- BAD: lazy accumulator
foldl (+) 0 [1..1000000]  -- builds giant thunk chain

-- GOOD: strict left fold
foldl' (+) 0 [1..1000000]  -- evaluates as it goes

-- BAD: lazy state
modify (\s -> s { count = count s + 1 })  -- thunk builds up

-- GOOD: strict state
modify' (\s -> s { count = count s + 1 })
-- Or: use strict fields + evaluate
```

## 命令参考

| 任务 | 命令 |
|------|---------|
| 构建项目 | `cabal build` |
| 运行项目 | `cabal run my-project` |
| 测试项目 | `cabal test --test-show-details=direct` |
| 实时交互式编译器（REPL） | `cabal repl` |
| 生成文档 | `cabal haddock` |
| 代码检查 | `hlint src/` |
| 监控文件更改 | `ghcid --command="cabal repl"` |
| 检查依赖项是否过时 | `cabal outdated` |
| 清理项目构建输出 | `cabal clean` |
| 使用 Nix 构建项目 | `nix build` |
| 使用 Nix 开发环境 | `nix develop` |

## 常见的问题与注意事项

1. **`String` 实际上是 `Char` 类型** — 在所有地方都应使用 `Text` 类型（来自 `text` 包）。如果需要处理 `Text` 类型的字符串字面量，请启用 `OverloadedStrings` 扩展。
2. **惰性 I/O** — `Prelude` 中的 `readFile` 是惰性的。建议使用 `Data.Text.IO.readFile` 或 `ByteString.readFile` 代替。
3. **“孤儿实例”（Orphan Instances）** — 不要在定义类型或类的模块之外定义类型类的实例。可以使用 `newtypes` 来包装这些实例。
4. **Cabal 使用问题** — 建议使用 Nix 或 Cabal 的内置构建工具（`v2-build`），避免使用 `cabal-install`（v1 版本）。
5. **记录类型（Records）** — 字段名是全局的。请使用统一且易于理解的命名前缀（例如 `_employee_familyName`）。
6. **部分函数（Partial Functions）** — 在生产代码中切勿使用 `head`、`tail`、`fromJust`、`read` 等函数。应使用模式匹配或其他安全的替代方法。
7. **不安全的操作** — 绝不要使用 `accursedUnutterablePerformIO`；只有在能够证明其使用正确的情况下才使用 `unsafePerformIO`。
8. **`undefined` 的使用** — `undefined` 可用于临时替代某些功能以支持增量开发或类型检查，但在生产代码中不应出现。
9. **`foldl` 与 `foldl'`** — 始终使用 `foldl'`（严格版本的函数）。`Prelude` 中的惰性 `foldl` 几乎永远不会是最佳选择。
10. **序列化相关函数** — `Show` 函数主要用于调试；对于 JSON 序列化使用 `aeson`，对于二进制序列化使用 `binary`/`cereal`。
11. **`MonadFail`** — 在 `do` 块中进行模式匹配时需要使用 `MonadFail`；避免在 `do` 块中使用部分模式。
12. **Haskell 模板（Template Haskell）的编写顺序** — 模板相关的声明必须放在它们引用的声明之后，以及引用生成代码的声明之前。

## 关键库

| 库名 | 用途 |
|---------|---------|
| `text` | 处理 Unicode 文本（支持惰性操作） |
| `bytestring` | 处理二进制数据 |
| `aeson` | JSON 编码/解码 |
| `postgresql-simple`, `mysql-simple` | 低级数据库操作库 |
| `lens` / `optics` | 提供可组合的获取/设置函数 |
| `mtl` | 单子（Monad）转换类 |
| `containers` | 提供 Map、Set、Seq（有序数据结构） |
| `unordered-containers` | 提供 HashMap、HashSet（高效的数据结构） |
| `vector` | 高效的数组操作 |
| `conduit` / `streaming` | 数据流处理库 |
| `warp` | 快速的 HTTP 服务器 |
| `http-client` | 发送 HTTP 请求的库 |
| `stm` | 软件事务内存管理 |
| `QuickCheck` | 基于属性的测试框架 |
| `hspec` | BDD 风格的测试框架 |
| `tasty` | 可组合的测试框架 |
| `criterion` | 用于性能基准测试的工具 |
| `optparse-applicative` | 命令行参数解析库 |
| `katip` | 结构化日志记录库 |
| `fake` | 用于生成模拟数据的库 |

## 参考资料

有关更多详细信息，请参阅：
- `references/type-system.md` — 关于抽象数据类型（ADTs）、广义抽象数据类型（GADTs）、类型族（type families）、类型类（type classes）、数据类型（DataKinds）、幻影类型（phantom types）的说明。
- `references/common-patterns.md` — 关于 MTL（Monadic Template Libraries）、ReaderT 模式、效果系统（effect systems）、光学操作（optics）、自由单体（free monads）以及类型级编程（type-level programming）的内容。
- `references/libraries.md` — 包含常用库及其使用示例的文档。
- `references/performance.md` — 关于代码严格性、性能分析、内存泄漏、并发处理以及性能基准测试的指南。
- `references/ghc-extensions.md` — 按类别分类的 GHC 扩展使用指南。
- `references/nix-haskell.md` — 基于 Nix 的 Haskell 开发方法（包括 `nixpkgs` 和 `haskell.nix` 的使用）。
- `references/cabal-guide.md` — Cabal 的使用指南，包括多包项目设置和 Hackage 的发布流程。
- `references/best-practices.md` — 关于代码组织、文档编写（Haddock）、持续集成（CI）以及代码风格的最佳实践。