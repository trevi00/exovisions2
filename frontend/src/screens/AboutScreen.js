/**
 * About Screen
 * 앱 정보 화면
 */

import React from 'react';
import { View, StyleSheet, ScrollView, Linking, Platform } from 'react-native';
import { Title, Paragraph, Card, Button, List } from 'react-native-paper';

const AboutScreen = () => {
  const openLink = (url) => {
    Linking.openURL(url).catch((err) =>
      console.error('Failed to open URL:', err)
    );
  };

  const Container = Platform.OS === 'web' ? View : ScrollView;
  const containerProps = Platform.OS === 'web'
    ? { style: styles.container }
    : { style: styles.container, contentContainerStyle: styles.scrollContent };

  return (
    <Container {...containerProps}>
      <View style={styles.content}>
        {/* 앱 정보 */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.title}>🌌 Exovisions</Title>
            <Paragraph style={styles.subtitle}>Version 1.0.0</Paragraph>
            <Paragraph style={styles.description}>
              NASA Space Apps Challenge 2024{'\n'}
              외계행성 탐지 머신러닝 시스템
            </Paragraph>
          </Card.Content>
        </Card>

        {/* 기술 스택 */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Technology Stack</Title>
            <List.Section>
              <List.Item
                title="Frontend"
                description="React Native (Expo) + React Native Paper"
                left={(props) => <List.Icon {...props} icon="cellphone" />}
              />
              <List.Item
                title="Backend"
                description="FastAPI + Python"
                left={(props) => <List.Icon {...props} icon="server" />}
              />
              <List.Item
                title="Machine Learning"
                description="Stacking Ensemble (LightGBM, GradientBoosting, RandomForest)"
                left={(props) => <List.Icon {...props} icon="brain" />}
              />
              <List.Item
                title="Database"
                description="MySQL"
                left={(props) => <List.Icon {...props} icon="database" />}
              />
            </List.Section>
          </Card.Content>
        </Card>

        {/* 데이터셋 정보 */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Training Datasets</Title>
            <List.Section>
              <List.Item
                title="Kepler Mission"
                description="9,618 samples"
                left={(props) => <List.Icon {...props} icon="telescope" />}
              />
              <List.Item
                title="K2 Mission"
                description="4,104 samples"
                left={(props) => <List.Icon {...props} icon="telescope" />}
              />
              <List.Item
                title="TESS Mission"
                description="7,773 samples"
                left={(props) => <List.Icon {...props} icon="telescope" />}
              />
              <List.Item
                title="Total"
                description="21,495 samples"
                left={(props) => <List.Icon {...props} icon="database-check" />}
              />
            </List.Section>
          </Card.Content>
        </Card>

        {/* 모델 정보 */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Model Information</Title>
            <Paragraph style={styles.paragraph}>
              <Paragraph style={styles.bold}>Type: </Paragraph>
              3-Class Classification
            </Paragraph>
            <Paragraph style={styles.paragraph}>
              <Paragraph style={styles.bold}>Classes: </Paragraph>
              CONFIRMED, CANDIDATE, FALSE_POSITIVE
            </Paragraph>
            <Paragraph style={styles.paragraph}>
              <Paragraph style={styles.bold}>Features: </Paragraph>
              10 parameters (orbital_period, transit_duration, transit_depth,
              planet_radius, equilibrium_temp, insolation, signal_to_noise,
              stellar_temp, stellar_logg, stellar_radius)
            </Paragraph>
            <Paragraph style={styles.paragraph}>
              <Paragraph style={styles.bold}>Architecture: </Paragraph>
              Stacking Ensemble with multiple base estimators
            </Paragraph>
          </Card.Content>
        </Card>

        {/* 링크 */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Resources</Title>
            <Button
              mode="outlined"
              icon="github"
              onPress={() =>
                openLink('https://github.com/nasa/space-apps-challenge')
              }
              style={styles.linkButton}
            >
              NASA Space Apps Challenge
            </Button>
            <Button
              mode="outlined"
              icon="web"
              onPress={() =>
                openLink('https://exoplanetarchive.ipac.caltech.edu/')
              }
              style={styles.linkButton}
            >
              NASA Exoplanet Archive
            </Button>
            <Button
              mode="outlined"
              icon="file-document"
              onPress={() => openLink('http://127.0.0.1:8000/docs')}
              style={styles.linkButton}
            >
              API Documentation
            </Button>
          </Card.Content>
        </Card>

        {/* 저작권 */}
        <View style={styles.footer}>
          <Paragraph style={styles.footerText}>
            © 2024 Exovisions Team
          </Paragraph>
          <Paragraph style={styles.footerText}>
            NASA Space Apps Challenge
          </Paragraph>
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
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  description: {
    fontSize: 16,
    lineHeight: 24,
  },
  cardTitle: {
    fontSize: 20,
    marginBottom: 12,
  },
  paragraph: {
    fontSize: 14,
    marginBottom: 8,
    lineHeight: 20,
  },
  bold: {
    fontWeight: 'bold',
  },
  linkButton: {
    marginBottom: 8,
  },
  footer: {
    alignItems: 'center',
    marginTop: 16,
    marginBottom: 32,
  },
  footerText: {
    fontSize: 12,
    color: '#999',
  },
});

export default AboutScreen;
