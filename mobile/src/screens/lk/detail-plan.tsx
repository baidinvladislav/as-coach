import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import moment from 'moment';

import { getCustomerPlanDetail } from '@api';
import { ExercisesList } from '@components';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { RoutesProps, useNavigation } from '@navigation';
import { colors, normVert } from '@theme';
import { Loader, ModalLayout, RowBorder, Text, ViewWithButtons } from '@ui';
import { renderNumber } from '@utils';

import { FontSize, FontWeight, TPlanType, UserType } from '~types';

export const DetailPlanScreen = ({ route }: RoutesProps) => {
  const [data, setData] = useState<TPlanType>();
  const { goBack } = useNavigation();
  const { user, customer } = useStore();
  const isCoach = user.me.user_type === UserType.COACH;
  const { id, planId } = route.params as { id: string; planId: string };

  useEffect(() => {
    getCustomerPlanDetail(id, planId).then(({ data }) => setData(data));
  }, [id, planId]);

  const isDifference = data?.proteins?.indexOf('/') !== -1;

  return (
    <ModalLayout>
      {data ? (
        <ViewWithButtons
          style={{ justifyContent: 'space-between' }}
          onCancel={goBack}
          cancelText={t(isCoach ? 'buttons.ok' : 'buttons.fine')}
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
          {isCoach && (
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
          )}
          <Text
            color={colors.white}
            style={styles.contentTitle}
            fontSize={FontSize.S20}
            weight={FontWeight.Bold}
          >
            {t(isCoach ? 'createPlan.title3' : 'createPlan.title4')}
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
    paddingTop: 10,
    textTransform: 'uppercase',
    marginBottom: normVert(40),
  },
  contentTitle: { marginBottom: normVert(19) },
  list: {
    marginBottom: normVert(21),
  },
});
