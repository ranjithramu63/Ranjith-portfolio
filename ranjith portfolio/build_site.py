from pathlib import Path
from shutil import copytree

from app import app


OUTPUT_DIRECTORY = Path("public")
ROUTES = ("/", "/about", "/skills", "/projects", "/certifications", "/contact")


def output_path(route: str) -> Path:
    if route == "/":
        return OUTPUT_DIRECTORY / "index.html"
    return OUTPUT_DIRECTORY / route.strip("/") / "index.html"


def build_site() -> None:
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    copytree("static", OUTPUT_DIRECTORY / "static")

    with app.test_client() as client:
        for route in ROUTES:
            response = client.get(route)
            if response.status_code != 200:
                raise RuntimeError(f"Failed to render {route}: HTTP {response.status_code}")

            destination = output_path(route)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(response.data)


if __name__ == "__main__":
    build_site()
