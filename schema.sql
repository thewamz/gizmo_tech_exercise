DROP TABLE IF EXISTS deck;
CREATE TABLE deck (
deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
-- parent_id INTEGER,
created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY(parent_id) references deck(deck_id));

DROP TABLE IF EXISTS card;
CREATE TABLE card (
card_id INTEGER PRIMARY KEY AUTOINCREMENT,
content TEXT,
-- deck_id integer references deck(deck_id),
created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY(deck_id) references deck(deck_id));


CREATE TABLE CardOrder(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id INTEGER,
    deck_id INTEGER,
    order_number INTEGER,
    FOREIGN KEY(card) references card(card_id),
    FOREIGN KEY(deck_id) references deck(deck_id),
    created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE DeckOrder(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deck_id INTEGER,
    deck_parent_id INTEGER,
    order_number INTEGER,
    FOREIGN KEY(deck_id) references deck(deck_id),
    FOREIGN KEY(deck_parent_id) references deck(deck_id));
    created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
);


INSERT INTO deck (name) VALUES ('deck1');
INSERT INTO deck (name) VALUES ('deck2');
INSERT INTO deck (name) VALUES ('deck3');

INSERT INTO card (content) VALUES ('card 1');
INSERT INTO card (content) VALUES ('card 2');
INSERT INTO card (content) VALUES ('card 3');
INSERT INTO card (content) VALUES ('card 4');
