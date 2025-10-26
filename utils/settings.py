from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # 讓它在本地開發時可以從 .env 讀取，但當環境變數存在時優先使用環境變數
        env_file=".env",
        # 允許忽略 .env 文件，如果部署環境沒有這個文件，它會去讀取 os.environ
        env_ignore_empty=True,
        extra="ignore",
    )

    TOKEN: str
    CHANNEL_ID: str
    GUILD_ID: Optional[str] = None


settings = Settings()
