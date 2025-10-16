/**
 * API Service
 * Exoplanet Detection API 통신 서비스
 */

import axios from 'axios';
import { config, log } from '../config/environment';

// Axios 인스턴스 생성 - 환경 설정에서 가져온 값 사용
const apiClient = axios.create({
  baseURL: config.apiUrl,
  timeout: config.apiTimeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터
apiClient.interceptors.request.use(
  (config) => {
    log.info(`[API Request] ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    log.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => {
    log.info(`[API Response] ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    log.error('[API Response Error]', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * API 서비스
 */
const ApiService = {
  /**
   * 헬스 체크
   */
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  /**
   * 외계행성 예측
   * @param {Object} features - 10개의 특징값
   * @param {boolean} saveResult - 결과 저장 여부
   */
  predictExoplanet: async (features, saveResult = false) => {
    try {
      const response = await apiClient.post('/predictions/', {
        features,
        save_result: saveResult,
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
      };
    }
  },

  /**
   * 예측 목록 조회
   * @param {number} skip - 건너뛸 개수
   * @param {number} limit - 조회할 개수
   * @param {boolean|null} isExoplanet - 외계행성 여부 필터
   */
  getPredictions: async (skip = 0, limit = 100, isExoplanet = null) => {
    try {
      const params = { skip, limit };
      if (isExoplanet !== null) {
        params.is_exoplanet = isExoplanet;
      }
      const response = await apiClient.get('/predictions/', { params });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
      };
    }
  },

  /**
   * 단일 예측 조회
   * @param {string} predictionId - 예측 ID
   */
  getPredictionById: async (predictionId) => {
    try {
      const response = await apiClient.get(`/predictions/${predictionId}`);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
      };
    }
  },

  /**
   * 예측 삭제
   * @param {string} predictionId - 예측 ID
   */
  deletePrediction: async (predictionId) => {
    try {
      const response = await apiClient.delete(`/predictions/${predictionId}`);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
      };
    }
  },

  /**
   * 전체 예측 삭제
   * @param {boolean|null} isExoplanet - 외계행성 여부 필터
   */
  deleteAllPredictions: async (isExoplanet = null) => {
    try {
      const params = {};
      if (isExoplanet !== null) {
        params.is_exoplanet = isExoplanet;
      }
      const response = await apiClient.delete('/predictions/', { params });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
      };
    }
  },

  /**
   * 특징값 분포 통계 조회
   */
  getDistributions: async () => {
    try {
      const response = await apiClient.get('/statistics/distributions');
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
      };
    }
  },

  /**
   * ROC 곡선 데이터 조회
   */
  getROCCurve: async () => {
    try {
      const response = await apiClient.get('/statistics/roc-curve');
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
      };
    }
  },

  /**
   * 모델 성능 통계 조회
   */
  getModelPerformance: async () => {
    try {
      const response = await apiClient.get('/statistics/model-performance');
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message,
      };
    }
  },
};

export default ApiService;
