import requests


def fetch_comics() -> None:
    response = requests.get(
        url=f"https://imgs.xkcd.com/comics/python.png"
    )
    response.raise_for_status()
    with open("python.png", "wb") as file:
        file.write(response.content)


if __name__ == "__main__":
    fetch_comics()
    
