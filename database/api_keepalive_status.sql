CREATE TABLE IF NOT EXISTS api_keepalive_status (
    id INTEGER PRIMARY KEY DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'idle',
    last_ping_time TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    error_message TEXT,
    CONSTRAINT check_single_row CHECK (id = 1)
);

INSERT INTO api_keepalive_status (id, status)
VALUES (1, 'idle')
ON CONFLICT (id) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_status ON api_keepalive_status(status);

ALTER TABLE api_keepalive_status ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow service role access"
ON api_keepalive_status
FOR ALL
TO service_role
USING (true);
