import React, { useState, useEffect, useRef } from 'react';
import { gameApi } from './api';
import { GameState } from './types';
import PokerTable from './components/PokerTable';
import ActionPanel from './components/ActionPanel';
import Settings, { GameSettings } from './components/Settings';
import HandHistoryPanel from './components/HandHistoryPanel';
import HandResultsCard from './components/HandResultsCard';

function App() {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [humanPlayerId, setHumanPlayerId] = useState<string>('');
  const [playerName, setPlayerName] = useState('');
  const [numAI, setNumAI] = useState(2);
  const [aiStrategy, setAiStrategy] = useState('aggressive');
  const [aiStrategies, setAiStrategies] = useState<string[]>(['aggressive', 'aggressive']);  // Individual strategy for each AI
  const [aiNames, setAiNames] = useState<string[]>(['AI #1', 'AI #2']);
  const [aiPrompts, setAiPrompts] = useState<string[]>(['', '']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [gameStarted, setGameStarted] = useState(false);
  const [watchMode, setWatchMode] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [availableStrategies, setAvailableStrategies] = useState<string[]>(['aggressive', 'conservative', 'random']);
  const autoAdvanceRef = useRef(false);
  
  // Load settings from localStorage
  const [settings, setSettings] = useState<GameSettings>(() => {
    const saved = localStorage.getItem('pokerSettings');
    if (saved) {
      return JSON.parse(saved);
    }
    return {
      startingStack: 1000,
      smallBlind: 5,
      bigBlind: 10,
      llmApiKeys: {
        openai: '',
        deepseek: '',
        anthropic: '',
        gemini: '',
        grok: '',
      },
    };
  });

  // Auto-refresh game state
  useEffect(() => {
    if (gameState && gameStarted) {
      const interval = setInterval(async () => {
        try {
          const updated = await gameApi.getGame(gameState.game_id);
          setGameState(updated);
        } catch (err) {
          console.error('Failed to refresh game state:', err);
        }
      }, 2000); // Refresh every 2 seconds

      return () => clearInterval(interval);
    }
  }, [gameState, gameStarted]);

  const handleSaveSettings = async (newSettings: GameSettings) => {
    setSettings(newSettings);
    localStorage.setItem('pokerSettings', JSON.stringify(newSettings));
    
    // Send API keys to backend and refresh strategies
    try {
      await gameApi.updateLLMKeys(newSettings.llmApiKeys);
      const strategies = await gameApi.getAIStrategies();
      setAvailableStrategies(strategies.strategies);
    } catch (err) {
      console.error('Failed to update LLM keys:', err);
    }
  };

  // Load available strategies on mount
  useEffect(() => {
    const loadStrategies = async () => {
      try {
        // Send saved API keys to backend
        await gameApi.updateLLMKeys(settings.llmApiKeys);
        const strategies = await gameApi.getAIStrategies();
        setAvailableStrategies(strategies.strategies);
      } catch (err) {
        console.error('Failed to load strategies:', err);
      }
    };
    loadStrategies();
  }, []);

  const handleCreateGame = async () => {
    if (!watchMode && !playerName.trim()) {
      setError('Please enter your name or enable Watch Mode');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const playerNames = watchMode ? [] : [playerName];
      // Use individual AI strategies if set, otherwise use the default strategy for all
      const aiPlayers = aiStrategies.length === numAI 
        ? aiStrategies 
        : Array(numAI).fill(aiStrategy);
      
      const aiPromptsPayload = Array.from({ length: numAI }, (_, idx) => aiPrompts[idx] || '');
      
      console.log('Creating game with:', {
        player_names: playerNames,
        ai_players: aiPlayers,
        ai_prompts: aiPromptsPayload,
        ai_names: aiNames,
        small_blind: settings.smallBlind,
        big_blind: settings.bigBlind,
        starting_stack: settings.startingStack,
      });
      
      const newGame = await gameApi.createGame({
        player_names: playerNames,
        ai_players: aiPlayers,
        ai_prompts: aiPromptsPayload,
        ai_names: aiNames,
        small_blind: settings.smallBlind,
        big_blind: settings.bigBlind,
        starting_stack: settings.startingStack,
      });

      console.log('Game created:', newGame);
      setGameState(newGame);
      // Find human player ID
      const humanPlayer = newGame.players.find(p => !p.id.startsWith('ai_'));
      if (humanPlayer) {
        setHumanPlayerId(humanPlayer.id);
      }
    } catch (err: any) {
      console.error('Create game error:', err);
      console.error('Error response:', err.response);
      setError(err.response?.data?.detail || err.message || 'Failed to create game');
    } finally {
      setLoading(false);
    }
  };

  const handleStartHand = async () => {
    if (!gameState) return;

    setLoading(true);
    setError('');

    try {
      const updated = await gameApi.startHand(gameState.game_id);
      setGameState(updated);
      setGameStarted(true);
      
      // Check if we need to auto-advance for watch mode
      if (watchMode) {
        // Give a moment to see the initial state
        setTimeout(() => {
          // The auto-refresh will handle updates
        }, 500);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start hand');
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (action: string, amount: number) => {
    if (!gameState || !humanPlayerId) return;

    setLoading(true);
    setError('');

    try {
      const updated = await gameApi.submitAction(gameState.game_id, {
        player_id: humanPlayerId,
        action,
        amount,
      });
      setGameState(updated);
    } catch (err: any) {
      console.error('Action error:', err);
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to submit action';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleAdvanceAI = async () => {
    if (!gameState) return;

    setLoading(true);
    setError('');

    try {
      const updated = await gameApi.advanceAI(gameState.game_id);
      setGameState(updated);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to advance AI');
    } finally {
      setLoading(false);
    }
  };

  const autoAdvanceAI = async () => {
    if (!gameState || autoAdvanceRef.current) return;
    autoAdvanceRef.current = true;
    try {
      const updated = await gameApi.advanceAI(gameState.game_id);
      setGameState(updated);
    } catch (err) {
      console.error('Auto advance failed:', err);
    } finally {
      autoAdvanceRef.current = false;
    }
  };

  const currentHuman = gameState?.players.find(p => p.id === humanPlayerId);
  const isSpectating = watchMode || !currentHuman || currentHuman.folded || currentHuman.all_in;

  useEffect(() => {
    if (!gameState || !gameStarted) return;
    if (!isSpectating) return;
    if (['showdown', 'complete'].includes(gameState.phase)) return;

    const timer = setTimeout(() => {
      autoAdvanceAI();
    }, 1200);

    return () => clearTimeout(timer);
  }, [gameState, gameStarted, isSpectating]);

  const latestHandSummary =
    gameState?.hand_history && gameState.hand_history.length > 0
      ? gameState.hand_history[gameState.hand_history.length - 1]
      : undefined;

  return (
    <div className="min-h-screen bg-poker-bg p-8">
      {/* Settings Modal */}
      <Settings
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
        onSave={handleSaveSettings}
        currentSettings={settings}
      />

      {/* Header */}
      <div className="text-center mb-8 relative">
        <button
          onClick={() => setShowSettings(true)}
          className="absolute right-0 top-0 bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg transition-colors flex items-center gap-2"
        >
          ⚙️ Settings
        </button>
        
        <h1 className="text-5xl font-bold text-white mb-2">
          🎰 Texas Hold'em AI Battle
        </h1>
        <p className="text-gray-400 text-lg">
          Play poker against AI opponents
        </p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="max-w-2xl mx-auto mb-4 bg-red-900 border border-red-700 text-white px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Game Setup or Game View */}
      {!gameState ? (
        <div className="max-w-md mx-auto bg-gray-800 rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-white mb-6">Create New Game</h2>
          
          <div className="space-y-4">
            {/* Watch Mode Toggle */}
            <div className="bg-gray-700 rounded p-4">
              <label className="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={watchMode}
                  onChange={(e) => setWatchMode(e.target.checked)}
                  className="w-5 h-5 text-poker-primary bg-gray-600 border-gray-500 rounded focus:ring-poker-primary"
                />
                <span className="ml-3 text-white font-semibold">
                  👁️ Watch Mode (AI vs AI only)
                </span>
              </label>
              <p className="text-gray-400 text-sm mt-2">
                Enable to watch AI players compete without joining the game
              </p>
            </div>

            {!watchMode && (
              <div>
                <label className="block text-gray-300 mb-2">Your Name</label>
                <input
                  type="text"
                  value={playerName}
                  onChange={(e) => setPlayerName(e.target.value)}
                  className="w-full bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poker-primary"
                  placeholder="Enter your name"
                />
              </div>
            )}

            <div>
              <label className="block text-gray-300 mb-2">
                {watchMode ? 'Number of AI Players' : 'Number of AI Opponents'}
              </label>
              <select
                value={numAI}
                onChange={(e) => {
                  const newNum = Number(e.target.value);
                  setNumAI(newNum);
                  // Adjust strategies array length
                  setAiStrategies((prev) => {
                    const updated = [...prev];
                    if (newNum > updated.length) {
                      while (updated.length < newNum) {
                        updated.push(aiStrategy);
                      }
                    } else {
                      updated.length = newNum;
                    }
                    return updated;
                  });
                  // Adjust prompts array length
                  setAiPrompts((prev) => {
                    const updated = [...prev];
                    if (newNum > updated.length) {
                      while (updated.length < newNum) {
                        updated.push('');
                      }
                    } else {
                      updated.length = newNum;
                    }
                    return updated;
                  });
                  // Adjust AI names
                  setAiNames((prev) => {
                    const updated = [...prev];
                    if (newNum > updated.length) {
                      while (updated.length < newNum) {
                        updated.push(`AI #${updated.length + 1}`);
                      }
                    } else {
                      updated.length = newNum;
                    }
                    return updated;
                  });
                }}
                className="w-full bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poker-primary"
              >
                {(watchMode ? [2, 3, 4, 5, 6, 7, 8, 9] : [1, 2, 3, 4, 5, 6, 7, 8]).map(n => (
                  <option key={n} value={n}>{n} AI Player{n > 1 ? 's' : ''}</option>
                ))}
              </select>
            </div>

            {/* Individual AI Strategy Selection */}
            <div className="bg-gray-700 rounded p-4">
              <div className="flex flex-wrap justify-between items-center gap-2 mb-3">
                <label className="text-gray-300 font-semibold">AI Strategies</label>
                <div className="flex items-center gap-3 text-xs">
                  <button
                    onClick={() => {
                      setAiStrategies(Array(numAI).fill(aiStrategy));
                    }}
                    className="text-blue-400 hover:text-blue-300"
                  >
                    Use same strategy
                  </button>
                  <button
                    onClick={() => {
                      const firstPrompt = aiPrompts[0] || '';
                      setAiPrompts(Array(numAI).fill(firstPrompt));
                    }}
                    className="text-purple-300 hover:text-purple-200"
                  >
                    Copy first prompt
                  </button>
                </div>
              </div>
              
              {availableStrategies.some(s => ['gpt4', 'gpt4o', 'deepseek', 'claude', 'gemini', 'grok'].includes(s)) && (
                <p className="text-green-400 text-xs mb-3">
                  ✨ LLM strategies available!
                </p>
              )}

              <div className="space-y-3">
                {Array.from({ length: numAI }).map((_, idx) => {
                  const strategyLabels: { [key: string]: string } = {
                    'aggressive': '🔥 Aggressive',
                    'conservative': '🛡️ Conservative',
                    'random': '🎲 Random',
                    'gpt4': '🤖 GPT-4 Mini',
                    'gpt4o': '🤖 GPT-4o',
                    'deepseek': '🧠 DeepSeek',
                    'claude': '🎭 Claude',
                    'gemini': '💎 Gemini',
                    'grok': '⚡ Grok',
                  };

                  return (
                    <div key={idx} className="space-y-2 bg-gray-800/40 p-3 rounded">
                      <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
                        <div className="flex-1">
                          <label className="text-gray-300 text-xs uppercase tracking-wide">AI Name</label>
                          <input
                            type="text"
                            value={aiNames[idx] !== undefined ? aiNames[idx] : `AI #${idx + 1}`}
                            onChange={(e) => {
                              const updated = [...aiNames];
                              while (updated.length < numAI) {
                                  updated.push(`AI #${updated.length + 1}`);
                              }
                              updated[idx] = e.target.value;
                              setAiNames(updated);
                            }}
                            className="w-full mt-1 bg-gray-600 text-white rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-poker-primary"
                            placeholder={`AI #${idx + 1}`}
                          />
                        </div>
                        <div className="flex-1">
                          <label className="text-gray-300 text-xs uppercase tracking-wide">Strategy</label>
                          <select
                            value={aiStrategies[idx] || aiStrategy}
                            onChange={(e) => {
                              const newStrategies = [...aiStrategies];
                              while (newStrategies.length < numAI) {
                                newStrategies.push(aiStrategy);
                              }
                              newStrategies[idx] = e.target.value;
                              setAiStrategies(newStrategies);
                            }}
                            className="w-full mt-1 bg-gray-600 text-white rounded px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-poker-primary"
                          >
                            {availableStrategies.map(strategy => (
                              <option key={strategy} value={strategy}>
                                {strategyLabels[strategy] || strategy}
                              </option>
                            ))}
                          </select>
                        </div>
                      </div>
                      <textarea
                        value={aiPrompts[idx] || ''}
                        onChange={(e) => {
                          const newPrompts = [...aiPrompts];
                          while (newPrompts.length < numAI) {
                            newPrompts.push('');
                          }
                          newPrompts[idx] = e.target.value;
                          setAiPrompts(newPrompts);
                        }}
                        rows={2}
                        placeholder="Optional: describe how this AI should play (style, goals, etc.)"
                        className="w-full bg-gray-600/70 text-white rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-poker-primary resize-none"
                      />
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="bg-gray-700 rounded p-4 text-gray-300 text-sm">
              <div className="flex justify-between items-start mb-2">
                <p><strong>Game Settings:</strong></p>
                <button
                  onClick={() => setShowSettings(true)}
                  className="text-xs text-blue-400 hover:text-blue-300"
                >
                  Edit ⚙️
                </button>
              </div>
              <ul className="list-disc list-inside space-y-1">
                <li>Starting Stack: ${settings.startingStack.toLocaleString()}</li>
                <li>Small Blind: ${settings.smallBlind}</li>
                <li>Big Blind: ${settings.bigBlind}</li>
              </ul>
            </div>

            <button
              onClick={handleCreateGame}
              disabled={loading}
              className="w-full btn-primary text-lg py-3"
            >
              {loading ? 'Creating...' : 'Create Game'}
            </button>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-[320px_minmax(0,1fr)] gap-6">
            <div className="lg:sticky lg:top-6 max-h-[calc(100vh-4rem)]">
              <HandHistoryPanel handHistory={gameState.hand_history} />
            </div>

            <div className="space-y-6">
              <PokerTable gameState={gameState} humanPlayerId={humanPlayerId} />

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                  {gameStarted ? (
                    watchMode ? (
                      <div className="bg-gray-800 rounded-lg p-8 text-center">
                        <h3 className="text-white text-2xl font-bold mb-4">👁️ Watch Mode</h3>
                        <p className="text-gray-400 mb-6">
                          Click below to advance AI actions one at a time
                        </p>
                        <button
                          onClick={handleAdvanceAI}
                          disabled={loading || gameState.phase === 'showdown' || gameState.phase === 'complete'}
                          className="btn-primary text-xl py-4 px-12"
                        >
                          {loading ? 'Processing...' : 'Next AI Action ▶️'}
                        </button>
                        {(gameState.phase === 'showdown' || gameState.phase === 'complete') && (
                          <>
                            <button
                              onClick={handleStartHand}
                              disabled={loading}
                              className="btn-secondary text-xl py-4 px-12 mt-4"
                            >
                              {loading ? 'Starting...' : 'Next Hand 🎴'}
                            </button>
                            {latestHandSummary && (
                              <div className="mt-4">
                                <HandResultsCard summary={latestHandSummary} />
                              </div>
                            )}
                          </>
                        )}
                      </div>
                    ) : (
                      <ActionPanel
                        gameState={gameState}
                        humanPlayerId={humanPlayerId}
                        onAction={handleAction}
                        onStartHand={handleStartHand}
                        disabled={loading}
                        latestHandSummary={latestHandSummary}
                      />
                    )
                  ) : (
                    <div className="bg-gray-800 rounded-lg p-8 text-center">
                      <h3 className="text-white text-2xl font-bold mb-4">Ready to Play?</h3>
                      <p className="text-gray-400 mb-6">
                        Click below to start a new hand
                      </p>
                      <button
                        onClick={handleStartHand}
                        disabled={loading}
                        className="btn-primary text-xl py-4 px-12"
                      >
                        {loading ? 'Starting...' : 'Start Hand 🎴'}
                      </button>
                    </div>
                  )}
                </div>

                <div className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-white font-bold text-xl mb-4">Game Info</h3>
                  <div className="space-y-3 text-gray-300">
                    <div className="flex justify-between">
                      <span>Phase:</span>
                      <span className="font-bold text-white capitalize">
                        {gameState.phase.replace('_', ' ')}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Pot:</span>
                      <span className="font-bold text-yellow-400">${gameState.pot}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Current Bet:</span>
                      <span className="font-bold text-green-400">${gameState.current_bet}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Players:</span>
                      <span className="font-bold">{gameState.players.length}</span>
                    </div>
                  </div>

                  {gameStarted && (
                    <button
                      onClick={handleStartHand}
                      disabled={loading || gameState.phase !== 'complete'}
                      className="w-full btn-primary mt-6"
                    >
                      {gameState.phase === 'complete' ? 'Next Hand' : 'Hand in Progress...'}
                    </button>
                  )}

                  <button
                    onClick={() => {
                      setGameState(null);
                      setGameStarted(false);
                      setHumanPlayerId('');
                    }}
                    className="w-full btn-danger mt-3"
                  >
                    New Game
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="text-center mt-12 text-gray-500 text-sm">
        <p>Texas Hold'em AI Battle Simulator v1.0</p>
        <p className="mt-1">Backend API: http://localhost:8000</p>
      </div>
    </div>
  );
}

export default App;

