import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pathlib import Path
from typing import Type, TypeVar, Optional

T = TypeVar("T", bound=BaseModel)


def load_env(pydantic_model: Type[T], dotenv_path: Optional[str] = None) -> T:
    """
    Load environment variables into a given Pydantic model.

    Args:
        pydantic_model (Type[T]): A Pydantic model class.
        dotenv_path (Optional[str]): Optional path to a .env file.

    Returns:
        T: An instance of the model populated with environment variables.
    """
    load_dotenv(dotenv_path=dotenv_path, override=True)

    env_values = {
        field_name: os.getenv(field_name)
        for field_name in pydantic_model.model_fields.keys()
    }

    return pydantic_model(**env_values)


def load_local_env(pydantic_model: Type[T], file_path: str) -> T:
    """
    Load environment variables from a .env file co-located with the file_path.
    e.g. to load a .env colocated with a given script/module, pass file_path=__file__

    Args:
        pydantic_model (Type[T]): A Pydantic model class.

    Returns:
        T: An instance of the model populated with environment variables.
    """
    dotenv_path = Path(file_path).parent / ".env"
    return load_env(pydantic_model, dotenv_path=dotenv_path)
