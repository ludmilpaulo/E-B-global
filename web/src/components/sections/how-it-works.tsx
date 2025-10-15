import { Search, Calendar, CreditCard, CheckCircle } from "lucide-react";

export function HowItWorks() {
  const steps = [
    {
      icon: Search,
      title: "1. Discover Services",
      description: "Browse our comprehensive catalog of professional services across Africa. Filter by category, location, and availability.",
    },
    {
      icon: Calendar,
      title: "2. Book Your Slot",
      description: "Select your preferred 90-minute time slot and provide any special requirements. All bookings are standardized for efficiency.",
    },
    {
      icon: CreditCard,
      title: "3. Secure Payment",
      description: "Complete your booking with secure, local payment methods. Support for multiple currencies and payment gateways.",
    },
    {
      icon: CheckCircle,
      title: "4. Get Service",
      description: "Receive professional service from verified partners. Track progress and communicate through our platform.",
    },
  ];

  return (
    <section className="py-16 bg-muted/30">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
            How E-B Global Works
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Our streamlined process makes it easy to find, book, and receive 
            professional services across Africa in just four simple steps.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div key={index} className="text-center">
                <div className="relative mb-6">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-4">
                    <Icon className="h-8 w-8 text-primary-foreground" />
                  </div>
                  {index < steps.length - 1 && (
                    <div className="hidden lg:block absolute top-8 left-full w-full h-0.5 bg-border transform translate-x-4" />
                  )}
                </div>
                <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
                <p className="text-muted-foreground">{step.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
