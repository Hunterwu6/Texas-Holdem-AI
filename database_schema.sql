-- ============================================================================
-- Texas Hold'em AI Battle Simulator - Database Schema
-- ============================================================================
-- Database: PostgreSQL 15+
-- Connection: postgresql://postgres:Admin@123@localhost:5432/postgres
-- Version: 1.0
-- Created: 2025-11-13
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- 1. AI CONFIGURATION TABLES
-- ============================================================================

-- AI Configurations: Store AI agent configurations and connection details
CREATE TABLE ai_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    
    -- Connection settings
    connection_type VARCHAR(20) NOT NULL CHECK (connection_type IN ('REST', 'WebSocket', 'Local', 'gRPC')),
    endpoint VARCHAR(500),
    auth_config JSONB,
    timeout_ms INTEGER DEFAULT 5000,
    retry_policy JSONB DEFAULT '{"maxRetries": 3, "backoffMultiplier": 1.5}'::jsonb,
    
    -- Strategy configuration
    strategy_config JSONB NOT NULL,
    -- Example structure:
    -- {
    --   "type": "LAG",
    --   "vpip": 45,
    --   "pfr": 35,
    --   "threeBet": 12,
    --   "cbet": 75,
    --   "aggressionFactor": 4.0,
    --   "positionAdjustment": {...},
    --   "stackDepthAdaptation": {...}
    -- }
    
    -- Capabilities
    capabilities JSONB DEFAULT '{"supportedGames": ["NLH"], "maxPlayers": 9, "supportsHistory": true}'::jsonb,
    
    -- Performance tracking
    avg_response_time_ms INTEGER,
    success_rate DECIMAL(5,2),
    last_health_check TIMESTAMP,
    health_status VARCHAR(20) DEFAULT 'unknown' CHECK (health_status IN ('healthy', 'degraded', 'unhealthy', 'unknown')),
    
    -- Rate limiting
    rate_limit_rpm INTEGER DEFAULT 600,
    rate_limit_burst INTEGER DEFAULT 50,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'archived')),
    
    -- Metadata
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(name, version)
);

-- ============================================================================
-- 2. GAME TABLES
-- ============================================================================

-- Games: Main game sessions
CREATE TABLE games (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Game configuration
    game_type VARCHAR(20) DEFAULT 'NLH' CHECK (game_type IN ('NLH', 'PLO', 'Stud')),
    small_blind INTEGER NOT NULL,
    big_blind INTEGER NOT NULL,
    ante INTEGER DEFAULT 0,
    min_buy_in INTEGER,
    max_buy_in INTEGER,
    max_players INTEGER NOT NULL CHECK (max_players BETWEEN 2 AND 9),
    
    -- Game state
    status VARCHAR(20) NOT NULL CHECK (status IN ('waiting', 'active', 'paused', 'completed', 'cancelled')),
    current_phase VARCHAR(20) CHECK (current_phase IN ('waiting', 'pre_flop', 'flop', 'turn', 'river', 'showdown')),
    dealer_position INTEGER,
    current_hand_number INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    last_action_at TIMESTAMP,
    
    -- Metadata
    created_by VARCHAR(100),
    game_mode VARCHAR(20) DEFAULT 'cash' CHECK (game_mode IN ('cash', 'tournament', 'sitNgo')),
    notes TEXT
);

-- Game Players: Players participating in a game
CREATE TABLE game_players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    
    -- Player identification
    player_id UUID,  -- NULL for anonymous/guest players
    ai_config_id UUID REFERENCES ai_configurations(id) ON DELETE SET NULL,
    player_type VARCHAR(20) NOT NULL CHECK (player_type IN ('human', 'ai')),
    player_name VARCHAR(100) NOT NULL,
    
    -- Position and stack
    position INTEGER NOT NULL,  -- 0-8 (seat number)
    initial_stack INTEGER NOT NULL,
    current_stack INTEGER NOT NULL,
    total_buy_in INTEGER DEFAULT 0,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'sitting_out', 'disconnected', 'eliminated')),
    is_dealer BOOLEAN DEFAULT FALSE,
    is_small_blind BOOLEAN DEFAULT FALSE,
    is_big_blind BOOLEAN DEFAULT FALSE,
    
    -- Statistics (real-time)
    hands_played INTEGER DEFAULT 0,
    hands_won INTEGER DEFAULT 0,
    total_wagered INTEGER DEFAULT 0,
    total_won INTEGER DEFAULT 0,
    
    -- Timestamps
    joined_at TIMESTAMP DEFAULT NOW(),
    last_action_at TIMESTAMP,
    left_at TIMESTAMP,
    
    UNIQUE(game_id, position),
    CHECK (
        (player_type = 'human' AND player_id IS NOT NULL AND ai_config_id IS NULL) OR
        (player_type = 'ai' AND ai_config_id IS NOT NULL)
    )
);

