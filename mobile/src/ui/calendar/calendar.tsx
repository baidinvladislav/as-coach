import React, {
  ChangeEvent,
  forwardRef,
  useCallback,
  useImperativeHandle,
  useMemo,
  useRef,
} from 'react';
import { StyleSheet, TextStyle, View } from 'react-native';

import { CalendarList, LocaleConfig } from 'react-native-calendars';

import {
  dayNames,
  dayNamesShort,
  monthNames,
  monthNamesShort,
  today,
} from '@constants';
import { colors, normHor, normVert } from '@theme';
import { windowWidth } from '@utils';

import { Text } from '../text';
import { CustomDay } from './day';

LocaleConfig.locales['ru'] = {
  monthNames,
  monthNamesShort,
  dayNames,
  dayNamesShort,
  today,
};

LocaleConfig.defaultLocale = 'ru';

const RANGE = 6;

const INITIAL_DATE = '2022-04-20';

type TProps = {
  horizontalView?: boolean;
  values: { start: string; end: string };
  onChange: {
    start: (e: string | React.ChangeEvent<any>) => void;
    end: (e: string | React.ChangeEvent<any>) => void;
  };
};

export const Calendar = forwardRef(
  ({ values, onChange, ...props }: TProps, ref) => {
    const dateType = useRef<'start' | 'end' | null>('start');
    const { horizontalView } = props;

    const handleChangeDateType = (type: 'start' | 'end') => {
      dateType.current = type;
    };

    useImperativeHandle(
      ref,
      () => ({
        handleChangeDateType,
      }),
      [],
    );

    const selected = useMemo(
      () => ({
        start: values.start,
        end: values.end,
      }),
      [values.end, values.start],
    );

    const isStartEmpty = selected.start === '';
    const isEndEmpty = selected.end === '';

    const onDayPress = useCallback(
      (day: string) => {
        const value = {
          target: { value: day },
        } as ChangeEvent<any>;

        if (
          dateType.current === 'start' &&
          (isEndEmpty || new Date(day) < new Date(selected.end))
        ) {
          onChange.start(value);
        }
        if (
          dateType.current === 'end' &&
          (isStartEmpty || new Date(day) > new Date(selected.start))
        ) {
          onChange.end(value);
        }
      },
      [isEndEmpty, isStartEmpty, onChange, selected.end, selected.start],
    );

    return (
      <View style={{ flex: 1 }}>
        <CalendarList
          style={{
            width: windowWidth + normHor(22),
            marginLeft: normHor(-28),
            height: '100%',
          }}
          calendarStyle={styles.calendarStyle}
          current={INITIAL_DATE}
          pastScrollRange={0}
          futureScrollRange={RANGE}
          theme={theme}
          dayComponent={params => (
            <CustomDay
              date={params.date?.dateString ?? ''}
              state={params.state as string}
              onDayPress={onDayPress}
              start={selected.start}
              end={selected.end}
            />
          )}
          markingType={'period'}
          renderHeader={!horizontalView ? renderCustomHeader : undefined}
          calendarHeight={normVert(442)}
          horizontal={horizontalView}
          pagingEnabled={horizontalView}
          staticHeader={horizontalView}
        />
      </View>
    );
  },
);

const theme = {
  calendarBackground: colors.black2,
  weekVerticalMargin: normVert(6),
};

const styles = StyleSheet.create({
  calendarStyle: {
    width: '100%',
    marginBottom: normVert(-120),
  },
  header: {
    flexDirection: 'row',
    width: '100%',
    justifyContent: 'space-between',
    marginBottom: normVert(24),
  },
  month: {
    marginLeft: 5,
  },
});

function renderCustomHeader(date: any) {
  const header = date.toString('MMMM yyyy');
  const [month, year] = header.split(' ');
  const textStyle: TextStyle = {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.white,
  };

  return (
    <View style={styles.header}>
      <Text style={[styles.month, textStyle]}>{`${month}, ${year}`}</Text>
    </View>
  );
}
