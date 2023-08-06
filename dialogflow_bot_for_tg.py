import os
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from google.cloud import api_keys_v2, dialogflow
from google.cloud.api_keys_v2 import Key

from dotenv import load_dotenv


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



def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Здравствуйте!",
    )


def echo(update: Update, context: CallbackContext) -> None:
    df_reply = get_df_reply(os.environ["PROJECT_ID"], update.message.chat_id, update.message.text)
    update.message.reply_text(df_reply)


def main() -> None:
    load_dotenv(".env")
    updater = Updater(os.environ["TG_TOKEN"])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
