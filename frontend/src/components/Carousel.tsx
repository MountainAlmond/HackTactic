import React, { FC, useState } from 'react';
// import './CardCarousel.css';

interface Card {
  title: string;
  content: string;
}

interface CardCarouselProps {
  cards: Card[];
}

export const CardCarousel: FC<CardCarouselProps> = ({ cards }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const cardsToShow = 3;

  const nextCard = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % Math.ceil(cards.length / cardsToShow));
  };

  const prevCard = () => {
    setCurrentIndex((prevIndex) => 
      (prevIndex - 1 + Math.ceil(cards.length / cardsToShow)) % Math.ceil(cards.length / cardsToShow)
    );
  };

  const visibleCards = cards.slice(currentIndex * cardsToShow, currentIndex * cardsToShow + cardsToShow);

  return (
    <div className="carousel-container">
      <button className="carousel-button" onClick={prevCard}>←</button>
      <div className="card-container">
        {visibleCards.map((card, index) => (
          <div className="card" key={index}>
            <h2>{card.title}</h2>
            <p>{card.content}</p>
            <button className="info-button" onClick={() => alert(card.content)}>
              Подробная информация
            </button>
          </div>
        ))}
      </div>
      <button className="carousel-button" onClick={nextCard}>→</button>
    </div>
  );
};