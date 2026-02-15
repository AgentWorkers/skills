---
name: data-validation
description: 使用各种语言和格式的规范来验证数据。适用于定义 JSON Schema（如使用 Zod（TypeScript）或 Pydantic（Python））、验证 API 请求/响应的结构、检查 CSV/JSON 数据的完整性，或在服务之间建立数据契约等场景。
metadata: {"clawdbot":{"emoji":"✅","requires":{"anyBins":["node","python3","jq"]},"os":["linux","darwin","win32"]}}
---

# 数据验证

支持跨语言和格式的基于模式的数据验证。涵盖 JSON Schema、Zod（TypeScript）、Pydantic（Python）、API 边界验证、数据契约以及数据完整性检查。

## 使用场景

- 定义 API 请求/响应体的结构
- 在处理用户输入之前对其进行验证
- 在服务之间建立数据契约
- 在导入 CSV/JSON 文件之前检查其完整性
- 在数据迁移过程中确保所有数据都被正确处理
- 从数据模式生成类型或文档

## JSON Schema

### 基本模式

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["name", "email", "age"],
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 150
    },
    "role": {
      "type": "string",
      "enum": ["user", "admin", "moderator"],
      "default": "user"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "uniqueItems": true,
      "maxItems": 10
    },
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" },
        "zip": { "type": "string", "pattern": "^\\d{5}(-\\d{4})?$" }
      },
      "required": ["street", "city"]
    }
  },
  "additionalProperties": false
}
```

### 常见模式

```json
// Nullable field
{ "type": ["string", "null"] }

// Union type (string or number)
{ "oneOf": [{ "type": "string" }, { "type": "number" }] }

// Conditional: if role is admin, require permissions
{
  "if": { "properties": { "role": { "const": "admin" } } },
  "then": { "required": ["permissions"] }
}

// Pattern properties (dynamic keys)
{
  "type": "object",
  "patternProperties": {
    "^env_": { "type": "string" }
  }
}

// Reusable definitions
{
  "$defs": {
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" }
      }
    }
  },
  "properties": {
    "home": { "$ref": "#/$defs/address" },
    "work": { "$ref": "#/$defs/address" }
  }
}
```

### 通过命令行进行验证

```bash
# Using ajv-cli (Node.js)
npx ajv-cli validate -s schema.json -d data.json

# Using jsonschema (Python)
pip install jsonschema
python3 -c "
import json, jsonschema
schema = json.load(open('schema.json'))
data = json.load(open('data.json'))
jsonschema.validate(data, schema)
print('Valid')
"

