/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['maps.googleapis.com', 'via.placeholder.com'],
  },
}

module.exports = nextConfig
