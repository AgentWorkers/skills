---
name: device-testing
description: 使用Jest、Detox E2E以及React Native Testing Library进行React Native应用测试。这些工具可用于移动应用的测试策略，以及模拟原生模块的功能。
---

# 设备测试专家

具备全面的React Native测试策略专业知识，从单元测试到在真实设备和模拟器上进行端到端测试。专注于使用Jest、Detox、React Native Testing Library以及移动测试的最佳实践。

## 我的专长

### 移动应用测试体系结构

**三个层次**
1. **单元测试**（70%）：快速、独立的测试逻辑
2. **集成测试**（20%）：测试组件之间的交互
3. **端到端测试**（10%）：在设备上测试完整的用户流程

**工具**
- **Jest**：用于单元测试和集成测试
- **React Native Testing Library**：用于组件测试
- **Detox**：用于在模拟器上进行端到端测试
- **Maestro**：另一种端到端测试工具（较新）

### 使用Jest进行单元测试

**基本组件测试**
```javascript
// UserProfile.test.js
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import UserProfile from './UserProfile';

describe('UserProfile', () => {
  it('renders user name correctly', () => {
    const user = { name: 'John Doe', email: 'john@example.com' };
    const { getByText } = render(<UserProfile user={user} />);

    expect(getByText('John Doe')).toBeTruthy();
    expect(getByText('john@example.com')).toBeTruthy();
  });

  it('calls onPress when button is pressed', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <UserProfile user={{ name: 'John' }} onPress={onPress} />
    );

    fireEvent.press(getByText('Edit Profile'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });
});
```

**测试钩子**
```javascript
// useCounter.test.js
import { renderHook, act } from '@testing-library/react-hooks';
import useCounter from './useCounter';

describe('useCounter', () => {
  it('increments counter', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('decrements counter', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });
});
```

**异步测试**
```javascript
// api.test.js
import { fetchUser } from './api';

describe('fetchUser', () => {
  it('fetches user data successfully', async () => {
    const user = await fetchUser('123');

    expect(user).toEqual({
      id: '123',
      name: 'John Doe',
      email: 'john@example.com'
    });
  });

  it('handles errors gracefully', async () => {
    await expect(fetchUser('invalid')).rejects.toThrow('User not found');
  });
});
```

**快照测试**
```javascript
// Button.test.js
import React from 'react';
import { render } from '@testing-library/react-native';
import Button from './Button';

describe('Button', () => {
  it('renders correctly', () => {
    const { toJSON } = render(<Button title="Press Me" />);
    expect(toJSON()).toMatchSnapshot();
  });

  it('renders with custom color', () => {
    const { toJSON } = render(<Button title="Press Me" color="red" />);
    expect(toJSON()).toMatchSnapshot();
  });
});
```

### 模拟（Mocking）

**模拟原生模块**
```javascript
// __mocks__/react-native-camera.js
export const RNCamera = {
  Constants: {
    Type: {
      back: 'back',
      front: 'front'
    }
  }
};

// In test file
jest.mock('react-native-camera', () => require('./__mocks__/react-native-camera'));

// Or inline mock
jest.mock('react-native-camera', () => ({
  RNCamera: {
    Constants: {
      Type: { back: 'back', front: 'front' }
    }
  }
}));
```

**模拟localStorage**
```javascript
// Setup file (jest.setup.js)
import mockAsyncStorage from '@react-native-async-storage/async-storage/jest/async-storage-mock';

jest.mock('@react-native-async-storage/async-storage', () => mockAsyncStorage);

// In test
import AsyncStorage from '@react-native-async-storage/async-storage';

describe('Storage', () => {
  beforeEach(() => {
    AsyncStorage.clear();
  });

  it('stores and retrieves data', async () => {
    await AsyncStorage.setItem('key', 'value');
    const value = await AsyncStorage.getItem('key');
    expect(value).toBe('value');
  });
});
```

**模拟导航逻辑**
```javascript
// Mock React Navigation
jest.mock('@react-navigation/native', () => ({
  useNavigation: () => ({
    navigate: jest.fn(),
    goBack: jest.fn()
  })
}));

// In test
import { useNavigation } from '@react-navigation/native';

describe('ProfileScreen', () => {
  it('navigates to settings on button press', () => {
    const navigate = jest.fn();
    useNavigation.mockReturnValue({ navigate });

    const { getByText } = render(<ProfileScreen />);
    fireEvent.press(getByText('Settings'));

    expect(navigate).toHaveBeenCalledWith('Settings');
  });
});
```

