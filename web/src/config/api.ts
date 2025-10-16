export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export function getApiUrl(endpoint: string): string {
  // Remove leading slash if present to avoid double slashes
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  return `${API_BASE_URL}/${cleanEndpoint}`;
}

export const API_ENDPOINTS = {
  // Authentication
  LOGIN: 'auth/login/',
  REGISTER: 'auth/register/',
  LOGOUT: 'auth/logout/',
  REFRESH_TOKEN: 'auth/token/refresh/',
  
  // User Management
  PROFILE: 'auth/profile/',
  PREFERENCES: 'auth/preferences/',
  
  // Services
  SERVICES: 'services/',
  CATEGORIES: 'services/categories/',
  
  // Bookings
  BOOKINGS: 'bookings/',
  
  // Internationalization
  I18N: (lang: string) => `i18n/${lang}/`,
} as const;