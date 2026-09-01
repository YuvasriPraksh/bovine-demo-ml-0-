import en from '../locales/en.json';
import ta from '../locales/ta.json';
import hi from '../locales/hi.json';

const translations = {
  en,
  ta,
  hi,
  te: en, // Fallback to English for Telugu for now
  kn: en  // Fallback to English for Kannada for now
};

let currentLanguage = localStorage.getItem('bovine_lang') || 'en';

export const setLanguage = (lang) => {
  if (translations[lang]) {
    currentLanguage = lang;
    localStorage.setItem('bovine_lang', lang);
    return true;
  }
  return false;
};

export const getLanguage = () => currentLanguage;

export const t = (key) => {
  const langObj = translations[currentLanguage] || translations['en'];
  return langObj[key] || translations['en'][key] || key;
};
