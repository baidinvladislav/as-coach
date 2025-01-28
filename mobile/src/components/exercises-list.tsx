import React, {
  forwardRef,
  useEffect,
  useImperativeHandle,
  useState,
} from 'react';
import { StyleSheet, View } from 'react-native';

import { ExercisesCard } from '@components';
import { normVert } from '@theme';

import { TPropsExercise } from '~types';

type TProps = {
  exercises: TPropsExercise[];
  onEdit?: (index: number) => void;
};

export const ExercisesList = forwardRef((props: TProps, ref) => {
  const [cards, setCards] = useState<boolean[]>([]);

  useImperativeHandle(
    ref,
    () => ({
      setCards,
      cards,
      handleOpen,
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  );

  useEffect(() => {
    setCards([]);
    setCards(new Array(props.exercises.length).fill(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleOpen = (key: number) => {
    setCards(new Array(props.exercises.length).fill(false));
    setCards(cards => cards.map((_, index) => index === key));
  };
  // console.log(' props.exercises.length======', props.exercises.length);
  // console.log(' exercises=====', JSON.stringify(props.exercises));

  return props.exercises.length ? (
    <View style={styles.list}>
      {props.exercises.map((exercises, key) => (
        <ExercisesCard
          key={key}
          onEdit={props.onEdit ? () => props.onEdit?.(key) : undefined}
          onOpen={() => handleOpen(key)}
          isOpen={Boolean(cards?.[key])}
          exercises={exercises}
        />
      ))}
    </View>
  ) : null;
});

const styles = StyleSheet.create({
  list: {
    marginBottom: normVert(21),
  },
});
