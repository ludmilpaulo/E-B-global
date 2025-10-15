"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';

type Language = 'en' | 'pt';
type Currency = 'USD' | 'EUR' | 'AOA' | 'ZAR' | 'NGN' | 'GHS' | 'KES';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  currency: Currency;
  setCurrency: (curr: Currency) => void;
  t: (key: string) => string;
  formatCurrency: (amount: number) => string;
  convertCurrency: (amount: number, fromCurrency?: Currency) => number;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

// Currency conversion rates (mock data - in production, use real API like exchangerate-api.com)
const currencyRates: Record<Currency, number> = {
  USD: 1.0,
  EUR: 0.85,
  AOA: 830.0, // Angolan Kwanza
  ZAR: 18.5,  // South African Rand
  NGN: 460.0, // Nigerian Naira
  GHS: 12.0,  // Ghanaian Cedi
  KES: 150.0, // Kenyan Shilling
};

// Country to currency mapping
const countryCurrencyMap: Record<string, Currency> = {
  'AO': 'AOA', // Angola
  'ZA': 'ZAR', // South Africa
  'NG': 'NGN', // Nigeria
  'GH': 'GHS', // Ghana
  'KE': 'KES', // Kenya
  'MZ': 'USD', // Mozambique (using USD as default)
  'CV': 'USD', // Cape Verde
  'GW': 'USD', // Guinea-Bissau
  'ST': 'USD', // São Tomé and Príncipe
};

// Currency symbols
const currencySymbols: Record<Currency, string> = {
  USD: '$',
  EUR: '€',
  AOA: 'Kz',
  ZAR: 'R',
  NGN: '₦',
  GHS: '₵',
  KES: 'KSh',
};

