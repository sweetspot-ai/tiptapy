import json
import os
import sys
from html import escape
from typing import Dict
import logging

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .image import url2mime
from .macros import (
    build_link_handler,
    get_audio_player_block,
    get_doc_block,
    make_img_src,
)

__version__ = "0.18.1"

renderers: Dict = {}


def init_env(path, config, ai_tag):
    env = Environment(
        loader=FileSystemLoader(path),
        autoescape=select_autoescape(enabled_extensions=("html")),
    )
    # https://stackoverflow.com/a/6038550
    env.globals["url2mime"] = url2mime
    env.globals["make_img_src"] = make_img_src
    env.globals["handle_links"] = build_link_handler(config)
    env.globals["get_audio_player_block"] = get_audio_player_block
    env.globals["get_doc_block"] = get_doc_block
    env.globals["tag_name"] = ai_tag

    return env


def _get_abs_template_path(path_str):
    # This is equivalent of pkgutil.get_data
    # But when diris passed to pkgutil.get_data it throws IsDirectoryError
    # Hence this function
    # Ref: https://github.com/python/cpython/blob/3.10/Lib/pkgutil.py#L614
    pkg_dir = os.path.dirname(sys.modules[__name__].__file__)
    return os.path.join(pkg_dir, path_str)


def escape_values_recursive(node):
    # Skip the html key in the node, as it is used to render the html
    # and should not be escaped. Users should clean the html before
    # passing it to the renderer.
    skip_key = "html"

    if isinstance(node, dict):
        return {
            escape(k): v if k == skip_key else escape_values_recursive(v)
            for k, v in node.items()
        }
    elif isinstance(node, list):
        return [escape_values_recursive(x) for x in node]
    elif isinstance(node, str):
        return escape(node)
    return node


class BaseDoc:
    doc_type = "doc"
    templates_path = (
        _get_abs_template_path("templates"),
        _get_abs_template_path("templates/extras"),
    )
    locked = False
    # `locked` helps in templates determine to show/hide in anonymous views
    # Useful in case where code is referring same template for both protected
    # and guest views

    def __init__(self, config, focus_tag):
        self.logger = logging.getLogger(__name__)
        environ = init_env(self.templates_path, config, focus_tag)
        
        # Add the custom filter
        environ.filters['template_exists'] = self.template_exists
        
        self.t = environ.get_template(f"{self.doc_type}.html")
        self.t.environment.globals["locked"] = self.locked

    def template_exists(self, template_name):
        exists = template_name in self.t.environment.list_templates()
        if not exists:
            self.logger.warning(f"Template not found: {template_name}")
        return exists

    def render(self, in_data):
        in_data = in_data if isinstance(in_data, dict) else json.loads(in_data)
        node = in_data if isinstance(in_data, dict) else json.loads(in_data)
        node = escape_values_recursive(node)
        return self.t.render(node=node)