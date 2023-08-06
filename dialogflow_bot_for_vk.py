import random
import os

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from google.cloud import dialogflow


def get_df_response(project_id, session_id, text, language_code="ru"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    query_input = dialogflow.QueryInput(text=dialogflow.TextInput(text=text, language_code=language_code))
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return None
    return response.query_result.fulfillment_text


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    load_dotenv(".env")
    vk_session = vk.VkApi(token=os.environ["VK_TOKEN"])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            df_response = get_df_response(os.environ["PROJECT_ID"], event.user_id, event.text)
            if df_response:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=df_response,
                    random_id=random.randint(1,1000)
                )