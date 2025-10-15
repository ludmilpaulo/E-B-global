import { Hero } from "@/components/sections/hero";
import { ServiceCategories } from "@/components/sections/service-categories";
import { HowItWorks } from "@/components/sections/how-it-works";
import { FeaturedPartners } from "@/components/sections/featured-partners";
import { Testimonials } from "@/components/sections/testimonials";
import { Stats } from "@/components/sections/stats";
import { CTA } from "@/components/sections/cta";

export default function Home() {
  return (
    <>
      <Hero />
      <Stats />
      <ServiceCategories />
      <HowItWorks />
      <FeaturedPartners />
      <Testimonials />
      <CTA />
    </>
  );
}