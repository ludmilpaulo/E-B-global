"use client";

import { createContext, useContext, useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';

type Language = 'en' | 'pt';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

// Translation data
const translations = {
  en: {
    'navigation.home': 'Home',
    'navigation.services': 'Services',
    'navigation.howItWorks': 'How it Works',
    'navigation.about': 'About',
    'navigation.contact': 'Contact',
    'navigation.login': 'Login',
    'navigation.signUp': 'Sign Up',
    'navigation.search': 'Search',
    'hero.title': 'Professional Services',
    'hero.subtitle': 'Across Africa',
    'hero.description': 'Connect with verified partners for Real Estate, Transportation, Legal Services, and more across Lusophone and Anglophone Africa',
    'hero.searchPlaceholder': 'Search for services...',
    'hero.getStarted': 'Get Started',
  },
  pt: {
    'navigation.home': 'Início',
    'navigation.services': 'Serviços',
    'navigation.howItWorks': 'Como Funciona',
    'navigation.about': 'Sobre',
    'navigation.contact': 'Contacto',
    'navigation.login': 'Entrar',
    'navigation.signUp': 'Registar',
    'navigation.search': 'Pesquisar',
    'hero.title': 'Serviços Profissionais',
    'hero.subtitle': 'Em Toda a África',
    'hero.description': 'Conecte-se com parceiros verificados para Imobiliário, Transporte, Serviços Jurídicos e mais em toda a África Lusófona e Anglófona',
    'hero.searchPlaceholder': 'Pesquisar serviços...',
    'hero.getStarted': 'Começar',
  }
};

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguage] = useState<Language>('en');

  // Detect device language on mount
  useEffect(() => {
    const detectLanguage = () => {
      if (typeof window !== 'undefined') {
        const browserLang = navigator.language.split('-')[0];
        const savedLang = localStorage.getItem('language') as Language;
        
        if (savedLang && (savedLang === 'en' || savedLang === 'pt')) {
          setLanguage(savedLang);
        } else if (browserLang === 'pt') {
          setLanguage('pt');
        } else {
          setLanguage('en');
        }
      }
    };

    detectLanguage();
  }, []);

  const handleLanguageChange = (newLang: Language) => {
    setLanguage(newLang);
    localStorage.setItem('language', newLang);
    
    // Update HTML lang attribute
    if (typeof document !== 'undefined') {
      document.documentElement.lang = newLang;
    }
  };

  const t = (key: string): string => {
    return translations[language][key as keyof typeof translations[typeof language]] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage: handleLanguageChange, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
