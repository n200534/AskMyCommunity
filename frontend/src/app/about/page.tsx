export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">About AskMyCommunity</h1>
          <p className="text-xl text-gray-600">
            Discover amazing places in your city with AI-powered recommendations
          </p>
        </div>

        <div className="prose prose-lg max-w-none">
          <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Our Mission</h2>
            <p className="text-gray-600 mb-4">
              AskMyCommunity is designed to help you discover the best places, events, and activities 
              in your city. We use AI technology combined with community insights to provide personalized 
              recommendations that match your interests and preferences.
            </p>
            <p className="text-gray-600">
              Whether you're looking for a cozy cafe to work from, a romantic restaurant for a date, 
              or fun activities for the weekend, we've got you covered.
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">How It Works</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🔍</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Search</h3>
                <p className="text-gray-600">Ask anything in natural language - "Chill rooftop cafe near me"</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🤖</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Analysis</h3>
                <p className="text-gray-600">Our AI understands your intent and finds the best matches</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">📍</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Discover</h3>
                <p className="text-gray-600">Get personalized recommendations with ratings and reviews</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Why Choose Us?</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">AI-Powered</h3>
                <p className="text-gray-600 mb-4">
                  Advanced AI technology that understands natural language queries and provides 
                  intelligent recommendations based on your preferences.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Community Driven</h3>
                <p className="text-gray-600 mb-4">
                  Real reviews and insights from local community members who know the best spots 
                  in your city.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Always Updated</h3>
                <p className="text-gray-600 mb-4">
                  Our database is constantly updated with new places, events, and activities 
                  to ensure you never miss out on the latest discoveries.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Free to Use</h3>
                <p className="text-gray-600 mb-4">
                  Completely free to use with no hidden costs. Discover amazing places without 
                  any subscription fees.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

