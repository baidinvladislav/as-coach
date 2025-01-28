import React, { useState } from 'react';
import { FlatList, ListRenderItemInfo, View } from 'react-native';

import styled from 'styled-components';

import { AddIcon } from '@assets';
import { LkEmpty, PlanCard } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { CustomerProps } from '@store';
import { colors, normVert } from '@theme';
import { Button, Text } from '@ui';

import { ButtonType, FontSize, TPlanType, UserType } from '~types';

type TProps = {
  data: Partial<CustomerProps>;
  getCustomerInfo: () => void;
  setPreviousScreen?: React.Dispatch<React.SetStateAction<Screens>>;
  title: string;
  description: string;
  withAddButton?: boolean; 
};

export const Plans = ({
  data,
  getCustomerInfo,
  setPreviousScreen,
  title,
  description,
  withAddButton = true,
}: TProps) => {
  const { navigate } = useNavigation();
  const { user } = useStore();
  const [isFetching, setIsFetching] = useState(false);

  const plans = data?.plans;

  const isCoach = user.me.user_type === UserType.COACH;

  const renderItem = (plan: ListRenderItemInfo<TPlanType>) => (
    <PlanCard
      plan={plan.item}
      onPress={() => handleNavigateDetailPlan(plan.item.id)}
      withMenu={isCoach}
    />
  );

  const handleNavigatePlan = () => {
    setPreviousScreen?.(Screens.PlanScreen);
    navigate(Screens.PlanScreen, data);
  };

  const handleNavigateDetailPlan = (id: string) => {
    setPreviousScreen?.(Screens.DetailPlanScreen);
    navigate(Screens.DetailPlanScreen, { id: data.id, planId: id });
  };

  const handleRefresh = () => {
    setIsFetching(true);
    getCustomerInfo();
    setIsFetching(false);
  };

  return plans?.length ? (
    <>
      <TopContainer>
        <Text fontSize={FontSize.S20} color={colors.white}>
          {t('detailCustomer.plans')}
        </Text>
        {isCoach && (
          <Button
            type={ButtonType.TEXT}
            onPress={handleNavigatePlan}
            leftIcon={<AddIcon fill={colors.green} />}
          >
            {t('buttons.createPlan')}
          </Button>
        )}
      </TopContainer>

      <FlatList
        nestedScrollEnabled={true}
        data={data.plans}
        renderItem={renderItem}
        keyExtractor={item => item.id}
        onRefresh={handleRefresh}
        refreshing={isFetching}
        bounces={!isFetching}
      />
    </>
  ) : (
    <LkEmpty
      title={title}
      description={description}
      onPress={handleNavigatePlan}
      buttonText={withAddButton ? t('buttons.createPlan') : undefined}
    />
  );
};

const TopContainer = styled(View)`
  margin-top: ${normVert(24)}px;
  margin-bottom: ${normVert(16)}px;
  padding-vertical: ${normVert(10)}px;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
`;
