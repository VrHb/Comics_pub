import random
import os

from dotenv import load_dotenv

import requests


COUNTED_COMICS = 2647
FIRST_COMICS = 1

def fetch_xkcd(comics_id: int) -> dict:
    response = requests.get(
        url=f"https://xkcd.com/{comics_id}/info.0.json"
    )
    response.raise_for_status()
    image_url = response.json()["img"]
    image_file = os.path.basename(image_url)
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    with open(image_file, "wb") as file:
        file.write(image_response.content)
    author_comment = response.json()["alt"]
    return {"comment": author_comment, "image_file": image_file}


def get_from_vk(method: str, payload: dict):
    url = f"https://api.vk.com/method/{method}"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()["response"]


def post_image_to_vkserver(url: str, filename: str) -> dict:
    with open(filename, 'rb') as file:
        files = {'photo': file}
        response = requests.post(url, files=files)
    response.raise_for_status()
    return response.json()


def post_to_vk(method: str, payload: dict):
    response = requests.post(
        url = f"https://api.vk.com/method/{method}",
        params=payload,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    load_dotenv()
    VK_TOKEN = str(os.getenv("VK_TOKEN"))
    VK_GROUP_ID = int(os.getenv("VK_GROUP_ID"))
    random_comics_id = random.choice(range(FIRST_COMICS, COUNTED_COMICS))
    comics_information = fetch_xkcd(random_comics_id)
    vk_uploadserver_params = get_from_vk(
        method="photos.getWallUploadServer",
        payload={
            "access_token": VK_TOKEN,
            "group_id": VK_GROUP_ID,
            "v": 5.131
        }
    )
    vkserver_params = post_image_to_vkserver(
        vk_uploadserver_params["upload_url"],
        filename=comics_information["image_file"]
    )
    vk_saved_image_params = post_to_vk(
        method="photos.saveWallPhoto",
        payload={
            "access_token": VK_TOKEN,
            "v": 5.131,
            "group_id": VK_GROUP_ID,
            "server": vkserver_params["server"],
            "photo": vkserver_params["photo"],
            "hash": vkserver_params["hash"]
        }
    )["response"][0]
    image_owner_id = vk_saved_image_params['owner_id']
    image_id = vk_saved_image_params['id']
    post_to_vk(
        method="wall.post",
        payload={
            "access_token": VK_TOKEN,
            "v": 5.131,
            "owner_id": -(VK_GROUP_ID),
            "from_group": 1,
            "attachments": [
                f"photo{image_owner_id}_{image_id}",
            ],
            "message": f"{comics_information['comment']}"
        }
    )
    removed_image_file = os.remove(comics_information["image_file"])
