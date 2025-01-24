import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { AxiosError } from 'axios';
import { useFormik } from 'formik';
import { observer } from 'mobx-react';
import { getFcmToken } from 'src/push/notificationServices';
import styled from 'styled-components';

import { LogoIcon } from '@assets';
import { PasswordInput } from '@components';
import { OTP_LENGTH, PHONE_MASK, TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { UserProps } from '@store';
import { colors, normVert } from '@theme';
import { Button, Input, Keyboard, Text } from '@ui';
import { loginValidationSchema, transformPhone } from '@utils';

import { ButtonType, FontSize } from '~types';

export const LoginScreen = observer(() => {
  const { navigate } = useNavigation();

  const { user, loading } = useStore();
  const isLoading = loading.isLoading;
  const [fcmToken, setFcmToken] = useState<string | null>(null);

  const handleLogin = (values: Partial<UserProps>) => {
    user
      .login({
        ...values,
        username: transformPhone(values.username),
        fcm_token: fcmToken,
      })
      .then(() => {
        if (values.password && values.password.length === OTP_LENGTH) {
          navigate(Screens.NewChangePasswordScreen);
        } else {
          navigate(Screens.User);
        }
      })
      .catch((e: AxiosError<{ detail: string }>) => {
        setErrors({ password: e.response?.data?.detail });
      });
  };

  const { dirty, setErrors, errors, handleChange, handleSubmit, values } =
    useFormik({
      initialValues: { username: '', password: '' },
      onSubmit: handleLogin,
      validationSchema: loginValidationSchema,
      validateOnChange: false,
      validateOnBlur: false,
    });

  useEffect(() => {
    const fetchFcmToken = async () => {
      const token = await getFcmToken();
      setFcmToken(token);
    };

    fetchFcmToken();
  }, []);

  return (
    <Keyboard style={{ paddingTop: TOP_PADDING, flex: 1 }}>
      <Logo />
      <Text
        style={styles.title}
        align="center"
        fontSize={FontSize.S24}
        color={colors.white}
      >
        {t('auth.loginTitle')}
      </Text>
      <Inputs>
        <Input
          keyboardType={'phone-pad'}
          mask={PHONE_MASK}
          style={styles.input}
          placeholder={t('inputs.phone')}
          value={values.username}
          onChangeText={handleChange('username')}
          error={errors.username}
        />
        <PasswordInput
          value={values.password}
          placeholder={t('inputs.password')}
          onChangeText={handleChange('password')}
          error={errors.password}
        />
      </Inputs>
      <Button
        style={styles.button}
        type={ButtonType.PRIMARY}
        onPress={() => handleSubmit()}
        isDisabled={!dirty}
        isLoading={isLoading}
      >
        {t('buttons.login')}
      </Button>
      <Flex>
        <Text fontSize={FontSize.S17} color={colors.white}>
          {t('auth.noAccount')}
        </Text>
        <Button
          style={styles.button2}
          type={ButtonType.TEXT}
          onPress={() => navigate(Screens.RegistrationScreen)}
        >
          {t('buttons.registration')}
        </Button>
      </Flex>
    </Keyboard>
  );
});

const styles = StyleSheet.create({
  title: {
    marginBottom: normVert(32),
  },
  button: {
    marginBottom: normVert(20),
  },
  button2: {
    marginLeft: 5,
  },
  input: {
    marginBottom: normVert(20),
  },
});

const Inputs = styled(View)`
  flex: 1;
`;

const Flex = styled(View)`
  flex-direction: row;
  align-items: center;
  justify-content: center;
`;

const Logo = styled(LogoIcon)`
  margin-left: auto;
  margin-right: auto;
  margin-bottom: ${normVert(119)}px;
`;
