import { useEffect, useState } from 'react';

export default function Home() {
  const [cards, setCards] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/deckTarot.json')
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load JSON");
        return res.json();
      })
      .then((data) => setCards(data))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>🃏 Butterfly Tarot Deck</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {cards.map((card, index) => (
          <li key={index} style={{ marginBottom: '1rem', borderBottom: '1px solid #ddd' }}>
            <h2>{card.name}</h2>
            <p>{card.description || 'No description available.'}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
