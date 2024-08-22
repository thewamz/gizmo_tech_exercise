import sqlite3
from flask import Flask, jsonify, request
import logging
from pydantic import BaseModel


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)

"""
Here are two sample endpoints to test the connection to the database and posting to the server.
Here's a sample curl request to test the post to the below sample route.
curl -X POST -H "Content-Type: application/json" -d '{"test_string":"test"}' http://localhost:5001/post

Please add the endpoint to this file.

You can specify the interface to the frontend using a pydantic model like the Body model below if you want, or do something better.
"""
def sql(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    column_names = [column[0] for column in cur.description]
    conn.close()
    return [dict(zip(column_names, row)) for row in results]

@app.route('/')
def sample_get_route():
    card_results = sql('SELECT * FROM card')
    deck_results = sql('SELECT * FROM deck')
    json_results = {'deck_results': deck_results, 'card_results': card_results}
    return jsonify(json_results)


"""

"""

class Body(BaseModel):
    test_string: str


@app.route('/post', methods=['POST'])
def sample_post_route():
    body = Body(**request.get_json())
    return jsonify(body.dict())


class GetDeckWithCardsRequest(BaseModel):
    deck_id: int


@app.route('/get_deck', methods=['POST'])
def get_deck():
    """A method to get all of a deck's cards and child decks
    """
    body = GetDeckWithCardsRequest(**request.get_json())
    card_results = sql(f'SELECT * FROM card WHERE deck_id = {body.deck_id}')
    deck_results = sql('SELECT * FROM deck WHERE parent_id = {body.deck_id}')
    json_results = {'deck_results': deck_results, 'card_results': card_results}
    return jsonify(json_results)


@app.route('/order', methods=['POST'])
def order():
    """
    {
        'deck_id': <int>,
        'deck_parent_id': <int>,
        'deck_order_number': <int>,
        'cards': [{'id': <int>, 'order_num': <int>}]
    }
    """
    deck_id = int(request.json['deck_id'])

    try:
        deck_parent_id = int(request.json['deck_parent_id'])
    except Exception:
        deck_parent_id = None

    try:
        deck_order_number = int(request.json['deck_order_number'])
    except Exception:
        deck_order_number = None

    cards = request.json['cards']

    # process ordering of decks
    if not cards:
        sql(
            f"""
            INSERT INTO DeckOrder (deck_id, deck_parent_id, order_number)
            VALUES ({deck_id}, {deck_parent_id}, {deck_order_number})
            """
        )
        return jsonify({
            'deck_id': deck_id,
            'deck_parent_id': deck_parent_id,
            'deck_order_number': deck_order_number,
        })

    # process ordering of cards within a deck
    for card in cards:
        sql(
            f"""
            INSERT INTO CardOrder (card_id, deck_id, order_number)
            VALUES ({card['id']}, {deck_id}, {card['order_num']})
            """
        )

    return jsonify({
        'deck_id': deck_id,
        'deck_parent_id': deck_parent_id,
        'deck_order_number': deck_order_number,
        'cards': cards
    })




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)