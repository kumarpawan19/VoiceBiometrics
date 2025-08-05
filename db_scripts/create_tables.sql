DROP TABLE IF EXISTS voice_embeddings;

CREATE TABLE voice_embeddings (
    user_id VARCHAR PRIMARY KEY,
    embedding TEXT NOT NULL
);
