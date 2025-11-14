"""LLM-based AI strategies using external APIs"""
from typing import Tuple, List, Optional
import httpx
import json
import os
from ..game_engine.engine import GameState, PlayerAction


class LLMStrategy:
    """Base class for LLM-based poker strategies"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        # Each instance gets its own client - no sharing between AI players!
        self._client = None
    
    @property
    def client(self):
        """Lazy-load client to avoid sharing between instances"""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=10.0))
        return self._client
    
    def _build_prompt(
        self,
        state: GameState,
        player_id: str,
        custom_instructions: Optional[str] = None
    ) -> str:
        """Build a poker decision prompt for the LLM"""
        player = next((p for p in state.players if p.id == player_id), None)
        if not player:
            return ""
        
        # Get player's position
        player_index = next((i for i, p in enumerate(state.players) if p.id == player_id), 0)
        total_players = len([p for p in state.players if not p.folded])
        position_names = {0: "Button (Dealer)", 1: "Small Blind", 2: "Big Blind"}
        position = position_names.get(player_index, f"Position {player_index + 1}")
        
        # Get player's cards
        cards_str = f"{player.cards[0]}, {player.cards[1]}" if player.cards else "unknown"
        
        # Get community cards
        if state.community_cards:
            community = ", ".join(str(c) for c in state.community_cards)
        else:
            community = "none yet (pre-flop)"
        
        # Get game state info
        pot = state.pot
        current_bet = state.current_bet
        player_bet = player.current_bet
        to_call = current_bet - player_bet
        stack = player.stack
        
        # Get detailed player info
        other_players = []
        for i, p in enumerate(state.players):
            if p.id == player_id:
                continue
            status = ""
            if p.folded:
                status = " [FOLDED]"
            elif p.all_in:
                status = " [ALL-IN]"
            
            pos_name = position_names.get(i, f"Pos {i + 1}")
            other_players.append(
                f"  {p.name} ({pos_name}): Stack=${p.stack}, Bet=${p.current_bet}{status}"
            )
        
        # Build action constraints
        can_check = (to_call == 0)
        min_raise = current_bet + state.big_blind if current_bet > 0 else state.big_blind
        
        prompt = f"""You are an expert Texas Hold'em poker player. Analyze this situation and make the best decision.

=== GAME INFORMATION ===
Game Type: No-Limit Texas Hold'em
Small Blind: ${state.small_blind}
Big Blind: ${state.big_blind}
Current Phase: {state.phase.value.upper()}
Total Players Active: {total_players}

=== YOUR POSITION ===
Position: {position}
Your Name: {player.name}

=== YOUR HAND ===
Hole Cards: {cards_str}
Community Cards: {community}

=== CURRENT BETTING ===
Pot Size: ${pot}
Current Bet to Match: ${current_bet}
Your Bet So Far: ${player_bet}
Amount to Call: ${to_call}
Your Remaining Stack: ${stack}

=== OTHER PLAYERS ===
{chr(10).join(other_players)}

=== AVAILABLE ACTIONS ===
"""
        
        if can_check:
            prompt += f"- check: No bet to call, pass action to next player\n"
        else:
            prompt += f"- call: Match current bet of ${to_call}\n"
        
        prompt += f"- fold: Give up this hand and lose your ${player_bet} already bet\n"
        
        if stack > min_raise:
            prompt += f"- raise: Increase bet (minimum raise to ${min_raise}, maximum ${stack})\n"
        
        prompt += f"- all_in: Bet all remaining ${stack} chips\n"
        
        prompt += f"""
=== RESPONSE FORMAT ===
Respond with ONLY a valid JSON object in this EXACT format:
{{"action": "fold", "amount": 0}}

Valid actions: "fold", "check", "call", "raise", "all_in"

Rules:
- For "fold", "check", "call", "all_in": amount must be 0
- For "raise": amount must be the TOTAL bet amount (not the raise amount)
  Example: If current bet is $50 and you want to raise to $100, use amount: 100
- Minimum raise amount: ${min_raise}
- Maximum raise amount: ${stack}

=== STRATEGIC CONSIDERATIONS ===
1. Hand Strength: Evaluate your hole cards + community cards
2. Position: {"Early position - be more selective" if player_index < 3 else "Late position - more flexibility"}
3. Pot Odds: Pot is ${pot}, you need ${to_call} to call
4. Stack Sizes: Monitor other players' stacks for all-in potential
5. Betting Patterns: Consider how much others have bet
6. Phase: {state.phase.value} - {"More cards coming" if state.phase.value in ["pre_flop", "flop", "turn"] else "Final decision"}

