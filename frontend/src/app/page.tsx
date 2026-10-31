/**
 * Landing Page
 */
'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-blue-600">TradeScope</h1>
          <div className="space-x-4">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h2 className="text-5xl font-bold mb-6">
          Professional Trading Strategy
          <br />
          <span className="text-blue-600">Backtesting Platform</span>
        </h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Test your trading strategies with historical data from Binance.
          Get detailed analytics and insights before risking real capital.
        </p>
        <div className="space-x-4">
          <Link href="/register">
            <Button size="lg">Start Free Trial</Button>
          </Link>
          <Link href="/login">
            <Button size="lg" variant="outline">
              Sign In
            </Button>
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-20">
        <h3 className="text-3xl font-bold text-center mb-12">Features</h3>
        <div className="grid md:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Historical Data</CardTitle>
              <CardDescription>
                Access years of OHLCV data from Binance for accurate backtesting
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Multiple Strategies</CardTitle>
              <CardDescription>
                Test SMA, RSI, and custom strategies with configurable parameters
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Detailed Analytics</CardTitle>
              <CardDescription>
                Get Sharpe ratio, max drawdown, win rate, and more metrics
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Pricing */}
      <section className="container mx-auto px-4 py-20">
        <h3 className="text-3xl font-bold text-center mb-12">Simple Pricing</h3>
        <div className="max-w-md mx-auto">
          <Card>
            <CardHeader className="text-center">
              <CardTitle className="text-3xl">$29/month</CardTitle>
              <CardDescription>Everything you need to backtest strategies</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <p className="flex items-center">
                ✓ Unlimited backtests
              </p>
              <p className="flex items-center">
                ✓ Historical data access
              </p>
              <p className="flex items-center">
                ✓ Multiple strategy types
              </p>
              <p className="flex items-center">
                ✓ Advanced analytics
              </p>
              <Link href="/register">
                <Button className="w-full mt-4" size="lg">
                  Subscribe Now
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 mt-20">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>&copy; 2024 TradeScope. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
