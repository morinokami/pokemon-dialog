import random

import dialogflow_v2 as dialogflow
from flask import Flask
from flask import request
import requests

app = Flask(__name__)


@app.route("/")
def root():
    return app.send_static_file("index.html")


@app.route("/dialog", methods=["POST"])
def dialog():
    if request.method == "POST":
        response = detect_intent(
            "pokemon-dialog",
            random.randint(2 ** 10, 2 ** 20),
            request.json["input"],
            "en",
        )

        if response.query_result.parameters:
            pokemon = response.query_result.parameters.fields[
                "name-pokemon"
            ].string_value.lower()
            res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
            if res.ok:
                return {"data": pokemon_desc(res.json())}
            else:
                return {"data": "Sorry, I didn't get that"}
        else:
            return {"data": response.query_result.fulfillment_text}


def detect_intent(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    return session_client.detect_intent(session=session, query_input=query_input)


def pokemon_desc(poke_json):
    fortune = random.randint(0, 2)
    if fortune == 0:
        return f'{poke_json["name"]} is a {poke_json["types"][0]["type"]["name"]}-type Pokémon'
    elif fortune == 1:
        return f'{poke_json["name"]} is {poke_json["height"]} decimeters tall'
    else:
        return f'{poke_json["name"]}\'s body weight is {poke_json["weight"]} hectograms'
