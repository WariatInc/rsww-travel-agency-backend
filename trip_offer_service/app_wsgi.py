from src.app import create_app
from src.config import ProductionConfig

app = create_app(config=ProductionConfig)