-- ============================================================================
-- 3. HAND HISTORY TABLES
-- ============================================================================

-- Hands: Individual hand history
CREATE TABLE hands (
    id BIGSERIAL PRIMARY KEY,
    game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    hand_number INTEGER NOT NULL,
    
    -- Blind configuration
    dealer_position INTEGER NOT NULL,
    small_blind_position INTEGER NOT NULL,
    big_blind_position INTEGER NOT NULL,
    small_blind_amount INTEGER NOT NULL,
    big_blind_amount INTEGER NOT NULL,
    ante_amount INTEGER DEFAULT 0,
    
    -- Cards
    community_cards JSONB,  -- Array of cards: ["As", "Kh", "9d", "7c", "2s"]
    burn_cards JSONB,        -- For audit purposes
    
    -- Pot information
    pot_total INTEGER NOT NULL,
    rake INTEGER DEFAULT 0,
    side_pots JSONB,  -- Array of side pot objects
    
    -- Hand result
    winning_hand_type VARCHAR(50),  -- "Royal Flush", "Straight", etc.
    winners JSONB,  -- Array of winner player IDs and amounts
    
    -- Timestamps
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    duration_seconds INTEGER,
    
    UNIQUE(game_id, hand_number)
);

-- Hand Players: Players in each hand with their hole cards
CREATE TABLE hand_players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hand_id BIGINT NOT NULL REFERENCES hands(id) ON DELETE CASCADE,
    game_player_id UUID NOT NULL REFERENCES game_players(id) ON DELETE CASCADE,
    
    -- Hole cards (encrypted or hidden for fairness)
    hole_cards JSONB NOT NULL,  -- ["Ac", "Kd"]
    
    -- Position
    position INTEGER NOT NULL,
    stack_before INTEGER NOT NULL,
    stack_after INTEGER NOT NULL,
    
    -- Action summary
    total_invested INTEGER DEFAULT 0,
    amount_won INTEGER DEFAULT 0,
    is_winner BOOLEAN DEFAULT FALSE,
    
    -- Final hand
    best_hand JSONB,  -- Best 5-card combination
    hand_rank VARCHAR(50),  -- Hand ranking
    hand_rank_value INTEGER,  -- Numeric rank for comparison
    
    -- Status
    folded_at VARCHAR(20),  -- pre_flop, flop, turn, river, NULL if didn't fold
    went_to_showdown BOOLEAN DEFAULT FALSE,
    
    UNIQUE(hand_id, game_player_id)
);

-- Actions: All player actions during hands
CREATE TABLE actions (
    id BIGSERIAL PRIMARY KEY,
    hand_id BIGINT NOT NULL REFERENCES hands(id) ON DELETE CASCADE,
    game_player_id UUID NOT NULL REFERENCES game_players(id) ON DELETE CASCADE,
    
    -- Action details
    action_type VARCHAR(20) NOT NULL CHECK (action_type IN ('fold', 'check', 'call', 'bet', 'raise', 'all_in', 'post_sb', 'post_bb', 'post_ante')),
    amount INTEGER DEFAULT 0,
    
    -- Context
    phase VARCHAR(20) NOT NULL CHECK (phase IN ('pre_flop', 'flop', 'turn', 'river')),
    action_sequence INTEGER NOT NULL,  -- Order of action in the hand
    pot_before INTEGER NOT NULL,
    pot_after INTEGER NOT NULL,
    
    -- AI specific
    thinking_time_ms INTEGER,  -- How long AI took to decide
    ai_confidence DECIMAL(5,2),  -- Optional: AI's confidence in decision
    
    -- Timestamps
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Hand Results: Detailed results for each player in each hand
CREATE TABLE hand_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hand_id BIGINT NOT NULL REFERENCES hands(id) ON DELETE CASCADE,
    game_player_id UUID NOT NULL REFERENCES game_players(id) ON DELETE CASCADE,
    
    -- Cards
    hole_cards JSONB NOT NULL,
    community_cards JSONB,
    best_hand JSONB,
    
    -- Hand evaluation
    hand_rank VARCHAR(50) NOT NULL,
    hand_rank_value INTEGER NOT NULL,
    hand_description TEXT,  -- e.g., "Full House, Kings over Nines"
    
    -- Result
    amount_won INTEGER DEFAULT 0,
    is_winner BOOLEAN DEFAULT FALSE,
    win_type VARCHAR(20),  -- 'showdown', 'everyone_folded', 'split'
    
    -- Analysis
    equity_at_showdown DECIMAL(5,2),  -- Calculated equity %
    pot_odds DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(hand_id, game_player_id)
);

