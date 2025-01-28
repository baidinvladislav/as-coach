import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';

import LinearGradient from 'react-native-linear-gradient';
import Reanimated, {
  Easing,
  Extrapolation,
  interpolate,
  interpolateColor,
  useAnimatedProps,
  useAnimatedStyle,
  useDerivedValue,
  withTiming,
} from 'react-native-reanimated';
import styled from 'styled-components';

import { ArrowDownIcon, ArrowUp2Icon, EditIcon } from '@assets';
import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { ExerciseWithSupersetSimple, Text } from '@ui';

import { FontSize, TPropsExercise } from '~types';

type TProps = {
  exercises: TPropsExercise;
  onEdit?: () => void;
  onOpen?: () => void;
  isOpen?: boolean;
};

const AnimatedLinearGradient =
  Reanimated.createAnimatedComponent(LinearGradient);

const height = normVert(78);
const width = normHor(313);
const fullWidth = normHor(345);

export const ExercisesCard = ({
  exercises,
  onEdit,
  onOpen,
  isOpen,
}: TProps) => {
  const firstRender = useRef(true);

  useLayoutEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
  });

  const [isLocallyOpen, setIsLocallyOpen] = useState(false);
  const [isEndAnimation, setIsEndAnimation] = useState(true);

  const count = exercises.exercises.length;
  const duration = 200;
  const countDuration = duration + 50 * count;

  const derived = useDerivedValue(
    () =>
      isLocallyOpen
        ? withTiming(1, { duration: countDuration, easing: Easing.linear })
        : withTiming(0, { duration: countDuration, easing: Easing.linear }),
    [isLocallyOpen],
  );

  const widthDerived = useDerivedValue(
    () =>
      isLocallyOpen
        ? withTiming(1, { duration, easing: Easing.linear })
        : withTiming(0, { duration, easing: Easing.linear }),
    [isLocallyOpen],
  );

  const heightStyles = useAnimatedStyle(() => ({
    maxHeight: interpolate(derived.value, [0, 1], [height, 150 + 150 * count], {
      extrapolateRight: Extrapolation.CLAMP,
    }),
  }));

  const widthStyles = useAnimatedStyle(() => ({
    width: interpolate(widthDerived.value, [0, 1], [width, fullWidth], {
      extrapolateRight: Extrapolation.CLAMP,
    }),
  }));

  const gradientProps = useAnimatedProps(() => ({
    colors: [
      interpolateColor(
        derived.value,
        [0, 1],
        ['rgba(255, 255, 255, 0.2)', colors.black3],
      ),
      interpolateColor(
        derived.value,
        [0, 1],
        ['rgba(255, 255, 255, 0.002)', colors.black3],
      ),
    ],
  }));

  const handleOpen = (from?: 'programmicly' | 'ui') => {
    from === 'ui' && onOpen?.();
    setIsLocallyOpen(isLocallyOpen => !isLocallyOpen);

    if (isEndAnimation) {
      setIsEndAnimation(isEndAnimation => !isEndAnimation);
    } else {
      setTimeout(() => {
        setIsEndAnimation(isEndAnimation => !isEndAnimation);
      }, countDuration);
    }
  };

  useEffect(() => {
    if (!firstRender.current && !isOpen && isLocallyOpen) {
      handleOpen('programmicly');
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);

  const quantity = exercises.exercises.length;

  return (
    <TouchableOpacity activeOpacity={0.9} onPress={() => handleOpen('ui')}>
      <Reanimated.View style={[styles.box, heightStyles, widthStyles]}>
        <Container
          colors={[colors.black3, colors.black3]}
          animatedProps={gradientProps}
        >
          <View style={[!isEndAnimation && styles.topContainer, styles.row]}>
            <View>
              <View style={[styles.row, { justifyContent: 'flex-start' }]}>
                <Text color={colors.white} fontSize={FontSize.S17}>
                  {exercises.name}
                </Text>
                {onEdit && (
                  <Icon onPress={onEdit}>
                    <EditIcon fill={colors.green} />
                  </Icon>
                )}
              </View>
              <Text
                style={styles.exercisesText}
                color={colors.black4}
                fontSize={FontSize.S12}
              >
                {t('createPlan.exercises')} {quantity}
              </Text>
            </View>
            {exercises.exercises.length ? (
              <Icon onPress={() => handleOpen('ui')}>
                {isLocallyOpen ? <ArrowUp2Icon /> : <ArrowDownIcon />}
              </Icon>
            ) : null}
          </View>
          {!isEndAnimation && (
            <ExerciseWithSupersetSimple exercises={exercises.exercises} />
          )}
        </Container>
      </Reanimated.View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  box: {
    overflow: 'hidden',
    marginBottom: normVert(19),
    borderRadius: 12,
    marginLeft: 'auto',
    marginRight: 'auto',
  },
  exercisesText: {
    marginTop: normVert(10),
  },
  topContainer: {
    borderBottomColor: colors.grey7,
    borderBottomWidth: 1,
    paddingBottom: normVert(16),
    marginBottom: normVert(4),
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
});

const Container = styled(AnimatedLinearGradient)`
  width: 100%;
  padding-vertical: ${normVert(16)}px;
  padding-horizontal: ${normHor(16)}px;
`;

const Icon = styled(TouchableOpacity)`
  margin-left: ${normHor(13)}px;
`;
