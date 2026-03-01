module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/test'],
  testPathIgnorePatterns: ['/node_modules/', '/test/integration/'],
  collectCoverageFrom: ['src/**/*.ts']
};