-- ============================================================================
-- 4. STATISTICS & ANALYTICS TABLES
-- ============================================================================

-- AI Statistics: Aggregated AI performance metrics
CREATE TABLE ai_statistics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ai_config_id UUID NOT NULL REFERENCES ai_configurations(id) ON DELETE CASCADE,
    
    -- Time period
    period_type VARCHAR(20) NOT NULL CHECK (period_type IN ('daily', 'weekly', 'monthly', 'all_time')),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    
    -- Basic stats
    hands_played INTEGER DEFAULT 0,
    hands_won INTEGER DEFAULT 0,
    
    -- Poker statistics
    vpip DECIMAL(5,2),  -- Voluntarily Put In Pot %
    pfr DECIMAL(5,2),   -- Pre-Flop Raise %
    three_bet DECIMAL(5,2),  -- 3-Bet %
    cbet DECIMAL(5,2),  -- Continuation Bet %
    fold_to_cbet DECIMAL(5,2),
    af DECIMAL(5,2),    -- Aggression Factor
    wtsd DECIMAL(5,2),  -- Went To Showdown %
    w_sd DECIMAL(5,2),  -- Won at Showdown %
    
    -- Profitability
    bb_per_100 DECIMAL(10,2),  -- Big blinds won per 100 hands
    total_profit INTEGER,
    total_invested INTEGER,
    roi DECIMAL(7,2),  -- Return on Investment %
    
    -- Performance
    avg_response_time_ms INTEGER,
    timeout_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2),
    
    -- Position stats
    position_stats JSONB,  -- Profitability by position
    -- {
    --   "BTN": {"hands": 100, "profit": 234, "vpip": 45.5},
    --   "CO": {"hands": 95, "profit": 187, "vpip": 38.2},
    --   ...
    -- }
    
    -- Hand range stats
    hand_range_stats JSONB,  -- Performance by starting hands
    -- {
    --   "AA": {"hands": 12, "winRate": 83.3, "profit": 456},
    --   "AKs": {"hands": 8, "winRate": 62.5, "profit": 123},
    --   ...
    -- }
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(ai_config_id, period_type, period_start, period_end)
);

-- Player Statistics: Human player statistics
CREATE TABLE player_statistics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL,
    
    -- Time period
    period_type VARCHAR(20) NOT NULL CHECK (period_type IN ('daily', 'weekly', 'monthly', 'all_time')),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    
    -- Basic stats
    hands_played INTEGER DEFAULT 0,
    hands_won INTEGER DEFAULT 0,
    games_played INTEGER DEFAULT 0,
    
    -- Poker statistics (same as AI stats)
    vpip DECIMAL(5,2),
    pfr DECIMAL(5,2),
    three_bet DECIMAL(5,2),
    cbet DECIMAL(5,2),
    af DECIMAL(5,2),
    wtsd DECIMAL(5,2),
    w_sd DECIMAL(5,2),
    
    -- Profitability
    bb_per_100 DECIMAL(10,2),
    total_profit INTEGER,
    total_invested INTEGER,
    roi DECIMAL(7,2),
    
    -- Behavioral
    avg_session_duration_minutes INTEGER,
    total_playtime_minutes INTEGER,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(player_id, period_type, period_start, period_end)
);

-- Hand Analysis: Cached analysis results
CREATE TABLE hand_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hand_id BIGINT NOT NULL REFERENCES hands(id) ON DELETE CASCADE,
    
    analysis_type VARCHAR(50) NOT NULL CHECK (analysis_type IN ('gto_deviation', 'equity_analysis', 'range_analysis', 'mistake_detection', 'optimal_action')),
    
    -- Analysis results
    analysis_data JSONB NOT NULL,
    -- Example for gto_deviation:
    -- {
    --   "action": "raise",
    --   "amount": 500,
    --   "gtoAction": "call",
    --   "gtoAmount": 200,
    --   "evLoss": -12.5,
    --   "severity": "minor",
    --   "suggestion": "Consider calling instead of raising in this spot"
    -- }
    
    analyzer_version VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(hand_id, analysis_type)
);

-- ============================================================================
-- 5. SYSTEM TABLES
-- ============================================================================

