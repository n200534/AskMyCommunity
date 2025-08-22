'use client'

import { useState } from 'react'
import { Search, MapPin, Users, Calendar, Star } from 'lucide-react'
import RecommendationForm from '@/components/RecommendationForm'
import FeatureCard from '@/components/FeatureCard'
import Header from '@/components/Header'

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false)

  const features = [
    {
      icon: <Search className="w-6 h-6" />,
      title: "AI-Powered Recommendations",
      description: "Get personalized suggestions using Google Gemini AI based on your specific needs and preferences."
    },
    {
      icon: <MapPin className="w-6 h-6" />,
      title: "Multi-Source Data",
      description: "Comprehensive recommendations from Google Maps, Reddit, and local community sources."
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: "Community Voting",
      description: "See what the community thinks with our social voting system for places and recommendations."
    },
    {
      icon: <Calendar className="w-6 h-6" />,
      title: "Event Planner Mode",
      description: "Discover and plan local events with our integrated event management system."
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />
      
      {/* Hero Section */}
      <section className="px-4 py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Ask My Community
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Where should I hang out on Saturday? Discover the best local places with AI-powered recommendations from your community.
          </p>
          
          {/* Recommendation Form */}
          <div className="max-w-2xl mx-auto">
            <RecommendationForm />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 py-20 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-900 mb-16">
            Why Choose AskMyCommunity?
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <FeatureCard
                key={index}
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
              />
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="px-4 py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-16">
            How It Works
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Ask a Question</h3>
              <p className="text-gray-600">Simply ask where you want to go or what you're looking for.</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">AI Analysis</h3>
              <p className="text-gray-600">Our AI analyzes data from multiple sources to find the best matches.</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Get Recommendations</h3>
              <p className="text-gray-600">Receive personalized recommendations with explanations and community insights.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-4 py-20 bg-blue-600 text-white text-center">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Discover Your Community?
          </h2>
          <p className="text-xl mb-8 text-blue-100">
            Join thousands of users who are already finding amazing local places with AI-powered recommendations.
          </p>
          <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors">
            Get Started Now
          </button>
        </div>
      </section>
    </div>
  )
}
