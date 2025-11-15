export interface Player {
  id: string;
  name: string;
  stack: number;
  position: number;
  current_bet: number;
  folded: boolean;
  all_in: boolean;
  cards?: string[];
}

export interface HandActionLog {
  hand_number: number;
  player_id: string;
  player_name: string;
  action: string;
  amount: number;
  phase: string;
  timestamp: string;
}

export interface HandPlayerResult {
  player_id: string;
  player_name: string;
  cards: string[];
  hand: string;
  result: number;
  stack_start: number;
  stack_end: number;
  total_bet: number;
}

export interface HandSummary {
  hand_number: number;
  timestamp: string;
  board: string[];
  pot: number;
  winners: { player_id: string; player_name: string; amount: number }[];
  players: HandPlayerResult[];
  actions: HandActionLog[];
}

export interface GameState {
  game_id: string;
  phase: string;
  pot: number;
  current_bet: number;
  community_cards: string[];
  players: Player[];
  dealer_position: number;
  current_player: number;
  small_blind: number;
  big_blind: number;
  hand_history?: HandSummary[];
  current_hand_log?: HandActionLog[];
}

export interface CreateGameRequest {
  player_names: string[];
  ai_players: string[];
  ai_prompts?: string[];
  ai_names?: string[];
  small_blind: number;
  big_blind: number;
  starting_stack: number;
}

export interface PlayerActionRequest {
  player_id: string;
  action: string;
  amount: number;
}

