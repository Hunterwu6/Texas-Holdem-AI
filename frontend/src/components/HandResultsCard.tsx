import React from 'react';
import { HandSummary } from '../types';

interface HandResultsCardProps {
  summary: HandSummary;
}

const HandResultsCard: React.FC<HandResultsCardProps> = ({ summary }) => (
  <div className="bg-gray-700 rounded p-3 text-sm text-gray-200 space-y-2">
    <div className="flex items-center justify-between text-xs text-gray-400">
      <span>Hand #{summary.hand_number}</span>
      <span>{new Date(summary.timestamp).toLocaleTimeString()}</span>
    </div>
    <div>
      <p className="text-xs uppercase tracking-wide text-gray-500">Winners</p>
      <div className="flex flex-wrap gap-2 mt-1">
        {summary.winners.length === 0 ? (
          <span>No showdown</span>
        ) : (
          summary.winners.map((winner) => (
            <span key={winner.player_id} className="text-green-300">
              {winner.player_name} +${winner.amount}
            </span>
          ))
        )}
      </div>
    </div>
    <div>
      <p className="text-xs uppercase tracking-wide text-gray-500">Results</p>
      <ul className="mt-1 space-y-1">
        {summary.players.map((player) => (
          <li
            key={player.player_id}
            className="flex items-center justify-between"
          >
            <span className="text-gray-300">{player.player_name}</span>
            <span className={player.result >= 0 ? 'text-green-300' : 'text-red-400'}>
              {player.result >= 0 ? '+' : ''}
              {player.result}
            </span>
          </li>
        ))}
      </ul>
    </div>
  </div>
);

export default HandResultsCard;

