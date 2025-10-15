"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { Menu, X, Globe, User, LogIn, Search, DollarSign } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useLanguage } from "@/contexts/language-context";

type Language = 'en' | 'pt';
type Currency = 'USD' | 'EUR' | 'AOA' | 'ZAR' | 'NGN' | 'GHS' | 'KES';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { language, setLanguage, currency, setCurrency, t } = useLanguage();

  const navigation = [
    { name: t('navigation.home'), href: "/" },
    { name: t('navigation.services'), href: "/services" },
    { name: t('navigation.howItWorks'), href: "/how-it-works" },
    { name: t('navigation.about'), href: "/about" },
    { name: t('navigation.contact'), href: "/contact" },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="relative h-8 w-8">
              <Image
                src="/logo.png"
                alt="E-B Global"
                fill
                className="object-contain"
                priority
              />
            </div>
            <span className="text-xl font-bold eb-gradient-text">E-B Global</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                {item.name}
              </Link>
            ))}
          </nav>

              {/* Right side actions */}
              <div className="flex items-center space-x-4">
                {/* Currency Selector */}
                <div className="hidden sm:flex items-center space-x-2">
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                  <select
                    value={currency}
                    onChange={(e) => setCurrency(e.target.value as Currency)}
                    className="bg-transparent text-sm border-none outline-none cursor-pointer"
                  >
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                    <option value="AOA">AOA</option>
                    <option value="ZAR">ZAR</option>
                    <option value="NGN">NGN</option>
                    <option value="GHS">GHS</option>
                    <option value="KES">KES</option>
                  </select>
                </div>

                {/* Language Selector */}
                <div className="hidden sm:flex items-center space-x-2">
                  <Globe className="h-4 w-4 text-muted-foreground" />
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value as Language)}
                    className="bg-transparent text-sm border-none outline-none cursor-pointer"
                  >
                    <option value="en">EN</option>
                    <option value="pt">PT</option>
                  </select>
                </div>

            {/* Search Button */}
            <Button variant="ghost" size="icon" className="hidden sm:flex">
              <Search className="h-4 w-4" />
            </Button>

            {/* Auth Buttons */}
            <div className="hidden sm:flex items-center space-x-2">
              <Link href="/auth/login">
                <Button variant="ghost" size="sm">
                  <LogIn className="h-4 w-4 mr-2" />
                  {t('navigation.login')}
                </Button>
              </Link>
              <Link href="/auth/register">
                <Button size="sm">
                  <User className="h-4 w-4 mr-2" />
                  {t('navigation.signUp')}
                </Button>
              </Link>
            </div>

            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden border-t">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="block px-3 py-2 text-base font-medium text-muted-foreground hover:text-foreground hover:bg-accent rounded-md transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
              
              {/* Mobile Auth Buttons */}
              <div className="pt-4 space-y-2">
                <Link href="/auth/login" className="w-full">
                  <Button variant="ghost" className="w-full justify-start">
                    <LogIn className="h-4 w-4 mr-2" />
                    {t('navigation.login')}
                  </Button>
                </Link>
                <Link href="/auth/register" className="w-full">
                  <Button className="w-full justify-start">
                    <User className="h-4 w-4 mr-2" />
                    {t('navigation.signUp')}
                  </Button>
                </Link>
              </div>

                  {/* Mobile Currency and Language Selectors */}
                  <div className="space-y-2 pt-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">{t('currency.select')}</span>
                      <select
                        value={currency}
                        onChange={(e) => setCurrency(e.target.value as Currency)}
                        className="bg-transparent text-sm border-none outline-none cursor-pointer"
                      >
                        <option value="USD">USD</option>
                        <option value="EUR">EUR</option>
                        <option value="AOA">AOA</option>
                        <option value="ZAR">ZAR</option>
                        <option value="NGN">NGN</option>
                        <option value="GHS">GHS</option>
                        <option value="KES">KES</option>
                      </select>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">{t('navigation.language')}</span>
                      <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value as Language)}
                        className="bg-transparent text-sm border-none outline-none cursor-pointer"
                      >
                        <option value="en">English</option>
                        <option value="pt">Português</option>
                      </select>
                    </div>
                  </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
