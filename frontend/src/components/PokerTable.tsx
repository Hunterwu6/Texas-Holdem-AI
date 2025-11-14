import React from 'react';
import { GameState } from '../types';
import PlayerSeat from './PlayerSeat';
import Card from './Card';

interface PokerTableProps {
  gameState: GameState;
  humanPlayerId?: string;
}

const PokerTable: React.FC<PokerTableProps> = ({ gameState, humanPlayerId }) => {
  const phaseNames: { [key: string]: string } = {
    'waiting': 'Waiting',
    'pre_flop': 'Pre-Flop',
    'flop': 'Flop',
    'turn': 'Turn',
    'river': 'River',
    'showdown': 'Showdown',
    'complete': 'Complete'
  };

  return (
    <div className="relative w-full max-w-7xl mx-auto">
      {/* Poker Table */}
      <div className="relative bg-poker-felt rounded-full border-8 border-poker-table shadow-2xl p-16 aspect-[16/10]">
        
        {/* Center Info */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
          {/* Phase */}
          <div className="bg-black bg-opacity-70 rounded-lg p-4 mb-4">
            <div className="text-yellow-400 font-bold text-xl mb-2">
              {phaseNames[gameState.phase] || gameState.phase}
            </div>
            
            {/* Pot */}
            <div className="text-white text-3xl font-bold mb-2">
              POT: ${gameState.pot}
            </div>
            
            {/* Community Cards */}
            {gameState.community_cards && gameState.community_cards.length > 0 && (
              <div className="flex justify-center gap-2 mt-4">
                {gameState.community_cards.map((card, idx) => (
                  <Card key={idx} card={card} />
                ))}
                {/* Placeholder cards for remaining community cards */}
                {Array.from({ length: 5 - gameState.community_cards.length }).map((_, idx) => (
                  <div key={`placeholder-${idx}`} className="card card-back opacity-30">
                    ?
                  </div>
                ))}
              </div>
            )}
            
            {gameState.current_bet > 0 && (
              <div className="text-green-400 text-sm mt-2">
                Current Bet: ${gameState.current_bet}
              </div>
            )}
          </div>
        </div>
        
        {/* Players in circle around table */}
        <div className="relative w-full h-full">
          {gameState.players.map((player, idx) => {
            // Position players in an ellipse (wider than tall)
            const angle = (idx / gameState.players.length) * 2 * Math.PI - Math.PI / 2;
            const radiusX = 47; // horizontal radius (percentage)
            const radiusY = 42; // vertical radius (percentage)
            const x = 50 + radiusX * Math.cos(angle);
            const y = 50 + radiusY * Math.sin(angle);
            
            return (
              <div
                key={player.id}
                className="absolute transform -translate-x-1/2 -translate-y-1/2"
                style={{
                  left: `${x}%`,
                  top: `${y}%`,
                }}
              >
                <PlayerSeat
                  player={player}
                  isCurrentPlayer={idx === gameState.current_player}
                  isDealer={idx === gameState.dealer_position}
                  showCards={player.id === humanPlayerId || gameState.phase === 'showdown'}
                />
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Table Info Bar */}
      <div className="mt-4 bg-gray-800 rounded-lg p-4 flex justify-between items-center text-white">
        <div>
          <span className="text-gray-400">Blinds:</span>{' '}
          <span className="font-bold">${gameState.small_blind}/${gameState.big_blind}</span>
        </div>
        <div>
          <span className="text-gray-400">Players:</span>{' '}
          <span className="font-bold">{gameState.players.length}</span>
        </div>
        <div>
          <span className="text-gray-400">Game ID:</span>{' '}
          <span className="font-mono text-xs">{gameState.game_id.slice(0, 8)}</span>
        </div>
      </div>
    </div>
  );
};

export default PokerTable;

