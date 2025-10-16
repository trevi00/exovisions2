/**
 * History Screen
 * 예측 기록 화면
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  FlatList,
  RefreshControl,
  Alert,
  Platform,
} from 'react-native';
import {
  Title,
  Paragraph,
  Card,
  Button,
  Chip,
  IconButton,
  ActivityIndicator,
  Checkbox,
  Divider,
} from 'react-native-paper';
import ApiService from '../services/api';
import { CLASSIFICATION_COLORS } from '../constants/features';

const HistoryScreen = ({ navigation }) => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter] = useState(null); // null, true, false

  // 페이지네이션
  const [page, setPage] = useState(0);
  const [pageSize] = useState(20);
  const [hasMore, setHasMore] = useState(true);

  // 선택 삭제
  const [selectedIds, setSelectedIds] = useState([]);
  const [selectionMode, setSelectionMode] = useState(false);

  useEffect(() => {
    setPage(0);
    loadPredictions(0);
    setSelectedIds([]);
  }, [filter]);

  const loadPredictions = async (currentPage = page) => {
    setLoading(true);
    try {
      const skip = currentPage * pageSize;
      const result = await ApiService.getPredictions(skip, pageSize, filter);
      if (result.success) {
        setPredictions(result.data.predictions);
        // 페이지네이션: 반환된 항목이 pageSize보다 적으면 더 이상 없음
        setHasMore(result.data.predictions.length === pageSize);
      } else {
        Alert.alert('Error', result.error);
      }
    } catch (error) {
      Alert.alert('Error', error.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    setRefreshing(true);
    setPage(0);
    loadPredictions(0);
    setSelectedIds([]);
  };

  // 페이지네이션 핸들러
  const handleNextPage = () => {
    if (hasMore) {
      const nextPage = page + 1;
      setPage(nextPage);
      loadPredictions(nextPage);
      setSelectedIds([]);
    }
  };

  const handlePrevPage = () => {
    if (page > 0) {
      const prevPage = page - 1;
      setPage(prevPage);
      loadPredictions(prevPage);
      setSelectedIds([]);
    }
  };

  // 선택 핸들러
  const toggleSelection = (id) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter((selectedId) => selectedId !== id));
    } else {
      setSelectedIds([...selectedIds, id]);
    }
  };

  const toggleSelectAll = () => {
    if (selectedIds.length === predictions.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(predictions.map((p) => p.id));
    }
  };

  const handleDeleteSelected = async () => {
    if (selectedIds.length === 0) {
      if (Platform.OS === 'web') {
        alert('Please select predictions to delete.');
      } else {
        Alert.alert('No Selection', 'Please select predictions to delete.');
      }
      return;
    }

    const confirmed = Platform.OS === 'web'
      ? window.confirm(`Are you sure you want to delete ${selectedIds.length} prediction(s)?`)
      : await new Promise((resolve) => {
          Alert.alert(
            'Delete Selected',
            `Are you sure you want to delete ${selectedIds.length} prediction(s)?`,
            [
              { text: 'Cancel', style: 'cancel', onPress: () => resolve(false) },
              { text: 'Delete', style: 'destructive', onPress: () => resolve(true) },
            ]
          );
        });

    if (confirmed) {
      try {
        // 각 항목을 개별적으로 삭제
        await Promise.all(
          selectedIds.map((id) => ApiService.deletePrediction(id))
        );
        setSelectedIds([]);
        loadPredictions();
        if (Platform.OS === 'web') {
          alert(`${selectedIds.length} prediction(s) deleted successfully.`);
        } else {
          Alert.alert('Success', `${selectedIds.length} prediction(s) deleted.`);
        }
      } catch (error) {
        if (Platform.OS === 'web') {
          alert(`Error: ${error.message}`);
        } else {
          Alert.alert('Error', error.message);
        }
      }
    }
  };

  const handleDelete = async (predictionId) => {
    const confirmed = Platform.OS === 'web'
      ? window.confirm('Are you sure you want to delete this prediction?')
      : await new Promise((resolve) => {
          Alert.alert(
            'Delete Prediction',
            'Are you sure you want to delete this prediction?',
            [
              { text: 'Cancel', style: 'cancel', onPress: () => resolve(false) },
              { text: 'Delete', style: 'destructive', onPress: () => resolve(true) },
            ]
          );
        });

    if (confirmed) {
      const result = await ApiService.deletePrediction(predictionId);
      if (result.success) {
        loadPredictions();
      } else {
        if (Platform.OS === 'web') {
          alert(`Error: ${result.error}`);
        } else {
          Alert.alert('Error', result.error);
        }
      }
    }
  };

  const handleDeleteAll = async () => {
    const filterMsg = filter === true
      ? 'exoplanet predictions'
      : filter === false
      ? 'non-exoplanet predictions'
      : 'all predictions';

    const confirmed = Platform.OS === 'web'
      ? window.confirm(`Are you sure you want to delete ${filterMsg}?`)
      : await new Promise((resolve) => {
          Alert.alert(
            'Delete All',
            `Are you sure you want to delete ${filterMsg}?`,
            [
              { text: 'Cancel', style: 'cancel', onPress: () => resolve(false) },
              { text: 'Delete All', style: 'destructive', onPress: () => resolve(true) },
            ]
          );
        });

    if (confirmed) {
      const result = await ApiService.deleteAllPredictions(filter);
      if (result.success) {
        if (Platform.OS === 'web') {
          alert(result.data.message);
        } else {
          Alert.alert('Success', result.data.message);
        }
        loadPredictions();
      } else {
        if (Platform.OS === 'web') {
          alert(`Error: ${result.error}`);
        } else {
          Alert.alert('Error', result.error);
        }
      }
    }
  };

  // 상세보기 핸들러
  const handleViewDetail = (item) => {
    // 선택 모드에서는 상세보기를 열지 않음
    if (selectionMode) return;

    // input_features가 있는지 확인
    if (!item.input_features) {
      if (Platform.OS === 'web') {
        alert('No feature data available for this prediction.');
      } else {
        Alert.alert('No Data', 'No feature data available for this prediction.');
      }
      return;
    }

    // PredictionResult 화면으로 이동
    navigation.navigate('PredictionResult', {
      prediction: item,
      features: item.input_features,
    });
  };

  const renderItem = ({ item }) => {
    const classificationColor =
      CLASSIFICATION_COLORS[item.classification] || '#757575';
    const isSelected = selectedIds.includes(item.id);

    return (
      <Card
        style={[styles.card, isSelected && styles.selectedCard]}
        onPress={() => handleViewDetail(item)}
      >
        <Card.Content>
          <View style={styles.cardHeader}>
            <View style={styles.headerLeft}>
              {/* 선택 모드일 때 체크박스 표시 */}
              {selectionMode && (
                <Checkbox
                  status={isSelected ? 'checked' : 'unchecked'}
                  onPress={() => toggleSelection(item.id)}
                  color="#6200ee"
                />
              )}
              <Title style={styles.cardIcon}>
                {item.is_exoplanet ? '✅' : '❌'}
              </Title>
              <View>
                <Title style={styles.cardTitle}>
                  {item.is_exoplanet ? 'Exoplanet' : 'Not Exoplanet'}
                </Title>
                <Paragraph style={styles.cardDate}>
                  {new Date(item.created_at).toLocaleString()}
                </Paragraph>
              </View>
            </View>
            <IconButton
              icon="delete"
              size={24}
              onPress={() => handleDelete(item.id)}
              style={styles.deleteButton}
            />
          </View>

          <View style={styles.cardBody}>
            <Chip
              style={[
                styles.classificationChip,
                { backgroundColor: classificationColor },
              ]}
              textStyle={styles.chipText}
            >
              {item.classification}
            </Chip>

            <View style={styles.probabilityContainer}>
              <View style={styles.probabilityRow}>
                <Paragraph style={styles.probabilityLabel}>
                  Confidence:
                </Paragraph>
                <Paragraph style={styles.probabilityValue}>
                  {(item.confidence_score * 100).toFixed(1)}%
                </Paragraph>
              </View>
              <View style={styles.probabilityRow}>
                <Paragraph style={styles.probabilityLabel}>
                  Planet Prob:
                </Paragraph>
                <Paragraph style={styles.probabilityValue}>
                  {(item.planet_probability * 100).toFixed(1)}%
                </Paragraph>
              </View>
            </View>
          </View>
        </Card.Content>
      </Card>
    );
  };

  const renderEmpty = () => (
    <View style={styles.emptyContainer}>
      <Paragraph style={styles.emptyText}>No predictions yet</Paragraph>
      <Button
        mode="contained"
        onPress={() => navigation.navigate('PredictionForm')}
        style={styles.emptyButton}
        icon="rocket-launch"
      >
        Make First Prediction
      </Button>
    </View>
  );

  if (loading && !refreshing) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* 필터 */}
      <View style={styles.filterContainer}>
        <View style={styles.filterChips}>
          <Chip
            selected={filter === null}
            onPress={() => setFilter(null)}
            style={styles.filterChip}
          >
            All
          </Chip>
          <Chip
            selected={filter === true}
            onPress={() => setFilter(true)}
            style={styles.filterChip}
          >
            Exoplanets
          </Chip>
          <Chip
            selected={filter === false}
            onPress={() => setFilter(false)}
            style={styles.filterChip}
          >
            Non-Exoplanets
          </Chip>
        </View>

        {/* 선택 모드 토글 */}
        <IconButton
          icon={selectionMode ? 'close' : 'checkbox-multiple-marked'}
          size={24}
          onPress={() => {
            setSelectionMode(!selectionMode);
            setSelectedIds([]);
          }}
          style={styles.selectionToggle}
        />
      </View>

      {/* 선택 모드 액션 바 */}
      {selectionMode && (
        <View style={styles.selectionBar}>
          <Button
            mode="text"
            onPress={toggleSelectAll}
            icon={selectedIds.length === predictions.length ? 'checkbox-marked' : 'checkbox-blank-outline'}
          >
            {selectedIds.length === predictions.length ? 'Deselect All' : 'Select All'}
          </Button>
          <Paragraph style={styles.selectionCount}>
            {selectedIds.length} selected
          </Paragraph>
          <Button
            mode="text"
            onPress={handleDeleteSelected}
            disabled={selectedIds.length === 0}
            icon="delete"
            textColor="#F44336"
          >
            Delete
          </Button>
        </View>
      )}

      <Divider />

      {/* 목록 */}
      <FlatList
        data={predictions}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        style={styles.list}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
        }
        ListEmptyComponent={renderEmpty}
      />

      {/* 페이지네이션 + 전체 삭제 */}
      {predictions.length > 0 && (
        <View style={styles.bottomActions}>
          {/* 페이지네이션 */}
          <View style={styles.paginationContainer}>
            <Button
              mode="outlined"
              onPress={handlePrevPage}
              disabled={page === 0}
              icon="chevron-left"
              style={styles.pageButton}
            >
              Prev
            </Button>
            <Paragraph style={styles.pageInfo}>
              Page {page + 1}
            </Paragraph>
            <Button
              mode="outlined"
              onPress={handleNextPage}
              disabled={!hasMore}
              icon="chevron-right"
              contentStyle={styles.nextButtonContent}
              style={styles.pageButton}
            >
              Next
            </Button>
          </View>

          {/* 전체 삭제 버튼 */}
          <Button
            mode="outlined"
            onPress={handleDeleteAll}
            style={styles.deleteAllButton}
            icon="delete-sweep"
          >
            Delete {filter === null ? 'All' : filter ? 'Exoplanets' : 'Non-Exoplanets'}
          </Button>
        </View>
      )}
    </View>
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  filterContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
    elevation: 2,
  },
  filterChips: {
    flexDirection: 'row',
    flex: 1,
  },
  filterChip: {
    marginRight: 8,
  },
  selectionToggle: {
    margin: 0,
  },
  selectionBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#E3F2FD',
  },
  selectionCount: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#1976D2',
  },
  list: {
    flex: 1,
  },
  listContent: {
    padding: 16,
    flexGrow: 1,
    paddingBottom: 32,
  },
  card: {
    marginBottom: 12,
    elevation: 2,
    ...(Platform.OS === 'web' && {
      cursor: 'pointer',
      transition: 'transform 0.2s, box-shadow 0.2s',
    }),
  },
  selectedCard: {
    borderWidth: 2,
    borderColor: '#6200ee',
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  cardIcon: {
    fontSize: 32,
    marginRight: 12,
  },
  cardTitle: {
    fontSize: 18,
    marginBottom: 4,
  },
  cardDate: {
    fontSize: 12,
    color: '#666',
  },
  deleteButton: {
    margin: 0,
  },
  cardBody: {
    marginTop: 8,
  },
  classificationChip: {
    alignSelf: 'flex-start',
    marginBottom: 12,
  },
  chipText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  probabilityContainer: {
    marginTop: 8,
  },
  probabilityRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 4,
  },
  probabilityLabel: {
    fontSize: 14,
  },
  probabilityValue: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  emptyContainer: {
    alignItems: 'center',
    marginTop: 48,
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
    marginBottom: 16,
  },
  emptyButton: {
    marginTop: 8,
  },
  bottomActions: {
    padding: 16,
  },
  paginationContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  pageButton: {
    marginHorizontal: 8,
  },
  nextButtonContent: {
    flexDirection: 'row-reverse',
  },
  pageInfo: {
    fontSize: 16,
    fontWeight: 'bold',
    marginHorizontal: 16,
  },
  deleteAllButton: {
    marginTop: 8,
  },
});

export default HistoryScreen;
