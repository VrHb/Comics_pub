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


def test_vk(method: str, token: str) -> str:
    url = f"https://api.vk.com/method/{method}"
    payload = {
        "access_token": token,
        "v": 5.131
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    vk_info = response.json()
    return vk_info
   

if __name__ == "__main__":
    load_dotenv()
    VK_TOKEN = str(os.getenv("VK_TOKEN"))
    # print(fetch_comics(353))
    print(VK_TOKEN)
    print(test_vk(method="groups.get", token=VK_TOKEN))
