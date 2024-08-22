import pytest

from tiptapy import BaseDoc


@pytest.fixture
def config():
    return type("Config", (), {"DOMAIN": "python.org"})()


def test_empty_codeblock(config):
    json_data = {
        "type": "doc",
        "content": [
            {
                "type": "code_block",
                "attrs": {"language": None},
                "content": [{"type": "text", "text": ""}],
            }
        ],
    }

    renderer = BaseDoc(config)
    try:
        rendered_output = renderer.render(json_data)
        assert rendered_output is not None, "Rendered output should not be None"
    except Exception as e:
        pytest.fail(f"Rendering empty codeblock raised an exception: {e}")


def test_codeblock_with_language(config):
    json_data = {
        "type": "doc",
        "content": [
            {
                "type": "code_block",
                "attrs": {"language": "python"},
                "content": [{"type": "text", "text": "print('Hello, World!')"}],
            }
        ],
    }

    renderer = BaseDoc(config)
    try:
        rendered_output = renderer.render(json_data)
        assert rendered_output is not None, "Rendered output should not be None"
    except Exception as e:
        pytest.fail(f"Rendering codeblock with language raised an exception: {e}")


def test_codeblock_with_multiple_lines(config):
    json_data = {
        "type": "doc",
        "content": [
            {
                "type": "code_block",
                "attrs": {"language": "javascript"},
                "content": [
                    {
                        "type": "text",
                        "text": "function greet(name) {\n    console.log(`Hello, ${name}!`);\n}",
                    }
                ],
            }
        ],
    }

    renderer = BaseDoc(config)
    try:
        rendered_output = renderer.render(json_data)
        assert rendered_output is not None, "Rendered output should not be None"
    except Exception as e:
        pytest.fail(f"Rendering codeblock with multiple lines raised an exception: {e}")


def test_codeblock_with_special_characters(config):
    json_data = {
        "type": "doc",
        "content": [
            {
                "type": "code_block",
                "attrs": {"language": "html"},
                "content": [
                    {
                        "type": "text",
                        "text": '<div class="special">&lt;Hello &amp; World&gt;</div>',
                    }
                ],
            }
        ],
    }

    renderer = BaseDoc(config)
    try:
        rendered_output = renderer.render(json_data)
        assert rendered_output is not None, "Rendered output should not be None"
    except Exception as e:
        pytest.fail(f"Rendering codeblock with special characters raised an exception: {e}")


def test_codeblock_without_language(config):
    json_data = {
        "type": "doc",
        "content": [
            {
                "type": "code_block",
                "attrs": {},
                "content": [
                    {
                        "type": "text",
                        "text": "This is a code block without a specified language.",
                    }
                ],
            }
        ],
    }

    renderer = BaseDoc(config)
    try:
        rendered_output = renderer.render(json_data)
        assert rendered_output is not None, "Rendered output should not be None"
    except Exception as e:
        pytest.fail(f"Rendering codeblock without language raised an exception: {e}")
