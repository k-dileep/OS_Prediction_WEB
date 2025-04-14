/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // This enables static export
  // Ensure trailing slashes for better compatibility
  trailingSlash: true,
  // Configure images
  images: {
    domains: ['os-prediction-backend.onrender.com'],
    unoptimized: true, // Required for static export
  },
};

export default nextConfig; 