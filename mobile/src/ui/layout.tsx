import React, { useCallback, useEffect } from 'react';
import { StyleProp, View, ViewStyle } from 'react-native';

import Reanimated, {
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withTiming,
} from 'react-native-reanimated';
import { Edge, SafeAreaView } from 'react-native-safe-area-context';
import styled from 'styled-components';

import { BackgroundImage } from '@assets';
import { colors, normHor } from '@theme';
import { windowHeight, windowWidth } from '@utils';

type TProps = {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  backgroundBlurRadius?: number;
  backgroundOpacity?: number;
  edges?: Edge[];
};

export const Layout = ({
  children,
  style,
  backgroundBlurRadius = 0,
  backgroundOpacity = 1,
  edges,
}: TProps) => {
  const opacity = useSharedValue(backgroundOpacity);

  const changeOpacityUp = useCallback(() => {
    opacity.value = withTiming(backgroundOpacity, {
      duration: 100,
      easing: Easing.linear,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [backgroundOpacity]);

  useEffect(() => {
    changeOpacityUp();
  }, [backgroundOpacity, changeOpacityUp]);

  const animatedStyles = useAnimatedStyle(
    () => ({
      opacity: opacity.value,
    }),
    [opacity.value],
  );

  return (
    <SafeAreaView style={{ flex: 1 }} edges={edges}>
      <BackgroundColor />
      <Background
        blurRadius={backgroundBlurRadius}
        source={BackgroundImage}
        style={animatedStyles}
      />
      <Container style={style}>{children}</Container>
    </SafeAreaView>
  );
};

const Background = styled(Reanimated.Image)`
  position: absolute;
  width: ${windowWidth}px;
  height: ${windowHeight}px;
`;

const BackgroundColor = styled(Reanimated.View)`
  position: absolute;
  width: ${windowWidth}px;
  height: ${windowHeight}px;
  top: 0;
  background-color: ${colors.black};
`;

const Container = styled(View)`
  flex: 1;
`;
