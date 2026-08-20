import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://powerbilearning.studio"),
  title: {
    default: "Power BI Learning Studio · CA Pradeep Gujaran",
    template: "%s · Power BI Learning Studio",
  },
  description:
    "A practical three-day Power BI learning programme with guided labs, validation checks and downloadable completed solutions.",
  keywords: ["Power BI training", "Power Query", "DAX", "data modelling", "audit analytics"],
  authors: [{ name: "CA Pradeep Gujaran" }],
  openGraph: {
    title: "Power BI Learning Studio",
    description: "Learn the full Power BI workflow through 28 guided topics and four practical labs.",
    type: "website",
    images: [{ url: "/social-card.png", width: 1200, height: 630 }],
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
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
