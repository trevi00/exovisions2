/**
 * 외계행성 특징값 상수 및 설정
 */

/**
 * 10개의 특징값 정의
 */
export const FEATURES = [
  {
    name: 'orbital_period',
    label: 'Orbital Period',
    unit: 'days',
    description: '궤도 주기',
    min: 0.1,
    max: 1000,
    default: 3.5,
    step: 0.1,
  },
  {
    name: 'transit_duration',
    label: 'Transit Duration',
    unit: 'hours',
    description: '통과 지속시간',
    min: 0.1,
    max: 24,
    default: 2.5,
    step: 0.1,
  },
  {
    name: 'transit_depth',
    label: 'Transit Depth',
    unit: 'ppm',
    description: '통과 깊이',
    min: 1,
    max: 10000,
    default: 500,
    step: 10,
  },
  {
    name: 'planet_radius',
    label: 'Planet Radius',
    unit: 'R⊕',
    description: '행성 반지름 (지구 기준)',
    min: 0.1,
    max: 20,
    default: 2.0,
    step: 0.1,
  },
  {
    name: 'equilibrium_temp',
    label: 'Equilibrium Temperature',
    unit: 'K',
    description: '평형 온도',
    min: 100,
    max: 3000,
    default: 1200,
    step: 10,
  },
  {
    name: 'insolation',
    label: 'Insolation',
    unit: 'S⊕',
    description: '일사량 (지구 기준)',
    min: 0.1,
    max: 2000,
    default: 100,
    step: 1,
  },
  {
    name: 'signal_to_noise',
    label: 'Signal to Noise',
    unit: '',
    description: '신호 대 잡음비',
    min: 1,
    max: 200,
    default: 50,
    step: 1,
  },
  {
    name: 'stellar_temp',
    label: 'Stellar Temperature',
    unit: 'K',
    description: '별의 온도',
    min: 2000,
    max: 10000,
    default: 5800,
    step: 100,
  },
  {
    name: 'stellar_logg',
    label: 'Stellar Log(g)',
    unit: 'log(g)',
    description: '별의 표면 중력',
    min: 3.0,
    max: 5.0,
    default: 4.5,
    step: 0.1,
  },
  {
    name: 'stellar_radius',
    label: 'Stellar Radius',
    unit: 'R☉',
    description: '별의 반지름 (태양 기준)',
    min: 0.1,
    max: 3.0,
    default: 1.0,
    step: 0.1,
  },
];

/**
 * 분류 결과 색상 매핑
 */
export const CLASSIFICATION_COLORS = {
  CONFIRMED: '#4CAF50',
  LIKELY_CONFIRMED: '#8BC34A',
  CANDIDATE: '#FFC107',
  FALSE_POSITIVE: '#F44336',
};

/**
 * 신뢰도 레벨 색상 매핑
 */
export const CONFIDENCE_COLORS = {
  VERY_HIGH: '#4CAF50',
  HIGH: '#8BC34A',
  MEDIUM: '#FFC107',
  LOW: '#FF9800',
  VERY_LOW: '#F44336',
};

/**
 * 사전 정의된 테스트 샘플
 */
export const TEST_SAMPLES = {
  typical_exoplanet: {
    name: 'Typical Exoplanet',
    description: '전형적인 외계행성 (CONFIRMED 예상)',
    features: {
      orbital_period: 3.5,
      transit_duration: 2.5,
      transit_depth: 500.0,
      planet_radius: 2.0,
      equilibrium_temp: 1200.0,
      insolation: 100.0,
      signal_to_noise: 50.0,
      stellar_temp: 5800.0,
      stellar_logg: 4.5,
      stellar_radius: 1.0,
    },
  },
  hot_jupiter: {
    name: 'Hot Jupiter',
    description: '뜨거운 목성형 행성 (FALSE_POSITIVE 예상)',
    features: {
      orbital_period: 0.5,
      transit_duration: 1.0,
      transit_depth: 1000.0,
      planet_radius: 12.0,
      equilibrium_temp: 2000.0,
      insolation: 1000.0,
      signal_to_noise: 80.0,
      stellar_temp: 6500.0,
      stellar_logg: 4.0,
      stellar_radius: 1.2,
    },
  },
  earth_analog: {
    name: 'Earth Analog',
    description: '지구 유사 행성 (FALSE_POSITIVE 예상)',
    features: {
      orbital_period: 365.0,
      transit_duration: 13.0,
      transit_depth: 84.0,
      planet_radius: 1.0,
      equilibrium_temp: 288.0,
      insolation: 1.0,
      signal_to_noise: 15.0,
      stellar_temp: 5778.0,
      stellar_logg: 4.44,
      stellar_radius: 1.0,
    },
  },
  false_positive: {
    name: 'Clear False Positive',
    description: '명확한 거짓 양성 (FALSE_POSITIVE 예상)',
    features: {
      orbital_period: 10.0,
      transit_duration: 8.0,
      transit_depth: 200.0,
      planet_radius: 0.5,
      equilibrium_temp: 800.0,
      insolation: 50.0,
      signal_to_noise: 5.0,
      stellar_temp: 4500.0,
      stellar_logg: 4.2,
      stellar_radius: 0.8,
    },
  },
  candidate: {
    name: 'Planet Candidate',
    description: '행성 후보 (CANDIDATE 예상)',
    features: {
      orbital_period: 3.5,
      transit_duration: 2.5,
      transit_depth: 150.0,
      planet_radius: 2.0,
      equilibrium_temp: 1200.0,
      insolation: 100.0,
      signal_to_noise: 12.0,
      stellar_temp: 5800.0,
      stellar_logg: 4.5,
      stellar_radius: 1.0,
    },
  },
};
