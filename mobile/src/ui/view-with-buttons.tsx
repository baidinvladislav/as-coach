import React from 'react';
import {
  ScrollView,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
} from 'react-native';

import styled from 'styled-components';

import { t } from '@i18n';
import { colors, normHor, normVert } from '@theme';
import { Button } from '@ui';
import { windowWidth } from '@utils';

import { ButtonType } from '~types';

type TProps = {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  onCancel: () => void;
  onConfirm: () => void;
  isDisabled?: boolean;
  confirmText?: string;
  cancelText?: string;
  isScroll?: boolean;
};

export const ViewWithButtons = ({
  children,
  style,
  onCancel,
  onConfirm,
  confirmText = t('buttons.save'),
  cancelText = t('buttons.cancel'),
  isDisabled,
  isScroll = false,
}: TProps) => {
  const Container = isScroll ? ScrollView : View;
  return (
    <ChildrenContainer style={style}>
      <Container
        style={styles.container}
        contentContainerStyle={styles.container}
      >
        {children}
      </Container>
      <ButtonsContainer>
        <Button
          style={styles.button}
          type={ButtonType.PRIMARY}
          onPress={onConfirm}
          isDisabled={isDisabled}
        >
          {confirmText}
        </Button>
        <Button type={ButtonType.SECONDARY} onPress={onCancel}>
          {cancelText}
        </Button>
      </ButtonsContainer>
    </ChildrenContainer>
  );
};

const styles = StyleSheet.create({
  button: { marginBottom: normVert(20) },
  container: { paddingBottom: normVert(16) },
});

const ChildrenContainer = styled(View)`
  padding-horizontal: ${normHor(16)}px;
  flex: 1;
`;

const ButtonsContainer = styled(View)`
  background-color: ${colors.grey2};
  width: ${windowWidth}px;
  left: -${normHor(16)}px;
  padding-horizontal: ${normHor(16)}px;
  padding-vertical: ${normVert(20)}px;
`;
