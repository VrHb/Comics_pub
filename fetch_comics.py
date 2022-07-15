import requests


def fetch_comics(comics_id: int) -> None:
    response = requests.get(
        url=f"https://xkcd.com/{comics_id}/info.0.json"
    )
    response.raise_for_status()
    image_url = response.json()["img"]
    author_comment = response.json()["alt"]
    return author_comment


if __name__ == "__main__":
    print(fetch_comics(353))
    
