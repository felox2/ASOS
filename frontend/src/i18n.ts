import { createI18n } from 'vue-i18n'
import en from './locales/en.json'

export const i18n = createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  legacy: false,
  messages: { en },
  numberFormats: {
    en: {
      currency: {
        style: 'currency',
        currency: 'eur',
        maximumFractionDigits: 2,
        minimumFractionDigits: 2,
      },
    },
    sk: {
      currency: {
        style: 'currency',
        currency: 'eur',
        maximumFractionDigits: 2,
        minimumFractionDigits: 2,
      },
    },
  },
})
