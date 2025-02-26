from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
from actions.api.apiGoogle import apiGoogleBooks
from actions.constants.messages import ASK_LIVRO_CORRETO
import requests

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")
 
        return []

class ActionProcuraLivros(Action):

    def name(self) -> Text:
        return "action_procura_livros"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Formata o livro para pesquisa
        livro = tracker.get_slot('livro')
        livro_pesquisa = livro.replace(" ", "+")
        
        # Faz a pesquisa do livro
        pesquisa = requests.get(f"{apiGoogleBooks}{livro_pesquisa}")
        livros_json = pesquisa.json()
        if 'items' in livros_json and len(livros_json['items']) > 0:
            titulo = livros_json['items'][0]['volumeInfo'].get('title', 'Título não encontrado') 

            print("O titulo do livro não é igual ao que o usuário digitou")

            buttons = [
                {"title": "Sim", "payload": f"/confirmar{{\"livro\": \"{titulo}\"}}"},
                {"title": "Não", "payload": "/negar"}
            ]

            dispatcher.utter_message(text=ASK_LIVRO_CORRETO.format(titulo=titulo), buttons=buttons)

        else:
            
            dispatcher.utter_message(text="Nenhum livro encontrado.")

        return []