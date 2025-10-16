"use client";

import Link from "next/link";
import { 
  Building2, 
  Car, 
  Briefcase, 
  Scale, 
  Languages, 
  FileText, 
  Utensils, 
  Award,
  ArrowRight 
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useLanguage } from "@/contexts/language-context";

export function ServiceCategories() {
  const { t } = useLanguage();
  
  const categories = [
    {
      icon: Building2,
      title: t('services.realEstate'),
      description: t('services.realEstateDesc'),
      href: "/services",
      color: "bg-blue-500",
    },
    {
      icon: Car,
      title: t('services.transportation'),
      description: t('services.transportationDesc'),
      href: "/services",
      color: "bg-green-500",
    },
    {
      icon: Briefcase,
      title: t('services.business'),
      description: t('services.businessDesc'),
      href: "/services",
      color: "bg-purple-500",
    },
    {
      icon: Scale,
      title: t('services.legal'),
      description: t('services.legalDesc'),
      href: "/services",
      color: "bg-red-500",
    },
    {
      icon: Languages,
      title: t('services.language'),
      description: t('services.languageDesc'),
      href: "/services",
      color: "bg-yellow-500",
    },
    {
      icon: FileText,
      title: t('services.documents'),
      description: t('services.documentsDesc'),
      href: "/services",
      color: "bg-indigo-500",
    },
    {
      icon: Utensils,
      title: t('services.catering'),
      description: t('services.cateringDesc'),
      href: "/services",
      color: "bg-orange-500",
    },
    {
      icon: Award,
      title: t('services.protocol'),
      description: t('services.protocolDesc'),
      href: "/services",
      color: "bg-pink-500",
    },
  ];

  return (
    <section className="py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
            {t('services.categoriesTitle')}
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            {t('services.categoriesDescription')}
          </p>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {categories.map((category, index) => {
            const Icon = category.icon;
            return (
              <Link key={index} href={category.href}>
                <Card className="group hover:shadow-lg transition-all duration-300 hover:-translate-y-1 h-full">
                  <CardHeader className="pb-4">
                    <div className={`inline-flex items-center justify-center w-12 h-12 ${category.color} rounded-lg mb-4 group-hover:scale-110 transition-transform`}>
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <CardTitle className="text-lg font-semibold group-hover:text-primary transition-colors">
                      {category.title}
                    </CardTitle>
                    <CardDescription className="text-sm text-muted-foreground">
                      {category.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="flex items-center text-primary font-medium group-hover:translate-x-1 transition-transform">
                      <span className="text-sm">{t('services.exploreServices')}</span>
                      <ArrowRight className="h-4 w-4 ml-2" />
                    </div>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>

        {/* Call to Action */}
        <div className="text-center mt-12">
          <p className="text-muted-foreground mb-4">
            {t('services.notFound')}
          </p>
          <Link 
            href="/services" 
            className="inline-flex items-center text-primary hover:text-primary/80 font-medium transition-colors"
          >
            {t('services.browseAll')}
            <ArrowRight className="h-4 w-4 ml-2" />
          </Link>
        </div>
      </div>
    </section>
  );
}
