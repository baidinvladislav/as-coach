import React, { useEffect } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { useStore } from '@hooks';
import { LkScreen } from '@screens';

import { UserType } from '~types';

import MyTabs from './bottom-tab';

const User = () => {
  const { user } = useStore();
  const isCoach = user.me.user_type == UserType.COACH;
  console.log(isCoach);

  return <>{isCoach ? <LkScreen /> : <MyTabs />}</>;
};

export default User;

const styles = StyleSheet.create({});
