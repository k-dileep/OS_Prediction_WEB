import PredictionForm from './components/PredictionForm';
import Footer from './components/Footer';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 py-6 sm:py-8 md:py-12 flex flex-col">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex-grow">
        <div className="text-center mb-6 sm:mb-8 md:mb-12">
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 mb-2 sm:mb-4">
            Oxidative Stress Prediction System
          </h1>
          <p className="text-sm sm:text-base md:text-lg text-gray-600 max-w-3xl mx-auto">
            Enter radiation and fibrinogen levels to predict SOD activity and oxidative stress exposure.
          </p>
        </div>
        <PredictionForm />
      </div>
      <Footer />
    </div>
  );
}
