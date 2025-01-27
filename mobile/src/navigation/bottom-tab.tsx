import React, { useEffect } from 'react';
import { Image } from 'react-native';

import MainScreen from 'src/screens/nutrition/main-screen';

import { Screens } from '@navigation';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { LkScreen } from '@screens';

const Tab = createBottomTabNavigator();

const MyTabs = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarIcon: ({ focused }) => {
          let iconName;

          if (route.name === Screens.MainScreen) {
            iconName = focused
              ? require('../assets/images/Nactive.png')
              : require('../assets/images/NunActive.png');
          } else if (route.name === 'plan') {
            iconName = focused
              ? require('../assets/images/Pactive.png')
              : require('../assets/images/PunActive.png');
          }

          return <Image source={iconName} style={{ width: 24, height: 24 }} />;
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '600',
        },
        tabBarActiveTintColor: '#B8FF5F',
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: {
          backgroundColor: '#000',
          borderTopColor: '#000',
        },
      })}
    >
      <Tab.Screen
        name={Screens.MainScreen}
        component={MainScreen}
        options={{ tabBarLabel: 'Nutrition' }}
      />
      <Tab.Screen
        name={'plan'}
        component={LkScreen}
        options={{ tabBarLabel: 'Plan' }}
      />
    </Tab.Navigator>
  );
};

export default MyTabs;
