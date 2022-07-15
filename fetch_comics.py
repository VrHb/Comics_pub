import os

from dotenv import load_dotenv

import requests


def fetch_comics(comics_id: int) -> None:
    response = requests.get(
        url=f"https://xkcd.com/{comics_id}/info.0.json"
    )
    response.raise_for_status()
    image_url = response.json()["img"]
    author_comment = response.json()["alt"]
    return author_comment


def fetch_from_vk(method: str, payload: dict):
    url = f"https://api.vk.com/method/{method}"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    vk_info = response.json()["response"]
    return vk_info
   

def get_vk_upload_info(url: str) -> dict:
    with open('python.png', 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
    vk_upload_info = response.json()
    return vk_upload_info


def save_image_to_vk(method: str, payload: dict):
    response = requests.post(
        url = f"https://api.vk.com/method/{method}",
        params=payload,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    load_dotenv()
    VK_TOKEN = str(os.getenv("VK_TOKEN"))
    comics_info = fetch_comics(353)
    user_groups = fetch_from_vk(
        method="groups.get", 
        payload={
            "access_token": VK_TOKEN,
            "v": 5.131
        }
    )
    url_uploadserver = fetch_from_vk(
        method="photos.getWallUploadServer", 
        payload={
            "access_token": VK_TOKEN,
            "group_id": 214532128,
            "v": 5.131
        }
    )
    vk_upload_info = get_vk_upload_info(url_uploadserver["upload_url"])
    image_info = save_image_to_vk(
        method="photos.saveWallPhoto",
        payload={
            "access_token": VK_TOKEN,
            "v": 5.131,
            "group_id": 214532128,
            "server": vk_upload_info["server"],
            "photo": vk_upload_info["photo"],
            "hash": vk_upload_info["hash"]
        }
    )
    image_owner_id = image_info['response'][0]['owner_id']
    image_id = image_info['response'][0]['id']
    posted_image = save_image_to_vk(
        method="wall.post",
        payload={
            "access_token": VK_TOKEN,
            "v": 5.131,
            "owner_id": -214532128,
            "from_group": 1,
            "attachments": [
                f"photo{image_owner_id}_{image_id}", 
            ],
            "message": f"{comics_info}"
        }
    )
