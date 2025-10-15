import { Stats } from "@/components/sections/stats";
import { Testimonials } from "@/components/sections/testimonials";

export const metadata = {
  title: "About Us - E-B Global",
  description: "Learn about E-B Global and our mission to connect Africa through professional services",
};

export default function AboutPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            About E-B Global
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 max-w-3xl mx-auto">
            Connecting Africa through professional services
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Our Mission
              </h2>
              <p className="text-lg text-gray-600 leading-relaxed">
                E-B Global is dedicated to bridging the gap between service providers and clients across Lusophone and Anglophone Africa. We believe in the power of professional connections to drive economic growth and development across the continent.
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  What We Do
                </h3>
                <ul className="space-y-3 text-gray-600">
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    Connect verified service providers with clients across Africa
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    Facilitate seamless booking and payment processes
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    Provide multilingual support in English and Portuguese
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    Ensure quality through our verification process
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  Our Values
                </h3>
                <ul className="space-y-3 text-gray-600">
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    Trust and transparency in all our interactions
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    Quality service delivery and customer satisfaction
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    Innovation in connecting people and services
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    Commitment to African economic development
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <Stats />

      {/* Testimonials */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              What Our Users Say
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Hear from our satisfied clients and service providers
            </p>
          </div>
          <Testimonials />
        </div>
      </section>

      {/* Team Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Our Team
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Dedicated professionals working to connect Africa
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="bg-blue-100 w-24 h-24 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-2xl font-bold text-blue-600">CEO</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Leadership Team</h3>
              <p className="text-gray-600">
                Experienced professionals with deep knowledge of African markets
              </p>
            </div>
            <div className="text-center">
              <div className="bg-blue-100 w-24 h-24 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-2xl font-bold text-blue-600">DEV</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Development Team</h3>
              <p className="text-gray-600">
                Skilled developers building innovative solutions for Africa
              </p>
            </div>
            <div className="text-center">
              <div className="bg-blue-100 w-24 h-24 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-2xl font-bold text-blue-600">SUP</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Support Team</h3>
              <p className="text-gray-600">
                Multilingual support specialists ready to help you succeed
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
