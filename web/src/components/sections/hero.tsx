"use client";

import { useState } from "react";
import { Search, MapPin, Calendar, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useLanguage } from "@/contexts/language-context";

export function Hero() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedLocation, setSelectedLocation] = useState("");
  const { t } = useLanguage();

  const categories = [
    "All Services",
    "Real Estate Consulting",
    "Transportation",
    "Business Consulting",
    "Legal Services",
    "Language Services",
    "Document Recognition",
    "Corporate Catering",
    "Protocol Services",
  ];

  const locations = [
    "All Locations",
    "Angola",
    "Mozambique",
    "Cape Verde",
    "Guinea-Bissau",
    "São Tomé and Príncipe",
    "South Africa",
    "Nigeria",
    "Ghana",
    "Kenya",
  ];

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background with gradient overlay */}
      <div className="absolute inset-0 eb-gradient opacity-90" />
      <div className="absolute inset-0 bg-[url('/hero-pattern.svg')] bg-cover bg-center opacity-10" />
      
      {/* Content */}
      <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="max-w-4xl mx-auto">
          {/* Main heading */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 fade-in">
            {t('hero.title')}
            <span className="block text-cyan-200">{t('hero.subtitle')}</span>
          </h1>
          
          {/* Subheading */}
          <p className="text-xl sm:text-2xl text-slate-100 mb-8 max-w-2xl mx-auto fade-in">
            {t('hero.description')}
          </p>

          {/* Search Section */}
          <Card className="max-w-4xl mx-auto mb-8 fade-in">
            <CardContent className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Search Input */}
                <div className="md:col-span-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                    <input
                      type="text"
                      placeholder="What service do you need?"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                    />
                  </div>
                </div>

                {/* Category Selector */}
                <div className="md:col-span-1">
                  <div className="relative">
                    <Users className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                    <select
                      value={selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                      className="w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-white"
                    >
                      {categories.map((category) => (
                        <option key={category} value={category}>
                          {category}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Location Selector */}
                <div className="md:col-span-1">
                  <div className="relative">
                    <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                    <select
                      value={selectedLocation}
                      onChange={(e) => setSelectedLocation(e.target.value)}
                      className="w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-white"
                    >
                      {locations.map((location) => (
                        <option key={location} value={location}>
                          {location}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Search Button */}
                <div className="md:col-span-1">
                  <Button 
                    size="lg" 
                    className="w-full h-full text-lg font-semibold"
                    onClick={() => {
                      // Handle search logic
                      console.log({ searchQuery, selectedCategory, selectedLocation });
                    }}
                  >
                    <Search className="h-5 w-5 mr-2" />
                    Search
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-2xl mx-auto">
            <div className="text-center fade-in">
              <div className="text-3xl font-bold text-white">500+</div>
              <div className="text-slate-200">Verified Partners</div>
            </div>
            <div className="text-center fade-in">
              <div className="text-3xl font-bold text-white">8</div>
              <div className="text-slate-200">Service Categories</div>
            </div>
            <div className="text-center fade-in">
              <div className="text-3xl font-bold text-white">10+</div>
              <div className="text-slate-200">African Countries</div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-white rounded-full flex justify-center">
          <div className="w-1 h-3 bg-white rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </section>
  );
}
