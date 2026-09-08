import type { Metadata } from 'next';
import './globals.css';
import Providers from './providers';
import AppShell from '@/components/layout/AppShell';

export const metadata: Metadata = {
  title: 'Lumen',
  description: 'AI meeting assistant clone',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <AppShell>{children}</AppShell>
        </Providers>
      </body>
    </html>
  );
}