-- Users: System users (for admin panel)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Profile
    full_name VARCHAR(100),
    avatar_url VARCHAR(500),
    
    -- Permissions
    role VARCHAR(20) DEFAULT 'player' CHECK (role IN ('admin', 'ai_manager', 'analyst', 'player')),
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP
);

-- API Keys: For AI agent authentication
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    key_prefix VARCHAR(10) NOT NULL,  -- First 8 chars for identification
    
    -- Association
    ai_config_id UUID REFERENCES ai_configurations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Metadata
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Permissions
    scopes JSONB DEFAULT '["game:read", "game:action"]'::jsonb,
    rate_limit_rpm INTEGER DEFAULT 600,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    CHECK (
        (ai_config_id IS NOT NULL AND user_id IS NULL) OR
        (ai_config_id IS NULL AND user_id IS NOT NULL)
    )
);

-- Audit Logs: System audit trail
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    
    -- Who
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    username VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    
    -- What
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    
    -- Changes
    old_values JSONB,
    new_values JSONB,
    changes JSONB,  -- Diff of old_values and new_values
    
    -- Context
    request_method VARCHAR(10),
    request_path VARCHAR(500),
    status_code INTEGER,
    
    -- Result
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    
    -- Timestamp
    timestamp TIMESTAMP DEFAULT NOW()
);

-- System Config: Global system configuration
CREATE TABLE system_config (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,  -- Can be read by non-admins
    updated_by UUID REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- 6. INDEXES FOR PERFORMANCE
-- ============================================================================

-- Games indexes
CREATE INDEX idx_games_status ON games(status);
CREATE INDEX idx_games_created_at ON games(created_at DESC);
CREATE INDEX idx_games_active ON games(status) WHERE status = 'active';

-- Game Players indexes
CREATE INDEX idx_game_players_game_id ON game_players(game_id);
CREATE INDEX idx_game_players_player_id ON game_players(player_id);
CREATE INDEX idx_game_players_ai_config_id ON game_players(ai_config_id);

-- Hands indexes
CREATE INDEX idx_hands_game_id ON hands(game_id);
CREATE INDEX idx_hands_started_at ON hands(started_at DESC);
CREATE INDEX idx_hands_game_hand_number ON hands(game_id, hand_number);

-- Actions indexes
CREATE INDEX idx_actions_hand_id ON actions(hand_id);
CREATE INDEX idx_actions_game_player_id ON actions(game_player_id);
CREATE INDEX idx_actions_timestamp ON actions(timestamp DESC);
CREATE INDEX idx_actions_hand_sequence ON actions(hand_id, action_sequence);

-- Hand Results indexes
CREATE INDEX idx_hand_results_hand_id ON hand_results(hand_id);
CREATE INDEX idx_hand_results_player_id ON hand_results(game_player_id);
CREATE INDEX idx_hand_results_winner ON hand_results(is_winner) WHERE is_winner = TRUE;

-- Statistics indexes
CREATE INDEX idx_ai_stats_ai_id ON ai_statistics(ai_config_id);
CREATE INDEX idx_ai_stats_period ON ai_statistics(period_type, period_start DESC);
CREATE INDEX idx_player_stats_player_id ON player_statistics(player_id);
CREATE INDEX idx_player_stats_period ON player_statistics(period_type, period_start DESC);

-- Hand Analysis indexes
CREATE INDEX idx_hand_analysis_hand_id ON hand_analysis(hand_id);
CREATE INDEX idx_hand_analysis_type ON hand_analysis(analysis_type);

-- AI Configurations indexes
CREATE INDEX idx_ai_config_status ON ai_configurations(status) WHERE status = 'active';
CREATE INDEX idx_ai_config_name ON ai_configurations(name);

-- Audit Logs indexes
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);

-- API Keys indexes
CREATE INDEX idx_api_keys_ai_config ON api_keys(ai_config_id) WHERE is_active = TRUE;
CREATE INDEX idx_api_keys_user ON api_keys(user_id) WHERE is_active = TRUE;

-- ============================================================================
-- 7. TRIGGERS
-- ============================================================================

-- Update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_ai_configurations_updated_at BEFORE UPDATE ON ai_configurations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 8. VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Active games with player count
CREATE VIEW v_active_games AS
SELECT 
    g.id,
    g.game_type,
    g.small_blind,
    g.big_blind,
    g.status,
    g.current_phase,
    g.current_hand_number,
    g.created_at,
    g.started_at,
    COUNT(gp.id) as player_count,
    g.max_players,
    ARRAY_AGG(gp.player_name) as player_names
FROM games g
LEFT JOIN game_players gp ON g.id = gp.game_id AND gp.status = 'active'
WHERE g.status IN ('waiting', 'active')
GROUP BY g.id;

