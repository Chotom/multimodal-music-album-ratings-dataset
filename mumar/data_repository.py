"""Module with generic data management mechanism."""
from typing import Self

import pandas as pd
from pydantic import RootModel, BaseModel


class DataRepository[T: BaseModel]:
    """Data management generic class for pydantic.BaseModel types.

    The DataRepository class provides a generic data management mechanism for various data models used within a project.
    """

    def __init__(self, model: type[T]) -> None:
        """Constructor for concrete DataRepository with the same type as model.

        Args:
            model: Entity data model - base type of the data repository, determine the data model type.
        """
        self.entity = model
        """Pydantic BaseModel class."""

        self.data_model = RootModel[dict[int, T]]({})
        """Container and validator for data."""

        self.data = self.data_model.root
        """Pointer to the 'root' attribute of a Pydantic RootModel."""

    @classmethod
    def from_csv(cls, model: type[T], filepath: str) -> Self:
        """Stores data in file in a CSV format.

        Args:
            model: Entity data model - base type of the repository, determine the data model type.
            filepath: Path to the file to store the model data.

        Returns:
            New instance of the DataRepository class with loaded data from a CSV file at the specified filepath.
        """
        repo = cls(model)
        df = pd.read_csv(filepath, sep=",")
        df.to_dict(orient="index")

        return repo

    def to_csv(self, filepath: str):
        """Stores data in file in a CSV format.

        Args:
            filepath: Path to the file to store the model data.
        """
        df = pd.DataFrame.from_dict(self.data, orient="index")
        df.to_csv(filepath, sep=",")


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

    AlbumRepository = DataRepository[AlbumEntity](AlbumEntity)
