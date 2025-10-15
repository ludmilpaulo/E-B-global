import { useEffect } from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import * as SplashScreen from 'expo-splash-screen';
import { Provider } from 'react-redux';
import { store } from '../store';
import '../styles/global.css';

// Keep the splash screen visible while we fetch resources
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  useEffect(() => {
    // Prepare resources here (fonts, API data, etc.)
    const prepare = async () => {
      try {
        // Pre-load fonts, make any API calls you need to do here
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate loading
      } catch (e) {
        console.warn(e);
      } finally {
        // Tell the application to render
        await SplashScreen.hideAsync();
      }
    };

    prepare();
  }, []);

  return (
    <Provider store={store}>
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: '#1e40af',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="index" 
          options={{ 
            title: 'E-B Global',
            headerShown: false 
          }} 
        />
        <Stack.Screen 
          name="auth/login" 
          options={{ 
            title: 'Login',
            presentation: 'modal'
          }} 
        />
        <Stack.Screen 
          name="auth/register" 
          options={{ 
            title: 'Register',
            presentation: 'modal'
          }} 
        />
        <Stack.Screen 
          name="services/index" 
          options={{ 
            title: 'Services'
          }} 
        />
        <Stack.Screen 
          name="services/[id]" 
          options={{ 
            title: 'Service Details'
          }} 
        />
        <Stack.Screen 
          name="bookings/index" 
          options={{ 
            title: 'My Bookings'
          }} 
        />
        <Stack.Screen 
          name="profile/index" 
          options={{ 
            title: 'Profile'
          }} 
        />
      </Stack>
      <StatusBar style="light" />
    </Provider>
  );
}
