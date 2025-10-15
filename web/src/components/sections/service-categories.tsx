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

export function ServiceCategories() {
  const categories = [
    {
      icon: Building2,
      title: "Real Estate Consulting",
      titlePt: "Consultoria Imobiliária",
      description: "Professional real estate services, property management, and investment consulting.",
      descriptionPt: "Serviços imobiliários profissionais, gestão de propriedades e consultoria de investimentos.",
      href: "/services/imobiliaria",
      color: "bg-blue-500",
    },
    {
      icon: Car,
      title: "Transportation Services",
      titlePt: "Serviços de Transporte",
      description: "Reliable transportation, vehicle rentals, and logistics solutions.",
      descriptionPt: "Transporte confiável, aluguer de viaturas e soluções logísticas.",
      href: "/services/transportes",
      color: "bg-green-500",
    },
    {
      icon: Briefcase,
      title: "Business Consulting",
      titlePt: "Consultoria de Negócios",
      description: "Strategic business advice, market analysis, and growth planning.",
      descriptionPt: "Conselhos estratégicos de negócios, análise de mercado e planeamento de crescimento.",
      href: "/services/negocios",
      color: "bg-purple-500",
    },
    {
      icon: Scale,
      title: "Legal Services",
      titlePt: "Serviços Jurídicos",
      description: "Legal consultation, document review, and compliance services.",
      descriptionPt: "Consultoria jurídica, revisão de documentos e serviços de conformidade.",
      href: "/services/juridica",
      color: "bg-red-500",
    },
    {
      icon: Languages,
      title: "Language Services",
      titlePt: "Serviços Linguísticos",
      description: "Translation, interpretation, language tutoring, and localization.",
      descriptionPt: "Tradução, interpretação, ensino de línguas e localização.",
      href: "/services/linguistica",
      color: "bg-yellow-500",
    },
    {
      icon: FileText,
      title: "Document Recognition",
      titlePt: "Reconhecimento de Documentos",
      description: "Notary services, embassy documentation, and official certifications.",
      descriptionPt: "Serviços notariais, documentação de embaixadas e certificações oficiais.",
      href: "/services/documentos",
      color: "bg-indigo-500",
    },
    {
      icon: Utensils,
      title: "Corporate Catering",
      titlePt: "Catering Corporativo",
      description: "Professional catering services for corporate events and meetings.",
      descriptionPt: "Serviços de catering profissionais para eventos corporativos e reuniões.",
      href: "/services/catering",
      color: "bg-orange-500",
    },
    {
      icon: Award,
      title: "Protocol Services",
      titlePt: "Serviços de Protocolo",
      description: "Event planning, diplomatic services, and ceremonial arrangements.",
      descriptionPt: "Planeamento de eventos, serviços diplomáticos e arranjos cerimoniais.",
      href: "/services/protocolo",
      color: "bg-pink-500",
    },
  ];

  return (
    <section className="py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
            Our Service Categories
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Comprehensive professional services across eight specialized categories, 
            designed to meet all your business and personal needs in Africa.
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
                      <span className="text-sm">Explore Services</span>
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
            Don't see what you're looking for?
          </p>
          <Link 
            href="/services" 
            className="inline-flex items-center text-primary hover:text-primary/80 font-medium transition-colors"
          >
            Browse All Services
            <ArrowRight className="h-4 w-4 ml-2" />
          </Link>
        </div>
      </div>
    </section>
  );
}
