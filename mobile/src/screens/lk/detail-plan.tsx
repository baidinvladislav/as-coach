import React, { useEffect, useState } from 'react';
import { Image, StyleSheet, View } from 'react-native';

import moment from 'moment';
import styled from 'styled-components';

import { getCustomerPlanDetail } from '@api';
import { BackgroundImage } from '@assets';
import { ExercisesList } from '@components';
import { t } from '@i18n';
import { RoutesProps, useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { Loader, ModalLayout, RowBorder, Text, ViewWithButtons } from '@ui';
import { renderNumber, windowHeight, windowWidth } from '@utils';

import { FontSize, FontWeight, TPlanType } from '~types';

export const DetailPlanScreen = ({ route }: RoutesProps) => {
  const [data, setData] = useState<TPlanType>();
  const { goBack } = useNavigation();

  const { id, planId } = route.params as { id: string; planId: string };

  useEffect(() => {
    getCustomerPlanDetail(id, planId).then(({ data }) => setData(data));
  }, [id, planId]);

  const isDifference = data?.proteins?.indexOf('/') !== -1;

  return (
    <ModalLayout>
      <BackgroundColor />
      <Background
        blurRadius={10}
        source={BackgroundImage}
        style={{ opacity: 0.3 }}
      />
      {data ? (
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={goBack}
          cancelText={t('buttons.ok')}
          isScroll={true}
        >
          <Text
            style={styles.title}
            color={colors.white}
            fontSize={FontSize.S20}
            weight={FontWeight.Bold}
          >
            {moment(data.start_date).format('D MMM').slice(0, -1)} —{' '}
            {moment(data.end_date).format('D MMM').slice(0, -1)}
          </Text>
          <RowBorder
            title={t('createPlan.title1')}
            cells={[
              {
                title: t('createPlan.placeholder1'),
                value: renderNumber(data.proteins, ' / '),
              },
              {
                title: t('createPlan.placeholder3'),
                value: renderNumber(data.carbs, ' / '),
              },
              {
                title: t('createPlan.placeholder2'),
                value: renderNumber(data.fats, ' / '),
              },
            ]}
            description={
              isDifference ? t('createPlan.differenceTime') : undefined
            }
          />
          <Text
            color={colors.white}
            style={styles.contentTitle}
            fontSize={FontSize.S20}
            weight={FontWeight.Bold}
          >
            {t('createPlan.title2')}
          </Text>
          <ExercisesList exercises={data.trainings} />
          <RowBorder
            title={t('createPlan.restTime')}
            cells={[
              {
                title: t('createPlan.description1'),
                value: `${data.set_rest} sec`,
              },
              {
                title: t('createPlan.description2'),
                value: `${data.exercise_rest} sec`,
              },
            ]}
          />
          <Text
            color={colors.white}
            style={styles.contentTitle}
            fontSize={FontSize.S20}
            weight={FontWeight.Bold}
          >
            {t('createPlan.title3')}
          </Text>
          <Text
            color={colors.white}
            fontSize={FontSize.S16}
            weight={FontWeight.Regular}
          >
            {data.notes}
          </Text>
        </ViewWithButtons>
      ) : (
        <View style={styles.loader}>
          <Loader />
        </View>
      )}
    </ModalLayout>
  );
};

const styles = StyleSheet.create({
  loader: {
    flex: 1,
    justifyContent: 'center',
  },
  title: {
    textTransform: 'uppercase',
    marginBottom: normVert(40),
  },
  contentTitle: { marginBottom: normVert(19) },
  list: {
    marginBottom: normVert(21),
  },
});

const Background = styled(Image)`
  position: absolute;
  width: ${windowWidth}px;
  height: ${windowHeight}px;
`;

const BackgroundColor = styled(View)`
  position: absolute;
  width: ${windowWidth}px;
  height: ${windowHeight}px;
  background-color: ${colors.black};
`;
