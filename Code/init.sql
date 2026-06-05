-- ============================================
-- Pokémon Budget Tracker – Datenbankschema
-- Modul 300
-- ============================================

CREATE DATABASE IF NOT EXISTS pokemon_tracker;
USE pokemon_tracker;

-- ============================================
-- Tabelle: cards
-- Gespeicherte Pokémon Karten (von TCG API)
-- ============================================
CREATE TABLE IF NOT EXISTS cards (
    id           VARCHAR(50) PRIMARY KEY,
    name         VARCHAR(255) NOT NULL,
    set_name     VARCHAR(255),
    image_url    VARCHAR(500),
    market_price DECIMAL(10,2),
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- Tabelle: entries
-- Alle Käufe und Verkäufe
-- ============================================
CREATE TABLE IF NOT EXISTS entries (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    type       ENUM('buy', 'sell', 'pack') NOT NULL,
    name       VARCHAR(255) NOT NULL,
    amount     DECIMAL(10,2) NOT NULL,
    date       DATE NOT NULL,
    card_id    VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_entries_card
        FOREIGN KEY (card_id)
        REFERENCES cards(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ============================================
-- Tabelle: portfolio
-- Aktuell gehaltene Karten
-- ============================================
CREATE TABLE IF NOT EXISTS portfolio (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    card_id   VARCHAR(50) NOT NULL UNIQUE,
    quantity  INT NOT NULL DEFAULT 1,
    buy_price DECIMAL(10,2) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_portfolio_card
        FOREIGN KEY (card_id)
        REFERENCES cards(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ============================================
-- Indexes
-- ============================================
CREATE INDEX idx_entries_date    ON entries(date);
CREATE INDEX idx_entries_type    ON entries(type);
CREATE INDEX idx_entries_card_id ON entries(card_id);
