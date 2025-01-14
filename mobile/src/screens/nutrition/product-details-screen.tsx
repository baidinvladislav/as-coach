import React from 'react';
import {
  Image,
  ImageSourcePropType,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';

import { useNavigation } from '@navigation';

const ProductDetailsScreen: React.FC = ({ route }) => {
  const { product } = route.params;
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      <View style={styles.closeIconContainer}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Image
            source={
              require('../../assets/images/close.png') as ImageSourcePropType
            }
            style={styles.closeIcon}
          />
        </TouchableOpacity>
      </View>

      <Text style={styles.foodName}>{product.name}</Text>

      <TextInput
        style={styles.input}
        placeholder="Unit"
        placeholderTextColor="#666"
        value={`${product.amount} ${product.type}`}
      />
      <TextInput
        style={styles.input}
        placeholder="Weight / Volume"
        placeholderTextColor="#666"
        value={`${product.amount}`}
      />

      <Text style={styles.nutritionHeader}>Nutrition Facts</Text>

      <View style={styles.nutritionFacts}>
        <View style={styles.factRow}>
          <Text style={styles.factText}>🍽️ Calories:</Text>
          <Text style={styles.factValue}>{product.calories} cal</Text>
        </View>
        <View style={styles.factRow}>
          <Text style={styles.factText}>🥚 Proteins:</Text>
          <Text style={styles.factValue}>{product.proteins} g</Text>
        </View>
        <View style={styles.factRow}>
          <Text style={styles.factText}>🌰 Fats:</Text>
          <Text style={styles.factValue}>{product.fats} g</Text>
        </View>
        <View style={styles.factRow}>
          <Text style={styles.factText}>🌾 Carbs:</Text>
          <Text style={styles.factValue}>{product.carbs} g</Text>
        </View>
      </View>

      <Text style={styles.nutritionDisclaimer}>
        * Nutrition Facts may not be completely accurate as these values may
        have been filled in by another app user
      </Text>

      <TouchableOpacity
        onPress={() => {
          navigation.goBack();
        }}
        style={styles.saveButton}
      >
        <Text style={styles.saveButtonText}>Save</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  closeIconContainer: {
    marginVertical: 15,
  },
  closeIcon: {
    height: 40,
    width: 40,
  },
  foodName: {
    color: '#fff',
    marginTop: 20,
    fontSize: 24,
    marginBottom: 20,
    marginHorizontal: 10,
  },
  input: {
    backgroundColor: '#333',
    paddingHorizontal: 20,
    marginHorizontal: 10,
    color: '#fff',
    padding: 10,
    borderRadius: 10,
    marginBottom: 20,
  },
  nutritionHeader: {
    fontSize: 20,
    fontWeight: '500',
    color: '#fff',
    marginHorizontal: 10,
  },
  nutritionFacts: {
    marginVertical: 20,
    marginHorizontal: 10,
  },
  factRow: {
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderColor: '#222',
    justifyContent: 'space-between',
    flexDirection: 'row',
  },
  factText: {
    color: '#fff',
    fontSize: 16,
  },
  factValue: {
    color: '#B8FF5F',
    fontSize: 16,
  },
  nutritionDisclaimer: {
    fontSize: 12,
    color: 'grey',
    marginHorizontal: 10,
  },
  saveButton: {
    backgroundColor: '#B8FF5F',
    padding: 15,
    borderRadius: 10,
    marginTop: 20,
    marginHorizontal: 10,
    position: 'absolute',
    bottom: 5,
    width: '90%',
    alignSelf: 'center',
  },
  saveButtonText: {
    color: 'black',
    textAlign: 'center',
  },
});

export default ProductDetailsScreen;
