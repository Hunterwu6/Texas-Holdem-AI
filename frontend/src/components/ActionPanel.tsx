import React, { useState } from 'react';
import { GameState, HandSummary } from '../types';
import HandResultsCard from './HandResultsCard';
import Card from './Card';

interface ActionPanelProps {
  gameState: GameState;
  humanPlayerId: string;
  onAction: (action: string, amount: number) => void;
  onStartHand?: () => void;
  disabled?: boolean;
  latestHandSummary?: HandSummary;
}

const ActionPanel: React.FC<ActionPanelProps> = ({ 
  gameState, 
  humanPlayerId, 
  onAction,
  onStartHand,
  disabled = false,
  latestHandSummary,
}) => {
  const [raiseAmount, setRaiseAmount] = useState(gameState.big_blind * 2);
  
  const humanPlayer = gameState.players.find(p => p.id === humanPlayerId);
  const isMyTurn = humanPlayer && gameState.players[gameState.current_player]?.id === humanPlayerId;
  const canAct = isMyTurn && !humanPlayer.folded && !humanPlayer.all_in && !disabled;
  
  if (!humanPlayer) return null;

  const callAmount = gameState.current_bet - humanPlayer.current_bet;
  const minRaise = Math.max(
    gameState.big_blind,
    gameState.current_bet === 0 ? gameState.big_blind : gameState.current_bet * 2
  );
  const maxRaise = humanPlayer.stack;
  const isOpenBetting = gameState.current_bet === 0;

  const handleRaise = () => {
    const amount = Math.min(Math.max(raiseAmount, minRaise), maxRaise);
    const actionType = isOpenBetting ? 'bet' : 'raise';
    onAction(actionType, amount);
  };

  // Check if hand is over
  const isHandOver = gameState.phase === 'showdown' || gameState.phase === 'complete';
  const playersWithChips = gameState.players.filter(p => p.stack > 0).length;
  const canContinue = playersWithChips >= 2;

  return (
    <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
      <div className="mb-4">
        <h3 className="text-white font-bold text-xl mb-2">Your Action</h3>
        {isHandOver ? (
          <div className="space-y-2">
            <p className="text-green-400 font-semibold">Hand Complete!</p>
            {latestHandSummary && <HandResultsCard summary={latestHandSummary} />}
          </div>
        ) : !isMyTurn ? (
          <p className="text-gray-400">Waiting for your turn...</p>
        ) : (
          <p className="text-yellow-400 animate-pulse font-semibold">It's your turn!</p>
        )}
      </div>

      {/* Your Cards */}
      {humanPlayer.cards && humanPlayer.cards.length >= 2 && (
        <div className="bg-gray-700 rounded p-4 mb-4">
          <p className="text-gray-300 text-sm mb-2 text-center">Your Hand</p>
          <div className="flex justify-center gap-3">
            <Card card={humanPlayer.cards[0]} />
            <Card card={humanPlayer.cards[1]} />
          </div>
        </div>
      )}

      {/* Your Info */}
      <div className="bg-gray-700 rounded p-4 mb-4 text-white">
        <div className="flex justify-between mb-2">
          <span className="text-gray-300">Your Stack:</span>
          <span className="font-bold text-yellow-400">${humanPlayer.stack}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-300">Your Bet:</span>
          <span className="font-bold text-green-400">${humanPlayer.current_bet}</span>
        </div>
        {callAmount > 0 && (
          <div className="flex justify-between mt-2 pt-2 border-t border-gray-600">
            <span className="text-gray-300">To Call:</span>
            <span className="font-bold text-blue-400">${callAmount}</span>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="space-y-3">
        {/* Fold */}
        <button
          onClick={() => onAction('fold', 0)}
          disabled={!canAct}
          className="w-full btn-danger"
        >
          Fold
        </button>

        {/* Check/Call */}
        {gameState.current_bet === humanPlayer.current_bet ? (
          <button
            onClick={() => onAction('check', 0)}
            disabled={!canAct}
            className="w-full btn-secondary"
          >
            Check
          </button>
        ) : (
          <button
            onClick={() => onAction('call', 0)}
            disabled={!canAct || humanPlayer.stack < callAmount}
            className="w-full btn-primary"
          >
            Call ${callAmount}
          </button>
        )}

        {/* Raise */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <input
              type="number"
              value={raiseAmount}
              onChange={(e) => setRaiseAmount(Number(e.target.value))}
              min={minRaise}
              max={maxRaise}
              step={gameState.big_blind}
              disabled={!canAct}
              className="flex-1 bg-gray-700 text-white rounded px-3 py-2 font-mono disabled:opacity-50"
            />
            <button
              onClick={handleRaise}
              disabled={!canAct || humanPlayer.stack < Math.min(minRaise, maxRaise)}
              className="btn-primary whitespace-nowrap"
            >
              {isOpenBetting ? 'Bet' : 'Raise'}
            </button>
          </div>
          
          {/* Quick bet buttons */}
          <div className="flex gap-2">
            <button
              onClick={() => setRaiseAmount(Math.floor(gameState.pot / 2))}
              disabled={!canAct}
              className="flex-1 bg-gray-600 hover:bg-gray-500 text-white py-1 px-2 rounded text-sm disabled:opacity-50"
            >
              1/2 Pot
            </button>
            <button
              onClick={() => setRaiseAmount(gameState.pot)}
              disabled={!canAct}
              className="flex-1 bg-gray-600 hover:bg-gray-500 text-white py-1 px-2 rounded text-sm disabled:opacity-50"
            >
              Pot
            </button>
            <button
              onClick={() => setRaiseAmount(humanPlayer.stack)}
              disabled={!canAct}
              className="flex-1 bg-gray-600 hover:bg-gray-500 text-white py-1 px-2 rounded text-sm disabled:opacity-50"
            >
              All-In
            </button>
          </div>
        </div>

        {/* All-In */}
        <button
          onClick={() => onAction('all_in', 0)}
          disabled={!canAct}
          className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-6 rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          All-In (${humanPlayer.stack})
        </button>
      </div>

      {/* Next Hand Button (shown after hand completes) */}
      {isHandOver && onStartHand && (
        <div className="mt-6 pt-6 border-t border-gray-700">
          {canContinue ? (
            <button
              onClick={onStartHand}
              disabled={disabled}
              className="w-full btn-primary text-lg py-3"
            >
              Next Hand 🎴
            </button>
          ) : (
            <div className="text-center">
              <p className="text-red-400 font-bold mb-2">Game Over!</p>
              <p className="text-gray-400 text-sm">Not enough players with chips to continue</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ActionPanel;

