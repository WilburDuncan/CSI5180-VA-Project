# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa-pro/concepts/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.anilist import *
import asyncio

class ActionGetDescription(Action):
 
    def name(self) -> Text:
        return "action_get_description"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("ani_title")
        clean_desc = getDescription(name)
        voice_desc = "Here is the description of Anime " + name +  ":\n"  + clean_desc
        # Chat output
        dispatcher.utter_message(text = voice_desc)
 
        return []

class ActionRcmdAni(Action):

    def name(self) -> Text:
        return "action_rcmd_ani"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        genre=tracker.get_slot("ani_genre")
        text=f"Nice choice! Here are the top five {genre} anime series:\n{getRcmdAni(genre)}"
        dispatcher.utter_message(text)

        return []
    
class ActionIntro(Action):

    def name(self) -> Text:
        return "action_intro_main"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name=tracker.get_slot("ani_name")
        text=f"Here are the three main characters of {name}:\n{getMainCharacter(name)}"
        dispatcher.utter_message(text)

        return []
    
class ActionIntroCh(Action):

    def name(self) -> Text:
        return "action_intro_ch"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name=tracker.get_slot("ch_name")
        text=f"Sure! Here is the description of {name}:\n{getCharacterDescription(name)}"
        dispatcher.utter_message(text)

        return []

