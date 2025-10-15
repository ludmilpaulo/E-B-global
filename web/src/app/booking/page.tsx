"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ProtectedRoute } from "@/components/auth/protected-route";
import { useToast } from "@/hooks/use-toast";
import { Calendar, Clock, User, CreditCard, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useLanguage } from "@/contexts/language-context";

interface Service {
  id: string;
  name: string;
  description: string;
  price: number;
  duration: number;
  category: string;
  partner: {
    id: string;
    name: string;
    rating: number;
  };
}

function BookingContent() {
  const [service, setService] = useState<Service | null>(null);
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedTime, setSelectedTime] = useState("");
  const [specialRequirements, setSpecialRequirements] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingService, setIsLoadingService] = useState(true);
  
  const router = useRouter();
  const searchParams = useSearchParams();
  const { toast } = useToast();
  const { t, formatCurrency } = useLanguage();
  
  const serviceId = searchParams.get('serviceId');

  useEffect(() => {
    if (serviceId) {
      fetchService();
    } else {
      router.push('/services');
    }
  }, [serviceId]);

  const fetchService = async () => {
    try {
      const response = await fetch(`/api/v1/services/${serviceId}/`);
      if (response.ok) {
        const data = await response.json();
        setService(data);
      } else {
        toast({
          title: t('common.error'),
          description: t('services.noServicesFound'),
          variant: "destructive",
        });
        router.push('/services');
      }
    } catch (error) {
      toast({
        title: t('common.error'),
        description: t('auth.networkError'),
        variant: "destructive",
      });
    } finally {
      setIsLoadingService(false);
    }
  };

  const handleBooking = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedDate || !selectedTime) {
      toast({
        title: t('common.error'),
        description: t('booking.selectDate') + ' ' + t('common.and') + ' ' + t('booking.selectTime'),
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/v1/bookings/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          service: serviceId,
          scheduled_date: selectedDate,
          scheduled_time: selectedTime,
          special_requirements: specialRequirements,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        toast({
          title: t('common.success'),
          description: t('booking.bookingConfirmed'),
        });
        router.push('/dashboard');
      } else {
        const error = await response.json();
        toast({
          title: t('common.error'),
          description: error.message || t('auth.anErrorOccurred'),
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: t('common.error'),
        description: t('auth.networkError'),
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoadingService) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">{t('common.loading')}</p>
        </div>
      </div>
    );
  }

  if (!service) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">{t('services.noServicesFound')}</p>
          <Link href="/services">
            <Button className="mt-4">{t('booking.backToServices')}</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <Link href="/services" className="inline-flex items-center text-blue-600 hover:text-blue-800">
              <ArrowLeft className="h-4 w-4 mr-2" />
              {t('booking.backToServices')}
            </Link>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Service Details */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <User className="h-5 w-5 mr-2" />
                  {t('booking.serviceDetails')}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h3 className="text-xl font-semibold">{service.name}</h3>
                  <p className="text-gray-600">{service.description}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="flex items-center">
                    <CreditCard className="h-4 w-4 mr-2 text-green-600" />
                    <span className="font-semibold">{formatCurrency(service.price)}</span>
                  </div>
                  <div className="flex items-center">
                    <Clock className="h-4 w-4 mr-2 text-blue-600" />
                    <span>{service.duration} minutes</span>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <h4 className="font-semibold mb-2">{t('services.partner')}</h4>
                  <div className="flex items-center">
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                      <User className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <p className="font-medium">{service.partner.name}</p>
                      <div className="flex items-center">
                        <span className="text-yellow-500">★</span>
                        <span className="text-sm text-gray-600 ml-1">
                          {service.partner.rating.toFixed(1)} {t('services.rating')}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Booking Form */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Calendar className="h-5 w-5 mr-2" />
                  {t('booking.bookService')}
                </CardTitle>
                <CardDescription>
                  {t('booking.selectDate')} {t('common.and')} {t('booking.selectTime')}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleBooking} className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="date">{t('booking.selectDate')}</Label>
                    <Input
                      id="date"
                      type="date"
                      value={selectedDate}
                      onChange={(e) => setSelectedDate(e.target.value)}
                      min={new Date().toISOString().split('T')[0]}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="time">{t('booking.selectTime')}</Label>
                    <Input
                      id="time"
                      type="time"
                      value={selectedTime}
                      onChange={(e) => setSelectedTime(e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="requirements">{t('booking.specialRequirements')} ({t('common.optional')})</Label>
                    <textarea
                      id="requirements"
                      value={specialRequirements}
                      onChange={(e) => setSpecialRequirements(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows={3}
                      placeholder={`${t('booking.specialRequirements')}...`}
                    />
                  </div>

                  <div className="border-t pt-4">
                    <div className="flex justify-between items-center mb-4">
                      <span className="font-medium">{t('booking.totalAmount')}:</span>
                      <span className="text-xl font-bold text-green-600">{formatCurrency(service.price)}</span>
                    </div>
                    
                    <Button 
                      type="submit" 
                      className="w-full" 
                      disabled={isLoading}
                    >
                      {isLoading ? t('booking.processing') : t('booking.confirmBooking')}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}

export default function BookingPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading booking page...</p>
        </div>
      </div>
    }>
      <BookingContent />
    </Suspense>
  );
}
