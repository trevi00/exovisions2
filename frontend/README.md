# Exovisions Frontend

React Native (Expo) frontend for the Exoplanet Detection system.

## Features

- 🚀 **New Prediction**: Input 10 feature parameters to predict exoplanet
- 📊 **Prediction Results**: View classification results with confidence scores
- 📜 **History**: View and manage prediction history
- 🧪 **Test Samples**: Quick test with pre-defined sample data
- ℹ️ **About**: Learn about the model and datasets

## Tech Stack

- **Framework**: React Native (Expo)
- **UI Library**: React Native Paper
- **Navigation**: React Navigation
- **HTTP Client**: Axios
- **API**: FastAPI backend at http://127.0.0.1:8000

## Project Structure

```
frontend/
├── src/
│   ├── screens/              # Screen components
│   │   ├── HomeScreen.js
│   │   ├── PredictionFormScreen.js
│   │   ├── PredictionResultScreen.js
│   │   ├── HistoryScreen.js
│   │   └── AboutScreen.js
│   ├── services/             # API services
│   │   └── api.js
│   ├── constants/            # Constants and configurations
│   │   └── features.js
│   ├── components/           # Reusable components
│   └── types/                # TypeScript types (future)
├── App.js                    # Main app entry point
├── package.json
└── README.md
```

## Installation

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn
- Expo CLI (installed automatically)
- Backend API running on http://127.0.0.1:8000

### Install Dependencies
```bash
cd frontend
npm install
```

## Running the App

### Development Mode

#### Web
```bash
npm run web
```
Opens in your default browser at http://localhost:19006

#### Android
```bash
npm run android
```
Requires Android Studio and Android emulator or physical device with USB debugging enabled.

#### iOS (macOS only)
```bash
npm run ios
```
Requires Xcode and iOS simulator or physical device.

### Using Expo Go
1. Install Expo Go app on your mobile device
2. Run `npm start`
3. Scan the QR code with Expo Go (Android) or Camera app (iOS)

## API Configuration

The API base URL is configured in `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
```

**Important**:
- For Android emulator, use `http://10.0.2.2:8000/api/v1`
- For iOS simulator, use `http://127.0.0.1:8000/api/v1`
- For physical devices, use your computer's IP address (e.g., `http://192.168.1.100:8000/api/v1`)

## Features Usage

### 1. New Prediction
1. Navigate to "New Prediction"
2. Select a test sample or manually input 10 feature values:
   - Orbital Period (days)
   - Transit Duration (hours)
   - Transit Depth (ppm)
   - Planet Radius (Earth radii)
   - Equilibrium Temperature (K)
   - Insolation (Earth units)
   - Signal to Noise Ratio
   - Stellar Temperature (K)
   - Stellar Log(g)
   - Stellar Radius (Solar radii)
3. Tap "Predict Exoplanet"
4. View results

### 2. Prediction History
- View all past predictions
- Filter by exoplanet/non-exoplanet
- Delete individual predictions
- Delete all predictions (with filter)
- Pull to refresh

### 3. Test Samples
Pre-defined samples for quick testing:
- **Typical Exoplanet**: Expected CONFIRMED
- **Hot Jupiter**: Expected FALSE_POSITIVE
- **Earth Analog**: Expected FALSE_POSITIVE
- **Clear False Positive**: Expected FALSE_POSITIVE

## API Endpoints Used

- `GET /api/v1/health` - Health check
- `POST /api/v1/predictions/` - Create prediction
- `GET /api/v1/predictions/` - List predictions
- `GET /api/v1/predictions/{id}` - Get prediction
- `DELETE /api/v1/predictions/{id}` - Delete prediction
- `DELETE /api/v1/predictions/` - Delete all predictions

## Troubleshooting

### Cannot connect to API
1. Ensure backend is running on port 8000
2. Check API_BASE_URL in `src/services/api.js`
3. For physical devices, use your computer's IP address
4. For Android emulator, use `10.0.2.2` instead of `localhost`

### Navigation errors
```bash
npm install @react-navigation/native @react-navigation/stack
npm install react-native-screens react-native-safe-area-context
```

### Paper UI errors
```bash
npm install react-native-paper react-native-vector-icons
```

### Axios errors
```bash
npm install axios
```

## Building for Production

### Android APK
```bash
expo build:android
```

### iOS IPA
```bash
expo build:ios
```

## Model Information

- **Type**: 3-Class Classification
- **Classes**: CONFIRMED, CANDIDATE, FALSE_POSITIVE
- **Datasets**: Kepler (9,618), K2 (4,104), TESS (7,773) = 21,495 samples
- **Features**: 10 parameters
- **Algorithm**: Stacking Ensemble (LightGBM + GradientBoosting + RandomForest + LogisticRegression)

## License

NASA Space Apps Challenge 2024
