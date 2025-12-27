import { useEffect, useState } from 'react';

export default function Home() {
  const [cards, setCards] = useState([]);
  const [error, setError] = useState(null);
  const [cardImages, setCardImages] = useState({});
  const [availableImages, setAvailableImages] = useState([]);

  useEffect(() => {
    // First, fetch the list of available images
    fetch('/api/images')
      .then((res) => res.json())
      .then((data) => {
        setAvailableImages(data.images || []);
      })
      .catch((err) => console.error('Failed to load images list:', err));

    // Fetch the tarot deck data
    fetch('/deckTarot.json')
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load JSON");
        return res.json();
      })
      .then((data) => {
        setCards(data.cards);
      })
      .catch((err) => setError(err.message));
  }, []);

  // When cards are loaded (and optionally images), assign images
  useEffect(() => {
    if (cards.length > 0) {
      const images = assignRandomImages(cards, availableImages);
      setCardImages(images);
    }
  }, [cards, availableImages]);

  // Assign a random image to each card (or use card-specific image if specified)
  const assignRandomImages = (cardsList, imagesList) => {
    const imageMap = {};
    cardsList.forEach((card, index) => {
      // If card has a specific image path, use that
      if (card.img) {
        imageMap[index] = `/tarot-cards/${card.img}`;
      }
      // Otherwise, pick a random image from the butterfly-images folder
      else if (imagesList.length > 0) {
        const randomImage = imagesList[Math.floor(Math.random() * imagesList.length)];
        imageMap[index] = `/butterfly-images/${randomImage}`;
      }
    });
    return imageMap;
  };

  // Get a random fallback image
  const getRandomFallbackImage = () => {
    if (availableImages.length > 0) {
      const randomImage = availableImages[Math.floor(Math.random() * availableImages.length)];
      return `/butterfly-images/${randomImage}`;
    }
    return '';
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
            {cardImages[index] && (
              <img
                src={cardImages[index]}
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
                  e.target.src = getRandomFallbackImage();
                }}
              />
            )}
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
