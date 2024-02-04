from pathlib import Path

import pandas as pd
import pytest
from pydantic import BaseModel

from mumar.data_repository import DataRepository
from mumar.utils.exceptions import ExactFileNotFoundError


class TestEntity(BaseModel):
    id: int
    name: str


class TestDataRepository:
    @pytest.fixture()
    def test_file(self, tmp_path: Path) -> Path:
        test_file = tmp_path / "test_data.csv"
        test_file.write_text("index,id,name\n1,1,a\n2,2,b")

        return test_file

    def test_constructor_without_file(self):
        repository = DataRepository[TestEntity](TestEntity)
        assert repository.data.model_dump() == {}

    def test_constructor_with_existing_file(self, test_file: Path):
        repository = DataRepository[TestEntity](TestEntity, filepath=test_file)
        assert repository.data.model_dump() == {
            1: {"id": 1, "name": "a"},  # Row 1
            2: {"id": 2, "name": "b"},  # Row 2
        }

    @pytest.mark.parametrize("filepath", [Path("nonexistent_file.csv"), Path("invalid_path")])
    def test_constructor_with_nonexistent_file(self, filepath: Path):
        with pytest.raises(ExactFileNotFoundError):
            DataRepository[TestEntity](TestEntity, filepath=filepath)

    def test_to_csv(self, tmp_path: Path, test_file: Path):
        test_output_path = tmp_path / "test_output.csv"

        repository = DataRepository[TestEntity](TestEntity, filepath=test_file)
        repository.to_csv(test_output_path)

        expected_data = pd.DataFrame({"index": [1, 2], "id": [1, 2], "name": ["a", "b"]})
        pd.testing.assert_frame_equal(pd.read_csv(test_output_path), expected_data)
