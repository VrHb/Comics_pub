import random
import os

from dotenv import load_dotenv

import requests


COUNTED_COMICS = 2647
FIRST_COMICS = 1
VK_API_VERSION = 5.131

class VKWrongDataException(Exception):
    pass 


def fetch_xkcd(comics_id: int) -> dict:
    response = requests.get(
        url=f"https://xkcd.com/{comics_id}/info.0.json"
    )
    response.raise_for_status()
    image_url = response.json()["img"]
    filename = os.path.basename(image_url)
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    with open(filename, "wb") as file:
        file.write(image_response.content)
    author_comment = response.json()["alt"]
    return {"comment": author_comment, "image_file": filename}


def get_from_vk(method: str, payload: dict) -> dict:
    url = f"https://api.vk.com/method/{method}"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response_params = response.json()
    if check_vk_errors(response_params):
        return check_vk_errors(response_params)
    return response_params["response"]


def post_image_to_vk(filename: str) -> dict:
    upload_server_params = get_from_vk(
            method="photos.getWallUploadServer",
            payload={
                "access_token": VK_TOKEN,
                "group_id": VK_GROUP_ID,
                "v": VK_API_VERSION
            }
        )
    with open(filename, 'rb') as file:
        files = {'photo': file}
        response_server_params = requests.post(
            upload_server_params["upload_url"],
            files=files
        )
    response_server_params.raise_for_status()
    server_params = response_server_params.json()
    if check_vk_errors(server_params):
        return check_vk_errors(server_params)
    save_image_response = requests.post(
        url = "https://api.vk.com/method/photos.saveWallPhoto",
        params={
            "access_token": VK_TOKEN,
            "v": VK_API_VERSION,
            "group_id": VK_GROUP_ID,
            "server": server_params["server"],
            "photo": server_params["photo"],
            "hash": server_params["hash"]
        }
    )
    save_image_response.raise_for_status()
    if check_vk_errors(save_image_response.json()):
        return check_vk_errors(save_image_response.json())
    saved_image_params = save_image_response.json()["response"][0]
    image_owner_id = saved_image_params["owner_id"]
    image_id = saved_image_params["id"]
    post_image_response = requests.post(
        url = "https://api.vk.com/method/wall.post",
        params={
            "access_token": VK_TOKEN,
            "v": VK_API_VERSION,
            "owner_id": -(VK_GROUP_ID),
            "from_group": 1,
            "attachments": [
                f"photo{image_owner_id}_{image_id}",
            ],
            "message": f"{comics_information['comment']}"
        }
    )
    post_image_response.raise_for_status()
    if check_vk_errors(post_image_response.json()):
        return check_vk_errors(post_image_response.json())
    return post_image_response.json()


def check_vk_errors(vk_response_params: dict) -> dict | None:
    if vk_response_params.get("error"):
        raise VKWrongDataException(
            f"Код ошибки: {vk_response_params['error']['error_code']}",
            f"Текст ошибки: {vk_response_params['error']['error_msg']}"
        )


if __name__ == "__main__":
    try:
        load_dotenv()
        VK_TOKEN = str(os.getenv("VK_TOKEN"))
        VK_GROUP_ID = int(os.getenv("VK_GROUP_ID"))
        random_comics_id = random.choice(range(FIRST_COMICS, COUNTED_COMICS))
        comics_information = fetch_xkcd(random_comics_id)
        post_image_to_vk(comics_information["image_file"])
    finally:
        removed_image_file = os.remove(comics_information["image_file"])
