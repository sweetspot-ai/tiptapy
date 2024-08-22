import pytest

from tiptapy import BaseDoc


class TestConfig:
    DOMAIN = "example.com"


@pytest.fixture
def table_content():
    return {
        "default": {
            "type": "doc",
            "content": [
                {
                    "type": "table",
                    "content": [
                        {
                            "type": "tableRow",
                            "content": [
                                {
                                    "type": "tableCell",
                                    "content": [{"type": "text", "text": "Header 1"}],
                                },
                                {
                                    "type": "tableCell",
                                    "content": [{"type": "text", "text": "Header 2"}],
                                },
                            ],
                        },
                        {
                            "type": "tableRow",
                            "content": [
                                {
                                    "type": "tableCell",
                                    "content": [{"type": "text", "text": "Cell 1"}],
                                },
                                {
                                    "type": "tableCell",
                                    "content": [{"type": "text", "text": "Cell 2"}],
                                },
                            ],
                        },
                    ],
                }
            ],
        }
    }


@pytest.fixture
def nested_table_content():
    return {
        "nested": {
            "type": "doc",
            "content": [
                {
                    "type": "table",
                    "content": [
                        {
                            "type": "tableRow",
                            "content": [
                                {
                                    "type": "tableCell",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "Outer Header 1",
                                        }
                                    ],
                                },
                                {
                                    "type": "tableCell",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "Outer Header 2",
                                        }
                                    ],
                                },
                            ],
                        },
                        {
                            "type": "tableRow",
                            "content": [
                                {
                                    "type": "tableCell",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "Outer Cell 1",
                                        }
                                    ],
                                },
                                {
                                    "type": "tableCell",
                                    "content": [
                                        {
                                            "type": "table",
                                            "content": [
                                                {
                                                    "type": "tableRow",
                                                    "content": [
                                                        {
                                                            "type": "tableCell",
                                                            "content": [
                                                                {
                                                                    "type": "text",
                                                                    "text": "Inner Header 1",
                                                                }
                                                            ],
                                                        },
                                                        {
                                                            "type": "tableCell",
                                                            "content": [
                                                                {
                                                                    "type": "text",
                                                                    "text": "Inner Header 2",
                                                                }
                                                            ],
                                                        },
                                                    ],
                                                },
                                                {
                                                    "type": "tableRow",
                                                    "content": [
                                                        {
                                                            "type": "tableCell",
                                                            "content": [
                                                                {
                                                                    "type": "text",
                                                                    "text": "Inner Cell 1",
                                                                }
                                                            ],
                                                        },
                                                        {
                                                            "type": "tableCell",
                                                            "content": [
                                                                {
                                                                    "type": "text",
                                                                    "text": "Inner Cell 2",
                                                                }
                                                            ],
                                                        },
                                                    ],
                                                },
                                            ],
                                        }
                                    ],
                                },
                            ],
                        },
                    ],
                }
            ],
        }
    }


def test_table_rendering(table_content) -> None:
    renderer = BaseDoc(TestConfig)
    try:
        rendered_output: str = renderer.render(table_content)
        assert rendered_output is not None, "Rendered output should not be None"
    except Exception as e:
        pytest.fail(f"Rendering table content raised an exception: {e}")


def test_nested_table_rendering(nested_table_content) -> None:
    renderer = BaseDoc(TestConfig)
    try:
        rendered_output: str = renderer.render(nested_table_content)
        assert rendered_output is not None, "Rendered output should not be None"
    except Exception as e:
        pytest.fail(f"Rendering nested table content raised an exception: {e}")


def test_empty_table() -> None:
    empty_table_content = {
        "default": {
            "type": "doc",
            "content": [{"type": "table", "content": []}],
        }
    }
    renderer = BaseDoc(TestConfig)
    try:
        rendered_output = renderer.render(empty_table_content)
        assert rendered_output is not None, "Rendered output should not be None"
    except Exception as e:
        pytest.fail(f"Rendering empty table content raised an exception: {e}")
