/**
 * Exovisions - Exoplanet Detection App
 * Main Application Entry Point
 */

import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider as PaperProvider } from 'react-native-paper';
import { StatusBar, Platform } from 'react-native';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import PredictionFormScreen from './src/screens/PredictionFormScreen';
import PredictionResultScreen from './src/screens/PredictionResultScreen';
import HistoryScreen from './src/screens/HistoryScreen';
import AboutScreen from './src/screens/AboutScreen';

const Stack = createStackNavigator();

// 테마 설정
const theme = {
  colors: {
    primary: '#6200ee',
    accent: '#03dac4',
    background: '#f5f5f5',
    surface: '#ffffff',
    error: '#b00020',
    text: '#000000',
    onSurface: '#000000',
    disabled: '#00000061',
    placeholder: '#00000099',
    backdrop: '#00000099',
    notification: '#f50057',
  },
};

export default function App() {
  // Fix scroll for React Native Web by overriding body overflow
  useEffect(() => {
    if (Platform.OS === 'web') {
      // Override React Native Web's body overflow: hidden
      document.body.style.overflow = 'auto';
      document.body.style.height = 'auto';

      // Also fix the root div
      const root = document.getElementById('root');
      if (root) {
        root.style.height = 'auto';
        root.style.overflow = 'visible';
      }
    }
  }, []);

  return (
    <PaperProvider theme={theme}>
      <StatusBar barStyle="dark-content" backgroundColor="#6200ee" />
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName="Home"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#6200ee',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          }}
        >
          <Stack.Screen
            name="Home"
            component={HomeScreen}
            options={{
              title: 'Exovisions',
              headerStyle: {
                backgroundColor: '#1a1a2e',
              },
            }}
          />
          <Stack.Screen
            name="PredictionForm"
            component={PredictionFormScreen}
            options={{
              title: 'New Prediction',
            }}
          />
          <Stack.Screen
            name="PredictionResult"
            component={PredictionResultScreen}
            options={{
              title: 'Prediction Result',
            }}
          />
          <Stack.Screen
            name="History"
            component={HistoryScreen}
            options={{
              title: 'Prediction History',
            }}
          />
          <Stack.Screen
            name="About"
            component={AboutScreen}
            options={{
              title: 'About',
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}
