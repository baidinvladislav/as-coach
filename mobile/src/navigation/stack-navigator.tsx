import React, { useEffect } from 'react';

import { observer } from 'mobx-react-lite';
import { SmsScreen } from 'src/screens/auth/sms';

import { TOKEN } from '@constants';
import { useStore } from '@hooks';
import { Screens } from '@navigation';
import { createStackNavigator } from '@react-navigation/stack';
import {
  AddClientScreen,
  ChangePasswordScreen,
  DetailClient,
  DetailPlanScreen,
  LkScreen,
  LoginScreen,
  NewChangePasswordScreen,
  PlanScreen,
  ProfileEditScreen,
  ProfileScreen,
  RegistrationScreen,
  WelcomeScreen,
} from '@screens';
import { storage } from '@utils';

import { UserType } from '~types';

import ProductDetailsScreen from '../screens/nutrition/product-details-screen';
import ProductSelectionScreen from '../screens/nutrition/product-selection-screen';
import User from './User';
import MyTabs from './bottom-tab';

export const Stack = createStackNavigator();

export const StackNavigator = observer(() => {
  const { user, customer } = useStore();

  const isGuest = !user.hasAccess; // меняем !user.hasAccess на !!!user.hasAccess для разработки. Чтобы открывался сразу лк

  useEffect(() => {
    const getToken = storage.getItem(TOKEN);
    getToken.then((token?: string) => {
      token && user.getMe();
    });

    const isCoach = user.me.user_type === UserType.COACH;
    if (isCoach) {
      customer.getExercises();
      user.getMuscleGroups();
    }
  }, [customer, isGuest, user]);

  return (
    <Stack.Navigator
      initialRouteName={isGuest ? Screens.WelcomeScreen : Screens.User}
      screenOptions={{
        headerShown: false,
        animationEnabled: false,
      }}
    >
      {isGuest ? (
        <Stack.Group>
          <Stack.Screen
            name={Screens.WelcomeScreen}
            component={WelcomeScreen}
          />
          <Stack.Screen
            name={Screens.RegistrationScreen}
            component={RegistrationScreen}
          />
          <Stack.Screen name={Screens.LoginScreen} component={LoginScreen} />
          <Stack.Screen name={Screens.SmsScreen} component={SmsScreen} />
        </Stack.Group>
      ) : (
        <Stack.Group>
          <Stack.Screen name={Screens.User} component={User} />
          <Stack.Screen name={Screens.BottomTab} component={MyTabs} />
          <Stack.Screen
            name={Screens.FoodDetailsScreen}
            component={ProductDetailsScreen}
          />
          <Stack.Screen
            name={Screens.FoodSelectionScreen}
            component={ProductSelectionScreen}
          />
          <Stack.Screen name={Screens.LkScreen} component={LkScreen} />
          <Stack.Screen name={Screens.DetailClient} component={DetailClient} />
          <Stack.Screen
            options={{
              presentation: 'modal',
              animationEnabled: true,
            }}
            name={Screens.AddClientScreen}
            component={AddClientScreen}
          />
          <Stack.Screen
            options={{
              presentation: 'modal',
              animationEnabled: true,
            }}
            name={Screens.DetailPlanScreen}
            component={DetailPlanScreen}
          />
          <Stack.Group
            screenOptions={{
              presentation: 'modal',
              animationEnabled: true,
            }}
          >
            <Stack.Screen name={Screens.PlanScreen} component={PlanScreen} />
          </Stack.Group>
          <Stack.Screen name={Screens.SmsScreen} component={SmsScreen} />
          <Stack.Screen
            name={Screens.ProfileScreen}
            component={ProfileScreen}
          />
          <Stack.Screen
            name={Screens.ProfileEditScreen}
            component={ProfileEditScreen}
          />
          <Stack.Screen
            name={Screens.ChangePasswordScreen}
            component={ChangePasswordScreen}
          />
          <Stack.Screen
            name={Screens.NewChangePasswordScreen}
            component={NewChangePasswordScreen}
          />
        </Stack.Group>
      )}
    </Stack.Navigator>
  );
});
