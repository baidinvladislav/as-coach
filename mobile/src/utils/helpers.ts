import moment from 'moment';
import { Asset } from 'react-native-image-picker';

import { URL_ANDROID, URL_IOS } from '@constants';
import { t } from '@i18n';
import { BadgeStatuses } from '@ui';

import { TPlan, TPropsExercises } from '~types';

import { isIOS } from './constants';

export const modifyPlan = (
  values: TPlan,
  dayName: string,
  value: TPropsExercises[],
) =>
  ({
    ...values,
    trainings: [
      ...values.trainings.map(training => {
        if (training?.name === dayName) {
          return {
            ...training,
            exercises: value.reduce((acc: TPropsExercises[], item, _, arr) => {
              if (item.superset_id) {
                item.supersets = [item.superset_id];

                for (let i = 0; i <= arr.length; i++) {
                  const el = arr[i];
                  if (
                    el?.superset_id === item.superset_id &&
                    el.id !== item.superset_id
                  ) {
                    item.supersets?.push(el.id);
                  }
                }
              }
              acc.push(item);
              return acc;
            }, []),
          };
        } else {
          return training;
        }
      }),
    ],
  } as TPlan);

// TODO: refactor the logic too complicated
export const addExerciseToPlan = (
  values: TPlan,
  dayName: string,
  id: string,
  name: string,
  value?: string[],
) =>
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
                      return value
                        ? { ...exercise, sets: value, name }
                        : undefined;
                    } else {
                      return exercise;
                    }
                  })
                  .filter(item => item);
                if (isExists) {
                  return arr;
                } else {
                  return [...arr, { id, sets: ['12', '12', '12'], name }];
                }
              } else {
                return [{ id, sets: ['12', '12', '12'], name }];
              }
            })(),
          };
        } else {
          return training;
        }
      }),
    ],
  } as TPlan);

export const clearArray = (arr: TPropsExercises[]) =>
  arr.map(
    (
      item,
      key,
      arr, // Очищаем массив с упражнениями от значений суперсетов, если упражнение не в суперсете
    ) =>
      item.superset_id &&
      (arr[key - 1]?.superset_id === item.superset_id ||
        arr[key + 1]?.superset_id === item.superset_id)
        ? item
        : { ...item, superset_id: undefined },
  );

export const changeFirstSupersetId = (
  data: TPropsExercises[],
  arr: TPropsExercises[],
  superset_id?: string,
) =>
  // Если первая позиция пропадает, то у упражнений суперсета меняем superset_id на тот id, который стал первым в суперсете
  arr.map(item => {
    if (item.superset_id === superset_id && item.id !== superset_id) {
      const id = data.find(
        item => item.superset_id === superset_id && item.id !== superset_id,
      )?.id;
      return { ...item, superset_id: id };
    }

    return item;
  });

export const moveExerciseFromUp = (
  to: number,
  data: TPropsExercises[],
  arr: TPropsExercises[],
  supersetsKeys: string[],
  supersetsValues: any[],
) => {
  for (let i = 0; i < supersetsValues.length; i++) {
    if (to >= supersetsValues[i][0] && to < supersetsValues[i][1]) {
      const superset_id = arr[to].superset_id;
      arr[to].superset_id = supersetsKeys[i];
      changeFirstSupersetId(data, arr, superset_id);
    }
  }
};

export const moveExerciseFromDown = (
  to: number,
  data: TPropsExercises[],
  arr: TPropsExercises[],
  supersetsKeys: string[],
  supersetsValues: any[],
) => {
  for (let i = 0; i < supersetsValues.length; i++) {
    if (to > supersetsValues[i][0] && to <= supersetsValues[i][1]) {
      const superset_id = arr[to].superset_id;
      arr[to].superset_id = supersetsKeys[i];
      changeFirstSupersetId(data, arr, superset_id);
    }
  }
};

