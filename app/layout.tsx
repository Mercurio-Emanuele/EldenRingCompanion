import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Elden Ring Companion — Item Tracker",
  description: "Track every collectible in Elden Ring: Talismans, Sorceries, Incantations, Weapons, Armor and more.",
  icons: {
    icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='26' font-size='26'>⚔️</text></svg>"
  }
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
