"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useLanguage } from "@/contexts/language-context";
import { Search, Star, Clock, MapPin, User } from "lucide-react";

interface Service {
  id: string;
  name: string;
  description: string;
  price: number;
  duration: number;
  category: string;
  partner: {
    id: string;
    name: string;
    rating: number;
  };
}

export default function ServicesPage() {
  const [services, setServices] = useState<Service[]>([]);
  const [filteredServices, setFilteredServices] = useState<Service[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const { t, formatCurrency } = useLanguage();

  const categories = [
    { value: "", label: t('services.allCategories') },
    { value: "real_estate", label: t('services.realEstate') },
    { value: "transportation", label: t('services.transportation') },
    { value: "business", label: t('services.business') },
    { value: "legal", label: t('services.legal') },
    { value: "language", label: t('services.language') },
    { value: "documents", label: t('services.documents') },
    { value: "catering", label: t('services.catering') },
    { value: "protocol", label: t('services.protocol') },
  ];

  useEffect(() => {
    fetchServices();
  }, []);

  useEffect(() => {
    filterServices();
  }, [services, searchQuery, selectedCategory]);

  const fetchServices = async () => {
    try {
      const response = await fetch('/api/v1/services/');
      if (response.ok) {
        const data = await response.json();
        setServices(data.results || data);
      } else {
        // Mock data for demonstration
        setServices([
          {
            id: "1",
            name: "Real Estate Consultation",
            description: "Professional real estate advice and property management services",
            price: 150,
            duration: 90,
            category: "real_estate",
            partner: { id: "1", name: "Angola Properties Ltd", rating: 4.8 }
          },
          {
            id: "2",
            name: "Business Setup Consultation",
            description: "Complete business registration and setup assistance",
            price: 200,
            duration: 120,
            category: "business",
            partner: { id: "2", name: "Business Solutions Angola", rating: 4.9 }
          },
          {
            id: "3",
            name: "Legal Document Translation",
            description: "Professional translation of legal documents",
            price: 75,
            duration: 60,
            category: "language",
            partner: { id: "3", name: "Legal Translators Pro", rating: 4.7 }
          },
          {
            id: "4",
            name: "Corporate Transportation",
            description: "Reliable transportation for business meetings and events",
            price: 100,
            duration: 180,
            category: "transportation",
            partner: { id: "4", name: "Elite Transport Services", rating: 4.6 }
          }
        ]);
      }
    } catch (error) {
      console.error('Error fetching services:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const filterServices = () => {
    let filtered = services;

    if (searchQuery) {
      filtered = filtered.filter(service =>
        service.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        service.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (selectedCategory) {
      filtered = filtered.filter(service => service.category === selectedCategory);
    }

    setFilteredServices(filtered);
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            {t('services.title')}
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 max-w-3xl mx-auto">
            {t('services.subtitle')}
          </p>
        </div>
      </section>

      {/* Search and Filter Section */}
      <section className="py-8 bg-white border-b">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                type="text"
                placeholder={t('services.searchPlaceholder')}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {categories.map(category => (
                <option key={category.value} value={category.value}>
                  {category.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          {isLoading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">{t('common.loading')}</p>
            </div>
          ) : filteredServices.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600 text-lg">{t('services.noServicesFound')}</p>
              <Button 
                onClick={() => {
                  setSearchQuery("");
                  setSelectedCategory("");
                }}
                className="mt-4"
              >
                {t('services.clearFilters')}
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredServices.map((service) => (
                <Card key={service.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <CardTitle className="text-lg">{service.name}</CardTitle>
                    <CardDescription>{service.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <User className="h-4 w-4 mr-2 text-gray-500" />
                          <span className="text-sm font-medium">{service.partner.name}</span>
                        </div>
                        <div className="flex items-center">
                          <Star className="h-4 w-4 text-yellow-500 mr-1" />
                          <span className="text-sm">{service.partner.rating}</span>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm text-gray-600">
                        <div className="flex items-center">
                          <Clock className="h-4 w-4 mr-1" />
                          <span>{service.duration} min</span>
                        </div>
                        <div className="text-lg font-bold text-green-600">
                          {formatCurrency(service.price)}
                        </div>
                      </div>
                      
                      <Link href={`/booking?serviceId=${service.id}`}>
                        <Button className="w-full">
                          {t('services.bookNow')}
                        </Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
