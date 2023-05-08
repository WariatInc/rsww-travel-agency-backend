from src.app import create_app, configure_consumers
from src.config import ProductionConfig


app = create_app(config=ProductionConfig)
