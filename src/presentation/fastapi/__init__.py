from fastapi.templating import Jinja2Templates
import os

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template")
print(TEMPLATE_PATH)
templates = Jinja2Templates(directory=TEMPLATE_PATH)