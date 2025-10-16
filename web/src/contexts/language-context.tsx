"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface LanguageContextType {
  language: string;
  setLanguage: (lang: string) => void;
  t: (key: string) => string;
  formatCurrency: (amount: number, currency?: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

// Default translations
const translations = {
  en: {
    // Navigation
    'navigation.dashboard': 'Dashboard',
    'navigation.logout': 'Logout',
    
    // Dashboard
    'dashboard.welcome': 'Welcome back',
    'dashboard.totalBookings': 'Total Bookings',
    'dashboard.allTimeBookings': 'All time bookings',
    'dashboard.completed': 'Completed',
    'dashboard.successfullyCompleted': 'Successfully completed',
    'dashboard.averageRating': 'Average Rating',
    'dashboard.outOf5Stars': 'Out of 5 stars',
    'dashboard.totalRevenue': 'Total Revenue',
    'dashboard.earnings': 'Earnings',
    'dashboard.spent': 'Spent',
    'dashboard.recentBookings': 'Recent Bookings',
    'dashboard.yourLatestBookings': 'Your latest service bookings',
    'dashboard.noBookings': 'No recent bookings found',
    'dashboard.quickActions': 'Quick Actions',
    'dashboard.commonTasks': 'Common tasks and shortcuts',
    'dashboard.bookService': 'Book Service',
    'dashboard.viewProfile': 'View Profile',
    
    // Admin
    'admin.dashboard': 'Admin Dashboard',
    'admin.administrator': 'Administrator',
    'admin.totalUsers': 'Total Users',
    'admin.activePartners': 'Active Partners',
    'admin.totalBookings': 'Total Bookings',
    'admin.totalRevenue': 'Platform Revenue',

    // Services
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
    
    // Footer
    'footer.company': 'Company',
    'footer.aboutUs': 'About Us',
    'footer.howItWorks': 'How it Works',
    'footer.contact': 'Contact',
    'footer.services': 'Services',
    'footer.realEstate': 'Real Estate Consulting',
    'footer.transportation': 'Transportation',
    'footer.business': 'Business Consulting',
    'footer.legal': 'Legal Services',
    'footer.language': 'Language Services',
    'footer.documents': 'Document Recognition',
    'footer.support': 'Support',
    'footer.helpCenter': 'Help Center',
    'footer.contactUs': 'Contact Us',
    'footer.safety': 'Safety',
    'footer.description': 'Connecting Lusophone and Anglophone Africa through professional services. Discover, compare, and book verified partners for all your business needs.',
    'footer.rightsReserved': 'All rights reserved.',
    'footer.tagline': '"We are One" - Connecting Africa through professional excellence',
    
    // Auth
    'auth.welcomeBack': 'Welcome back',
    'auth.createAccount': 'Create an account',
    'auth.enterCredentials': 'Enter your email and password to sign in',
    'auth.enterDetails': 'Enter your details to create your account',
    'auth.firstName': 'First Name',
    'auth.lastName': 'Last Name',
    'auth.phoneNumber': 'Phone Number',
    'auth.accountType': 'Account Type',
    'auth.client': 'Client',
    'auth.partner': 'Service Provider',
    'auth.preferredLanguage': 'Preferred Language',
    'auth.email': 'Email',
    'auth.password': 'Password',
    'auth.confirmPassword': 'Confirm Password',
    'auth.signIn': 'Sign In',
    'auth.signUp': 'Sign Up',
    'auth.forgotPassword': 'Forgot your password?',
    'auth.dontHaveAccount': 'Don\'t have an account?',
    'auth.alreadyHaveAccount': 'Already have an account?',
    'auth.emailRequired': 'Email is required',
    'auth.emailInvalid': 'Email is invalid',
    'auth.passwordRequired': 'Password is required',
    'auth.passwordMinLength': 'Password must be at least 8 characters',
    'auth.firstNameRequired': 'First name is required',
    'auth.lastNameRequired': 'Last name is required',
    'auth.confirmPasswordRequired': 'Please confirm your password',
    'auth.passwordsDoNotMatch': 'Passwords do not match',
    'auth.loginSuccessful': 'Login successful!',
    'auth.registrationSuccessful': 'Registration successful!',
    'auth.anErrorOccurred': 'An error occurred',
    'auth.networkError': 'Network error. Please try again.',

    // Common
    'common.success': 'Success',
    'common.error': 'Error',
  },
  pt: {
    // Navigation
    'navigation.dashboard': 'Painel',
    'navigation.logout': 'Sair',
    
    // Dashboard
    'dashboard.welcome': 'Bem-vindo de volta',
    'dashboard.totalBookings': 'Total de Reservas',
    'dashboard.allTimeBookings': 'Reservas de todos os tempos',
    'dashboard.completed': 'Concluídas',
    'dashboard.successfullyCompleted': 'Concluídas com sucesso',
    'dashboard.averageRating': 'Avaliação Média',
    'dashboard.outOf5Stars': 'De 5 estrelas',
    'dashboard.totalRevenue': 'Receita Total',
    'dashboard.earnings': 'Ganhos',
    'dashboard.spent': 'Gasto',
    'dashboard.recentBookings': 'Reservas Recentes',
    'dashboard.yourLatestBookings': 'Suas últimas reservas de serviços',
    'dashboard.noBookings': 'Nenhuma reserva recente encontrada',
    'dashboard.quickActions': 'Ações Rápidas',
    'dashboard.commonTasks': 'Tarefas comuns e atalhos',
    'dashboard.bookService': 'Reservar Serviço',
    'dashboard.viewProfile': 'Ver Perfil',
    
    // Admin
    'admin.dashboard': 'Painel Administrativo',
    'admin.administrator': 'Administrador',
    'admin.totalUsers': 'Total de Utilizadores',
    'admin.activePartners': 'Parceiros Ativos',
    'admin.totalBookings': 'Total de Reservas',
    'admin.totalRevenue': 'Receita da Plataforma',

    // Services
    'services.categoriesTitle': 'Nossas Categorias de Serviços',
    'services.categoriesDescription': 'Serviços profissionais abrangentes em oito categorias especializadas, projetados para atender todas as suas necessidades comerciais e pessoais em África.',
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
    
    // Footer
    'footer.company': 'Empresa',
    'footer.aboutUs': 'Sobre Nós',
    'footer.howItWorks': 'Como Funciona',
    'footer.contact': 'Contacto',
    'footer.services': 'Serviços',
    'footer.realEstate': 'Consultoria Imobiliária',
    'footer.transportation': 'Transporte',
    'footer.business': 'Consultoria de Negócios',
    'footer.legal': 'Serviços Jurídicos',
    'footer.language': 'Serviços Linguísticos',
    'footer.documents': 'Reconhecimento de Documentos',
    'footer.support': 'Suporte',
    'footer.helpCenter': 'Centro de Ajuda',
    'footer.contactUs': 'Contacte-nos',
    'footer.safety': 'Segurança',
    'footer.description': 'Conectando África Lusófona e Anglófona através de serviços profissionais. Descubra, compare e reserve parceiros verificados para todas as suas necessidades comerciais.',
    'footer.rightsReserved': 'Todos os direitos reservados.',
    'footer.tagline': '"Somos Um" - Conectando África através da excelência profissional',
    
    // Auth
    'auth.welcomeBack': 'Bem-vindo de volta',
    'auth.createAccount': 'Criar uma conta',
    'auth.enterCredentials': 'Digite seu email e senha para entrar',
    'auth.enterDetails': 'Digite seus dados para criar sua conta',
    'auth.firstName': 'Nome',
    'auth.lastName': 'Sobrenome',
    'auth.phoneNumber': 'Número de Telefone',
    'auth.accountType': 'Tipo de Conta',
    'auth.client': 'Cliente',
    'auth.partner': 'Prestador de Serviços',
    'auth.preferredLanguage': 'Idioma Preferido',
    'auth.email': 'Email',
    'auth.password': 'Senha',
    'auth.confirmPassword': 'Confirmar Senha',
    'auth.signIn': 'Entrar',
    'auth.signUp': 'Registrar',
    'auth.forgotPassword': 'Esqueceu sua senha?',
    'auth.dontHaveAccount': 'Não tem uma conta?',
    'auth.alreadyHaveAccount': 'Já tem uma conta?',
    'auth.emailRequired': 'Email é obrigatório',
    'auth.emailInvalid': 'Email é inválido',
    'auth.passwordRequired': 'Senha é obrigatória',
    'auth.passwordMinLength': 'Senha deve ter pelo menos 8 caracteres',
    'auth.firstNameRequired': 'Nome é obrigatório',
    'auth.lastNameRequired': 'Sobrenome é obrigatório',
    'auth.confirmPasswordRequired': 'Por favor confirme sua senha',
    'auth.passwordsDoNotMatch': 'As senhas não coincidem',
    'auth.loginSuccessful': 'Login bem-sucedido!',
    'auth.registrationSuccessful': 'Registro bem-sucedido!',
    'auth.anErrorOccurred': 'Ocorreu um erro',
    'auth.networkError': 'Erro de rede. Tente novamente.',

    // Common
    'common.success': 'Sucesso',
    'common.error': 'Erro',
  },
};

interface LanguageProviderProps {
  children: ReactNode;
}

export function LanguageProvider({ children }: LanguageProviderProps) {
  const [language, setLanguage] = useState<string>('en');

  useEffect(() => {
    // Detect browser language or use stored preference
    const storedLang = localStorage.getItem('preferred-language');
    const browserLang = navigator.language.startsWith('pt') ? 'pt' : 'en';
    setLanguage(storedLang || browserLang);
  }, []);

  const t = (key: string): string => {
    const langTranslations = translations[language as keyof typeof translations] || translations.en;
    return langTranslations[key as keyof typeof langTranslations] || key;
  };

  const formatCurrency = (amount: number, currency: string = 'USD'): string => {
    const locale = language === 'pt' ? 'pt-AO' : 'en-US';
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currency,
    }).format(amount);
  };

  const handleSetLanguage = (lang: string) => {
    setLanguage(lang);
    localStorage.setItem('preferred-language', lang);
  };

  return (
    <LanguageContext.Provider
      value={{
      language, 
        setLanguage: handleSetLanguage,
      t, 
      formatCurrency, 
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage(): LanguageContextType {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}