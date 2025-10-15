"use client";

import { Users, MapPin, Star, Clock } from "lucide-react";
import { useLanguage } from "@/contexts/language-context";

export function Stats() {
  const { t } = useLanguage();
  
  const stats = [
    {
      icon: Users,
      value: "500+",
      label: t('stats.verifiedPartners'),
      description: t('stats.verifiedPartnersDesc'),
    },
    {
      icon: MapPin,
      value: "10+",
      label: t('stats.countries'),
      description: t('stats.countriesDesc'),
    },
    {
      icon: Star,
      value: "4.8",
      label: t('stats.averageRating'),
      description: t('stats.averageRatingDesc'),
    },
    {
      icon: Clock,
      value: "90min",
      label: t('stats.bookingSlots'),
      description: t('stats.bookingSlotsDesc'),
    },
  ];

  return (
    <section className="py-16 bg-muted/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div
                key={index}
                className="text-center group hover:scale-105 transition-transform duration-300"
              >
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary/10 rounded-full mb-4 group-hover:bg-primary/20 transition-colors">
                  <Icon className="h-8 w-8 text-primary" />
                </div>
                <div className="text-3xl font-bold text-foreground mb-2">
                  {stat.value}
                </div>
                <div className="text-lg font-semibold text-foreground mb-1">
                  {stat.label}
                </div>
                <div className="text-sm text-muted-foreground">
                  {stat.description}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
