import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

app_tsx = """import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import AppNavigator from './navigation/AppNavigator';

export default function App() {
  return (
    <NavigationContainer>
      <AppNavigator />
    </NavigationContainer>
  );
}
"""

home_screen = """import React from 'react';
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
"""

write_file("mobile/App.tsx", app_tsx)
write_file("mobile/package.json", '{\\n  "name": "sportsbrain-mobile",\\n  "main": "node_modules/expo/AppEntry.js",\\n  "dependencies": {\\n    "expo": "~51.0.0",\\n    "react-native": "0.74.1",\\n    "@react-navigation/native": "^6.1.9"\\n  }\\n}')
write_file("mobile/screens/HomeScreen.tsx", home_screen)
write_file("mobile/screens/MatchDetailScreen.tsx", "// Match detail with gauge and factors\\n")
write_file("mobile/screens/AccuracyScreen.tsx", "// Accuracy stats and brier score\\n")
write_file("mobile/screens/AlertsScreen.tsx", "// High confidence alerts feed\\n")
write_file("mobile/components/PredictionCard.tsx", "export default function PredictionCard() { return null; }")
write_file("mobile/components/ConfidenceBadge.tsx", "export default function ConfidenceBadge() { return null; }")
write_file("mobile/navigation/AppNavigator.tsx", "export default function AppNavigator() { return null; }")
write_file("mobile/services/api.ts", "// Axios client\\n")

print("React Native Mobile files generated.")
