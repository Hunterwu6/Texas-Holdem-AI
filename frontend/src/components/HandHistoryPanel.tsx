import React from 'react';
import Card from './Card';
import { HandSummary } from '../types';

interface HandHistoryPanelProps {
  handHistory?: HandSummary[];
}

const phaseLabels: Record<string, string> = {
  pre_flop: 'Pre-Flop',
  flop: 'Flop',
  turn: 'Turn',
  river: 'River',
  showdown: 'Showdown',
};

const HandHistoryPanel: React.FC<HandHistoryPanelProps> = ({ handHistory }) => {
  const history = handHistory ?? [];
  const orderedHistory = [...history].reverse();

  return (
    <div className="bg-gray-800 rounded-xl shadow-xl p-4 h-full flex flex-col">
      <h3 className="text-white text-xl font-bold mb-4">Hand Tracker</h3>

      {orderedHistory.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-gray-400 text-sm text-center">
          Play a hand to start tracking results.
        </div>
      ) : (
        <div className="space-y-4 overflow-y-auto pr-2">
          {orderedHistory.map((summary) => {
            const groupedActions = ['pre_flop', 'flop', 'turn', 'river', 'showdown']
              .map((phase) => ({
                phase,
                actions: summary.actions.filter((a) => a.phase === phase),
              }))
              .filter((group) => group.actions.length > 0);

            return (
              <div key={summary.hand_number} className="bg-gray-900 rounded-lg p-4 border border-gray-700">
                <div className="flex items-center justify-between text-sm text-gray-400 mb-2">
                  <span className="font-semibold text-white">Hand #{summary.hand_number}</span>
                  <span>{new Date(summary.timestamp).toLocaleTimeString()}</span>
                </div>

                <div className="mb-3">
                  <p className="text-xs uppercase tracking-wide text-gray-500">Winners</p>
                  <div className="flex flex-wrap gap-2 mt-1">
                    {summary.winners.length === 0 ? (
                      <span className="text-sm text-gray-400">Split pot or no showdown</span>
                    ) : (
                      summary.winners.map((winner) => (
                        <span
                          key={winner.player_id}
                          className="text-sm text-green-300 bg-green-900/40 px-2 py-0.5 rounded"
                        >
                          {winner.player_name} +${winner.amount}
                        </span>
                      ))
                    )}
                  </div>
                </div>

                <div className="mb-3">
                  <p className="text-xs uppercase tracking-wide text-gray-500">Board</p>
                  <div className="flex gap-1 mt-1">
                    {summary.board.length === 0 ? (
                      <span className="text-sm text-gray-400">No community cards</span>
                    ) : (
                      summary.board.map((card, idx) => <Card key={idx} card={card} />)
                    )}
                  </div>
                </div>

                <div className="mb-3">
                  <p className="text-xs uppercase tracking-wide text-gray-500">Player Results</p>
                  <ul className="mt-1 space-y-1 text-sm">
                    {summary.players.map((player) => (
                      <li key={player.player_id} className="flex items-center justify-between text-gray-300">
                        <span>
                          {player.player_name}{' '}
                          {player.hand && (
                            <span className="text-xs text-gray-500">({player.hand})</span>
                          )}
                        </span>
                        <span className={player.result >= 0 ? 'text-green-300' : 'text-red-400'}>
                          {player.result >= 0 ? '+' : ''}
                          {player.result}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <p className="text-xs uppercase tracking-wide text-gray-500 mb-1">Actions</p>
                  <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                    {groupedActions.map((group) => (
                      <div key={group.phase}>
                        <p className="text-xs text-gray-400 mb-1">{phaseLabels[group.phase] || group.phase}</p>
                        <ul className="text-xs text-gray-300 space-y-0.5">
                          {group.actions.map((action, idx) => (
                            <li key={`${action.timestamp}-${idx}`}>
                              <span className="font-semibold text-white">{action.player_name}</span>{' '}
                              {action.action}
                              {action.amount > 0 && <span> ${action.amount}</span>}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default HandHistoryPanel;

