BEGIN;
CREATE TABLE IF NOT EXISTS urls (
  id SERIAL PRIMARY KEY,
  url VARCHAR(255) DEFAULT '',
  protocol VARCHAR(255) DEFAULT '',
  domain VARCHAR(255) DEFAULT '',
  subdomain VARCHAR(255) DEFAULT '',
  path VARCHAR(255) DEFAULT '',
  is_phishing BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
COMMIT;
