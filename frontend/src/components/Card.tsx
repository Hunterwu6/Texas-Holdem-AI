import React from 'react';

interface CardProps {
  card: string;
  hidden?: boolean;
}

const Card: React.FC<CardProps> = ({ card, hidden = false }) => {
  if (hidden || !card) {
    return (
      <div className="card card-back">
        <span>🂠</span>
      </div>
    );
  }

  const rank = card[0];
  const suit = card[1];

  const suitSymbols: { [key: string]: string } = {
    's': '♠',
    'h': '♥',
    'd': '♦',
    'c': '♣',
  };

  const rankDisplay = rank === 'T' ? '10' : rank;
  
  const suitClass = suit === 's' || suit === 'c' ? 'card-spades' : 'card-hearts';

  return (
    <div className={`card ${suitClass}`}>
      <div className="flex flex-col items-center -space-y-1">
        <span className="text-lg">{rankDisplay}</span>
        <span className="text-2xl">{suitSymbols[suit]}</span>
      </div>
    </div>
  );
};

export default Card;

