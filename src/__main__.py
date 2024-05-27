import uvicorn

from src.app import FastAPIWebApplication


def main():
    app = FastAPIWebApplication()
    app.run()


if __name__ == "__main__":
    uvicorn.run("src.app:asgi", host="0.0.0.0", port=8000, reload=True)
