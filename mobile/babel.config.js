module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: [
    [
      'module-resolver',
      {
        root: ['.'],
        extensions: [
          '.ios.ts',
          '.android.ts',
          '.ts',
          '.ios.tsx',
          '.android.tsx',
          '.tsx',
          '.jsx',
          '.js',
          '.json',
        ],
        alias: {
          '@components': './src/components',
          '@ui': './src/ui',
          '@theme': './src/theme',
          '@screens': './src/screens',
          '@navigation': './src/navigation',
          '@assets': './src/assets',
          '@data': './src/data',
          '@utils': './src/utils',
          '@i18n': './src/i18n',
          '@hooks': './src/hooks',
          '@constants': './src/constants',
          '@api': './src/api',
          '@store': './src/store',
          '~types': './src/types.ts',
        },
      },
    ],
    ['@babel/plugin-proposal-decorators', { legacy: true }],
    ['react-native-reanimated/plugin'],
  ],
};
