import { useEffect, useState } from 'react';

export default function Home() {
  const [cards, setCards] = useState([]);
  const [error, setError] = useState(null);
  const [cardImages, setCardImages] = useState({});

  useEffect(() => {
    // Fetch the tarot deck data
    fetch('/deckTarot.json')
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load JSON");
        return res.json();
      })
      .then((data) => {
        setCards(data.cards);
        // Assign a random image to each card
        const images = assignRandomImages(data.cards);
        setCardImages(images);
      })
      .catch((err) => setError(err.message));
  }, []);

  // Function to get a random image filename
  const getRandomImageFilename = () => {
    // This will randomly select from images in /public/butterfly-images/
    // The images are numbered/named - we'll use a random index
    const randomNum = Math.floor(Math.random() * 1000);
    return `/butterfly-images/image${randomNum}.jpg`;
  };

  // Assign a random image to each card on initial load
  const assignRandomImages = (cardsList) => {
    const imageMap = {};
    cardsList.forEach((card, index) => {
      // Generate a random number for each card
      const randomImageNum = Math.floor(Math.random() * 1000) + 1;
      imageMap[index] = `/butterfly-images/image${randomImageNum}.jpg`;
    });
    return imageMap;
  };

  return (
    <div style={{
      padding: '2rem',
      fontFamily: 'sans-serif',
      backgroundColor: '#1a1a2e',
      minHeight: '100vh'
    }}>
      <h1 style={{
        textAlign: 'center',
        color: '#eee',
        fontSize: '3rem',
        marginBottom: '2rem'
      }}>
        🦋 Butterfly Tarot Deck 🦋
      </h1>
      {error && <p style={{ color: '#ff6b6b', textAlign: 'center' }}>{error}</p>}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
        gap: '2rem',
        padding: '1rem'
      }}>
        {cards.map((card, index) => (
          <div
            key={index}
            style={{
              backgroundColor: '#16213e',
              border: '2px solid #0f3460',
              borderRadius: '12px',
              padding: '1.5rem',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
              transition: 'transform 0.2s',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
          >
            <img
              src={cardImages[index] || '/butterfly-images/image1.jpg'}
              alt={card.name}
              style={{
                width: '100%',
                height: '350px',
                objectFit: 'cover',
                borderRadius: '8px',
                marginBottom: '1rem',
                border: '1px solid #0f3460'
              }}
              onError={(e) => {
                // Fallback to a different random image if one fails to load
                e.target.src = `/butterfly-images/image${Math.floor(Math.random() * 100) + 1}.jpg`;
              }}
            />
            <h2 style={{
              color: '#e94560',
              marginBottom: '0.5rem',
              fontSize: '1.5rem'
            }}>
              {card.name}
            </h2>
            {card.keywords && (
              <p style={{
                color: '#a8dadc',
                fontSize: '0.9rem',
                fontStyle: 'italic',
                marginBottom: '0.5rem'
              }}>
                {card.keywords.join(', ')}
              </p>
            )}
            <p style={{
              color: '#ddd',
              lineHeight: '1.6'
            }}>
              {card.description || card.meanings?.light?.[0] || 'No description available.'}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
