import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Star, MapPin, Calendar } from "lucide-react";

export function FeaturedPartners() {
  const partners = [
    {
      name: "Maria Santos",
      business: "Santos Legal Services",
      category: "Legal Services",
      location: "Luanda, Angola",
      rating: 4.9,
      reviews: 127,
      availability: "Available Today",
      image: "/partners/maria-santos.jpg",
    },
    {
      name: "Ahmed Hassan",
      business: "Hassan Transportation",
      category: "Transportation",
      location: "Lagos, Nigeria",
      rating: 4.8,
      reviews: 89,
      availability: "Available Tomorrow",
      image: "/partners/ahmed-hassan.jpg",
    },
    {
      name: "Fatima Almeida",
      business: "Almeida Real Estate",
      category: "Real Estate",
      location: "Maputo, Mozambique",
      rating: 4.9,
      reviews: 156,
      availability: "Available Today",
      image: "/partners/fatima-almeida.jpg",
    },
  ];

  return (
    <section className="py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
            Featured Partners
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Meet some of our top-rated professional service providers across Africa. 
            All partners are verified and committed to delivering excellence.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {partners.map((partner, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                    <span className="text-lg font-semibold text-primary">
                      {partner.name.split(' ').map(n => n[0]).join('')}
                    </span>
                  </div>
                  <div>
                    <CardTitle className="text-lg">{partner.name}</CardTitle>
                    <p className="text-sm text-muted-foreground">{partner.business}</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <MapPin className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">{partner.location}</span>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Star className="h-4 w-4 text-yellow-500" />
                    <span className="text-sm font-medium">{partner.rating}</span>
                    <span className="text-sm text-muted-foreground">({partner.reviews} reviews)</span>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Calendar className="h-4 w-4 text-green-500" />
                    <span className="text-sm text-green-600 font-medium">{partner.availability}</span>
                  </div>

                  <div className="pt-2">
                    <span className="inline-block px-3 py-1 bg-primary/10 text-primary text-xs font-medium rounded-full">
                      {partner.category}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
