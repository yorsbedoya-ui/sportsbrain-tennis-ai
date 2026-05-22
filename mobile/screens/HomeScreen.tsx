import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import PredictionCard from '../components/PredictionCard';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>Upcoming ATP/WTA Matches</Text>
      <FlatList 
        data={[]} 
        renderItem={({item}) => <PredictionCard match={item} />}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000', padding: 16 },
  header: { color: '#fff', fontSize: 24, fontWeight: 'bold' }
});
