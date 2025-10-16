/**
 * Orbit Visualization Component
 * 별을 중심으로 행성이 궤도를 도는 시각화
 */

import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Platform } from 'react-native';

const OrbitVisualization = ({ orbitalPeriod = 10, planetRadius = 1 }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);

  useEffect(() => {
    if (Platform.OS !== 'web') return; // Web only

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;

    // 궤도 반지름 (orbital period에 비례)
    const orbitRadius = Math.min(width, height) * 0.35;

    // 별 크기
    const starRadius = 20;

    // 행성 크기 (planet radius에 비례)
    const planetSize = Math.max(5, Math.min(15, planetRadius * 3));

    let angle = 0;
    const speed = (2 * Math.PI) / (orbitalPeriod * 60); // 회전 속도

    const draw = () => {
      // 배경 지우기
      ctx.clearRect(0, 0, width, height);

      // 궤도 그리기
      ctx.strokeStyle = '#444';
      ctx.lineWidth = 1;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.arc(centerX, centerY, orbitRadius, 0, 2 * Math.PI);
      ctx.stroke();
      ctx.setLineDash([]);

      // 별 그리기 (중심)
      const starGradient = ctx.createRadialGradient(
        centerX, centerY, 0,
        centerX, centerY, starRadius
      );
      starGradient.addColorStop(0, '#FFF9C4');
      starGradient.addColorStop(0.5, '#FFC107');
      starGradient.addColorStop(1, '#FF6F00');

      ctx.fillStyle = starGradient;
      ctx.beginPath();
      ctx.arc(centerX, centerY, starRadius, 0, 2 * Math.PI);
      ctx.fill();

      // 별 빛 효과
      ctx.fillStyle = 'rgba(255, 193, 7, 0.2)';
      ctx.beginPath();
      ctx.arc(centerX, centerY, starRadius + 10, 0, 2 * Math.PI);
      ctx.fill();

      // 행성 위치 계산
      const planetX = centerX + orbitRadius * Math.cos(angle);
      const planetY = centerY + orbitRadius * Math.sin(angle);

      // 행성 그리기
      const planetGradient = ctx.createRadialGradient(
        planetX, planetY, 0,
        planetX, planetY, planetSize
      );
      planetGradient.addColorStop(0, '#4CAF50');
      planetGradient.addColorStop(0.7, '#2E7D32');
      planetGradient.addColorStop(1, '#1B5E20');

      ctx.fillStyle = planetGradient;
      ctx.beginPath();
      ctx.arc(planetX, planetY, planetSize, 0, 2 * Math.PI);
      ctx.fill();

      // 행성 외곽선
      ctx.strokeStyle = '#81C784';
      ctx.lineWidth = 1;
      ctx.stroke();

      // 각도 업데이트
      angle += speed;
      if (angle > 2 * Math.PI) angle -= 2 * Math.PI;

      // 다음 프레임
      animationRef.current = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [orbitalPeriod, planetRadius]);

  if (Platform.OS !== 'web') {
    return null; // Web only component
  }

  return (
    <View style={styles.container}>
      <canvas
        ref={canvasRef}
        width={250}
        height={250}
        style={styles.canvas}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#000',
    borderRadius: 8,
    padding: 8,
  },
  canvas: {
    maxWidth: '100%',
  },
});

export default OrbitVisualization;