-- AI leaderboard
CREATE VIEW v_ai_leaderboard AS
SELECT 
    ac.id,
    ac.name,
    ac.version,
    s.hands_played,
    s.bb_per_100,
    s.total_profit,
    s.vpip,
    s.pfr,
    s.three_bet,
    s.w_sd,
    s.avg_response_time_ms
FROM ai_configurations ac
LEFT JOIN LATERAL (
    SELECT *
    FROM ai_statistics
    WHERE ai_config_id = ac.id AND period_type = 'all_time'
    ORDER BY period_start DESC
    LIMIT 1
) s ON TRUE
WHERE ac.status = 'active'
ORDER BY s.bb_per_100 DESC NULLS LAST;

-- Recent hands with details
CREATE VIEW v_recent_hands AS
SELECT 
    h.id,
    h.hand_number,
    g.id as game_id,
    g.small_blind,
    g.big_blind,
    h.pot_total,
    h.community_cards,
    h.winning_hand_type,
    h.started_at,
    h.duration_seconds,
    COUNT(DISTINCT hp.id) as player_count
FROM hands h
JOIN games g ON h.game_id = g.id
LEFT JOIN hand_players hp ON h.id = hp.hand_id
GROUP BY h.id, g.id
ORDER BY h.started_at DESC;

-- ============================================================================
-- 9. INITIAL DATA
-- ============================================================================

-- Insert default system configuration
INSERT INTO system_config (key, value, description, is_public) VALUES
    ('default_ai_timeout', '5000', 'Default AI decision timeout in milliseconds', true),
    ('max_ai_retries', '3', 'Maximum number of retry attempts for AI requests', true),
    ('min_players', '2', 'Minimum players to start a game', true),
    ('max_players', '9', 'Maximum players per game', true),
    ('enable_rake', 'false', 'Whether to collect rake from pots', false),
    ('rake_percentage', '2.5', 'Rake percentage (0-100)', false),
    ('max_rake', '50', 'Maximum rake per hand', false),
    ('session_timeout_minutes', '30', 'User session timeout', true),
    ('enable_analytics', 'true', 'Enable real-time analytics', true);

-- Insert default admin user (password: admin123 - CHANGE THIS!)
-- Password hash is bcrypt of "admin123"
INSERT INTO users (username, email, password_hash, full_name, role) VALUES
    ('admin', 'admin@poker-simulator.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oDPxvHmJ7bPi', 'System Administrator', 'admin');

-- ============================================================================
-- 10. FUNCTIONS FOR COMMON OPERATIONS
-- ============================================================================

-- Function to calculate player statistics for a time period
CREATE OR REPLACE FUNCTION calculate_player_stats(
    p_player_id UUID,
    p_start_date DATE,
    p_end_date DATE
)
RETURNS TABLE (
    hands_played BIGINT,
    hands_won BIGINT,
    vpip DECIMAL,
    pfr DECIMAL,
    total_profit BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(DISTINCT hp.hand_id)::BIGINT,
        COUNT(DISTINCT CASE WHEN hr.is_winner THEN hp.hand_id END)::BIGINT,
        (COUNT(DISTINCT CASE WHEN a.action_type IN ('call', 'bet', 'raise') AND a.phase = 'pre_flop' THEN hp.hand_id END)::DECIMAL / 
         NULLIF(COUNT(DISTINCT hp.hand_id), 0) * 100)::DECIMAL(5,2),
        (COUNT(DISTINCT CASE WHEN a.action_type IN ('bet', 'raise') AND a.phase = 'pre_flop' THEN hp.hand_id END)::DECIMAL / 
         NULLIF(COUNT(DISTINCT hp.hand_id), 0) * 100)::DECIMAL(5,2),
        SUM(hp.amount_won - hp.total_invested)::BIGINT
    FROM hand_players hp
    JOIN hands h ON hp.hand_id = h.id
    JOIN game_players gp ON hp.game_player_id = gp.id
    LEFT JOIN hand_results hr ON hp.hand_id = hr.hand_id AND hp.game_player_id = hr.game_player_id
    LEFT JOIN actions a ON h.id = a.hand_id AND gp.id = a.game_player_id
    WHERE gp.player_id = p_player_id
      AND h.started_at >= p_start_date
      AND h.started_at < p_end_date + INTERVAL '1 day';
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- Grant permissions (adjust as needed for your security model)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO poker_app;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO poker_app;

-- Display table count
SELECT 'Schema created successfully!' as message;
SELECT 'Total tables: ' || COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';

