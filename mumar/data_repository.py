"""Module with generic data management mechanism."""
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, RootModel

from mumar.utils.exceptions import ExactFileNotFoundError


class DataRepository[T: BaseModel]:
    """Data management generic class for pydantic.BaseModel types.

    The DataRepository class provides a flexible data management mechanism
    for various data models used within a project. It serves as a repository
    for storing, loading, and manipulating models data based on provided Pydantic BaseModel types.
    """

    def __init__(self, model: type[T], filepath: Path | None = None) -> None:
        """Constructor for concrete DataRepository with the same type as model.

        Args:
            model: Entity data model - base type of the data repository, determine the data model type.
            filepath: Optional path to the file with data. If provided, data will be read from the file.
        """
        self.entity = model
        """Pydantic BaseModel class."""

        self.root_model = RootModel[dict[int, model]]
        """Container and validator class for data."""

        init_data = {}
        if filepath:
            if filepath.is_file():
                init_data = self._load_from_csv(filepath)
            else:
                raise ExactFileNotFoundError(filepath)

        self.data = self.root_model.model_validate(init_data)
        """Root model instance with data."""

    @staticmethod
    def _load_from_csv(filepath: Path | str) -> dict[int, dict]:
        """Load data from file in a CSV format and return it as a dict.

        Args:
            filepath: Path to the file to store the model data.

        Returns:
            Dict with loaded data where the key is index and the value is serialized model.
        """
        data_from_file = pd.read_csv(filepath, sep=",", index_col=0)
        serialized_data = data_from_file.to_dict(orient="index")

        return serialized_data

    def to_csv(self, filepath: str) -> None:
        """Stores data to file in a CSV format.

        Args:
            filepath: Path to the file to store the model data.
        """
        loaded_dumped_data = pd.DataFrame.from_dict(self.data.model_dump(), orient="index")
        loaded_dumped_data.to_csv(filepath, sep=",", index_label="index")


if __name__ == "__main__":

    class AlbumEntity(BaseModel):
        """Tmp album entity class."""

        id: int
        name: str

    class SongEntity(BaseModel):
        """Tmp song entity class."""

        id: int
        song_nr: int

    a1 = AlbumEntity(id=1, name="a")
    a2 = AlbumEntity(id=2, name="b")
    s1 = SongEntity(id=1, song_nr=1)
    s2 = SongEntity(id=2, song_nr=2)

    album_repository = DataRepository[AlbumEntity](AlbumEntity)
    song_repository = DataRepository[SongEntity](SongEntity)
