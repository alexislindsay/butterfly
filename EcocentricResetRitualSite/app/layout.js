export const metadata = {
  title: "Ecocentric Reset",
  description: "Ritual portal for planetary drift",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-white text-gray-900 p-4">{children}</body>
    </html>
  );
}
