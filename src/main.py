from src.dependencies import db_connection
from src.app_manager import AppManager, AppManagerSettings

app_manager_settings = AppManagerSettings()
app = AppManager(
    app_manager_settings=app_manager_settings, db_connection=db_connection
).get_fast_api_app()