"""
        
        if custom_instructions:
            prompt += f"""
=== CUSTOM STRATEGY INSTRUCTIONS ===
{custom_instructions}
"""
        
        prompt += "\nYour decision (JSON only):"
        
        return prompt
    
    def call_llm_sync(self, prompt: str) -> dict:
        """Call the LLM API synchronously - to be implemented by subclasses"""
        raise NotImplementedError
    
    async def call_llm(self, prompt: str) -> dict:
        """Call the LLM API asynchronously - to be implemented by subclasses"""
        raise NotImplementedError
    
    def decide(
        self,
        state: GameState,
        player_id: str,
        valid_actions: List[PlayerAction],
        custom_instructions: Optional[str] = None
    ) -> Tuple[PlayerAction, int]:
        """Make a poker decision using LLM"""
        try:
            prompt = self._build_prompt(state, player_id, custom_instructions)
            
            print(f"[LLM] ========== CALLING LLM API ==========")
            print(f"[LLM] Player: {player_id}")
            print(f"[LLM] Prompt length: {len(prompt)} characters")
            print(f"[LLM] Sending request to LLM...")
            
            # Call the LLM synchronously to avoid event loop issues
            response = self.call_llm_sync(prompt)
            
            print(f"[LLM] ========== LLM RESPONSE ==========")
            print(f"[LLM] Response: {response}")
            print(f"[LLM] ======================================")
            
            action_str = response.get("action", "fold").lower()
            amount = response.get("amount", 0)
            
            # Map string to PlayerAction
            action_map = {
                "fold": PlayerAction.FOLD,
                "check": PlayerAction.CHECK,
                "call": PlayerAction.CALL,
                "raise": PlayerAction.RAISE,
                "all_in": PlayerAction.ALL_IN,
            }
            
            action = action_map.get(action_str, PlayerAction.FOLD)
            
            # Validate action is in valid_actions
            if action not in valid_actions:
                # Fallback to safe action
                if PlayerAction.CHECK in valid_actions:
                    return PlayerAction.CHECK, 0
                elif PlayerAction.CALL in valid_actions:
                    return PlayerAction.CALL, 0
                else:
                    return PlayerAction.FOLD, 0
            
            return action, amount
            
        except Exception as e:
            print(f"[LLM] ERROR calling LLM: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            # Fallback to safe conservative action
            print(f"[LLM] Falling back to safe action (check/call/fold)")
            if PlayerAction.CHECK in valid_actions:
                print(f"[LLM] Fallback: CHECK")
                return PlayerAction.CHECK, 0
            elif PlayerAction.CALL in valid_actions:
                print(f"[LLM] Fallback: CALL")
                return PlayerAction.CALL, 0
            print(f"[LLM] Fallback: FOLD")
            return PlayerAction.FOLD, 0


class OpenAIStrategy(LLMStrategy):
    """OpenAI GPT-based poker strategy"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        super().__init__(api_key, model)
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    async def call_llm(self, prompt: str) -> dict:
        """Call OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert poker player. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        response = await self.client.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        
        # Extract JSON from response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        return json.loads(content)


class DeepSeekStrategy(LLMStrategy):
    """DeepSeek-based poker strategy"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        super().__init__(api_key, model)
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
    
    def call_llm_sync(self, prompt: str) -> dict:
        """Call DeepSeek API synchronously using requests"""
        import requests
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are an expert poker player. Respond ONLY with a valid JSON object in the format: {\"action\": \"fold\", \"amount\": 0}. No other text."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 150
            }
            
            print(f"[DeepSeek] Sending request to {self.api_url}")
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30.0)
            
            print(f"[DeepSeek] Response status: {response.status_code}")
            
            if response.status_code != 200:
                error_text = response.text
                print(f"[DeepSeek] Error response: {error_text}")
                raise Exception(f"DeepSeek API error {response.status_code}: {error_text}")
            
            data = response.json()
            print(f"[DeepSeek] Response data: {data}")
            
            content = data["choices"][0]["message"]["content"].strip()
            print(f"[DeepSeek] LLM content: {content}")
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            print(f"[DeepSeek] Parsed result: {result}")
            return result
            
        except json.JSONDecodeError as e:
            print(f"[DeepSeek] JSON decode error: {e}")
            print(f"[DeepSeek] Content was: {content}")
            raise Exception(f"Invalid JSON from DeepSeek: {content}")
        except Exception as e:
            print(f"[DeepSeek] Exception: {type(e).__name__}: {str(e)}")
            raise
    
    async def call_llm(self, prompt: str) -> dict:
        """Call DeepSeek API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are an expert poker player. Respond ONLY with a valid JSON object in the format: {\"action\": \"fold\", \"amount\": 0}. No other text."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 150
            }
            
            print(f"[DeepSeek] Sending request to {self.api_url}")
            response = await self.client.post(self.api_url, headers=headers, json=payload, timeout=30.0)
            
            print(f"[DeepSeek] Response status: {response.status_code}")
            
            if response.status_code != 200:
                error_text = response.text
                print(f"[DeepSeek] Error response: {error_text}")
                raise Exception(f"DeepSeek API error {response.status_code}: {error_text}")
            
            data = response.json()
            print(f"[DeepSeek] Response data: {data}")
            
            content = data["choices"][0]["message"]["content"].strip()
            print(f"[DeepSeek] LLM content: {content}")
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            print(f"[DeepSeek] Parsed result: {result}")
            return result
            
        except json.JSONDecodeError as e:
            print(f"[DeepSeek] JSON decode error: {e}")
            print(f"[DeepSeek] Content was: {content}")
            raise Exception(f"Invalid JSON from DeepSeek: {content}")
        except Exception as e:
            print(f"[DeepSeek] Exception: {type(e).__name__}: {str(e)}")
            raise


class ClaudeStrategy(LLMStrategy):
    """Anthropic Claude-based poker strategy"""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(api_key, model)
        self.api_url = "https://api.anthropic.com/v1/messages"
    
    async def call_llm(self, prompt: str) -> dict:
        """Call Claude API"""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "max_tokens": 200,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = await self.client.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        content = data["content"][0]["text"].strip()
        
        # Extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        return json.loads(content)


class GeminiStrategy(LLMStrategy):
    """Google Gemini-based poker strategy"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        super().__init__(api_key.strip(), model)
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    def _build_payload(self, prompt: str) -> dict:
        return {
            "contents": [{
                "parts": [{
                    "text": f"You are an expert poker player. Respond only with valid JSON.\n\n{prompt}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 150
            }
        }
    
    def _parse_response(self, data: dict) -> dict:
        candidates = data.get("candidates") or []
        if not candidates:
            raise KeyError("candidates")
        
        text_content = ""
        for candidate in candidates:
            content = candidate.get("content")
            parts_list = []
            if isinstance(content, dict):
                parts_list = content.get("parts") or []
            elif isinstance(content, list):
                parts_list = content
            
            for part in parts_list:
                if isinstance(part, dict):
                    if "text" in part:
                        text_content = part["text"].strip()
                        break
                    elif "inlineData" in part and "data" in part["inlineData"]:
                        text_content = part["inlineData"]["data"]
                        break
            if text_content:
                break
            
            if "text" in candidate:
                text_content = candidate["text"].strip()
                break
        
        if not text_content:
            raise KeyError("parts")
        
        content = text_content
        
        # Extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        return json.loads(content)
    
    def call_llm_sync(self, prompt: str) -> dict:
        """Call Gemini API synchronously using requests"""
        import requests
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        
        payload = self._build_payload(prompt)
        response = requests.post(self.base_url, headers=headers, json=payload, timeout=30.0)
        print(f"[Gemini] Response status: {response.status_code}")
        if response.status_code != 200:
            raise Exception(f"Gemini API error {response.status_code}: {response.text}")
        
        data = response.json()
        return self._parse_response(data)
    
    async def call_llm(self, prompt: str) -> dict:
        """Call Gemini API asynchronously"""
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        
        payload = self._build_payload(prompt)
        response = await self.client.post(self.base_url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        return self._parse_response(data)


class GrokStrategy(LLMStrategy):
    """xAI Grok-based poker strategy"""
    
    def __init__(self, api_key: str, model: str = "grok-beta"):
        super().__init__(api_key, model)
        self.api_url = "https://api.x.ai/v1/chat/completions"
    
    async def call_llm(self, prompt: str) -> dict:
        """Call Grok API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert poker player. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        response = await self.client.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        
        # Extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        return json.loads(content)

