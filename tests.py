import pytest

from script import split_message


def test_simple_text():
    text = "This is a simple text"
    max_len = 10
    with pytest.raises(ValueError) as e:
        list(split_message(text, max_len))
    assert (
        str(e.value) == "Text too long to fit in max_len: simple text"
    ), "Unexpected error message"


def test_boundary_conditions():
    text = "<p>This is a text</p>"
    max_len = len(text)
    fragments = list(split_message(text, max_len))
    assert fragments == [text], "Boundary condition failed"


if __name__ == "__main__":
    pytest.main()
