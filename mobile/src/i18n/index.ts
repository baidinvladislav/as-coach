import { createIntl, createIntlCache } from 'react-intl';

import { flattenMessages } from '@utils';

import { en } from './locales/en';

const cache = createIntlCache();

const locale = 'en';

const i18nMsg: { [key: string]: Record<string, string> } = {
  en: flattenMessages(en),
};

export const intl = createIntl(
  {
    locale,
    messages: i18nMsg[locale],
  },
  cache,
);

export const t = (id: string, values = {}): string =>
  intl.formatMessage({ id }, values);
