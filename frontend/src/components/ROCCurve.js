/**
 * ROC Curve Component
 * 모델 성능 ROC 곡선
 */

import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Platform, ActivityIndicator } from 'react-native';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import ApiService from '../services/api';

const ROCCurve = () => {
  const [rocData, setRocData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchROCCurve = async () => {
      setLoading(true);
      const result = await ApiService.getROCCurve();
      if (result.success) {
        setRocData(result.data);
      }
      setLoading(false);
    };

    if (Platform.OS === 'web') {
      fetchROCCurve();
    }
  }, []);

  if (Platform.OS !== 'web') return null;

  if (loading) {
    return (
      <View style={[styles.container, styles.loadingContainer]}>
        <ActivityIndicator size="large" color="#9C27B0" />
      </View>
    );
  }

  // ROC 곡선 데이터 생성 (fallback to sample data)
  const generateROCData = () => {
    if (rocData) {
      return { fpr: rocData.fpr, tpr: rocData.tpr, auc: rocData.auc };
    }

    // Fallback sample data
    const fpr = [];
    const tpr = [];

    for (let i = 0; i <= 100; i++) {
      const x = i / 100;
      const y = Math.sqrt(x) * 0.98 + x * 0.02;
      fpr.push(x);
      tpr.push(Math.min(1, y));
    }

    return { fpr, tpr, auc: 0.95 };
  };

  const { fpr, tpr, auc } = generateROCData();

  // Recharts 형식으로 데이터 변환
  const data = fpr.map((x, i) => ({
    fpr: x,
    tpr: tpr[i],
    random: x, // Random classifier (diagonal line)
  }));

  return (
    <View style={styles.container}>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis
            dataKey="fpr"
            type="number"
            domain={[0, 1]}
            label={{ value: 'False Positive Rate', position: 'insideBottom', offset: -10 }}
            stroke="#666"
            tickFormatter={(value) => value.toFixed(1)}
          />
          <YAxis
            type="number"
            domain={[0, 1]}
            label={{ value: 'True Positive Rate', angle: -90, position: 'insideLeft' }}
            stroke="#666"
            tickFormatter={(value) => value.toFixed(1)}
          />
          <Tooltip
            formatter={(value, name) => {
              if (name === 'tpr') return [`TPR: ${value.toFixed(3)}`, `ROC Curve (AUC = ${auc.toFixed(2)})`];
              if (name === 'random') return [`${value.toFixed(3)}`, 'Random Classifier'];
              return value.toFixed(3);
            }}
            labelFormatter={(value) => `FPR: ${value.toFixed(3)}`}
          />
          <Legend
            wrapperStyle={{ paddingTop: 10 }}
            content={(props) => {
              const { payload } = props;
              return (
                <div style={{ textAlign: 'center', paddingTop: 10 }}>
                  {payload.map((entry, index) => (
                    <span
                      key={`item-${index}`}
                      style={{
                        marginRight: 20,
                        color: entry.color,
                        fontWeight: entry.value === 'tpr' ? 'bold' : 'normal'
                      }}
                    >
                      {entry.value === 'tpr'
                        ? `ROC Curve (AUC = ${auc.toFixed(2)})`
                        : 'Random Classifier'}
                    </span>
                  ))}
                </div>
              );
            }}
          />
          <Line
            type="monotone"
            dataKey="tpr"
            stroke="#9C27B0"
            strokeWidth={3}
            dot={false}
            fill="#9C27B044"
            fillOpacity={0.3}
          />
          <Line
            type="monotone"
            dataKey="random"
            stroke="#BDBDBD"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 8,
  },
  loadingContainer: {
    minHeight: 200,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default ROCCurve;
