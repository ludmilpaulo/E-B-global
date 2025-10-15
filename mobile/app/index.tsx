import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Image } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function HomeScreen() {
  const categories = [
    {
      id: 'imobiliaria',
      name: 'Real Estate',
      namePt: 'Imobiliária',
      icon: 'business-outline',
      color: '#3B82F6',
    },
    {
      id: 'transportes',
      name: 'Transportation',
      namePt: 'Transportes',
      icon: 'car-outline',
      color: '#10B981',
    },
    {
      id: 'negocios',
      name: 'Business',
      namePt: 'Negócios',
      icon: 'briefcase-outline',
      color: '#8B5CF6',
    },
    {
      id: 'juridica',
      name: 'Legal',
      namePt: 'Jurídica',
      icon: 'scale-outline',
      color: '#EF4444',
    },
    {
      id: 'linguistica',
      name: 'Language',
      namePt: 'Linguística',
      icon: 'language-outline',
      color: '#F59E0B',
    },
    {
      id: 'documentos',
      name: 'Documents',
      namePt: 'Documentos',
      icon: 'document-text-outline',
      color: '#6366F1',
    },
    {
      id: 'catering',
      name: 'Catering',
      namePt: 'Catering',
      icon: 'restaurant-outline',
      color: '#F97316',
    },
    {
      id: 'protocolo',
      name: 'Protocol',
      namePt: 'Protocolo',
      icon: 'ribbon-outline',
      color: '#EC4899',
    },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.headerContent}>
            <Image 
              source={require('../assets/icon.png')} 
              style={styles.logo}
              resizeMode="contain"
            />
            <Text style={styles.headerTitle}>E-B Global</Text>
          </View>
          <Text style={styles.headerSubtitle}>
            Professional Services Across Africa
          </Text>
        </View>

        {/* Quick Actions */}
        <View style={styles.quickActions}>
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={() => router.push('/services')}
          >
            <Ionicons name="search-outline" size={24} color="#1E40AF" />
            <Text style={styles.actionButtonText}>Find Services</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={() => router.push('/bookings')}
          >
            <Ionicons name="calendar-outline" size={24} color="#1E40AF" />
            <Text style={styles.actionButtonText}>My Bookings</Text>
          </TouchableOpacity>
        </View>

        {/* Service Categories */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Service Categories</Text>
          <View style={styles.categoriesGrid}>
            {categories.map((category) => (
              <TouchableOpacity
                key={category.id}
                style={styles.categoryCard}
                onPress={() => router.push(`/services?category=${category.id}`)}
              >
                <View style={[styles.categoryIcon, { backgroundColor: category.color }]}>
                  <Ionicons name={category.icon as any} size={24} color="white" />
                </View>
                <Text style={styles.categoryName}>{category.name}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Featured Services */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Featured Services</Text>
          <View style={styles.featuredCard}>
            <Text style={styles.featuredTitle}>Need Help Finding the Right Service?</Text>
            <Text style={styles.featuredDescription}>
              Our verified partners are ready to help with professional services across Africa.
            </Text>
            <TouchableOpacity 
              style={styles.featuredButton}
              onPress={() => router.push('/services')}
            >
              <Text style={styles.featuredButtonText}>Explore All Services</Text>
              <Ionicons name="arrow-forward" size={16} color="white" />
            </TouchableOpacity>
          </View>
        </View>

        {/* How It Works */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>How It Works</Text>
          <View style={styles.stepsContainer}>
            <View style={styles.step}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>1</Text>
              </View>
              <Text style={styles.stepText}>Search & Select</Text>
            </View>
            <View style={styles.step}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>2</Text>
              </View>
              <Text style={styles.stepText}>Book 90-min Slot</Text>
            </View>
            <View style={styles.step}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepNumberText}>3</Text>
              </View>
              <Text style={styles.stepText}>Get Service</Text>
            </View>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8FAFC',
  },
  scrollView: {
    flex: 1,
  },
  header: {
    backgroundColor: '#1E40AF',
    padding: 20,
    paddingTop: 10,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  logo: {
    width: 32,
    height: 32,
    marginRight: 12,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#93C5FD',
    marginLeft: 44,
  },
  quickActions: {
    flexDirection: 'row',
    padding: 20,
    gap: 12,
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    gap: 8,
  },
  actionButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1E40AF',
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 16,
  },
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  categoryCard: {
    width: '47%',
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  categoryIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  categoryName: {
    fontSize: 12,
    fontWeight: '600',
    color: '#374151',
    textAlign: 'center',
  },
  featuredCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  featuredTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 8,
  },
  featuredDescription: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 16,
    lineHeight: 20,
  },
  featuredButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#1E40AF',
    padding: 12,
    borderRadius: 8,
    gap: 8,
  },
  featuredButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: 'white',
  },
  stepsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  step: {
    alignItems: 'center',
    flex: 1,
  },
  stepNumber: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#1E40AF',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  stepNumberText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: 'white',
  },
  stepText: {
    fontSize: 12,
    color: '#6B7280',
    textAlign: 'center',
  },
});
