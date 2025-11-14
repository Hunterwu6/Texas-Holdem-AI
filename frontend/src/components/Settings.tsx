import React, { useState, useEffect } from 'react';

interface SettingsProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (settings: GameSettings) => void;
  currentSettings: GameSettings;
}

export interface GameSettings {
  startingStack: number;
  smallBlind: number;
  bigBlind: number;
  llmApiKeys: {
    openai: string;
    deepseek: string;
    anthropic: string;
    gemini: string;
    grok: string;
  };
}

const Settings: React.FC<SettingsProps> = ({ isOpen, onClose, onSave, currentSettings }) => {
  const [settings, setSettings] = useState<GameSettings>(currentSettings);
  const [showApiKeys, setShowApiKeys] = useState(false);
  const [validationStatus, setValidationStatus] = useState<{[key: string]: 'idle' | 'testing' | 'valid' | 'invalid'}>({});
  const [validationErrors, setValidationErrors] = useState<{[key: string]: string}>({});

  useEffect(() => {
    setSettings(currentSettings);
  }, [currentSettings]);

  if (!isOpen) return null;

  const handleSave = () => {
    onSave(settings);
    onClose();
  };

  const handleReset = () => {
    setSettings({
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
    });
    setValidationStatus({});
    setValidationErrors({});
  };

  const validateApiKey = async (provider: string, apiKey: string) => {
    if (!apiKey || apiKey.trim() === '') {
      setValidationStatus(prev => ({ ...prev, [provider]: 'idle' }));
      return;
    }

    setValidationStatus(prev => ({ ...prev, [provider]: 'testing' }));
    setValidationErrors(prev => ({ ...prev, [provider]: '' }));

    try {
      const response = await fetch('/api/llm/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider, apiKey }),
      });

      const data = await response.json();

      if (response.ok && data.valid) {
        setValidationStatus(prev => ({ ...prev, [provider]: 'valid' }));
      } else {
        setValidationStatus(prev => ({ ...prev, [provider]: 'invalid' }));
        setValidationErrors(prev => ({ ...prev, [provider]: data.error || 'Invalid API key' }));
      }
    } catch (error: any) {
      setValidationStatus(prev => ({ ...prev, [provider]: 'invalid' }));
      setValidationErrors(prev => ({ ...prev, [provider]: 'Connection error' }));
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-lg shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gray-900 px-6 py-4 border-b border-gray-700 flex justify-between items-center sticky top-0">
          <h2 className="text-2xl font-bold text-white">⚙️ Game Settings</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white text-2xl"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Game Settings */}
          <div>
            <h3 className="text-xl font-bold text-white mb-4">💰 Game Configuration</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-gray-300 mb-2">Starting Stack ($)</label>
                <input
                  type="number"
                  value={settings.startingStack}
                  onChange={(e) => setSettings({ ...settings, startingStack: Number(e.target.value) })}
                  className="w-full bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poker-primary"
                  min="100"
                  step="100"
                />
                <p className="text-gray-500 text-sm mt-1">Each player starts with this amount</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-gray-300 mb-2">Small Blind ($)</label>
                  <input
                    type="number"
                    value={settings.smallBlind}
                    onChange={(e) => setSettings({ ...settings, smallBlind: Number(e.target.value) })}
                    className="w-full bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poker-primary"
                    min="1"
                  />
                </div>

                <div>
                  <label className="block text-gray-300 mb-2">Big Blind ($)</label>
                  <input
                    type="number"
                    value={settings.bigBlind}
                    onChange={(e) => setSettings({ ...settings, bigBlind: Number(e.target.value) })}
                    className="w-full bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poker-primary"
                    min="2"
                  />
                </div>
              </div>

              <div className="bg-gray-700 rounded p-3 text-sm text-gray-300">
                <p><strong>Recommended ratios:</strong></p>
                <ul className="list-disc list-inside mt-1 space-y-1">
                  <li>Big Blind = 2× Small Blind</li>
                  <li>Starting Stack = 100-200× Big Blind</li>
                  <li>Example: SB=$5, BB=$10, Stack=$1000</li>
                </ul>
              </div>
            </div>
          </div>

          {/* LLM API Keys */}
          <div>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-white">🤖 LLM API Keys</h3>
              <button
                onClick={() => setShowApiKeys(!showApiKeys)}
                className="text-sm text-blue-400 hover:text-blue-300"
              >
                {showApiKeys ? '🔒 Hide Keys' : '👁️ Show Keys'}
              </button>
            </div>

            <div className="space-y-4">
              {/* OpenAI */}
              <div>
                <label className="block text-gray-300 mb-2 flex items-center gap-2">
                  <span className="font-semibold">OpenAI API Key</span>
                  <span className="text-xs bg-green-600 px-2 py-0.5 rounded">GPT-4</span>
                </label>
                <div className="flex gap-2">
                  <input
                    type={showApiKeys ? "text" : "password"}
                    value={settings.llmApiKeys.openai}
                    onChange={(e) => {
                      setSettings({
                        ...settings,
                        llmApiKeys: { ...settings.llmApiKeys, openai: e.target.value }
                      });
                      setValidationStatus(prev => ({ ...prev, openai: 'idle' }));
                    }}
                    className="flex-1 bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poker-primary font-mono text-sm"
                    placeholder="sk-..."
                  />
                  <button
                    onClick={() => validateApiKey('openai', settings.llmApiKeys.openai)}
                    disabled={!settings.llmApiKeys.openai || validationStatus.openai === 'testing'}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded text-sm font-semibold"
                  >
                    {validationStatus.openai === 'testing' ? '⏳' : validationStatus.openai === 'valid' ? '✅' : validationStatus.openai === 'invalid' ? '❌' : 'Test'}
                  </button>
                </div>
                {validationStatus.openai === 'valid' && (
                  <p className="text-green-400 text-xs mt-1">✅ API key is valid!</p>
                )}
                {validationStatus.openai === 'invalid' && (
                  <p className="text-red-400 text-xs mt-1">❌ {validationErrors.openai || 'Invalid API key'}</p>
                )}
                <p className="text-gray-500 text-xs mt-1">
                  Get from: <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">platform.openai.com</a>
                </p>
              </div>

              {/* DeepSeek */}
              <div>
                <label className="block text-gray-300 mb-2 flex items-center gap-2">
                  <span className="font-semibold">DeepSeek API Key</span>
                  <span className="text-xs bg-purple-600 px-2 py-0.5 rounded">Cheap</span>
                </label>
                <div className="flex gap-2">
                  <input
                    type={showApiKeys ? "text" : "password"}
                    value={settings.llmApiKeys.deepseek}
                    onChange={(e) => {
                      setSettings({
                        ...settings,
                        llmApiKeys: { ...settings.llmApiKeys, deepseek: e.target.value }
                      });
                      setValidationStatus(prev => ({ ...prev, deepseek: 'idle' }));
                    }}
                    className="flex-1 bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poker-primary font-mono text-sm"
                    placeholder="sk-..."
                  />
                  <button
                    onClick={() => validateApiKey('deepseek', settings.llmApiKeys.deepseek)}
                    disabled={!settings.llmApiKeys.deepseek || validationStatus.deepseek === 'testing'}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded text-sm font-semibold"
                  >
                    {validationStatus.deepseek === 'testing' ? '⏳' : validationStatus.deepseek === 'valid' ? '✅' : validationStatus.deepseek === 'invalid' ? '❌' : 'Test'}
                  </button>
                </div>
                {validationStatus.deepseek === 'valid' && (
                  <p className="text-green-400 text-xs mt-1">✅ API key is valid!</p>
                )}
                {validationStatus.deepseek === 'invalid' && (
                  <p className="text-red-400 text-xs mt-1">❌ {validationErrors.deepseek || 'Invalid API key'}</p>
                )}
                <p className="text-gray-500 text-xs mt-1">
                  Get from: <a href="https://platform.deepseek.com/" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">platform.deepseek.com</a>
                </p>
              </div>

              {/* Anthropic Claude */}
              <div>
                <label className="block text-gray-300 mb-2 flex items-center gap-2">
                  <span className="font-semibold">Anthropic API Key</span>
                  <span className="text-xs bg-orange-600 px-2 py-0.5 rounded">Claude</span>
                </label>
                <div className="flex gap-2">
                  <input
                    type={showApiKeys ? "text" : "password"}
                    value={settings.llmApiKeys.anthropic}
                    onChange={(e) => {
                      setSettings({
                        ...settings,
                        llmApiKeys: { ...settings.llmApiKeys, anthropic: e.target.value }
                      });
                      setValidationStatus(prev => ({ ...prev, anthropic: 'idle' }));
                    }}
                    className="flex-1 bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poker-primary font-mono text-sm"
                    placeholder="sk-ant-..."
                  />
                  <button
                    onClick={() => validateApiKey('anthropic', settings.llmApiKeys.anthropic)}
                    disabled={!settings.llmApiKeys.anthropic || validationStatus.anthropic === 'testing'}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded text-sm font-semibold"
                  >
                    {validationStatus.anthropic === 'testing' ? '⏳' : validationStatus.anthropic === 'valid' ? '✅' : validationStatus.anthropic === 'invalid' ? '❌' : 'Test'}
                  </button>
                </div>
                {validationStatus.anthropic === 'valid' && (
                  <p className="text-green-400 text-xs mt-1">✅ API key is valid!</p>
                )}
                {validationStatus.anthropic === 'invalid' && (
                  <p className="text-red-400 text-xs mt-1">❌ {validationErrors.anthropic || 'Invalid API key'}</p>
                )}
                <p className="text-gray-500 text-xs mt-1">
                  Get from: <a href="https://console.anthropic.com/" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">console.anthropic.com</a>
                </p>
              </div>

              {/* Google Gemini */}
              <div>
                <label className="block text-gray-300 mb-2 flex items-center gap-2">
                  <span className="font-semibold">Google Gemini API Key</span>
                  <span className="text-xs bg-blue-600 px-2 py-0.5 rounded">Free Tier</span>
                </label>
                <div className="flex gap-2">
                  <input
                    type={showApiKeys ? "text" : "password"}
                    value={settings.llmApiKeys.gemini}
                    onChange={(e) => {
                      setSettings({
                        ...settings,
                        llmApiKeys: { ...settings.llmApiKeys, gemini: e.target.value }
                      });
                      setValidationStatus(prev => ({ ...prev, gemini: 'idle' }));
                    }}
                    className="flex-1 bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poker-primary font-mono text-sm"
                    placeholder="AIza..."
                  />
                  <button
                    onClick={() => validateApiKey('gemini', settings.llmApiKeys.gemini)}
                    disabled={!settings.llmApiKeys.gemini || validationStatus.gemini === 'testing'}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded text-sm font-semibold"
                  >
                    {validationStatus.gemini === 'testing' ? '⏳' : validationStatus.gemini === 'valid' ? '✅' : validationStatus.gemini === 'invalid' ? '❌' : 'Test'}
                  </button>
                </div>
                {validationStatus.gemini === 'valid' && (
                  <p className="text-green-400 text-xs mt-1">✅ API key is valid!</p>
                )}
                {validationStatus.gemini === 'invalid' && (
                  <p className="text-red-400 text-xs mt-1">❌ {validationErrors.gemini || 'Invalid API key'}</p>
                )}
                <p className="text-gray-500 text-xs mt-1">
                  Get from: <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">makersuite.google.com</a>
                </p>
              </div>

              {/* xAI Grok */}
              <div>
                <label className="block text-gray-300 mb-2 flex items-center gap-2">
                  <span className="font-semibold">xAI Grok API Key</span>
                  <span className="text-xs bg-red-600 px-2 py-0.5 rounded">New</span>
                </label>
                <div className="flex gap-2">
                  <input
                    type={showApiKeys ? "text" : "password"}
                    value={settings.llmApiKeys.grok}
                    onChange={(e) => {
                      setSettings({
                        ...settings,
                        llmApiKeys: { ...settings.llmApiKeys, grok: e.target.value }
                      });
                      setValidationStatus(prev => ({ ...prev, grok: 'idle' }));
                    }}
                    className="flex-1 bg-gray-700 text-white rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-poker-primary font-mono text-sm"
                    placeholder="xai-..."
                  />
                  <button
                    onClick={() => validateApiKey('grok', settings.llmApiKeys.grok)}
                    disabled={!settings.llmApiKeys.grok || validationStatus.grok === 'testing'}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded text-sm font-semibold"
                  >
                    {validationStatus.grok === 'testing' ? '⏳' : validationStatus.grok === 'valid' ? '✅' : validationStatus.grok === 'invalid' ? '❌' : 'Test'}
                  </button>
                </div>
                {validationStatus.grok === 'valid' && (
                  <p className="text-green-400 text-xs mt-1">✅ API key is valid!</p>
                )}
                {validationStatus.grok === 'invalid' && (
                  <p className="text-red-400 text-xs mt-1">❌ {validationErrors.grok || 'Invalid API key'}</p>
                )}
                <p className="text-gray-500 text-xs mt-1">
                  Get from: <a href="https://console.x.ai/" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">console.x.ai</a>
                </p>
              </div>

              <div className="bg-yellow-900 bg-opacity-30 border border-yellow-600 rounded p-3 text-sm text-yellow-200">
                <p className="font-semibold mb-1">🔒 Security Note:</p>
                <p>API keys are stored in your browser's local storage only. They are sent to the backend to configure LLM players.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-900 px-6 py-4 border-t border-gray-700 flex justify-between sticky bottom-0">
          <button
            onClick={handleReset}
            className="bg-gray-600 hover:bg-gray-500 text-white font-bold py-2 px-6 rounded-lg transition-colors"
          >
            Reset to Defaults
          </button>
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="bg-gray-600 hover:bg-gray-500 text-white font-bold py-2 px-6 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="btn-primary"
            >
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;

