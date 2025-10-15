"use client";

import Link from "next/link";
import Image from "next/image";
import { Facebook, Twitter, Instagram, Linkedin, Mail, Phone, MapPin } from "lucide-react";
import { useLanguage } from "@/contexts/language-context";

export function Footer() {
  const currentYear = new Date().getFullYear();
  const { t } = useLanguage();

  const footerSections = {
    company: {
      title: t('footer.company'),
      links: [
        { name: t('footer.aboutUs'), href: "/about" },
        { name: t('footer.howItWorks'), href: "/how-it-works" },
        { name: t('footer.contact'), href: "/contact" },
      ],
    },
    services: {
      title: t('footer.services'),
      links: [
        { name: t('footer.realEstate'), href: "/services" },
        { name: t('footer.transportation'), href: "/services" },
        { name: t('footer.business'), href: "/services" },
        { name: t('footer.legal'), href: "/services" },
        { name: t('footer.language'), href: "/services" },
        { name: t('footer.documents'), href: "/services" },
      ],
    },
    support: {
      title: t('footer.support'),
      links: [
        { name: t('footer.helpCenter'), href: "/contact" },
        { name: t('footer.contactUs'), href: "/contact" },
        { name: t('footer.safety'), href: "/about" },
      ],
    },
  };

  const socialLinks = [
    { name: "Facebook", href: "#", icon: Facebook },
    { name: "Twitter", href: "#", icon: Twitter },
    { name: "Instagram", href: "#", icon: Instagram },
    { name: "LinkedIn", href: "#", icon: Linkedin },
  ];

  return (
    <footer className="bg-muted/50 border-t">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
          {/* Company Info */}
          <div className="lg:col-span-2">
            <Link href="/" className="flex items-center space-x-2 mb-4">
              <div className="relative h-8 w-8">
                <Image
                  src="/logo.png"
                  alt="E-B Global"
                  fill
                  className="object-contain"
                />
              </div>
              <span className="text-xl font-bold eb-gradient-text">E-B Global</span>
            </Link>
            <p className="text-sm text-muted-foreground mb-4 max-w-sm">
              {t('footer.description')}
            </p>
            
            {/* Contact Info */}
            <div className="space-y-2 text-sm text-muted-foreground">
              <div className="flex items-center space-x-2">
                <Mail className="h-4 w-4" />
                <span>info@ebglobal.com</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="h-4 w-4" />
                <span>+244 912 345 678</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="h-4 w-4" />
                <span>Luanda, Angola</span>
              </div>
            </div>
          </div>

          {/* Footer Links */}
          {Object.entries(footerSections).map(([key, section]) => (
            <div key={key}>
              <h3 className="text-sm font-semibold mb-4">{section.title}</h3>
              <ul className="space-y-2">
                {section.links.map((link) => (
                  <li key={link.name}>
                    <Link
                      href={link.href}
                      className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Footer */}
        <div className="border-t mt-8 pt-8 flex flex-col sm:flex-row justify-between items-center">
          <div className="text-sm text-muted-foreground mb-4 sm:mb-0">
            © {currentYear} E-B Global. {t('footer.rightsReserved')}
          </div>
          
          {/* Social Links */}
          <div className="flex items-center space-x-4">
            {socialLinks.map((social) => {
              const Icon = social.icon;
              return (
                <Link
                  key={social.name}
                  href={social.href}
                  className="text-muted-foreground hover:text-foreground transition-colors"
                  aria-label={social.name}
                >
                  <Icon className="h-5 w-5" />
                </Link>
              );
            })}
          </div>
        </div>

        {/* Tagline */}
        <div className="text-center mt-8 pt-8 border-t">
          <p className="text-sm text-muted-foreground italic">
            {t('footer.tagline')}
          </p>
        </div>
      </div>
    </footer>
  );
}
