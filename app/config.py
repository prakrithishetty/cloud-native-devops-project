import os


class Config:
    APP_NAME = os.getenv(
        "APP_NAME",
        "Cloud-Native DevOps Platform"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://devops:devops_password@127.0.0.1:5433/devopsdb"
    )
