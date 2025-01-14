import React, { useEffect, useRef, useState } from 'react';
import {
  FlatList,
  Image,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';

import {
  getDietDetails,
  getProductDetails,
  getProductHistory,
  searchProduct,
  addProductToDiet,
} from '@api';
import { useNavigation } from '@navigation';
import { Loader } from '@ui';

import { NutritionProduct } from '~types';

const FoodSelectionScreen = ({ route }) => {
  const navigation = useNavigation();

  const { meal, diet_id } = route?.params;
  const [products, setProducts] = useState<NutritionProduct | []>([]);
  const [filteredProducts, setFilteredProducts] = useState<
    NutritionProduct[] | []
  >([]);
  const [selectedIndices, setSelectedIndices] = useState<
    NutritionProduct[] | []
  >([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [inputFocsed, setInputFocused] = useState(false);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    setProductList();
  }, []);
  const setProductList = async () => {
    setLoading(true);
    const product = await getProductHistory();
    const mealProducts = product;
    setProducts(mealProducts);
    setFilteredProducts(mealProducts);
    setLoading(false);
  };

  const handleSearch = async (text: string) => {
    setSearchQuery(text);
    if (text === '') {
      setFilteredProducts(products);
    } else {
      const filtered = products.filter(item =>
        item?.name?.toLowerCase().includes(text.toLowerCase()),
      );
      if (filtered.length <= 0) {
        setLoading(true);
        const liveProduct = await searchProduct(text);
        setFilteredProducts(liveProduct);
        setLoading(false);
      } else {
        setFilteredProducts(filtered);
      }
    }
  };

  const handleSelectItem = index => {
    if (selectedIndices.includes(index)) {
      setSelectedIndices(selectedIndices.filter(i => i !== index));
    } else {
      setSelectedIndices([...selectedIndices, index]);
    }
  };
  const inputRef = useRef(null);
  const handleClearSearch = () => {
    setSearchQuery('');
    setFilteredProducts(products);
    if (inputRef.current != null) {
      inputRef.current?.blur();
    }
  };
  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Loader />
      </View>
    );
  }
  const saveDiet = async () => {
    setLoading(true);
    try {
      const selectedProducts = products.filter((item, index) =>
        selectedIndices.includes(index),
      );
      const data = {
        daily_diet_id: diet_id,
        meal_type: meal ? meal?.toLowerCase() : '',
        product_data: [
          ...selectedProducts.map(item => ({
            barcode: item?.barcode ? item?.barcode?.toString() : '',
            amount: 100,
          })),
        ],
      };

      const response = await addProductToDiet(data);
      if (response) {
        navigation.goBack();
        // setLoading(false);
        return;
      }
      setLoading(false);
    } catch (err) {
      console.log(err);
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.searchWrapper}>
        <View style={styles.searchInput}>
          <Image
            source={require('../../assets/images/search.png')}
            style={styles.searchIcon}
          />
          <TextInput
            ref={inputRef}
            placeholder="Search"
            placeholderTextColor="#666"
            value={searchQuery}
            onChangeText={handleSearch}
            style={styles.textInput}
            onFocus={() => setInputFocused(true)}
            onBlur={() => setInputFocused(false)}
          />
          {searchQuery ? (
            <TouchableOpacity
              onPress={() => {
                setSearchQuery(''), setFilteredProducts(products);
              }}
            >
              <Text style={{ color: '#fff', marginRight: '5%' }}>X</Text>
            </TouchableOpacity>
          ) : !inputFocsed ? (
            <Image
              source={require('../../assets/images/Icon.png')}
              style={styles.icon}
            />
          ) : null}
        </View>
        {inputFocsed && searchQuery == '' ? (
          <TouchableOpacity onPress={handleClearSearch}>
            <Text style={styles.cancelText}>Cancel</Text>
          </TouchableOpacity>
        ) : null}
      </View>

      {filteredProducts.length > 0 ? (
        <FlatList
          data={filteredProducts}
          keyExtractor={item => item.id}
          contentContainerStyle={{ paddingBottom: 65 }}
          renderItem={({ item, index }) => (
            <View>
              <View style={styles.foodItem}>
                <View>
                  <Text style={styles.foodText}>{item?.name}</Text>
                  <View style={styles.foodDetails}>
                    <Text style={[styles.foodText, styles.weightText]}>
                      {item?.weight}
                    </Text>
                    <Text style={[styles.foodText, styles.caloriesText]}>
                      {item?.calories}
                    </Text>
                  </View>
                  <View style={styles.nutritionContainer}>
                    <Text style={styles.nutritionText}>
                      🥚 {item?.proteins}
                    </Text>
                    <Text style={styles.nutritionText}>🌰 {item?.fats}</Text>
                    <Text style={styles.nutritionText}>🌾 {item?.carbs}</Text>
                  </View>
                </View>
                <TouchableOpacity
                  onPress={() => handleSelectItem(index)}
                  style={[
                    styles.checkbox,
                    {
                      borderWidth: selectedIndices.includes(index) ? 0 : 1,
                      backgroundColor: selectedIndices.includes(index)
                        ? '#B8FF5F'
                        : 'transparent',
                    },
                  ]}
                >
                  {selectedIndices.includes(index) && (
                    <Image
                      source={require('../../assets/images/Checkbox.png')}
                      style={styles.checkboxIcon}
                    />
                  )}
                </TouchableOpacity>
              </View>
              {index == filteredProducts.length - 1 &&
              searchQuery &&
              filteredProducts.length > 0 ? (
                <View
                  style={{
                    paddingVertical: 5,
                    alignItems: 'center',
                    width: '100%',
                    // borderWidth: 2,
                    // borderColor: 'red',
                  }}
                >
                  <Text style={{ color: '#fff', zIndex: 1 }}>
                    Didn't find the product?
                    <Text style={{ color: '#B8FF5F' }}> Add More</Text>
                  </Text>
                </View>
              ) : null}
            </View>
          )}
        />
      ) : (
        searchQuery != '' && (
          <View
            style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}
          >
            <View style={{ marginTop: '-35%', alignItems: 'center' }}>
              <Text style={{ color: '#fff', fontWeight: '400', fontSize: 18 }}>
                No such product found
              </Text>
              <Text
                style={{
                  color: '#fff',
                  fontWeight: '300',
                  fontSize: 12,
                  marginTop: '5%',
                }}
              >
                But you can add it yourself
              </Text>
              <Text style={{ color: '#B8FF5F', fontSize: 25, marginTop: '5%' }}>
                {'+ '}
                <Text
                  style={{
                    fontWeight: '700',
                    fontSize: 18,
                  }}
                >
                  "{`${searchQuery}`}"
                </Text>
              </Text>
            </View>
          </View>
        )
      )}

      <View style={styles.buttonContainer}>
        <TouchableOpacity
          onPress={() => navigation.goBack()}
          style={styles.cancelButton}
        >
          <Text style={styles.buttonText}>Cancel</Text>
        </TouchableOpacity>
        <TouchableOpacity
          disabled={selectedIndices.length === 0}
          onPress={() => {
            saveDiet();
          }}
          style={[styles.saveButton]}
        >
          <Text style={styles.buttonText}>Save ({selectedIndices.length})</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  searchWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 10,
    marginTop: 10,
  },
  searchInput: {
    backgroundColor: '#333',
    flex: 1,
    color: '#fff',
    paddingHorizontal: 10,
    borderRadius: 10,
    height: 50,
    flexDirection: 'row',
    alignItems: 'center',
  },
  searchIcon: {
    height: 25,
    width: 25,
  },
  textInput: {
    flex: 1,
    color: '#fff',
    marginLeft: 10,
  },
  clearIcon: {
    height: 20,
    width: 20,
  },
  icon: {
    height: 25,
    width: 25,
  },
  cancelText: {
    color: '#B8FF5F',
    marginLeft: 10,
  },
  foodItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderColor: '#222',
    padding: 15,
    marginVertical: 5,
    borderRadius: 10,
  },
  foodText: {
    color: '#fff',
  },
  weightText: {
    color: '#B8FF5F',
  },
  caloriesText: {
    marginLeft: 10,
    color: 'rgba(255, 255, 255, 0.5)',
  },
  foodDetails: {
    flexDirection: 'row',
    marginTop: 10,
  },
  nutritionContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  nutritionText: {
    color: 'rgba(255, 255, 255, 0.5)',
    marginLeft: 10,
  },
  checkbox: {
    width: 20,
    height: 20,
    borderColor: '#fff',
    borderRadius: 3,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxIcon: {
    width: 15,
    height: 15,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 20,
    backgroundColor: '#222',
    width: '100%',
    paddingVertical: 10,
    position: 'absolute',
    bottom: 0,
    alignSelf: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  cancelButton: {
    backgroundColor: '#555',
    padding: 15,
    borderRadius: 10,
    flex: 1,
    marginRight: 10,
  },
  saveButton: {
    backgroundColor: '#B8FF5F',
    padding: 15,
    borderRadius: 10,
    flex: 1,
    marginLeft: 10,
  },
  buttonText: {
    color: '#192026',
    textAlign: 'center',
  },
});

export default FoodSelectionScreen;
