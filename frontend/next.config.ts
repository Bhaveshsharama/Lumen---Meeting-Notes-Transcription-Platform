import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  async rewrites() {
    // NEXT_PUBLIC_API_URL should point to the backend ROOT (without /api), e.g. https://lumen-api.onrender.com
    // In development, falls back to http://localhost:8000
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    return [
      {
        source: '/api/:path*',
        destination: backendUrl + '/api/:path*',
      },
    ];
  },
};

export default nextConfig;

