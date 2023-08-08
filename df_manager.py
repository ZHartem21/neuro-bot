import os
import json
import argparse

from dotenv import load_dotenv
from google.cloud import dialogflow


def get_df_response(project_id, session_id, text, language_code="ru"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    query_input = dialogflow.QueryInput(text=dialogflow.TextInput(text=text, language_code=language_code))
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text, response.query_result.intent.is_fallback


def teach_df_from_json(project_id, filename="questions.json"):
    with open(filename, "r", encoding="utf8") as file:
        questions_file = file.read()
    questions = json.loads(questions_file)

    for intent, training_params in questions.items():
        create_intent(project_id, intent, training_params["questions"], training_params["answer"])


def create_intent(project_id, display_name, training_phrases_parts, message_texts, language_code="ru"):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrases.append(dialogflow.Intent.TrainingPhrase(parts=[part]))

    message = dialogflow.Intent.Message(text=dialogflow.Intent.Message.Text(text=[message_texts]))

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent, "language_code": language_code}
    )

    print("Intent created: {}".format(response))


def get_df_reply(project_id, session_id, text, language_code="ru"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    query_input = dialogflow.QueryInput(text=dialogflow.TextInput(text=text, language_code=language_code))
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


if __name__ == "__main__":
    load_dotenv('.env')

    parser = argparse.ArgumentParser(description="Dialogflow manager")
    parser.add_argument("filename", help="Filename for file to teach dialogflow from")
    args = parser.parse_args()

    teach_df_from_json(os.environ["PROJECT_ID"], args.filename)
