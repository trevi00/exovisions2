/**
 * Transit Light Curve Component
 * 행성 통과 시 광도 변화 곡선
 */

import React from 'react';
import { View, StyleSheet, Platform } from 'react-native';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';

const TransitLightCurve = ({ transitDepth = 500, transitDuration = 2.5 }) => {
  if (Platform.OS !== 'web') return null;

  // Transit light curve 데이터 생성
  const generateLightCurve = () => {
    const points = [];
    const totalPoints = 100;
    const transitStart = 35;
    const transitEnd = 35 + (transitDuration / 24) * 30; // 24시간 = 30 포인트

    for (let i = 0; i < totalPoints; i++) {
      let flux = 1.0; // 정상 밝기 (normalized)

      if (i >= transitStart && i <= transitEnd) {
        // Transit 중 (밝기 감소)
        const progress = (i - transitStart) / (transitEnd - transitStart);
        const depth = transitDepth / 1000000; // ppm to fraction

        // 부드러운 곡선 (ingress, full transit, egress)
        if (progress < 0.2) {
          // Ingress
          flux = 1.0 - depth * (progress / 0.2);
        } else if (progress > 0.8) {
          // Egress
          flux = 1.0 - depth * ((1 - progress) / 0.2);
        } else {
          // Full transit
          flux = 1.0 - depth;
        }
      }

      points.push({ time: i, flux });
    }

    return points;
  };

  const data = generateLightCurve();

  return (
    <View style={styles.container}>
      <ResponsiveContainer width="100%" height={350}>
        <AreaChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
        >
          <defs>
            <linearGradient id="fluxGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#2196F3" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#2196F3" stopOpacity={0.05} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis
            dataKey="time"
            label={{ value: 'Time (arbitrary units)', position: 'insideBottom', offset: -10 }}
            stroke="#666"
          />
          <YAxis
            domain={[0.98, 1.01]}
            label={{ value: 'Normalized Flux', angle: -90, position: 'insideLeft' }}
            stroke="#666"
            tickFormatter={(value) => value.toFixed(3)}
          />
          <Tooltip
            formatter={(value) => [`Flux: ${value.toFixed(6)}`]}
            labelFormatter={(label) => `Time: ${label}`}
          />
          <Area
            type="monotone"
            dataKey="flux"
            stroke="#2196F3"
            strokeWidth={2}
            fill="url(#fluxGradient)"
          />
        </AreaChart>
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
});

export default TransitLightCurve;
