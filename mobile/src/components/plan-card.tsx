import React from 'react';
import { Platform, ScrollView, StyleSheet, View } from 'react-native';

import moment from 'moment';
import { TouchableOpacity } from 'react-native-gesture-handler';
import styled from 'styled-components';

import { MoreIcon } from '@assets';
import { t } from '@i18n';
import { MenuAction, MenuView } from '@react-native-menu/menu';
import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';
import { renderNumber } from '@utils';

import { FontSize, TPlanType } from '~types';

type TProps = {
  plan: TPlanType;
  onPress: () => void;
  withMenu?: boolean;
};

const ACTIONS = [
  {
    id: 'share',
    title: 'Повторить',
    titleColor: colors.white,
    image: Platform.select({
      ios: 'arrow.clockwise',
      android: 'ic_menu_share',
    }),
    imageColor: colors.white,
  },
  {
    id: 'destructive',
    title: 'Удалить',
    attributes: {
      destructive: true,
    },
    image: Platform.select({
      ios: 'trash',
      android: 'ic_menu_delete',
    }),
  },
] as MenuAction[];

export const PlanCard = ({ plan, onPress, withMenu = true }: TProps) => (
  <Container onPress={onPress}>
    <View style={styles.top}>
      <View pointerEvents="none">
        <Text style={styles.title} color={colors.white} fontSize={FontSize.S17}>
          {moment(plan.start_date, 'YYYY-MM-DD').format('D MMM').slice(0, -1)} —{' '}
          {moment(plan.end_date, 'YYYY-MM-DD').format('D MMM').slice(0, -1)}
        </Text>
      </View>
      {withMenu && (
        <MenuView
          onPressAction={({ nativeEvent }) => {
            console.log(JSON.stringify(nativeEvent));
          }}
          actions={ACTIONS}
          shouldOpenOnLongPress={true}
        >
          <Icon>
            <MoreIcon stroke={colors.green} />
          </Icon>
        </MenuView>
      )}
    </View>
    <ScrollView horizontal={true} contentContainerStyle={styles.row}>
      <NumberContainer>
        <NumberText color={colors.white} fontSize={FontSize.S10}>
          {t('detailCustomer.proteins', {
            number: renderNumber(plan.proteins, ' gr / '),
          })}
        </NumberText>
      </NumberContainer>
      <NumberContainer>
        <NumberText color={colors.white} fontSize={FontSize.S10}>
          {t('detailCustomer.carbs', {
            number: renderNumber(plan.carbs, ' gr / '),
          })}
        </NumberText>
      </NumberContainer>
      <NumberContainer isLast={true}>
        <NumberText color={colors.white} fontSize={FontSize.S10}>
          {t('detailCustomer.fats', {
            number: renderNumber(plan.fats, ' gr / '),
          })}
        </NumberText>
      </NumberContainer>
    </ScrollView>
  </Container>
);

const styles = StyleSheet.create({
  modal: {
    borderRadius: 14,
    width: normHor(250),
    backgroundColor: colors.black6,
    right: 0,
  },
  top: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginHorizontal: normHor(16),
    marginBottom: normVert(20),
  },
  title: {
    textTransform: 'uppercase',
  },
  row: {
    flexDirection: 'row',
    paddingLeft: normHor(16),
  },
  border: {
    borderBottomColor: colors.black3,
    borderBottomWidth: 1,
  },
});

const NumberContainer = styled(View)<{ isLast?: boolean }>`
  padding-vertical: ${normVert(2)}px;
  padding-horizontal: ${normHor(6)}px;
  background-color: ${colors.grey5};
  border-radius: 6px;
  margin-right: ${({ isLast }) => (isLast ? 0 : normHor(10))}px;
`;

const NumberText = styled(Text)`
  text-transform: uppercase;
`;

const Container = styled(TouchableOpacity)`
  background-color: ${colors.black3};
  border-radius: 12px;
  width: 100%;
  padding-vertical: ${normVert(16)}px;
  margin-bottom: ${normVert(19)}px;
  overflow: hidden;
`;

const Icon = styled(View)`
  /* position: absolute;
  right: ${normHor(16)}px;
  top: ${normVert(18)}px; */
  width: ${normHor(20)}px;
  height: ${normVert(20)}px;
`;

const ModalItem = styled(TouchableOpacity)`
  flex-direction: row;
  justify-content: space-between;
  padding-vertical: ${normVert(11)}px;
  padding-horizontal: ${normHor(16)}px;
`;
