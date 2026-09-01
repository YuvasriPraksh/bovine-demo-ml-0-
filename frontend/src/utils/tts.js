import { getLanguage } from './i18n';

export const speakText = (text) => {
  if (!window.speechSynthesis) {
    console.warn("Text-to-Speech is not supported in this browser.");
    return;
  }

  // Cancel any ongoing speech
  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  
  // Try to set appropriate language code based on current selection
  const lang = getLanguage();
  const langMap = {
    'en': 'en-IN', // Indian English preferred
    'ta': 'ta-IN',
    'hi': 'hi-IN',
    'te': 'te-IN',
    'kn': 'kn-IN'
  };
  
  utterance.lang = langMap[lang] || 'en-US';
  
  // Set slight adjustments for better readability for farmers
  utterance.rate = 0.9; 
  utterance.pitch = 1.0;

  window.speechSynthesis.speak(utterance);
};
