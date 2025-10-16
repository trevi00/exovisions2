/**
 * Home Screen
 * 메인 화면 - 앱 소개 및 메뉴
 */

import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Platform } from 'react-native';
import { Title, Paragraph, Button, Card, Chip } from 'react-native-paper';
import ApiService from '../services/api';

const HomeScreen = ({ navigation }) => {
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    const result = await ApiService.healthCheck();
    setApiStatus(result.success ? 'healthy' : 'error');
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
            <Title style={styles.title}>🌌 Exovisions</Title>
            <Paragraph style={styles.subtitle}>
              NASA Space Apps Challenge
            </Paragraph>
            <Paragraph style={styles.description}>
              외계행성 탐지 머신러닝 시스템
            </Paragraph>

            {/* API 상태 */}
            <View style={styles.statusContainer}>
              <Chip
                icon={apiStatus === 'healthy' ? 'check-circle' : 'alert-circle'}
                style={[
                  styles.statusChip,
                  apiStatus === 'healthy' ? styles.statusHealthy : styles.statusError,
                ]}
                textStyle={styles.statusText}
              >
                API: {apiStatus === 'healthy' ? 'Connected' : 'Disconnected'}
              </Chip>
            </View>
          </Card.Content>
        </Card>

        {/* 모델 정보 */}
        <Card style={styles.infoCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>📊 Model Information</Title>
            <View style={styles.infoRow}>
              <Paragraph style={styles.infoLabel}>Type:</Paragraph>
              <Paragraph style={styles.infoValue}>
                3-Class Classification
              </Paragraph>
            </View>
            <View style={styles.infoRow}>
              <Paragraph style={styles.infoLabel}>Classes:</Paragraph>
              <View style={styles.classChips}>
                <Chip style={styles.classChip} textStyle={styles.chipText}>
                  CONFIRMED
                </Chip>
                <Chip style={styles.classChip} textStyle={styles.chipText}>
                  CANDIDATE
                </Chip>
                <Chip style={styles.classChip} textStyle={styles.chipText}>
                  FALSE POSITIVE
                </Chip>
              </View>
            </View>
            <View style={styles.infoRow}>
              <Paragraph style={styles.infoLabel}>Datasets:</Paragraph>
              <Paragraph style={styles.infoValue}>
                Kepler, K2, TESS (21,495 samples)
              </Paragraph>
            </View>
            <View style={styles.infoRow}>
              <Paragraph style={styles.infoLabel}>Features:</Paragraph>
              <Paragraph style={styles.infoValue}>10 parameters</Paragraph>
            </View>
          </Card.Content>
        </Card>

        {/* 메뉴 버튼 */}
        <View style={styles.menuContainer}>
          <Button
            mode="contained"
            icon="rocket-launch"
            onPress={() => navigation.navigate('PredictionForm')}
            style={styles.menuButton}
            contentStyle={styles.buttonContent}
          >
            New Prediction
          </Button>

          <Button
            mode="outlined"
            icon="history"
            onPress={() => navigation.navigate('History')}
            style={styles.menuButton}
            contentStyle={styles.buttonContent}
          >
            Prediction History
          </Button>

          <Button
            mode="outlined"
            icon="information"
            onPress={() => navigation.navigate('About')}
            style={styles.menuButton}
            contentStyle={styles.buttonContent}
          >
            About
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
  headerCard: {
    marginBottom: 16,
    elevation: 4,
    backgroundColor: '#1a1a2e',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: '#aaa',
    marginBottom: 8,
  },
  description: {
    fontSize: 16,
    color: '#ddd',
    marginBottom: 12,
  },
  statusContainer: {
    marginTop: 8,
  },
  statusChip: {
    alignSelf: 'flex-start',
  },
  statusHealthy: {
    backgroundColor: '#4CAF50',
  },
  statusError: {
    backgroundColor: '#F44336',
  },
  statusText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  infoCard: {
    marginBottom: 16,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 20,
    marginBottom: 12,
  },
  infoRow: {
    marginBottom: 12,
  },
  infoLabel: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  infoValue: {
    fontSize: 14,
    color: '#666',
  },
  classChips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 4,
  },
  classChip: {
    marginRight: 8,
    marginBottom: 4,
  },
  chipText: {
    fontSize: 12,
  },
  menuContainer: {
    marginTop: 8,
  },
  menuButton: {
    marginBottom: 12,
  },
  buttonContent: {
    height: 50,
  },
});

export default HomeScreen;
