import React from 'react';
import { StyleSheet, View } from 'react-native';

import { TouchableOpacity } from 'react-native-gesture-handler';

import { ArrowRightIcon } from '@assets';
import { colors, normHor, normVert } from '@theme';
import { Badge, BadgeStatuses, Text } from '@ui';

import { FontSize } from '~types';

type ClientCardProps = {
  firstName: string;
  lastName: string;
  onPress: () => void;
};

export const ClientCard: React.FC<ClientCardProps> = ({
  firstName,
  lastName,
  onPress,
}) => (
  <TouchableOpacity onPress={onPress} style={styles.card}>
    <View style={styles.line} />
    <View style={styles.userInfo}>
      <View>
        <Badge text={'План истекает 20.04'} status={BadgeStatuses.GOOD} />
      </View>
      <View style={styles.names}>
        <Text color={colors.white} fontSize={FontSize.S17}>
          {lastName}
        </Text>
        <Text
          style={{ marginLeft: normHor(4) }}
          color={colors.white}
          fontSize={FontSize.S17}
        >
          {firstName}
        </Text>
      </View>
    </View>
    <View style={styles.arrowContainer}>
      <ArrowRightIcon />
    </View>
  </TouchableOpacity>
);

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: normVert(16),
    paddingBottom: normVert(18),
    backgroundColor: colors.grey5,
    borderRadius: 12,
    marginVertical: normVert(10),
  },

  line: {
    backgroundColor: colors.green,
    height: normVert(60),
    position: 'absolute',
    marginLeft: normVert(8),
    width: normHor(3),
    borderRadius: 10,
  },

  userInfo: {
    height: normVert(50),
    flexDirection: 'column',
    marginLeft: normHor(24),
    borderRadius: 10,
    justifyContent: 'space-between',
  },

  names: {
    alignSelf: 'flex-start',
    flexDirection: 'row',
  },

  arrowContainer: {
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'flex-end',
    marginRight: normVert(32),
  },
});
