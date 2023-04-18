import { TPlan } from '~types';

export const addExerciseToPlan = (values: TPlan, dayName: string, id: string) =>
  ({
    ...values,
    trainings: [
      ...values.trainings.map(training => {
        if (training?.name === dayName) {
          return {
            ...training,
            exercises: (() => {
              const exercises = training?.exercises;
              if (exercises?.length) {
                const isExists = !!exercises.find(item => item.id === id);
                const arr = exercises
                  .map(exercise => {
                    if (exercise.id === id) {
                      return undefined;
                    } else {
                      return exercise;
                    }
                  })
                  .filter(item => item);
                if (isExists) {
                  return arr;
                } else {
                  return [...arr, { id, sets: [12, 12, 12] }];
                }
              } else {
                return [{ id, sets: [12, 12, 12] }];
              }
            })(),
          };
        } else {
          return training;
        }
      }),
    ],
  } as TPlan);
