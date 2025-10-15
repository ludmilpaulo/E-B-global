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
    'footer.company': 'Company',
    'footer.services': 'Services',
    'footer.support': 'Support',
    'footer.aboutUs': 'About Us',
    'footer.howItWorks': 'How it Works',
    'footer.contact': 'Contact',
    'footer.realEstate': 'Real Estate',
    'footer.transportation': 'Transportation',
    'footer.business': 'Business',
    'footer.legal': 'Legal',
    'footer.language': 'Language',
    'footer.documents': 'Documents',
    'footer.helpCenter': 'Help Center',
    'footer.contactUs': 'Contact Us',
    'footer.safety': 'Safety',
    'footer.description': 'Connecting Lusophone and Anglophone Africa through professional services. Discover, compare, and book verified partners for all your business needs.',
    'footer.rightsReserved': 'All rights reserved.',
    'footer.tagline': '"We are One" - Connecting Africa through professional excellence',
    'services.categoriesTitle': 'Our Service Categories',
    'services.categoriesDescription': 'Comprehensive professional services across eight specialized categories, designed to meet all your business and personal needs in Africa.',
    'services.realEstate': 'Real Estate Consulting',
    'services.realEstateDesc': 'Professional real estate services, property management, and investment consulting.',
    'services.transportation': 'Transportation Services',
    'services.transportationDesc': 'Reliable transportation, vehicle rentals, and logistics solutions.',
    'services.business': 'Business Consulting',
    'services.businessDesc': 'Strategic business advice, market analysis, and growth planning.',
    'services.legal': 'Legal Services',
    'services.legalDesc': 'Legal consultation, document review, and compliance services.',
    'services.language': 'Language Services',
    'services.languageDesc': 'Translation, interpretation, language tutoring, and localization.',
    'services.documents': 'Document Recognition',
    'services.documentsDesc': 'Notary services, embassy documentation, and official certifications.',
    'services.catering': 'Corporate Catering',
    'services.cateringDesc': 'Professional catering services for corporate events and meetings.',
    'services.protocol': 'Protocol Services',
    'services.protocolDesc': 'Event planning, diplomatic services, and ceremonial arrangements.',
    'services.exploreServices': 'Explore Services',
    'services.notFound': 'Don\'t see what you\'re looking for?',
    'services.browseAll': 'Browse All Services',
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
    'footer.company': 'Empresa',
    'footer.services': 'Serviços',
    'footer.support': 'Suporte',
    'footer.aboutUs': 'Sobre Nós',
    'footer.howItWorks': 'Como Funciona',
    'footer.contact': 'Contacto',
    'footer.realEstate': 'Imobiliário',
    'footer.transportation': 'Transportes',
    'footer.business': 'Negócios',
    'footer.legal': 'Jurídico',
    'footer.language': 'Linguística',
    'footer.documents': 'Documentos',
    'footer.helpCenter': 'Centro de Ajuda',
    'footer.contactUs': 'Contacte-nos',
    'footer.safety': 'Segurança',
    'footer.description': 'Conectando África Lusófona e Anglófona através de serviços profissionais. Descubra, compare e reserve parceiros verificados para todas as suas necessidades empresariais.',
    'footer.rightsReserved': 'Todos os direitos reservados.',
    'footer.tagline': '"Somos Um" - Conectando África através da excelência profissional',
    'services.categoriesTitle': 'As Nossas Categorias de Serviços',
    'services.categoriesDescription': 'Serviços profissionais abrangentes em oito categorias especializadas, projetados para atender todas as suas necessidades empresariais e pessoais em África.',
    'services.realEstate': 'Consultoria Imobiliária',
    'services.realEstateDesc': 'Serviços imobiliários profissionais, gestão de propriedades e consultoria de investimentos.',
    'services.transportation': 'Serviços de Transporte',
    'services.transportationDesc': 'Transporte confiável, aluguer de viaturas e soluções logísticas.',
    'services.business': 'Consultoria de Negócios',
    'services.businessDesc': 'Conselhos estratégicos de negócios, análise de mercado e planeamento de crescimento.',
    'services.legal': 'Serviços Jurídicos',
    'services.legalDesc': 'Consultoria jurídica, revisão de documentos e serviços de conformidade.',
    'services.language': 'Serviços Linguísticos',
    'services.languageDesc': 'Tradução, interpretação, ensino de línguas e localização.',
    'services.documents': 'Reconhecimento de Documentos',
    'services.documentsDesc': 'Serviços notariais, documentação de embaixadas e certificações oficiais.',
    'services.catering': 'Catering Corporativo',
    'services.cateringDesc': 'Serviços de catering profissionais para eventos corporativos e reuniões.',
    'services.protocol': 'Serviços de Protocolo',
    'services.protocolDesc': 'Planeamento de eventos, serviços diplomáticos e arranjos cerimoniais.',
    'services.exploreServices': 'Explorar Serviços',
    'services.notFound': 'Não encontra o que procura?',
    'services.browseAll': 'Ver Todos os Serviços',
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
