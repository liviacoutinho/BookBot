from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
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

    apiGoogleBooks = "https://www.googleapis.com/books/v1/volumes?q="

    def name(self) -> Text:
        return "action_procura_livros"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        livro = tracker.get_slot('livro')
        livro_pesquisa = livro.replace(" ", "+")
        print(livro_pesquisa)

        Pesquisa_Livro = requests.get(f"{self.apiGoogleBooks}{livro_pesquisa}")
        livros_json = Pesquisa_Livro.json()

        # Extrair todos os títulos dos livros
        titulos = [item['volumeInfo']['title'] for item in livros_json.get('items', [])]

        # Enviar os títulos de volta ao usuário
        dispatcher.utter_message(text=f"Os títulos dos livros encontrados são: {', '.join(titulos)}")

        return []