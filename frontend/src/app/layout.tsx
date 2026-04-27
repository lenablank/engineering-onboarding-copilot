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
        <nav className="border-b-2 border-[var(--border)] bg-[var(--surface)]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <Link
                href="/"
                className="text-xl font-mono font-bold text-[var(--foreground)] hover:text-[var(--accent)] transition-colors tracking-tight"
              >
                ENGINEERING COPILOT
              </Link>
              <div className="flex gap-8">
                <Link
                  href="/ask"
                  className="text-[var(--foreground)] hover:text-[var(--accent)] font-mono font-semibold transition-colors tracking-tight"
                >
                  Ask Question
                </Link>
                <Link
                  href="/gaps"
                  className="text-[var(--foreground)] hover:text-[var(--accent)] font-mono font-semibold transition-colors tracking-tight"
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
