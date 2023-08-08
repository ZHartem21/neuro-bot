import random
import os

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from df_manager import get_df_response


if __name__ == "__main__":
    load_dotenv(".env")
    vk_session = vk.VkApi(token=os.environ["VK_TOKEN"])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            df_response, is_fallback = get_df_response(os.environ["PROJECT_ID"], event.user_id, event.text)
            if df_response and not is_fallback:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=df_response,
                    random_id=random.randint(1, 1000),
                )
