import React, { useEffect, useState } from 'react';
import {
  Image,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { getDietDetails } from '@api';
import { Screens, useNavigation } from '@navigation';
import { useIsFocused } from '@react-navigation/native';
import { Loader } from '@ui';

import { NutritionData } from '~types';

const MainScreen: React.FC = () => {
  const [exListIndex, setExListIndex] = useState<number | null>(null);
  const [data, setData] = useState<NutritionData | null>(null);
  const [loading, setLoading] = useState(false);
  const focused = useIsFocused();
  const { top } = useSafeAreaInsets();
  useEffect(() => {
    setDataApi();
  }, [focused]);
  const getFormattedDate = () => {
    const today = new Date();
    return today.toLocaleDateString('en-CA');
  };

  const setDataApi = async () => {
    try {
      setLoading(true);
      const fromateDate = getFormattedDate();
      const fetchedData = await getDietDetails('2024-09-23');
      setData(fetchedData);
      console.log(
        'Products: ',
        fetchedData?.actual_nutrition?.['breakfast']?.products,
      );
    } catch (error) {
      console.error('Error fetching data:', error);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const fractionToPercentage = (numerator: number, denominator: number) => {
    if (!denominator || denominator === 0) return 0; // Avoid division by zero
    return (numerator / denominator) * 100;
  };

  const handlePressMeal = (index: number) => {
    setExListIndex(index === exListIndex ? null : index); // Toggle index for showing details
  };

  const navigation = useNavigation();

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Loader />
      </View>
    );
  }

  if (!data) {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text style={{ color: '#FF0000' }}>
          Failed to load data. Please try again later.
        </Text>
      </View>
    );
  }

  const meals = Object.keys(data.actual_nutrition || {}).filter(
    item => item !== 'daily_total' && item !== 'date',
  ) || ['breakfast', 'lunch', 'dinner', 'snacks'];

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        {/*remove calendar */}
        <TouchableOpacity>
          <Image
            source={require('../../assets/images/calendar.png')}
            style={{ height: 30, width: 30 }}
          />
        </TouchableOpacity>

        {/*remove date */}
        <Text style={styles.headerText}>
          {data?.actual_nutrition?.date || 'No date available'}
        </Text>

        {/*remove profile pic */}
        <View style={styles.profilePic} />
      </View>

      <View style={styles.statsContainer}>
        <View style={styles.statsRow}>
          <View style={{ width: '25%', alignItems: 'center' }}>
            <Text style={styles.statsText}>🥩 Proteins</Text>
          </View>
          <View style={{ width: '25%', alignItems: 'center' }}>
            <Text style={styles.statsText}>🌰 Fats</Text>
          </View>
          <View style={{ width: '25%', alignItems: 'center' }}>
            <Text style={styles.statsText}>🌾 Carbs</Text>
          </View>
        </View>

        <View style={styles.progressRow}>
          <View style={styles.progressBar}>
            <View
              style={{
                height: '100%',
                width: `${fractionToPercentage(
                  data?.actual_nutrition?.daily_total?.consumed_proteins || 0,
                  data?.actual_nutrition?.daily_total?.total_proteins || 1,
                )}%`,
                backgroundColor: '#7856FF',
                borderRadius: 20,
              }}
            />
          </View>
          <View style={styles.progressBar}>
            <View
              style={{
                height: '100%',
                width: `${fractionToPercentage(
                  data?.actual_nutrition?.daily_total?.consumed_fats || 0,
                  data?.actual_nutrition?.daily_total?.total_fats || 1,
                )}%`,
                backgroundColor: '#7856FF',
                borderRadius: 20,
              }}
            />
          </View>
          <View style={styles.progressBar}>
            <View
              style={{
                height: '100%',
                width: `${fractionToPercentage(
                  data?.actual_nutrition?.daily_total?.consumed_carbs || 0,
                  data?.actual_nutrition?.daily_total?.total_carbs || 1,
                )}%`,
                backgroundColor: '#7856FF',
                borderRadius: 20,
              }}
            />
          </View>
        </View>

        <View style={styles.statsValuesRow}>
          <View style={styles.statsValueContainer}>
            <Text style={styles.statsValue}>
              {data?.actual_nutrition?.daily_total?.consumed_proteins || 0}
            </Text>
            <Text style={styles.statsTotalValue}>
              / {data?.actual_nutrition?.daily_total?.total_proteins || 0} g
            </Text>
          </View>
          <View style={styles.statsValueContainer}>
            <Text style={styles.statsValue}>
              {data?.actual_nutrition?.daily_total?.consumed_fats || 0}
            </Text>
            <Text style={styles.statsTotalValue}>
              / {data?.actual_nutrition?.daily_total?.total_fats || 0} g
            </Text>
          </View>
          <View style={styles.statsValueContainer}>
            <Text style={styles.statsValue}>
              {data?.actual_nutrition?.daily_total?.consumed_carbs || 0}
            </Text>
            <Text style={styles.statsTotalValue}>
              / {data?.actual_nutrition?.daily_total?.total_carbs || 0} g
            </Text>
          </View>
        </View>
      </View>

      <ScrollView>
        {meals.map((meal, index) => (
          <TouchableOpacity
            activeOpacity={1}
            key={index}
            style={styles.mealTouchable}
            onPress={() => handlePressMeal(index)}
          >
            <View style={styles.mealContainer}>
              <View style={styles.mealHeader}>
                <Text style={styles.mealText}>
                  {meal.charAt(0).toUpperCase() + meal.slice(1)} (
                  {data?.actual_nutrition?.[meal]?.products?.length || 0})
                </Text>
                {exListIndex === index && (
                  <Image
                    source={require('../../assets/images/uparrow.png')}
                    style={styles.arrowIcon}
                  />
                )}
              </View>
              <TouchableOpacity
                onPress={() => {
                  console.log(data?.actual_nutrition);

                  navigation.navigate(Screens.FoodSelectionScreen, {
                    meal,
                    diet_id: data?.id,
                  });
                }}
                style={styles.addButton}
              >
                <Text style={styles.plusText}>+</Text>
              </TouchableOpacity>
            </View>

            {exListIndex === index && (
              <View style={styles.expandedMealContainer}>
                <View style={styles.nutritionFactsRow}>
                  <View style={styles.nutritionFacts}>
                    <Text style={[styles.nutritionFact, { marginLeft: 0 }]}>
                      🍖{' '}
                      {parseFloat(
                        String(
                          data?.actual_nutrition?.[meal]?.total_proteins ?? 0,
                        ),
                      ).toFixed(2) || 0}
                    </Text>
                    <Text style={styles.nutritionFact}>
                      🌰{' '}
                      {parseFloat(
                        String(data?.actual_nutrition?.[meal]?.total_fats ?? 0),
                      ).toFixed(2) || 0}
                    </Text>
                    <Text style={styles.nutritionFact}>
                      🌾{' '}
                      {parseFloat(
                        String(
                          data?.actual_nutrition?.[meal]?.total_carbs ?? 0,
                        ),
                      ).toFixed(2) || 0}
                    </Text>
                  </View>
                  <Text style={styles.caloriesText}>
                    🍽️ Calories:{' '}
                    {data?.actual_nutrition?.[meal]?.total_calories || 0}
                  </Text>
                </View>

                <View style={{ marginTop: '5%' }}>
                  {data?.actual_nutrition?.[meal].products?.map(
                    (product, index) => (
                      <TouchableOpacity
                        key={product.barcode || index}
                        onPress={() =>
                          navigation.navigate(Screens.FoodDetailsScreen, {
                            product,
                          })
                        }
                        style={{ marginTop: index === 0 ? '1%' : '7%' }}
                      >
                        <View
                          style={{
                            flexDirection: 'row',
                            justifyContent: 'space-between',
                          }}
                        >
                          <View>
                            <Text style={styles.mealDetailText}>
                              {product?.name?.length > 20
                                ? product?.name.substring(0, 20) + '...'
                                : product?.name}
                            </Text>
                            <Text style={styles.servingSizeText}>
                              {product.amount}g
                            </Text>
                          </View>
                          <Text style={{ color: '#FFFFFF', fontSize: 12 }}>
                            {parseFloat(product?.calories ?? 0).toFixed(2)}
                          </Text>
                        </View>

                        <View style={styles.nutritionFactsRow}>
                          <View style={styles.nutritionFacts}>
                            <Text
                              style={[styles.nutritionFact, { marginLeft: 0 }]}
                            >
                              🍖{' '}
                              {parseFloat(product?.proteins ?? 0).toFixed(2) ||
                                0}
                            </Text>
                            <Text style={styles.nutritionFact}>
                              🌰{' '}
                              {parseFloat(product?.fats ?? 0).toFixed(2) || 0}
                            </Text>
                            <Text style={styles.nutritionFact}>
                              🌾 {parseFloat(product?.carbs).toFixed(2) || 0}
                            </Text>
                          </View>
                        </View>
                      </TouchableOpacity>
                    ),
                  )}
                </View>
              </View>
            )}
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginHorizontal: 10,
    marginTop: 10,
  },
  headerText: {
    color: '#fff',
    fontSize: 20,
  },
  profilePic: {
    width: 40,
    height: 40,
    backgroundColor: '#ccc',
    borderRadius: 20,
  },
  statsContainer: {
    marginVertical: 20,
    backgroundColor: '#2E2D55',
    borderRadius: 10,
    paddingVertical: 10,
  },
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
  },
  statsText: {
    color: '#fff',
    fontSize: 16,
  },
  progressRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingHorizontal: 10,
  },
  progressBar: {
    height: 5,
    borderRadius: 30,
    width: '25%',
    backgroundColor: '#555',
    marginTop: 20,
    overflow: 'hidden',
  },
  statsValuesRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
  },
  statsValueContainer: {
    marginTop: 20,
    flexDirection: 'row',
  },
  statsValue: {
    color: '#fff',
    fontSize: 16,
  },
  statsTotalValue: {
    color: 'grey',
    fontSize: 16,
  },
  mealTouchable: {
    backgroundColor: '#333',
    padding: 15,
    marginVertical: 5,
    borderRadius: 10,
  },
  mealContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  mealHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  mealText: {
    color: '#fff',
    fontSize: 18,
  },
  arrowIcon: {
    height: 25,
    width: 25,
    marginLeft: 20,
  },
  addButton: {
    backgroundColor: '#B8FF5F',
    height: 30,
    width: 30,
    borderRadius: 15,
    alignItems: 'center',
    justifyContent: 'center',
  },
  plusText: {
    color: '#2E2D55',
    fontSize: 18,
  },
  expandedMealContainer: {
    paddingVertical: 10,
    marginTop: 5,
  },
  nutritionFactsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  nutritionFacts: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 15,
  },
  nutritionFact: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '500',
    marginLeft: 10,
  },
  caloriesText: { color: '#fff', fontSize: 14, fontWeight: '500' },
  mealDetailText: { color: '#fff', fontSize: 17, fontWeight: '500' },
  servingSizeText: {
    color: '#B8FF5F',
    fontSize: 14,
    fontWeight: '500',
    marginTop: 5,
  },
});

export default MainScreen;