**模拟API调用**
```javascript
// Using jest.mock
jest.mock('./api', () => ({
  fetchUser: jest.fn(() => Promise.resolve({
    id: '123',
    name: 'Mock User'
  }))
}));

// Using MSW (Mock Service Worker)
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/user/:id', (req, res, ctx) => {
    return res(ctx.json({
      id: req.params.id,
      name: 'Mock User'
    }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### 使用React Native Testing Library进行组件测试

**数据查询**
```javascript
import { render, screen } from '@testing-library/react-native';

// By text
screen.getByText('Submit');
screen.findByText('Loading...');  // Async
screen.queryByText('Error');  // Returns null if not found

// By testID
<View testID="profile-container" />
screen.getByTestId('profile-container');

// By placeholder
<TextInput placeholder="Enter email" />
screen.getByPlaceholderText('Enter email');

// By display value
screen.getByDisplayValue('john@example.com');

// Multiple queries
screen.getAllByText('Item');  // Returns array
```

**用户交互**
```javascript
import { render, fireEvent, waitFor } from '@testing-library/react-native';

describe('LoginForm', () => {
  it('submits form with valid data', async () => {
    const onSubmit = jest.fn();
    const { getByPlaceholderText, getByText } = render(
      <LoginForm onSubmit={onSubmit} />
    );

    // Type into inputs
    fireEvent.changeText(getByPlaceholderText('Email'), 'test@example.com');
    fireEvent.changeText(getByPlaceholderText('Password'), 'password123');

    // Press button
    fireEvent.press(getByText('Login'));

    // Wait for async operation
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      });
    });
  });
});
```

### 使用Detox进行端到端测试

**安装**
```bash
# Install Detox
npm install --save-dev detox

# iOS: Install dependencies
brew tap wix/brew
brew install applesimutils

# Initialize Detox
detox init

# Build app for testing (iOS)
detox build --configuration ios.sim.debug

# Run tests
detox test --configuration ios.sim.debug
```

**配置文件 (.detoxrc.js)**
```javascript
module.exports = {
  testRunner: 'jest',
  runnerConfig: 'e2e/config.json',
  apps: {
    'ios.debug': {
      type: 'ios.app',
      binaryPath: 'ios/build/Build/Products/Debug-iphonesimulator/MyApp.app',
      build: 'xcodebuild -workspace ios/MyApp.xcworkspace -scheme MyApp -configuration Debug -sdk iphonesimulator -derivedDataPath ios/build'
    },
    'android.debug': {
      type: 'android.apk',
      binaryPath: 'android/app/build/outputs/apk/debug/app-debug.apk',
      build: 'cd android && ./gradlew assembleDebug assembleAndroidTest -DtestBuildType=debug'
    }
  },
  devices: {
    simulator: {
      type: 'ios.simulator',
      device: { type: 'iPhone 15 Pro' }
    },
    emulator: {
      type: 'android.emulator',
      device: { avdName: 'Pixel_6_API_34' }
    }
  },
  configurations: {
    'ios.sim.debug': {
      device: 'simulator',
      app: 'ios.debug'
    },
    'android.emu.debug': {
      device: 'emulator',
      app: 'android.debug'
    }
  }
};
```

**编写Detox测试用例**
```javascript
// e2e/login.test.js
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should login successfully with valid credentials', async () => {
    // Type email
    await element(by.id('email-input')).typeText('test@example.com');

    // Type password
    await element(by.id('password-input')).typeText('password123');

    // Tap login button
    await element(by.id('login-button')).tap();

    // Verify navigation to home screen
    await expect(element(by.id('home-screen'))).toBeVisible();
  });

  it('should show error with invalid credentials', async () => {
    await element(by.id('email-input')).typeText('invalid@example.com');
    await element(by.id('password-input')).typeText('wrong');
    await element(by.id('login-button')).tap();

    await expect(element(by.text('Invalid credentials'))).toBeVisible();
  });

  it('should scroll to bottom of list', async () => {
    await element(by.id('user-list')).scrollTo('bottom');
    await expect(element(by.id('load-more-button'))).toBeVisible();
  });
});
```

**高级Detox功能**
```javascript
// Swipe
await element(by.id('carousel')).swipe('left', 'fast', 0.75);

// Scroll
await element(by.id('scroll-view')).scroll(200, 'down');

// Long press
await element(by.id('item-1')).longPress();

// Multi-tap
await element(by.id('like-button')).multiTap(2);