export const createFormData = (photo?: Asset, body = {}) => {
  const data = new FormData();
  if (photo) {
    data.append('photo', {
      name: photo.fileName,
      type: photo.type,
      uri: isIOS ? photo?.uri?.replace('file://', '') : photo.uri,
    });
  }
  Object.keys(body).forEach(key => {
    if (key !== 'photo') {
      data.append(key, (body as any)[key]);
    }
  });

  return data;
};

export const makeAvatarLink = (link: string | null) => {
  const api = isIOS ? URL_IOS : URL_ANDROID;
  return link ? api + link : '';
};

export const getWeek = (date: Date) => {
  const firstWeekday = new Date(
    date.getFullYear(),
    date.getMonth(),
    1,
  ).getDay();
  const offsetDate = date.getDate() + firstWeekday - 1;
  return Math.floor(offsetDate / 7);
};

export const renderNumber = (number: string, join: string) => {
  const arr = number.split('/');

  return arr.join(join) + ' gr';
};

const getDifferenceInDays = (dateEnd: string): number => {
  const currentDate = moment().startOf('day');
  const dateCompletion = moment(dateEnd).startOf('day');
  return dateCompletion.diff(currentDate, 'days');
};

const getCustomerStatus = (dateEnd: string) => {
  if (!dateEnd) {
    return BadgeStatuses.PLAN_NOT_EXISTS;
  } else {
    const differenceInDays = getDifferenceInDays(dateEnd);

    if (differenceInDays > 3) {
      return BadgeStatuses.GOOD;
    } else if (differenceInDays == 0) {
      return BadgeStatuses.WARNING_TODAY;
    } else if (differenceInDays == 1) {
      return BadgeStatuses.WARNING_TOMORROW;
    } else if (differenceInDays == -1) {
      return BadgeStatuses.EXPIRED_YESTERDAY;
    } else if (0 < differenceInDays && differenceInDays <= 3) {
      return BadgeStatuses.WARNING;
    } else {
      return BadgeStatuses.EXPIRED;
    }
  }
};

const getDayWord = (difference: number) => {
  let num = Math.abs(difference);
  num = num % 100;

  if (num > 19) {
    num = num % 10;
  }
  switch (num) {
    case 1:
      return 'день';
    case 2:
    case 3:
    case 4:
      return 'дня';
    default:
      return 'дней';
  }
};

const getTextByCustomerStatus = (status: BadgeStatuses, dateEnd: string) => {
  const differenceInDays = getDifferenceInDays(dateEnd);
  let text = '';

  if (status === BadgeStatuses.GOOD) {
    text = t('lk.customerStatus.expiring', {
      days: Math.abs(differenceInDays),
      dayWord: getDayWord(differenceInDays),
    });
  } else if (status === BadgeStatuses.WARNING_TODAY) {
    text = t('lk.customerStatus.expiring_today');
  } else if (status === BadgeStatuses.WARNING_TOMORROW) {
    text = t('lk.customerStatus.expiring_tomorrow');
  } else if (status === BadgeStatuses.WARNING) {
    text = t('lk.customerStatus.expiring', {
      days: Math.abs(differenceInDays),
      dayWord: getDayWord(differenceInDays),
    });
  } else if (status === BadgeStatuses.EXPIRED) {
    text = t('lk.customerStatus.expired', {
      days: Math.abs(differenceInDays),
      dayWord: getDayWord(differenceInDays),
    });
  } else if (status === BadgeStatuses.EXPIRED_YESTERDAY) {
    text = t('lk.customerStatus.expired_yesterday');
  } else if (status === BadgeStatuses.PLAN_NOT_EXISTS) {
    text = t('lk.customerStatus.noPlan');
  }
  return text;
};

export const getCustomerStatusAndText = (dateEnd: string) => {
  const status = getCustomerStatus(dateEnd);
  const text = getTextByCustomerStatus(status, dateEnd);
  return { status, text };
};
