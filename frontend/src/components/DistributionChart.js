/**
 * Distribution Chart Component
 * 행성 반지름 및 통과 지속시간 분포 히스토그램
 */

import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Platform, ActivityIndicator, Dimensions } from 'react-native';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import ApiService from '../services/api';

const DistributionChart = ({ type, currentValue }) => {
  const [distributionData, setDistributionData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDistributions = async () => {
      setLoading(true);
      const result = await ApiService.getDistributions();
      if (result.success) {
        setDistributionData(result.data);
      }
      setLoading(false);
    };

    if (Platform.OS === 'web') {
      fetchDistributions();
    }
  }, []);

  if (Platform.OS !== 'web') return null;

  if (loading) {
    return (
      <View style={[styles.container, styles.loadingContainer]}>
        <ActivityIndicator size="large" color="#4CAF50" />
      </View>
    );
  }

  const generateDistributionData = () => {
    if (!distributionData) {
      // Fallback to sample data
      if (type === 'radius') {
        const bins = ['0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16', '16-18', '18-20'];
        const counts = [120, 95, 70, 45, 30, 20, 15, 10, 7, 3];
        return { bins, counts, xlabel: 'Planet Radius (R⊕)', color: '#4CAF50' };
      } else {
        const bins = ['0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16', '16-18', '18-20', '20-24'];
        const counts = [85, 110, 95, 70, 55, 40, 30, 20, 15, 10, 5];
        return { bins, counts, xlabel: 'Transit Duration (hours)', color: '#2196F3' };
      }
    }

    if (type === 'radius') {
      return {
        bins: distributionData.planet_radius_distribution.bins,
        counts: distributionData.planet_radius_distribution.counts,
        xlabel: 'Planet Radius (R⊕)',
        color: '#4CAF50'
      };
    } else {
      return {
        bins: distributionData.transit_duration_distribution.bins,
        counts: distributionData.transit_duration_distribution.counts,
        xlabel: 'Transit Duration (hours)',
        color: '#2196F3'
      };
    }
  };

  const { bins, counts, xlabel, color } = generateDistributionData();

  // 현재 값이 속한 bin 찾기
  const getCurrentBinIndex = () => {
    if (!currentValue) return -1;

    const value = parseFloat(currentValue);
    for (let i = 0; i < bins.length; i++) {
      const [min, max] = bins[i].split('-').map(Number);
      if (value >= min && value < max) return i;
    }
    return -1;
  };

  const currentBinIndex = getCurrentBinIndex();

  // Recharts 형식으로 데이터 변환
  const data = bins.map((bin, index) => ({
    name: bin,
    count: counts[index],
    fill: index === currentBinIndex ? '#FF9800' : color,
  }));

  const chartTitle = type === 'radius'
    ? 'Planet Radius Distribution'
    : 'Transit Duration Distribution';

  return (
    <View style={styles.container}>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis
            dataKey="name"
            label={{ value: xlabel, position: 'insideBottom', offset: -5 }}
            stroke="#666"
          />
          <YAxis
            label={{ value: 'Count', angle: -90, position: 'insideLeft' }}
            stroke="#666"
          />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const isCurrentBin = payload[0].payload.fill === '#FF9800';
                return (
                  <div style={{
                    backgroundColor: '#fff',
                    padding: '10px',
                    border: '1px solid #ccc',
                    borderRadius: '4px'
                  }}>
                    <p style={{ margin: 0 }}>{`Count: ${payload[0].value}`}</p>
                    {isCurrentBin && (
                      <p style={{ margin: '5px 0 0 0', color: '#FF9800', fontWeight: 'bold' }}>
                        ← Your prediction is here
                      </p>
                    )}
                  </div>
                );
              }
              return null;
            }}
          />
          <Bar dataKey="count" />
        </BarChart>
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

export default DistributionChart;
