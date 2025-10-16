/**
 * 환경 설정
 * 개발/프로덕션 환경별 설정을 관리합니다.
 */

import { Platform } from 'react-native';

// 환경 변수 (필요시 .env 파일이나 react-native-dotenv로 대체 가능)
const ENV = {
  development: {
    apiUrl: 'http://127.0.0.1:8000/api/v1',
    apiTimeout: 30000,
    debug: true,
  },
  production: {
    apiUrl: process.env.API_URL || 'https://api.exovisions.com/api/v1',
    apiTimeout: 30000,
    debug: false,
  },
};

// 현재 환경 결정 (__DEV__는 React Native에서 제공하는 전역 변수)
const currentEnv = __DEV__ ? 'development' : 'production';

// 현재 환경 설정 export
export const config = ENV[currentEnv];

// 플랫폼별 설정
export const platformConfig = {
  isWeb: Platform.OS === 'web',
  isIOS: Platform.OS === 'ios',
  isAndroid: Platform.OS === 'android',
};

// 로깅 유틸리티
export const log = {
  info: (...args) => {
    if (config.debug) {
      console.log('[INFO]', ...args);
    }
  },
  error: (...args) => {
    if (config.debug) {
      console.error('[ERROR]', ...args);
    }
  },
  warn: (...args) => {
    if (config.debug) {
      console.warn('[WARN]', ...args);
    }
  },
};

export default config;
