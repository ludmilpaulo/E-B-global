// API Configuration for Mobile App
const isProduction = __DEV__ === false;

export const API_CONFIG = {
  // Production API URL
  PRODUCTION_URL: 'https://www.e-b-global.online',
  
  // Development API URL
  DEVELOPMENT_URL: 'http://localhost:8000',
  
  // Current API URL based on environment
  BASE_URL: isProduction ? 'https://www.e-b-global.online' : 'http://localhost:8000',
  
  // API endpoints
  ENDPOINTS: {
    AUTH: {
      LOGIN: '/api/v1/auth/login/',
      REGISTER: '/api/v1/auth/register/',
      REFRESH: '/api/v1/auth/refresh/',
      FORGOT_PASSWORD: '/api/v1/auth/forgot-password/',
      RESET_PASSWORD: '/api/v1/auth/reset-password/',
      USER_PROFILE: '/api/v1/auth/users/me/',
    },
    SERVICES: {
      LIST: '/api/v1/services/',
      DETAIL: (id: string) => `/api/v1/services/${id}/`,
      CATEGORIES: '/api/v1/services/categories/',
    },
    BOOKINGS: {
      LIST: '/api/v1/bookings/',
      CREATE: '/api/v1/bookings/',
      DETAIL: (id: string) => `/api/v1/bookings/${id}/`,
      UPDATE: (id: string) => `/api/v1/bookings/${id}/`,
      CANCEL: (id: string) => `/api/v1/bookings/${id}/cancel/`,
    },
    PAYMENTS: {
      CREATE: '/api/v1/payments/',
      VERIFY: '/api/v1/payments/verify/',
      HISTORY: '/api/v1/payments/history/',
    },
    ANALYTICS: {
      DASHBOARD: '/api/v1/analytics/dashboard/',
      BOOKINGS: '/api/v1/analytics/bookings/',
      REVENUE: '/api/v1/analytics/revenue/',
    },
  },
  
  // Request timeout (in milliseconds)
  TIMEOUT: 30000,
  
  // Retry configuration
  RETRY: {
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000,
  },
};

// Helper function to get full API URL
export const getApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

// Helper function to check if API is available
export const checkApiHealth = async (): Promise<boolean> => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);
    
    const response = await fetch(`${API_CONFIG.BASE_URL}/api/v1/health/`, {
      method: 'GET',
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);
    return response.ok;
  } catch (error) {
    console.error('API health check failed:', error);
    return false;
  }
};

export default API_CONFIG;
