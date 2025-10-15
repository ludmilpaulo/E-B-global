import { Users, MapPin, Star, Clock } from "lucide-react";

export function Stats() {
  const stats = [
    {
      icon: Users,
      value: "500+",
      label: "Verified Partners",
      description: "Professional service providers across Africa",
    },
    {
      icon: MapPin,
      value: "10+",
      label: "Countries",
      description: "Serving Lusophone and Anglophone Africa",
    },
    {
      icon: Star,
      value: "4.8",
      label: "Average Rating",
      description: "Based on customer reviews and feedback",
    },
    {
      icon: Clock,
      value: "90min",
      label: "Booking Slots",
      description: "Standardized 1.5-hour service windows",
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
