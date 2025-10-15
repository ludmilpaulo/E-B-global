import { Button } from "@/components/ui/button";
import { ArrowRight, User, Briefcase } from "lucide-react";

export function CTA() {
  return (
    <section className="py-16 bg-primary">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-primary-foreground mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-primary-foreground/90 mb-8">
            Join thousands of satisfied clients and professional partners 
            who trust E-B Global for their service needs across Africa.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              variant="secondary"
              className="text-primary hover:text-primary-foreground"
            >
              <User className="h-5 w-5 mr-2" />
              Find Services
              <ArrowRight className="h-5 w-5 ml-2" />
            </Button>
            
            <Button 
              size="lg" 
              variant="outline"
              className="border-primary-foreground text-primary-foreground hover:bg-primary-foreground hover:text-primary"
            >
              <Briefcase className="h-5 w-5 mr-2" />
              Become a Partner
              <ArrowRight className="h-5 w-5 ml-2" />
            </Button>
          </div>

          <div className="mt-8 text-primary-foreground/80">
            <p className="text-sm">
              Already have an account?{" "}
              <a href="/login" className="underline hover:text-primary-foreground">
                Sign in here
              </a>
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
