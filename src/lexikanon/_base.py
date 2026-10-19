from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    """Base for lexikanon's config objects: extra keys allowed, as in the 1.x models."""

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
