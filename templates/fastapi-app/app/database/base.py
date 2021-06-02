# Import all the models, so that Base has them before being
# imported by Alembic
from app.database.base_class import Base  # noqa: F401

# from app.models.<REPO_NAME> import <Models for this service>  # noqa: F401
