import random
import os

from dotenv import load_dotenv

import requests


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
    vk_data = response.json()["response"]
    return vk_data


def post_vk_upload_data(url: str, filename: str) -> dict:
    with open(filename, 'rb') as file:
        files = {'photo': file}
        response = requests.post(url, files=files)
        response.raise_for_status()
    vk_upload_data = response.json()
    return vk_upload_data


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
    random_comics_id = random.choice(range(1, 2645))
    comics_data = fetch_xkcd(random_comics_id)
    vk_uploadserver_data = get_from_vk(
        method="photos.getWallUploadServer",
        payload={
            "access_token": VK_TOKEN,
            "group_id": 214532128,
            "v": 5.131
        }
    )
    vk_upload_data = post_vk_upload_data(
        vk_uploadserver_data["upload_url"],
        filename=comics_data["image_file"]
    )
    vk_image_data = post_to_vk(
        method="photos.saveWallPhoto",
        payload={
            "access_token": VK_TOKEN,
            "v": 5.131,
            "group_id": 214532128,
            "server": vk_upload_data["server"],
            "photo": vk_upload_data["photo"],
            "hash": vk_upload_data["hash"]
        }
    )
    image_owner_id = vk_image_data['response'][0]['owner_id']
    image_id = vk_image_data['response'][0]['id']
    posted_image = post_to_vk(
        method="wall.post",
        payload={
            "access_token": VK_TOKEN,
            "v": 5.131,
            "owner_id": -214532128,
            "from_group": 1,
            "attachments": [
                f"photo{image_owner_id}_{image_id}",
            ],
            "message": f"{comics_data['comment']}"
        }
    )
    remove_image_file = os.remove(comics_data["image_file"])
