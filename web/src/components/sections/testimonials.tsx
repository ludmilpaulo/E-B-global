import { Card, CardContent } from "@/components/ui/card";
import { Star, Quote } from "lucide-react";

export function Testimonials() {
  const testimonials = [
    {
      name: "João Silva",
      location: "Luanda, Angola",
      service: "Real Estate Consulting",
      rating: 5,
      text: "E-B Global connected me with an excellent real estate consultant who helped me find the perfect property. The 90-minute booking system is very convenient and professional.",
      textPt: "O E-B Global conectou-me com um excelente consultor imobiliário que me ajudou a encontrar a propriedade perfeita. O sistema de reservas de 90 minutos é muito conveniente e profissional.",
    },
    {
      name: "Sarah Johnson",
      location: "Cape Town, South Africa",
      service: "Language Services",
      rating: 5,
      text: "I needed urgent translation services for a business document. The platform made it easy to find a qualified translator and book a same-day appointment.",
      textPt: "Precisava de serviços urgentes de tradução para um documento de negócios. A plataforma facilitou encontrar um tradutor qualificado e agendar uma consulta no mesmo dia.",
    },
    {
      name: "Carlos Mendes",
      location: "Maputo, Mozambique",
      service: "Transportation",
      rating: 5,
      text: "The transportation service was reliable and punctual. The driver was professional and the booking process was seamless through the E-B Global platform.",
      textPt: "O serviço de transporte foi confiável e pontual. O motorista foi profissional e o processo de reserva foi perfeito através da plataforma E-B Global.",
    },
  ];

  return (
    <section className="py-16 bg-muted/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
            What Our Clients Say
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Don't just take our word for it. Here's what our satisfied clients 
            have to say about their E-B Global experience.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="relative">
              <CardContent className="pt-6">
                <div className="absolute top-4 right-4">
                  <Quote className="h-8 w-8 text-primary/20" />
                </div>
                
                <div className="mb-4">
                  <div className="flex items-center space-x-1 mb-2">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>
                  <p className="text-sm text-muted-foreground">{testimonial.service}</p>
                </div>

                <blockquote className="text-foreground mb-4 italic">
                  "{testimonial.text}"
                </blockquote>

                <div className="border-t pt-4">
                  <div className="font-semibold">{testimonial.name}</div>
                  <div className="text-sm text-muted-foreground">{testimonial.location}</div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
