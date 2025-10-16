/**
 * Prediction Form Screen
 * 예측 입력 화면 - 10개의 특징값 입력
 */

import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Alert, Platform } from 'react-native';
import {
  Title,
  TextInput,
  Button,
  Card,
  HelperText,
  Chip,
  Switch,
  Paragraph,
} from 'react-native-paper';
import ApiService from '../services/api';
import { FEATURES, TEST_SAMPLES } from '../constants/features';

const PredictionFormScreen = ({ navigation }) => {
  const [features, setFeatures] = useState(
    FEATURES.reduce((acc, feature) => {
      acc[feature.name] = feature.default.toString();
      return acc;
    }, {})
  );
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [saveResult, setSaveResult] = useState(true); // 결과 저장 옵션

  // 특징값 업데이트
  const updateFeature = (name, value) => {
    setFeatures({ ...features, [name]: value });
    // 에러 제거
    if (errors[name]) {
      const newErrors = { ...errors };
      delete newErrors[name];
      setErrors(newErrors);
    }
  };

  // 유효성 검사
  const validateFeatures = () => {
    const newErrors = {};
    let isValid = true;

    FEATURES.forEach((feature) => {
      const value = parseFloat(features[feature.name]);
      if (isNaN(value)) {
        newErrors[feature.name] = 'Invalid number';
        isValid = false;
      } else if (value < feature.min || value > feature.max) {
        newErrors[feature.name] = `Must be between ${feature.min} and ${feature.max}`;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  };

  // 예측 실행
  const handlePredict = async () => {
    if (!validateFeatures()) {
      Alert.alert('Validation Error', 'Please check all input values');
      return;
    }

    setLoading(true);
    try {
      // 문자열을 숫자로 변환
      const numericFeatures = Object.keys(features).reduce((acc, key) => {
        acc[key] = parseFloat(features[key]);
        return acc;
      }, {});

      const result = await ApiService.predictExoplanet(numericFeatures, saveResult);

      if (result.success) {
        // 결과 화면으로 이동
        navigation.navigate('PredictionResult', {
          prediction: result.data,
          features: numericFeatures,
        });
      } else {
        Alert.alert('Prediction Error', result.error);
      }
    } catch (error) {
      Alert.alert('Error', error.message);
    } finally {
      setLoading(false);
    }
  };

  // 테스트 샘플 로드
  const loadTestSample = (sampleKey) => {
    const sample = TEST_SAMPLES[sampleKey];
    const newFeatures = {};
    Object.keys(sample.features).forEach((key) => {
      newFeatures[key] = sample.features[key].toString();
    });
    setFeatures(newFeatures);
    setErrors({});
  };

  const Container = Platform.OS === 'web' ? View : ScrollView;
  const containerProps = Platform.OS === 'web'
    ? { style: styles.container }
    : { style: styles.container, contentContainerStyle: styles.scrollContent };

  return (
    <Container {...containerProps}>
      <View style={styles.content}>
        {/* 헤더 */}
        <Card style={styles.headerCard}>
          <Card.Content>
            <Title style={styles.title}>🔭 New Prediction</Title>
          </Card.Content>
        </Card>

        {/* 테스트 샘플 */}
        <Card style={styles.samplesCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Quick Test Samples</Title>
            <View style={styles.sampleChips}>
              {Object.keys(TEST_SAMPLES).map((key) => (
                <Chip
                  key={key}
                  style={styles.sampleChip}
                  onPress={() => loadTestSample(key)}
                >
                  {TEST_SAMPLES[key].name}
                </Chip>
              ))}
            </View>
          </Card.Content>
        </Card>

        {/* 입력 폼 */}
        <Card style={styles.formCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>Features (10 Parameters)</Title>
            {FEATURES.map((feature) => (
              <View key={feature.name} style={styles.inputContainer}>
                <TextInput
                  label={`${feature.label} (${feature.unit})`}
                  value={features[feature.name]}
                  onChangeText={(value) => updateFeature(feature.name, value)}
                  keyboardType="numeric"
                  error={!!errors[feature.name]}
                  style={styles.input}
                  mode="outlined"
                />
                {errors[feature.name] ? (
                  <HelperText type="error" visible={!!errors[feature.name]}>
                    {errors[feature.name]}
                  </HelperText>
                ) : (
                  <HelperText type="info">
                    {feature.description} ({feature.min} - {feature.max})
                  </HelperText>
                )}
              </View>
            ))}
          </Card.Content>
        </Card>

        {/* 저장 옵션 */}
        <Card style={styles.optionsCard}>
          <Card.Content>
            <View style={styles.switchContainer}>
              <View style={styles.switchLabel}>
                <Title style={styles.switchTitle}>💾 Save Result</Title>
                <Paragraph style={styles.switchDescription}>
                  Save prediction to history
                </Paragraph>
              </View>
              <Switch
                value={saveResult}
                onValueChange={setSaveResult}
                color="#6200ee"
              />
            </View>
          </Card.Content>
        </Card>

        {/* 예측 버튼 */}
        <Button
          mode="contained"
          onPress={handlePredict}
          loading={loading}
          disabled={loading}
          style={styles.predictButton}
          contentStyle={styles.buttonContent}
          icon="rocket-launch"
        >
          {loading ? 'Analyzing...' : 'Predict Exoplanet'}
        </Button>
      </View>
    </Container>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    ...(Platform.OS === 'web' && {
      height: '100vh',
      overflow: 'auto',
    }),
  },
  scrollContent: {
    flexGrow: 1,
  },
  content: {
    padding: 16,
    paddingBottom: 32,
  },
  headerCard: {
    marginBottom: 16,
    elevation: 2,
  },
  title: {
    fontSize: 24,
  },
  samplesCard: {
    marginBottom: 16,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 18,
    marginBottom: 12,
  },
  sampleChips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  sampleChip: {
    marginRight: 8,
    marginBottom: 8,
  },
  formCard: {
    marginBottom: 16,
    elevation: 2,
  },
  inputContainer: {
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#fff',
  },
  optionsCard: {
    marginBottom: 16,
    elevation: 2,
  },
  switchContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  switchLabel: {
    flex: 1,
  },
  switchTitle: {
    fontSize: 18,
    marginBottom: 4,
  },
  switchDescription: {
    fontSize: 14,
    color: '#666',
  },
  predictButton: {
    marginBottom: 24,
  },
  buttonContent: {
    height: 50,
  },
});

export default PredictionFormScreen;
