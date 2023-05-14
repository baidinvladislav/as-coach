import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { observer } from 'mobx-react';
import RadioGroup from 'react-native-radio-buttons-group';

import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Input, Text, ViewWithButtons } from '@ui';

import { FontSize, TExercises } from '~types';

import { PlanScreens } from './plan';

type TProps = {
  handleNavigate: (
    nextScreen: PlanScreens,
    params?: Record<string, any>,
    withValidate?: boolean,
  ) => void;
};

export const CreateExerciseScreen = observer(({ handleNavigate }: TProps) => {
  const { loading, user } = useStore();
  const isLoading = loading.isLoading;
  const data = user.muscleGroups;
  const [muscleGroupId, setMuscleGroupId] = useState<string | undefined>();
  const [exerciseName, setExerciseName] = useState('');
  const { navigate } = useNavigation();

  // send request to api to fetch muscle groups
  useEffect(() => {
    user.getMuscleGroups();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // mapping response to create radio buttons
  const formattedOptions = data.map(option => ({
    id: option.id,
    label: option.name,
    value: option.id,
    color: colors.green,
    labelStyle: {
      color: colors.white,
      fontSize: 16,
      paddingVertical: normVert(10),
    },
  }));

  // send request to create exercise
  const handleSubmit = () => {
    user
      .createExercise({
        name: exerciseName,
        muscle_group_id: muscleGroupId,
      })
      .then(() => navigate(Screens.DetailClient));
  };

  return (
    <>
      <Text style={styles.title} color={colors.white} fontSize={FontSize.S20}>
        {t('newExercise.title')}
      </Text>
      <View style={styles.input}>
        <Input
          placeholder={t('newExercise.placeholder')}
          onChangeText={setExerciseName}
          value={exerciseName}
        />
      </View>
      <Text
        style={styles.subtitle}
        color={colors.grey4}
        fontSize={FontSize.S12}
      >
        {t('newExercise.subtitle')}
      </Text>
      <ViewWithButtons
        style={{ justifyContent: 'space-between' }}
        confirmText={t('buttons.create')}
        onConfirm={handleSubmit}
        cancelText={t('buttons.cancel')}
        onCancel={() => handleNavigate(PlanScreens.CREATE_DATE_SCREEN)}
        isLoading={isLoading}
        isScroll={true}
      >
        <RadioGroup
          radioButtons={formattedOptions}
          onPress={setMuscleGroupId}
          selectedId={muscleGroupId}
          containerStyle={styles.radioButton}
        />
      </ViewWithButtons>
    </>
  );
});

const styles = StyleSheet.create({
  radioButton: {
    alignItems: 'flex-start',
  },

  title: {
    marginTop: normVert(14),
    marginBottom: normVert(16),
    marginLeft: normHor(16),
  },

  subtitle: {
    textTransform: 'uppercase',
    marginLeft: normHor(16),
    marginBottom: normVert(8),
    fontWeight: 'bold',
  },

  border: {
    borderTopColor: colors.black3,
    borderTopWidth: 1,
  },

  input: {
    marginBottom: normVert(40),
    marginHorizontal: normHor(16),
  },
});