// Comprehensive translation data
const translations = {
  en: {
    // Navigation
    'navigation.home': 'Home',
    'navigation.services': 'Services',
    'navigation.howItWorks': 'How it Works',
    'navigation.about': 'About',
    'navigation.contact': 'Contact',
    'navigation.login': 'Login',
    'navigation.signUp': 'Sign Up',
    'navigation.search': 'Search',
    'navigation.dashboard': 'Dashboard',
    'navigation.profile': 'Profile',
    'navigation.bookings': 'Bookings',
    'navigation.settings': 'Settings',
    'navigation.logout': 'Logout',
    'navigation.admin': 'Admin',
    'navigation.partner': 'Partner',

    // Hero Section
    'hero.title': 'Professional Services',
    'hero.subtitle': 'Across Africa',
    'hero.description': 'Connect with verified partners for Real Estate, Transportation, Legal Services, and more across Lusophone and Anglophone Africa',
    'hero.searchPlaceholder': 'Search for services...',
    'hero.getStarted': 'Get Started',
    'hero.findServices': 'Find Services',
    'hero.trustedPartners': 'Trusted Partners',
    'hero.verifiedServices': 'Verified Services',

    // Services
    'services.title': 'Our Services',
    'services.subtitle': 'Professional services across Lusophone and Anglophone Africa',
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
    'services.allCategories': 'All Categories',
    'services.searchPlaceholder': 'Search for services...',
    'services.noServicesFound': 'No services found matching your criteria',
    'services.clearFilters': 'Clear Filters',
    'services.bookNow': 'Book Now',
    'services.price': 'Price',
    'services.duration': 'Duration',
    'services.rating': 'Rating',
    'services.partner': 'Service Provider',
    'services.category': 'Category',

    // Booking
    'booking.title': 'Book Service',
    'booking.selectDate': 'Select Date',
    'booking.selectTime': 'Select Time',
    'booking.specialRequirements': 'Special Requirements',
    'booking.bookService': 'Book Service',
    'booking.bookingSummary': 'Booking Summary',
    'booking.totalAmount': 'Total Amount',
    'booking.paymentMethod': 'Payment Method',
    'booking.confirmBooking': 'Confirm Booking',
    'booking.bookingConfirmed': 'Booking Confirmed',
    'booking.serviceDetails': 'Service Details',
    'booking.processing': 'Processing...',
    'booking.backToServices': 'Back to Services',
    'booking.optional': 'Optional',
    'booking.required': 'Required',

    // Dashboard
    'dashboard.welcome': 'Welcome back',
    'dashboard.totalBookings': 'Total Bookings',
    'dashboard.completed': 'Completed',
    'dashboard.averageRating': 'Average Rating',
    'dashboard.totalRevenue': 'Total Revenue',
    'dashboard.recentBookings': 'Recent Bookings',
    'dashboard.quickActions': 'Quick Actions',
    'dashboard.bookService': 'Book Service',
    'dashboard.viewProfile': 'View Profile',
    'dashboard.noBookings': 'No recent bookings found',
    'dashboard.allTimeBookings': 'All time bookings',
    'dashboard.successfullyCompleted': 'Successfully completed',
    'dashboard.outOf5Stars': 'Out of 5 stars',
    'dashboard.earnings': 'Earnings',
    'dashboard.spent': 'Spent',

    // Admin Dashboard
    'admin.dashboard': 'Admin Dashboard',
    'admin.totalUsers': 'Total Users',
    'admin.activePartners': 'Active Partners',
    'admin.totalBookings': 'Total Bookings',
    'admin.totalRevenue': 'Total Revenue',
    'admin.pendingBookings': 'Pending Bookings',
    'admin.completedBookings': 'Completed Bookings',
    'admin.averageRating': 'Average Rating',
    'admin.activeServices': 'Active Services',
    'admin.recentActivity': 'Recent Activity',
    'admin.platformOverview': 'Platform Overview',
    'admin.userManagement': 'User Management',
    'admin.bookingManagement': 'Booking Management',
    'admin.revenueTracking': 'Revenue Tracking',
    'admin.platformAnalytics': 'Platform Analytics',
    'admin.exportData': 'Export Data',
    'admin.settings': 'Settings',
    'admin.administrator': 'Administrator',

    // Authentication
    'auth.login': 'Login',
    'auth.register': 'Register',
    'auth.logout': 'Logout',
    'auth.email': 'Email',
    'auth.password': 'Password',
    'auth.confirmPassword': 'Confirm Password',
    'auth.firstName': 'First Name',
    'auth.lastName': 'Last Name',
    'auth.phoneNumber': 'Phone Number',
    'auth.accountType': 'Account Type',
    'auth.preferredLanguage': 'Preferred Language',
    'auth.client': 'Client',
    'auth.partner': 'Service Provider',
    'auth.welcomeBack': 'Welcome back',
    'auth.createAccount': 'Create an account',
    'auth.enterCredentials': 'Enter your email and password to sign in',
    'auth.enterDetails': 'Enter your details to create your account',
    'auth.signIn': 'Sign In',
    'auth.signUp': 'Sign Up',
    'auth.dontHaveAccount': 'Don\'t have an account?',
    'auth.alreadyHaveAccount': 'Already have an account?',
    'auth.loginSuccessful': 'Login successful!',
    'auth.registrationSuccessful': 'Registration successful!',
    'auth.emailRequired': 'Email is required',
    'auth.emailInvalid': 'Email is invalid',
    'auth.passwordRequired': 'Password is required',
    'auth.passwordMinLength': 'Password must be at least 8 characters',
    'auth.firstNameRequired': 'First name is required',
    'auth.lastNameRequired': 'Last name is required',
    'auth.confirmPasswordRequired': 'Please confirm your password',
    'auth.passwordsDoNotMatch': 'Passwords do not match',
    'auth.networkError': 'Network error. Please try again.',
    'auth.anErrorOccurred': 'An error occurred',

    // Common
    'common.loading': 'Loading...',
    'common.error': 'Error',
    'common.success': 'Success',
    'common.cancel': 'Cancel',
    'common.save': 'Save',
    'common.edit': 'Edit',
    'common.delete': 'Delete',
    'common.confirm': 'Confirm',
    'common.back': 'Back',
    'common.next': 'Next',
    'common.previous': 'Previous',
    'common.search': 'Search',
    'common.filter': 'Filter',
    'common.sort': 'Sort',
    'common.view': 'View',
    'common.close': 'Close',
    'common.yes': 'Yes',
    'common.no': 'No',
    'common.submit': 'Submit',
    'common.reset': 'Reset',
    'common.clear': 'Clear',
    'common.select': 'Select',
    'common.choose': 'Choose',
    'common.optional': 'Optional',
    'common.required': 'Required',
    'common.and': 'and',
    'common.none': 'None',
    'common.today': 'Today',
    'common.yesterday': 'Yesterday',
    'common.tomorrow': 'Tomorrow',
    'common.thisWeek': 'This Week',
    'common.lastWeek': 'Last Week',
    'common.thisMonth': 'This Month',
    'common.lastMonth': 'Last Month',
    'common.thisYear': 'This Year',
    'common.lastYear': 'Last Year',

    // Footer
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

    // Currency
    'currency.usd': 'US Dollar',
    'currency.eur': 'Euro',
    'currency.aoa': 'Angolan Kwanza',
    'currency.zar': 'South African Rand',
    'currency.ngn': 'Nigerian Naira',
    'currency.ghs': 'Ghanaian Cedi',
    'currency.kes': 'Kenyan Shilling',
    'currency.select': 'Select Currency',
    'currency.convert': 'Convert Currency',
  },
  pt: {
    // Navigation
    'navigation.home': 'Início',
    'navigation.services': 'Serviços',
    'navigation.howItWorks': 'Como Funciona',
    'navigation.about': 'Sobre',
    'navigation.contact': 'Contacto',
    'navigation.login': 'Entrar',
    'navigation.signUp': 'Registar',
    'navigation.search': 'Pesquisar',
    'navigation.dashboard': 'Painel',
    'navigation.profile': 'Perfil',
    'navigation.bookings': 'Reservas',
    'navigation.settings': 'Configurações',
    'navigation.logout': 'Sair',
    'navigation.admin': 'Administrador',
    'navigation.partner': 'Parceiro',

    // Hero Section
    'hero.title': 'Serviços Profissionais',
    'hero.subtitle': 'Em Toda a África',
    'hero.description': 'Conecte-se com parceiros verificados para Imobiliário, Transporte, Serviços Jurídicos e mais em toda a África Lusófona e Anglófona',
    'hero.searchPlaceholder': 'Pesquisar serviços...',
    'hero.getStarted': 'Começar',
    'hero.findServices': 'Encontrar Serviços',
    'hero.trustedPartners': 'Parceiros Confiáveis',
    'hero.verifiedServices': 'Serviços Verificados',

    // Services
    'services.title': 'Os Nossos Serviços',
    'services.subtitle': 'Serviços profissionais em toda a África Lusófona e Anglófona',
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
    'services.allCategories': 'Todas as Categorias',
    'services.searchPlaceholder': 'Pesquisar serviços...',
    'services.noServicesFound': 'Nenhum serviço encontrado com os seus critérios',
    'services.clearFilters': 'Limpar Filtros',
    'services.bookNow': 'Reservar Agora',
    'services.price': 'Preço',
    'services.duration': 'Duração',
    'services.rating': 'Avaliação',
    'services.partner': 'Prestador de Serviços',
    'services.category': 'Categoria',

    // Booking
    'booking.title': 'Reservar Serviço',
    'booking.selectDate': 'Selecionar Data',
    'booking.selectTime': 'Selecionar Hora',
    'booking.specialRequirements': 'Requisitos Especiais',
    'booking.bookService': 'Reservar Serviço',
    'booking.bookingSummary': 'Resumo da Reserva',
    'booking.totalAmount': 'Valor Total',
    'booking.paymentMethod': 'Método de Pagamento',
    'booking.confirmBooking': 'Confirmar Reserva',
    'booking.bookingConfirmed': 'Reserva Confirmada',
    'booking.serviceDetails': 'Detalhes do Serviço',
    'booking.processing': 'A processar...',
    'booking.backToServices': 'Voltar aos Serviços',
    'booking.optional': 'Opcional',
    'booking.required': 'Obrigatório',

    // Dashboard
    'dashboard.welcome': 'Bem-vindo de volta',
    'dashboard.totalBookings': 'Total de Reservas',
    'dashboard.completed': 'Concluídas',
    'dashboard.averageRating': 'Avaliação Média',
    'dashboard.totalRevenue': 'Receita Total',
    'dashboard.recentBookings': 'Reservas Recentes',
    'dashboard.quickActions': 'Ações Rápidas',
    'dashboard.bookService': 'Reservar Serviço',
    'dashboard.viewProfile': 'Ver Perfil',
    'dashboard.noBookings': 'Nenhuma reserva recente encontrada',
    'dashboard.allTimeBookings': 'Reservas de sempre',
    'dashboard.successfullyCompleted': 'Concluídas com sucesso',
    'dashboard.outOf5Stars': 'De 5 estrelas',
    'dashboard.earnings': 'Ganhos',
    'dashboard.spent': 'Gasto',

    // Admin Dashboard
    'admin.dashboard': 'Painel de Administração',
    'admin.totalUsers': 'Total de Utilizadores',
    'admin.activePartners': 'Parceiros Ativos',
    'admin.totalBookings': 'Total de Reservas',
    'admin.totalRevenue': 'Receita Total',
    'admin.pendingBookings': 'Reservas Pendentes',
    'admin.completedBookings': 'Reservas Concluídas',
    'admin.averageRating': 'Avaliação Média',
    'admin.activeServices': 'Serviços Ativos',
    'admin.recentActivity': 'Atividade Recente',
    'admin.platformOverview': 'Visão Geral da Plataforma',
    'admin.userManagement': 'Gestão de Utilizadores',
    'admin.bookingManagement': 'Gestão de Reservas',
    'admin.revenueTracking': 'Acompanhamento de Receitas',
    'admin.platformAnalytics': 'Análise da Plataforma',
    'admin.exportData': 'Exportar Dados',
    'admin.settings': 'Configurações',
    'admin.administrator': 'Administrador',

    // Authentication
    'auth.login': 'Entrar',
    'auth.register': 'Registar',
    'auth.logout': 'Sair',
    'auth.email': 'Email',
    'auth.password': 'Palavra-passe',
    'auth.confirmPassword': 'Confirmar Palavra-passe',
    'auth.firstName': 'Nome',
    'auth.lastName': 'Apelido',
    'auth.phoneNumber': 'Número de Telefone',
    'auth.accountType': 'Tipo de Conta',
    'auth.preferredLanguage': 'Idioma Preferido',
    'auth.client': 'Cliente',
    'auth.partner': 'Prestador de Serviços',
    'auth.welcomeBack': 'Bem-vindo de volta',
    'auth.createAccount': 'Criar uma conta',
    'auth.enterCredentials': 'Digite seu email e palavra-passe para entrar',
    'auth.enterDetails': 'Digite seus dados para criar sua conta',
    'auth.signIn': 'Entrar',
    'auth.signUp': 'Registar',
    'auth.dontHaveAccount': 'Não tem uma conta?',
    'auth.alreadyHaveAccount': 'Já tem uma conta?',
    'auth.loginSuccessful': 'Login realizado com sucesso!',
    'auth.registrationSuccessful': 'Registo realizado com sucesso!',
    'auth.emailRequired': 'Email é obrigatório',
    'auth.emailInvalid': 'Email inválido',
    'auth.passwordRequired': 'Palavra-passe é obrigatória',
    'auth.passwordMinLength': 'Palavra-passe deve ter pelo menos 8 caracteres',
    'auth.firstNameRequired': 'Nome é obrigatório',
    'auth.lastNameRequired': 'Apelido é obrigatório',
    'auth.confirmPasswordRequired': 'Por favor confirme sua palavra-passe',
    'auth.passwordsDoNotMatch': 'As palavras-passe não coincidem',
    'auth.networkError': 'Erro de rede. Por favor tente novamente.',
    'auth.anErrorOccurred': 'Ocorreu um erro',

    // Common
    'common.loading': 'A carregar...',
    'common.error': 'Erro',
    'common.success': 'Sucesso',
    'common.cancel': 'Cancelar',
    'common.save': 'Guardar',
    'common.edit': 'Editar',
    'common.delete': 'Eliminar',
    'common.confirm': 'Confirmar',
    'common.back': 'Voltar',
    'common.next': 'Seguinte',
    'common.previous': 'Anterior',
    'common.search': 'Pesquisar',
    'common.filter': 'Filtrar',
    'common.sort': 'Ordenar',
    'common.view': 'Ver',
    'common.close': 'Fechar',
    'common.yes': 'Sim',
    'common.no': 'Não',
    'common.submit': 'Submeter',
    'common.reset': 'Repor',
    'common.clear': 'Limpar',
    'common.select': 'Selecionar',
    'common.choose': 'Escolher',
    'common.optional': 'Opcional',
    'common.required': 'Obrigatório',
    'common.and': 'e',
    'common.none': 'Nenhum',
    'common.today': 'Hoje',
    'common.yesterday': 'Ontem',
    'common.tomorrow': 'Amanhã',
    'common.thisWeek': 'Esta Semana',
    'common.lastWeek': 'Semana Passada',
    'common.thisMonth': 'Este Mês',
    'common.lastMonth': 'Mês Passado',
    'common.thisYear': 'Este Ano',
    'common.lastYear': 'Ano Passado',

    // Footer
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

    // Currency
    'currency.usd': 'Dólar Americano',
    'currency.eur': 'Euro',
    'currency.aoa': 'Kwanza Angolano',
    'currency.zar': 'Rand Sul-Africano',
    'currency.ngn': 'Naira Nigeriano',
    'currency.ghs': 'Cedi Ganês',
    'currency.kes': 'Xelim Queniano',
    'currency.select': 'Selecionar Moeda',
    'currency.convert': 'Converter Moeda',
  }
};

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguage] = useState<Language>('en');
  const [currency, setCurrency] = useState<Currency>('USD');

  // Detect device language and currency on mount
  useEffect(() => {
    const detectLanguageAndCurrency = () => {
      if (typeof window !== 'undefined') {
        // Detect language
        const browserLang = navigator.language.split('-')[0];
        const savedLang = localStorage.getItem('language') as Language;
        
        if (savedLang && (savedLang === 'en' || savedLang === 'pt')) {
          setLanguage(savedLang);
        } else if (browserLang === 'pt') {
          setLanguage('pt');
        } else {
          setLanguage('en');
        }

        // Detect currency based on country
        const savedCurrency = localStorage.getItem('currency') as Currency;
        if (savedCurrency && currencyRates[savedCurrency]) {
          setCurrency(savedCurrency);
        } else {
          // Try to detect country from browser
          const countryCode = Intl.DateTimeFormat().resolvedOptions().locale?.split('-')[1]?.toUpperCase();
          if (countryCode && countryCurrencyMap[countryCode]) {
            setCurrency(countryCurrencyMap[countryCode]);
          } else {
            setCurrency('USD'); // Default to USD
          }
        }
      }
    };

    detectLanguageAndCurrency();
  }, []);

  const handleLanguageChange = (newLang: Language) => {
    setLanguage(newLang);
    localStorage.setItem('language', newLang);
    
    // Update HTML lang attribute
    if (typeof document !== 'undefined') {
      document.documentElement.lang = newLang;
    }
  };

  const handleCurrencyChange = (newCurrency: Currency) => {
    setCurrency(newCurrency);
    localStorage.setItem('currency', newCurrency);
  };

  const t = (key: string): string => {
    return translations[language][key as keyof typeof translations[typeof language]] || key;
  };

  const formatCurrency = (amount: number): string => {
    const convertedAmount = convertCurrency(amount);
    const symbol = currencySymbols[currency];
    
    if (currency === 'USD' || currency === 'EUR') {
      return `${symbol}${convertedAmount.toFixed(2)}`;
    } else {
      return `${symbol} ${convertedAmount.toLocaleString()}`;
    }
  };

  const convertCurrency = (amount: number, fromCurrency: Currency = 'USD'): number => {
    if (fromCurrency === currency) {
      return amount;
    }
    
    // Convert from source currency to USD first
    const amountInUSD = amount / currencyRates[fromCurrency];
    
    // Convert from USD to target currency
    return amountInUSD * currencyRates[currency];
  };

  return (
    <LanguageContext.Provider value={{ 
      language, 
      setLanguage: handleLanguageChange, 
      currency, 
      setCurrency: handleCurrencyChange,
      t, 
      formatCurrency, 
      convertCurrency 
    }}>
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