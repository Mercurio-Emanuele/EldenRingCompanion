import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "eldenring.wiki.fextralife.com",
        pathname: "/file/Elden-Ring/**",
      },
    ],
  },
};

export default nextConfig;
