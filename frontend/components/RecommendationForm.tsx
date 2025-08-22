'use client'

import { useState } from 'react'
import { Search, MapPin, Heart, Calendar, Sparkles } from 'lucide-react'

interface RecommendationFormData {
  query: string
  location: string
  preferences: string[]
  context: string
}

export default function RecommendationForm() {
  const [formData, setFormData] = useState<RecommendationFormData>({
    query: '',
    location: '',
    preferences: [],
    context: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [recommendations, setRecommendations] = useState<any>(null)

  const preferenceOptions = [
    'Family-friendly', 'Romantic', 'Budget-friendly', 'Upscale',
    'Quick service', 'Outdoor seating', 'Live music', 'Quiet atmosphere',
    'Pet-friendly', 'Wheelchair accessible', 'Parking available'
  ]

  const contextOptions = [
    'Date night', 'Family outing', 'Business meeting', 'Solo adventure',
    'Group celebration', 'Quick lunch', 'Weekend brunch', 'Late night'
  ]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/v1/recommendations/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: formData.query,
          user_location: formData.location,
          user_preferences: formData.preferences,
          context: formData.context
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setRecommendations(data)
      } else {
        console.error('Failed to get recommendations')
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const togglePreference = (pref: string) => {
    setFormData(prev => ({
      ...prev,
      preferences: prev.preferences.includes(pref)
        ? prev.preferences.filter(p => p !== pref)
        : [...prev.preferences, pref]
    }))
  }

  const toggleContext = (ctx: string) => {
    setFormData(prev => ({
      ...prev,
      context: prev.context === ctx ? '' : ctx
    }))
  }

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Main Query Input */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={formData.query}
            onChange={(e) => setFormData(prev => ({ ...prev, query: e.target.value }))}
            placeholder="Where should I hang out on Saturday?"
            className="input pl-10 text-lg"
            required
          />
        </div>

        {/* Location Input */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <MapPin className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={formData.location}
            onChange={(e) => setFormData(prev => ({ ...prev, location: e.target.value }))}
            placeholder="Your location (city, neighborhood, etc.)"
            className="input pl-10"
          />
        </div>

        {/* Preferences */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            <Heart className="inline w-4 h-4 mr-2" />
            What are you looking for?
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {preferenceOptions.map((pref) => (
              <button
                key={pref}
                type="button"
                onClick={() => togglePreference(pref)}
                className={`px-3 py-2 text-sm rounded-full border transition-colors ${
                  formData.preferences.includes(pref)
                    ? 'bg-blue-100 border-blue-300 text-blue-700'
                    : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                }`}
              >
                {pref}
              </button>
            ))}
          </div>
        </div>

        {/* Context */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            <Calendar className="inline w-4 h-4 mr-2" />
            What's the occasion?
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {contextOptions.map((ctx) => (
              <button
                key={ctx}
                type="button"
                onClick={() => toggleContext(ctx)}
                className={`px-3 py-2 text-sm rounded-full border transition-colors ${
                  formData.context === ctx
                    ? 'bg-blue-100 border-blue-300 text-blue-700'
                    : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                }`}
              >
                {ctx}
              </button>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading || !formData.query}
          className="w-full btn-primary text-lg py-3 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Getting Recommendations...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5 mr-2" />
              Get AI Recommendations
            </>
          )}
        </button>
      </form>

      {/* Recommendations Display */}
      {recommendations && (
        <div className="mt-8 p-6 bg-white rounded-lg shadow-lg border">
          <h3 className="text-xl font-semibold mb-4 text-gray-900">
            Your Personalized Recommendations
          </h3>
          
          <div className="mb-4">
            <p className="text-gray-600">{recommendations.summary}</p>
          </div>

          {recommendations.places && recommendations.places.length > 0 && (
            <div className="space-y-4">
              <h4 className="font-medium text-gray-900">Top Places:</h4>
              {recommendations.places.map((place: any, index: number) => (
                <div key={index} className="p-4 bg-gray-50 rounded-lg">
                  <h5 className="font-semibold text-gray-900">{place.name}</h5>
                  <p className="text-sm text-gray-600 mt-1">{place.reasoning}</p>
                  {place.best_for && (
                    <p className="text-xs text-blue-600 mt-1">
                      Best for: {place.best_for}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}

          {recommendations.additional_tips && (
            <div className="mt-4 p-4 bg-blue-50 rounded-lg">
              <h4 className="font-medium text-blue-900 mb-2">💡 Additional Tips</h4>
              <p className="text-blue-800 text-sm">{recommendations.additional_tips}</p>
            </div>
          )}

          <div className="mt-4 text-xs text-gray-500">
            Sources: {recommendations.sources_used?.join(', ') || 'Multiple sources'}
          </div>
        </div>
      )}
    </div>
  )
}