// Wait for element
await waitFor(element(by.id('success-message')))
  .toBeVisible()
  .withTimeout(5000);

// Take screenshot
await device.takeScreenshot('login-success');
```

### Maestro（另一种端到端测试工具）

**安装**
```bash
# Install Maestro
curl -Ls "https://get.maestro.mobile.dev" | bash

# Verify installation
maestro --version
```

**Maestro测试流程（基于YAML）**
```yaml
# flows/login.yaml
appId: com.myapp

---
# Launch app
- launchApp

# Wait for login screen
- assertVisible: "Login"

# Enter credentials
- tapOn: "Email"
- inputText: "test@example.com"
- tapOn: "Password"
- inputText: "password123"

# Submit
- tapOn: "Login"

# Verify success
- assertVisible: "Welcome"
```

**运行Maestro测试流程**
```bash
# iOS Simulator
maestro test flows/login.yaml

# Android Emulator
maestro test --platform android flows/login.yaml

# Real device (USB connected)
maestro test --device <device-id> flows/login.yaml
```

## 适用场景

当您需要以下帮助时，请联系我：
- 为React Native项目配置Jest
- 为组件和测试钩子编写单元测试
- 模拟原生模块及其依赖项
- 编写集成测试
- 配置Detox或Maestro进行端到端测试
- 测试异步操作
- 采用快照测试策略
- 测试导航流程
- 调试测试失败
- 在持续集成/持续部署（CI/CD）流程中运行测试
- 在真实设备上进行测试
- 制定性能测试策略

## 测试配置

**Jest配置文件 (jest.config.js)**
```javascript
module.exports = {
  preset: 'react-native',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  transformIgnorePatterns: [
    'node_modules/(?!(react-native|@react-native|@react-navigation|expo|@expo)/)'
  ],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.test.{js,jsx,ts,tsx}',
    '!src/**/__tests__/**'
  ],
  coverageThreshold: {
    global: {
      statements: 80,
      branches: 75,
      functions: 80,
      lines: 80
    }
  }
};
```

**Jest初始化配置 (jest.setup.js)**
```javascript
import 'react-native-gesture-handler/jestSetup';

// Mock native modules
jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');

// Mock AsyncStorage
import mockAsyncStorage from '@react-native-async-storage/async-storage/jest/async-storage-mock';
jest.mock('@react-native-async-storage/async-storage', () => mockAsyncStorage);

// Global test utilities
global.fetch = jest.fn();

// Silence console warnings in tests
global.console = {
  ...console,
  warn: jest.fn(),
  error: jest.fn()
};
```

## 专业技巧与建议

### 1. 为端到端测试添加测试ID

在组件中添加测试ID，以确保测试选择器的准确性：
```javascript
// In component
<TouchableOpacity testID="submit-button" onPress={handleSubmit}>
  <Text>Submit</Text>
</TouchableOpacity>

// In Detox test
await element(by.id('submit-button')).tap();

// Avoid using text or accessibility labels (can change with i18n)
```

### 2. 使用测试工厂生成模拟数据

```javascript
// testUtils/factories.js
export const createMockUser = (overrides = {}) => ({
  id: '123',
  name: 'John Doe',
  email: 'john@example.com',
  ...overrides
});

// In test
const user = createMockUser({ name: 'Jane Doe' });
```

### 3. 使用Provider实现自定义渲染逻辑

```javascript
// testUtils/render.js
import { render } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { Provider } from 'react-redux';
import { store } from '../store';

export function renderWithProviders(ui, options = {}) {
  return render(
    <Provider store={store}>
      <NavigationContainer>
        {ui}
      </NavigationContainer>
    </Provider>,
    options
  );
}

// In test
import { renderWithProviders } from './testUtils/render';
renderWithProviders(<MyScreen />);
```

### 4. 并行执行测试

```json
// package.json
{
  "scripts": {
    "test": "jest --maxWorkers=4",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

## 与SpecWeave的集成

**测试规划**
- 在 `spec.md` 文件中记录测试策略
- 在 `tasks.md` 文件中指定测试覆盖目标
- 将测试用例嵌入到测试任务中（采用BDD格式）

**测试覆盖率监控**
- 为关键路径设定覆盖率阈值（80%以上）
- 跟踪每次代码更新后的覆盖率变化
- 在版本报告中记录测试覆盖情况

**持续集成/持续部署（CI/CD）**
- 在每次代码提交时自动运行测试
- 如果测试失败，则阻止代码合并
- 生成测试覆盖率报告
- 在预发布版本（staging build）上执行端到端测试