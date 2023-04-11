import React, { Ref, useRef, useState } from 'react';
import { TextInput, View } from 'react-native';

import moment from 'moment';
import DatePicker from 'react-native-date-picker';
import { TouchableOpacity } from 'react-native-gesture-handler';
import styled from 'styled-components';

import { colors, normHor, normVert } from '@theme';
import { Placeholder, TInputProps, Text } from '@ui';

import { FontSize } from '~types';

export const DatePickerInput = ({ placeholder, style }: TInputProps) => {
  const ref = useRef<{ focus: () => void; blur: () => void }>();
  const [isFirstOpen, setIsFirstOpen] = useState(true);
  const [isOpen, setIsOpen] = useState(false);
  const [date, setDate] = useState(new Date());

  const text = moment(date).format('dd D MMM');

  const handleFocus = () => {
    if (isFirstOpen) setIsFirstOpen(false);
    setIsOpen(() => true);
  };

  const handleBlur = () => {
    setIsOpen(() => false);
  };

  const handlePress = () => {
    if (isOpen) {
      ref.current?.blur();
    } else {
      ref.current?.focus();
    }
  };

  return (
    <Container onPress={handlePress} height={isOpen ? 241 : 48} style={style}>
      <HiddenInput
        ref={ref as unknown as Ref<TextInput>}
        caretHidden={true}
        onFocus={handleFocus}
        onBlur={handleBlur}
      />
      {placeholder && (
        <Placeholder isActive={!(!isOpen && isFirstOpen)} text={placeholder} />
      )}
      {!isFirstOpen && (
        <Text
          style={{ marginTop: normVert(22) }}
          color={colors.white}
          fontSize={FontSize.S16}
        >
          {text}
        </Text>
      )}
      {isOpen && (
        <DatePicker
          style={{ marginLeft: 'auto', marginRight: 'auto' }}
          theme={'dark'}
          mode={'datetime'}
          date={date}
          onDateChange={setDate}
        />
      )}
    </Container>
  );
};

const Container = styled(TouchableOpacity)<{ height: number }>`
  height: ${({ height }) => normVert(height)}px;
  background-color: ${colors.black3};
  border-radius: 12px;
  padding-horizontal: ${normHor(16)}px;
`;

const HiddenInput = styled(TextInput)`
  position: absolute;
`;
