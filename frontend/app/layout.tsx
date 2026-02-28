import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AISwitch - AI 模型聚合平台",
  description: "AI 模型聚合和智能切换平台",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <div className="min-h-screen bg-gray-50">
          <nav className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex">
                  <Link href="/" className="flex items-center px-2 text-xl font-bold text-gray-900">
                    AISwitch
                  </Link>
                  <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                    <Link href="/channels" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-600">
                      渠道管理
                    </Link>
                    <Link href="/models" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-600">
                      模型管理
                    </Link>
                    <Link href="/test" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-600">
                      模型测试
                    </Link>
                    <Link href="/config" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-600">
                      配置生成
                    </Link>
                    <Link href="/analytics" className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-600">
                      数据分析
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </nav>
          <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
