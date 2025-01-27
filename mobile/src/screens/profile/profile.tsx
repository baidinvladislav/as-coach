import React from 'react';
import { Alert, Image, StyleSheet, TouchableOpacity, View } from 'react-native';

import { observer } from 'mobx-react';
import styled from 'styled-components';

import { profileDelete } from '@api';
import {
  ArrowLeftIcon,
  ArrowRightIcon,
  DefaultAvatarImage,
  LockIcon,
  LogoutIcon,
  UserEditIcon,
} from '@assets';
import { ProfileListItem } from '@components';
import { BASE_URL, TOP_PADDING } from '@constants';
import { useStore } from '@hooks';
import { t } from '@i18n';
import { Screens, useNavigation } from '@navigation';
import { colors, normHor, normVert } from '@theme';
import { Text } from '@ui';

import { FontSize } from '~types';

const DATA = (
  onPress1: () => void,
  onPress2: () => void,
  onPress3: () => void,
) => [
  {
    id: 1,
    name: t('profile.nav1'),
    icon: <UserEditIcon stroke={colors.green} />,
    rightIcon: <ArrowRightIcon />,
    onPress: onPress1,
  },
  {
    id: 2,
    name: t('profile.nav2'),
    icon: <LockIcon stroke={colors.green} />,
    rightIcon: <ArrowRightIcon />,
    onPress: onPress2,
  },
  {
    id: 3,
    color: colors.red,
    name: t('profile.nav4'),
    icon: <LogoutIcon stroke={colors.red} />,
    onPress: onPress3,
  },
];

const DeleteAccountContainer = styled(TouchableOpacity)`
  flex-direction: row;
  align-items: center;
  height: ${normVert(100)}px;
  justify-content: center;
  margin-top: ${normVert(40)}px;
`;

const RegularText = styled(Text)`
  color: ${colors.grey9};
  font-size: ${FontSize.S12};
`;

const ClickableText = styled(Text)`
  color: ${colors.grey9};
  text-decoration-line: underline;
  font-size: ${FontSize.S12};
`;

export const ProfileScreen = observer(() => {
  const { user, customer } = useStore();

  const { navigate, goBack } = useNavigation();

  const handleGoEdit = () => {
    navigate(Screens.ProfileEditScreen);
  };

  const handleGoChangePassword = () => {
    navigate(Screens.ChangePasswordScreen);
  };

  const handleLogout = () => {
    customer.setInitialCustomers();
    user.logout().then(() => navigate(Screens.WelcomeScreen));
  };

  const handleDeleteAccount = () => {
    console.log();
    profileDelete().then(() =>
      user.logout().then(() => navigate(Screens.WelcomeScreen)),
    );
  };

  const showConfirmationDialog = () => {
    Alert.alert(
      t('profile.confirmDeleteDialogQuestion'),
      t('profile.confirmDeleteDialogWarning'),
      [
        {
          text: t('profile.confirmDeleteDialogCancel'),
          onPress: () => console.log('profile.deletion.is.canceled'),
          style: 'cancel',
        },
        {
          text: t('profile.confirmDeleteDialogConfirm'),
          onPress: () => handleDeleteAccount(),
          style: 'destructive',
        },
      ],
      { cancelable: false },
    );
  };

  return (
    <View style={{ paddingTop: TOP_PADDING }}>
      <BackButton
        style={{ width: normHor(20) }}
        // onPress={() => navigate(Screens.LkScreen)}
        onPress={() => goBack()}
      >
        <ArrowLeftIcon />
      </BackButton>
      <Text align="center" fontSize={FontSize.S17} color={colors.white}>
        {t('profile.profileTitle')}
      </Text>
      <Avatar
        source={
          user.me.photo_link
            ? { uri: BASE_URL + user.me.photo_link }
            : DefaultAvatarImage
        }
      />
      <Text
        style={styles.text}
        align="center"
        fontSize={FontSize.S24}
        color={colors.white}
      >
        {user.me.first_name}
      </Text>
      {DATA(handleGoEdit, handleGoChangePassword, handleLogout).map(
        (item, key) => (
          <ProfileListItem
            index={key}
            color={item.color}
            icon={item.icon}
            name={item.name}
            key={item.id}
            rightIcon={item.rightIcon}
            handlePress={item.onPress}
          />
        ),
      )}
      <DeleteAccountContainer onPress={showConfirmationDialog}>
        <RegularText>{t('profile.profileDeletionPrefix') + ' '}</RegularText>
        <ClickableText>{t('profile.profileDeletionClickable')}</ClickableText>
      </DeleteAccountContainer>
    </View>
  );
});

const styles = StyleSheet.create({
  text: { marginBottom: normVert(62) },
});

const BackButton = styled(TouchableOpacity)`
  margin-bottom: ${normVert(24)}px;
`;

const Avatar = styled(Image)`
  width: ${normHor(113.5)}px;
  height: ${normVert(113.5)}px;
  border-radius: 100px;
  margin-left: auto;
  margin-right: auto;
  margin-vertical: ${normVert(32)}px;
`;
