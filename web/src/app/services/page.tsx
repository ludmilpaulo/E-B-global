import { ServiceCategories } from "@/components/sections/service-categories";
import { FeaturedPartners } from "@/components/sections/featured-partners";
import { Stats } from "@/components/sections/stats";

export const metadata = {
  title: "Services - E-B Global",
  description: "Discover professional services across Lusophone and Anglophone Africa",
};

export default function ServicesPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Our Services
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 max-w-3xl mx-auto">
            Professional services across Lusophone and Anglophone Africa
          </p>
        </div>
      </section>

      {/* Service Categories */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Service Categories
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Explore our comprehensive range of professional services
            </p>
          </div>
          <ServiceCategories />
        </div>
      </section>

      {/* Stats */}
      <Stats />

      {/* Featured Partners */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Featured Partners
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Trusted professionals ready to serve you
            </p>
          </div>
          <FeaturedPartners />
        </div>
      </section>
    </div>
  );
}
