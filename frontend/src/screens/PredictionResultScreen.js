/**
 * Prediction Result Screen
 * 예측 결과 화면
 */

import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Platform, Alert } from 'react-native';
import {
  Title,
  Paragraph,
  Card,
  Chip,
  Button,
  DataTable,
  ProgressBar,
} from 'react-native-paper';
import { CLASSIFICATION_COLORS, CONFIDENCE_COLORS } from '../constants/features';
import ApiService from '../services/api';

// 시각화 컴포넌트
import OrbitVisualization from '../components/OrbitVisualization';
import TransitLightCurve from '../components/TransitLightCurve';
import DistributionChart from '../components/DistributionChart';
import ROCCurve from '../components/ROCCurve';

const PredictionResultScreen = ({ route, navigation }) => {
  const { prediction, features } = route.params;
  const [saving, setSaving] = useState(false);
  const [isSaved, setIsSaved] = useState(!!prediction.id); // id가 있으면 이미 저장됨

  // 분류 색상
  const classificationColor =
    CLASSIFICATION_COLORS[prediction.classification] || '#757575';

  // 신뢰도 색상
  const confidenceColor =
    CONFIDENCE_COLORS[prediction.confidence_level] || '#757575';

  // 결과 저장 핸들러
  const handleSaveResult = async () => {
    if (isSaved) {
      Alert.alert('Already Saved', 'This prediction is already saved in history.');
      return;
    }

    setSaving(true);
    try {
      // 숫자 형식으로 변환된 features로 다시 예측 (save_result=true)
      const result = await ApiService.predictExoplanet(features, true);

      if (result.success) {
        setIsSaved(true);
        Alert.alert(
          'Saved Successfully',
          'Prediction has been saved to history.',
          [
            {
              text: 'View History',
              onPress: () => navigation.navigate('History'),
            },
            { text: 'OK' },
          ]
        );
      } else {
        Alert.alert('Save Error', result.error);
      }
    } catch (error) {
      Alert.alert('Error', error.message);
    } finally {
      setSaving(false);
    }
  };

  const Container = Platform.OS === 'web' ? View : ScrollView;
  const containerProps = Platform.OS === 'web'
    ? { style: styles.container }
    : { style: styles.container, contentContainerStyle: styles.scrollContent };

  return (
    <Container {...containerProps}>
      <View style={styles.content}>
        {/* 결과 카드 */}
        <Card style={styles.resultCard}>
          <Card.Content>
            <View style={styles.iconContainer}>
              <Title style={styles.resultIcon}>
                {prediction.is_exoplanet ? '✅' : '❌'}
              </Title>
            </View>

            <Title style={styles.resultTitle}>
              {prediction.is_exoplanet ? 'Exoplanet Detected!' : 'Not an Exoplanet'}
            </Title>

            <View style={styles.classificationContainer}>
              <Chip
                style={[
                  styles.classificationChip,
                  { backgroundColor: classificationColor },
                ]}
                textStyle={styles.chipText}
              >
                {prediction.classification}
              </Chip>
            </View>
          </Card.Content>
        </Card>

        {/* 신뢰도 카드 */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Confidence</Title>

            <View style={styles.confidenceRow}>
              <Paragraph style={styles.confidenceLabel}>Score:</Paragraph>
              <Paragraph style={styles.confidenceValue}>
                {(prediction.confidence_score * 100).toFixed(1)}%
              </Paragraph>
            </View>
            <ProgressBar
              progress={prediction.confidence_score}
              color={confidenceColor}
              style={styles.progressBar}
            />

            <View style={styles.confidenceChipContainer}>
              <Chip
                style={[
                  styles.confidenceChip,
                  { backgroundColor: confidenceColor },
                ]}
                textStyle={styles.chipText}
              >
                {prediction.confidence_level.replace('_', ' ')}
              </Chip>
            </View>
          </Card.Content>
        </Card>

        {/* 확률 카드 */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Probabilities</Title>

            <View style={styles.probabilitySection}>
              <View style={styles.probabilityRow}>
                <Paragraph style={styles.probabilityLabel}>
                  CONFIRMED Planet:
                </Paragraph>
                <Paragraph style={styles.probabilityValue}>
                  {(prediction.planet_probability * 100).toFixed(2)}%
                </Paragraph>
              </View>
              <ProgressBar
                progress={prediction.planet_probability}
                color="#4CAF50"
                style={styles.progressBar}
              />
            </View>

            <View style={styles.probabilitySection}>
              <View style={styles.probabilityRow}>
                <Paragraph style={styles.probabilityLabel}>
                  CANDIDATE:
                </Paragraph>
                <Paragraph style={styles.probabilityValue}>
                  {(prediction.candidate_probability * 100).toFixed(2)}%
                </Paragraph>
              </View>
              <ProgressBar
                progress={prediction.candidate_probability}
                color="#FFC107"
                style={styles.progressBar}
              />
            </View>

            <View style={styles.probabilitySection}>
              <View style={styles.probabilityRow}>
                <Paragraph style={styles.probabilityLabel}>
                  FALSE POSITIVE:
                </Paragraph>
                <Paragraph style={styles.probabilityValue}>
                  {(
                    (1 -
                      prediction.planet_probability -
                      prediction.candidate_probability) *
                    100
                  ).toFixed(2)}
                  %
                </Paragraph>
              </View>
              <ProgressBar
                progress={
                  1 - prediction.planet_probability - prediction.candidate_probability
                }
                color="#F44336"
                style={styles.progressBar}
              />
            </View>
          </Card.Content>
        </Card>

        {/* 입력 특징값 카드 */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Input Features</Title>
            <DataTable>
              {Object.keys(features).map((key) => (
                <DataTable.Row key={key}>
                  <DataTable.Cell>
                    {key.replace(/_/g, ' ').toUpperCase()}
                  </DataTable.Cell>
                  <DataTable.Cell numeric>{features[key]}</DataTable.Cell>
                </DataTable.Row>
              ))}
            </DataTable>
          </Card.Content>
        </Card>

        {/* 시각화: 행성 궤도 */}
        {Platform.OS === 'web' && (
          <Card style={styles.card}>
            <Card.Content>
              <Title style={styles.cardTitle}>🪐 Predicted Orbit</Title>
              <OrbitVisualization
                orbitalPeriod={features.orbital_period || 10}
                planetRadius={features.planet_radius || 1}
              />
            </Card.Content>
          </Card>
        )}

        {/* 시각화: Transit Light Curve */}
        {Platform.OS === 'web' && (
          <Card style={styles.card}>
            <Card.Content>
              <TransitLightCurve
                transitDepth={features.transit_depth || 500}
                transitDuration={features.transit_duration || 2.5}
              />
            </Card.Content>
          </Card>
        )}

        {/* 시각화: ROC Curve */}
        {Platform.OS === 'web' && (
          <Card style={styles.card}>
            <Card.Content>
              <ROCCurve />
            </Card.Content>
          </Card>
        )}

        {/* 시각화: Planet Radius Distribution */}
        {Platform.OS === 'web' && (
          <Card style={styles.card}>
            <Card.Content>
              <DistributionChart
                type="radius"
                currentValue={features.planet_radius}
              />
            </Card.Content>
          </Card>
        )}

        {/* 시각화: Transit Duration Distribution */}
        {Platform.OS === 'web' && (
          <Card style={styles.card}>
            <Card.Content>
              <DistributionChart
                type="duration"
                currentValue={features.transit_duration}
              />
            </Card.Content>
          </Card>
        )}

        {/* 액션 버튼 */}
        <View style={styles.buttonContainer}>
          {/* 저장 버튼 (저장되지 않은 경우만 표시) */}
          {!isSaved && (
            <Button
              mode="contained"
              onPress={handleSaveResult}
              loading={saving}
              disabled={saving}
              style={[styles.button, styles.saveButton]}
              icon="content-save"
            >
              {saving ? 'Saving...' : 'Save to History'}
            </Button>
          )}

          {/* 이미 저장된 경우 표시 */}
          {isSaved && (
            <Button
              mode="contained"
              disabled
              style={[styles.button, styles.savedButton]}
              icon="check-circle"
            >
              Saved to History
            </Button>
          )}

          <Button
            mode="contained"
            onPress={() => navigation.navigate('PredictionForm')}
            style={styles.button}
            icon="replay"
          >
            New Prediction
          </Button>

          <Button
            mode="outlined"
            onPress={() => navigation.navigate('Home')}
            style={styles.button}
            icon="home"
          >
            Back to Home
          </Button>
        </View>
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
  resultCard: {
    marginBottom: 16,
    elevation: 4,
    backgroundColor: '#1a1a2e',
  },
  iconContainer: {
    alignItems: 'center',
    marginBottom: 12,
  },
  resultIcon: {
    fontSize: 64,
  },
  resultTitle: {
    fontSize: 24,
    textAlign: 'center',
    color: '#fff',
    marginBottom: 16,
  },
  classificationContainer: {
    alignItems: 'center',
  },
  classificationChip: {
    paddingHorizontal: 12,
  },
  chipText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 14,
  },
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 18,
    marginBottom: 12,
  },
  confidenceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  confidenceLabel: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  confidenceValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
    marginBottom: 12,
  },
  confidenceChipContainer: {
    alignItems: 'center',
  },
  confidenceChip: {
    marginTop: 8,
  },
  probabilitySection: {
    marginBottom: 16,
  },
  probabilityRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  probabilityLabel: {
    fontSize: 14,
  },
  probabilityValue: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  buttonContainer: {
    marginTop: 8,
    marginBottom: 24,
  },
  button: {
    marginBottom: 12,
  },
  saveButton: {
    backgroundColor: '#4CAF50',
  },
  savedButton: {
    backgroundColor: '#9E9E9E',
  },
});

export default PredictionResultScreen;
