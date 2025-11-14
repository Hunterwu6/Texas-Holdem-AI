import React from 'react';
import { Player } from '../types';
import Card from './Card';

interface PlayerSeatProps {
  player: Player;
  isCurrentPlayer: boolean;
  isDealer: boolean;
  showCards?: boolean;
}

const PlayerSeat: React.FC<PlayerSeatProps> = ({ 
  player, 
  isCurrentPlayer, 
  isDealer,
  showCards = false 
}) => {
  const getStatusColor = () => {
    if (player.folded) return 'bg-gray-700 opacity-50';
    if (player.all_in) return 'bg-purple-800';
    if (isCurrentPlayer) return 'bg-green-700 ring-4 ring-yellow-400';
    return 'bg-gray-800';
  };

  const isAI = player.id.startsWith('ai_');

  return (
    <div className={`relative ${getStatusColor()} rounded-lg p-4 min-w-[180px] shadow-lg transition-all`}>
      {/* Dealer Button */}
      {isDealer && (
        <div className="absolute -top-3 -right-3 bg-white text-black rounded-full w-8 h-8 flex items-center justify-center font-bold border-2 border-yellow-400">
          D
        </div>
      )}
      
      {/* Player Info */}
      <div className="text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <span className="text-white font-bold text-lg">
            {player.name}
          </span>
          {isAI && <span className="text-xs bg-blue-500 px-2 py-1 rounded">AI</span>}
        </div>
        
        {/* Stack */}
        <div className="text-yellow-400 font-bold text-xl mb-2">
          ${player.stack}
        </div>
        
        {/* Current Bet */}
        {player.current_bet > 0 && (
          <div className="text-green-400 text-sm">
            Bet: ${player.current_bet}
          </div>
        )}
        
        {/* Status */}
        {player.folded && (
          <div className="text-red-400 text-sm font-semibold mt-1">FOLDED</div>
        )}
        {player.all_in && (
          <div className="text-purple-400 text-sm font-semibold mt-1">ALL-IN</div>
        )}
        {isCurrentPlayer && !player.folded && !player.all_in && (
          <div className="text-yellow-400 text-sm font-semibold mt-1 animate-pulse">
            YOUR TURN
          </div>
        )}
      </div>
      
      {/* Cards */}
      <div className="flex justify-center gap-1 mt-3">
        {player.cards && player.cards.length >= 2 ? (
          <>
            <Card card={player.cards[0]} hidden={!showCards} />
            <Card card={player.cards[1]} hidden={!showCards} />
          </>
        ) : (
          <>
            <Card card={""} hidden={true} />
            <Card card={""} hidden={true} />
          </>
        )}
      </div>
    </div>
  );
};

export default PlayerSeat;

