import tempfile

import pytest
from pydantic import ValidationError

from loom.abstracts import BaseDataClass


class SampleDataClass(BaseDataClass):
    a: int
    b: int
    c: int | None = None


class TestBaseDataClass:
    def setup_method(self) -> None:
        self.test_class = SampleDataClass(a=1, b=2)

    def test_to_dict(self) -> None:
        expected_dict = {"a": 1, "b": 2}

        assert self.test_class.as_dictionary == expected_dict
        assert "c" not in self.test_class.as_dictionary

    def test_to_json(self) -> None:
        expected_json = '{"a":1,"b":2}'

        assert self.test_class.as_json.strip() == expected_json

    def test_from_dict(self) -> None:
        input_dict = {"a": 3, "b": 4, "c": 5}
        instance = SampleDataClass.from_dictionary(input_dict)

        assert isinstance(instance, SampleDataClass)
        assert instance.a == 3
        assert instance.b == 4
        assert instance.c == 5

    def test_post_init(self) -> None:
        class CustomDataClass(SampleDataClass):
            def __post_init__(self) -> None:
                self.c = self.a + self.b

        instance = CustomDataClass(a=5, b=10)
        assert instance.c == 15

    def test_from_yaml(self) -> None:
        yaml_content = """
        a: 7
        b: 8
        c: 9
        """

        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".yaml", delete=False
        ) as temp_file:
            temp_file.write(yaml_content)
            temp_file_path = temp_file.name

        instance = SampleDataClass.from_yaml(temp_file_path)
        assert instance.a == 7
        assert instance.b == 8
        assert instance.c == 9

    def test_invalid_config_path(self) -> None:
        with pytest.raises(FileNotFoundError):
            SampleDataClass.from_yaml("non_existent_file.yaml")

    def test_as_json_includes_newline(self) -> None:
        json_output = self.test_class.as_json
        assert json_output.endswith("\n")

    def test_as_dictionary_with_none_values(self) -> None:
        instance = SampleDataClass(a=1, b=2, c=None)
        assert "c" not in instance.as_dictionary

    def test_from_dictionary_with_dict_config(self) -> None:
        from omegaconf import DictConfig

        config = DictConfig({"a": 10, "b": 20})
        instance = SampleDataClass.from_dictionary(config)
        assert instance.a == 10
        assert instance.b == 20

    def test_model_config_extra_forbid(self) -> None:
        with pytest.raises(ValidationError) as context:
            SampleDataClass(a=1, b=2, extra_field=3)  # type: ignore

        assert "Extra inputs are not permitted" in str(context.value)

    def test_validate_assignment(self) -> None:
        instance = SampleDataClass(a=1, b=2)
        with pytest.raises(ValidationError) as context:
            instance.a = "not_an_int"  # type: ignore

        assert "Input should be a valid integer" in str(context.value)

    def test_from_json(self) -> None:
        json_content = """
        {
            "a": 15,
            "b": 25,
            "c": 35
        }
        """
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".json", delete=False
        ) as temp_file:
            temp_file.write(json_content)
            temp_file_path = temp_file.name
        instance = SampleDataClass.from_json(temp_file_path)
        assert instance.a == 15
        assert instance.b == 25
        assert instance.c == 35

    def test_from_json_invalid_path(self) -> None:
        with pytest.raises(FileNotFoundError):
            SampleDataClass.from_json("non_existent_file.json")