# Validate multiple files
for f in data/*.json; do
  npx ajv-cli validate -s schema.json -d "$f" 2>&1 || echo "INVALID: $f"
done
```

## Zod（TypeScript）

### 基本模式

```typescript
import { z } from 'zod';

// Primitives
const nameSchema = z.string().min(1).max(100);
const ageSchema = z.number().int().min(0).max(150);
const emailSchema = z.string().email();
const urlSchema = z.string().url();

// Objects
const userSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().min(0),
  role: z.enum(['user', 'admin', 'moderator']).default('user'),
  tags: z.array(z.string()).max(10).default([]),
  createdAt: z.string().datetime(),
});

// Infer TypeScript type from schema
type User = z.infer<typeof userSchema>;
// { name: string; email: string; age: number; role: "user" | "admin" | "moderator"; ... }

// Validate
const result = userSchema.safeParse(data);
if (result.success) {
  console.log(result.data); // typed as User
} else {
  console.log(result.error.issues); // validation errors
}

// Parse (throws on invalid)
const user = userSchema.parse(data);
```

### 高级模式

```typescript
// Optional and nullable
const schema = z.object({
  name: z.string(),
  nickname: z.string().optional(),       // string | undefined
  middleName: z.string().nullable(),     // string | null
  suffix: z.string().nullish(),          // string | null | undefined
});

// Transforms (validate then transform)
const dateSchema = z.string().datetime().transform(s => new Date(s));
const trimmed = z.string().trim().toLowerCase();
const parsed = z.string().transform(s => parseInt(s, 10)).pipe(z.number().int());

// Discriminated unions (tagged unions)
const eventSchema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('click'), x: z.number(), y: z.number() }),
  z.object({ type: z.literal('keypress'), key: z.string() }),
  z.object({ type: z.literal('scroll'), delta: z.number() }),
]);

// Recursive types
const categorySchema: z.ZodType<Category> = z.object({
  name: z.string(),
  children: z.lazy(() => z.array(categorySchema)).default([]),
});

// Refinements (custom validation)
const passwordSchema = z.string()
  .min(8)
  .refine(s => /[A-Z]/.test(s), 'Must contain uppercase')
  .refine(s => /[0-9]/.test(s), 'Must contain digit')
  .refine(s => /[^a-zA-Z0-9]/.test(s), 'Must contain special character');

// Extend/merge objects
const baseUser = z.object({ name: z.string(), email: z.string() });
const adminUser = baseUser.extend({ permissions: z.array(z.string()) });

// Pick/omit
const createUser = userSchema.omit({ createdAt: true });
const userSummary = userSchema.pick({ name: true, email: true });

// Passthrough (allow extra fields)
const flexible = userSchema.passthrough();

// Strip unknown fields
const strict = userSchema.strict(); // Error on extra fields
```

### 使用 Zod 进行 API 验证

```typescript
// Express middleware
import { z } from 'zod';

const createUserBody = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  password: z.string().min(8),
});

app.post('/api/users', (req, res) => {
  const result = createUserBody.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: result.error.issues });
  }
  const { name, email, password } = result.data;
  // ... create user
});

// Query parameter validation
const listParams = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['newest', 'oldest', 'name']).default('newest'),
  q: z.string().optional(),
});

app.get('/api/users', (req, res) => {
  const params = listParams.parse(req.query);
  // params.page is a number, params.sort is typed
});
```

## Pydantic（Python）

### 基本模型

```python
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class Address(BaseModel):
    street: str
    city: str
    zip_code: str = Field(pattern=r"^\d{5}(-\d{4})?$")

class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    role: Role = Role.USER
    tags: list[str] = Field(default_factory=list, max_length=10)
    address: Optional[Address] = None
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be blank")
        return v.strip()

# Validate
user = User(name="Alice", email="alice@example.com", age=30)
print(user.model_dump())      # dict
print(user.model_dump_json())  # JSON string

# Validation errors
try:
    User(name="", email="bad", age=-1)
except Exception as e:
    print(e)  # Detailed validation errors
```

### 高级模式

```python
from pydantic import BaseModel, model_validator, ConfigDict
from typing import Literal, Union, Annotated

# Discriminated union
class ClickEvent(BaseModel):
    type: Literal["click"]
    x: int
    y: int

class KeypressEvent(BaseModel):
    type: Literal["keypress"]
    key: str

Event = Annotated[Union[ClickEvent, KeypressEvent], Field(discriminator="type")]

# Model-level validation (cross-field)
class DateRange(BaseModel):
    start: datetime
    end: datetime

    @model_validator(mode="after")
    def end_after_start(self):
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self

# Strict mode (no type coercion)
class StrictUser(BaseModel):
    model_config = ConfigDict(strict=True)
    age: int  # "30" will be rejected, must be int 30

# Alias (accept different field names in input)
class APIResponse(BaseModel):
    user_name: str = Field(alias="userName")
    created_at: datetime = Field(alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

# Computed fields
from pydantic import computed_field

class Order(BaseModel):
    items: list[dict]
    tax_rate: float = 0.08

    @computed_field
    @property
    def total(self) -> float:
        subtotal = sum(i.get("price", 0) * i.get("qty", 1) for i in self.items)
        return round(subtotal * (1 + self.tax_rate), 2)

# Generate JSON Schema
print(User.model_json_schema())
```

### 与 FastAPI 的集成

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class CreateUser(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.post("/api/users", response_model=UserResponse)
async def create_user(body: CreateUser):
    # body is already validated
    return {"id": 1, "name": body.name, "email": body.email}

@app.get("/api/users")
async def list_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = Query(default=None),
):
    # All params validated and typed
    pass
```

## 数据完整性检查

### CSV 验证

```bash
#!/bin/bash
# validate-csv.sh — Check CSV structure and data quality
FILE="${1:?Usage: validate-csv.sh <file.csv>}"

echo "=== CSV Validation: $FILE ==="

# Row count
ROWS=$(wc -l < "$FILE")
echo "Rows: $ROWS (including header)"

# Column count consistency
HEADER_COLS=$(head -1 "$FILE" | awk -F',' '{print NF}')
echo "Columns (header): $HEADER_COLS"

BAD_ROWS=$(awk -F',' -v expected="$HEADER_COLS" 'NR>1 && NF!=expected {count++} END {print count+0}' "$FILE")
if [ "$BAD_ROWS" -gt 0 ]; then
    echo "ERROR: $BAD_ROWS rows have wrong column count"
    awk -F',' -v expected="$HEADER_COLS" 'NR>1 && NF!=expected {print "  Line "NR": "NF" columns (expected "expected")"}' "$FILE" | head -5
else
    echo "Column count: consistent"
fi

# Empty fields
EMPTY=$(awk -F',' '{for(i=1;i<=NF;i++) if($i=="") count++} END {print count}' "$FILE")
echo "Empty fields: $EMPTY"

# Duplicate rows
DUPES=$(($(sort "$FILE" | uniq -d | wc -l)))
echo "Duplicate rows: $DUPES"

echo "=== Done ==="
```

### JSON 验证

```bash
# Check if file is valid JSON
jq empty data.json && echo "Valid JSON" || echo "Invalid JSON"

# Validate structure of each object in an array
jq -e '
  .[] |
  select(
    (.name | type) != "string" or
    (.email | type) != "string" or
    (.age | type) != "number" or
    .age < 0
  )
' data.json && echo "INVALID records found" || echo "All records valid"

# Check for required fields
jq -e '.[] | select(.id == null or .name == null)' data.json

# Check for unique IDs
jq '[.[].id] | length != (. | unique | length)' data.json
# true = duplicates exist

# Compare record counts between source and target
SRC=$(jq length source.json)
TGT=$(jq length target.json)
echo "Source: $SRC, Target: $TGT, Match: $([ "$SRC" = "$TGT" ] && echo yes || echo NO)"
```

### 数据迁移验证

```python
#!/usr/bin/env python3
"""Validate that a data migration preserved all records."""
import json
import sys

def validate_migration(source_path, target_path, key_field="id"):
    with open(source_path) as f:
        source = {r[key_field]: r for r in json.load(f)}
    with open(target_path) as f:
        target = {r[key_field]: r for r in json.load(f)}

    missing = set(source) - set(target)
    extra = set(target) - set(source)
    changed = []

    for key in set(source) & set(target):
        if source[key] != target[key]:
            changed.append(key)

    print(f"Source records: {len(source)}")
    print(f"Target records: {len(target)}")
    print(f"Missing in target: {len(missing)}")
    print(f"Extra in target: {len(extra)}")
    print(f"Changed: {len(changed)}")

    if missing:
        print(f"\nMissing IDs (first 10): {list(missing)[:10]}")
    if extra:
        print(f"\nExtra IDs (first 10): {list(extra)[:10]}")
    if changed:
        print(f"\nChanged IDs (first 5): {changed[:5]}")
        for key in changed[:3]:
            print(f"\n  {key}:")
            for field in set(source[key]) | set(target[key]):
                s = source[key].get(field)
                t = target[key].get(field)
                if s != t:
                    print(f"    {field}: {s!r} → {t!r}")

    return len(missing) == 0 and len(extra) == 0

if __name__ == "__main__":
    ok = validate_migration(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "id")
    sys.exit(0 if ok else 1)
```

## 提示

- 在系统边界（API 端点、文件导入、消息队列等）进行验证，而不是深入到业务逻辑内部。对于内部数据可以适当放宽验证要求。
- Zod 和 Pydantic 都能根据定义自动生成 JSON Schema，可用于文档编写、OpenAPI 规范以及跨语言的数据契约。
- 在 JSON Schema 中设置 `additionalProperties: false` 可以避免字段名称的拼写错误，适用于对数据要求严格的 API。
- Pydantic v2 的性能明显优于 v1；如果不需要隐式类型转换，请使用 `model_config = ConfigDict(strict=True)`。
- Zod 的 `.safeParse()` 方法会返回验证结果对象，而 `.parse()` 方法会抛出异常。在 API 处理函数中应使用 `.safeParse()` 以返回结构化的错误信息。
- 对于 CSV 验证，首先检查列数是否一致——大多数下游问题都源于列对齐错误。
- 数据迁移验证应包括记录数量的对比、检查是否存在缺失或多余的记录，以及对字段值的抽样检查。仅通过计数是不够的。