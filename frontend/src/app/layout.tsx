import type { Metadata } from "next";
import localFont from "next/font/local";
import Link from "next/link";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Engineering Onboarding Copilot",
  description: "AI-powered guide to engineering processes and documentation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {/* Navigation Bar */}
        <nav className="bg-white border-b border-gray-200 shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <Link
                href="/"
                className="text-xl font-bold text-gray-900 hover:text-blue-600"
              >
                Engineering Copilot
              </Link>
              <div className="flex gap-6">
                <Link
                  href="/ask"
                  className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
                >
                  Ask Question
                </Link>
                <Link
                  href="/gaps"
                  className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
                >
                  Gap Radar
                </Link>
              </div>
            </div>
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}
