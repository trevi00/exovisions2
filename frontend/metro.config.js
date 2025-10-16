/**
 * Metro configuration for React Native
 * https://reactnative.dev/docs/metro
 */

const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// recharts 및 웹 전용 라이브러리 지원  
config.resolver = {
  ...config.resolver,
  sourceExts: [...(config.resolver?.sourceExts || []), 'jsx', 'js', 'ts', 'tsx', 'json'],
};

module.exports = config;
