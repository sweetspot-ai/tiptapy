import json

from typing import List
from inspect import isclass


renderers = {}


class BaseNode:
    type = 'prose-mirror_content-type'
    wrap_tag = None

    def render(self, in_data):
        out = self.inner_render(in_data)
        if self.wrap_tag:
            return f'<{self.wrap_tag}>{out}</{self.wrap_tag}>'
        return out

    def inner_render(self, node):
        return node['content']


class BaseContainer(BaseNode):

    def inner_render(self, nodes: List):
        out = ''
        for node in nodes['content']:
            node_type = node.get('type')
            renderer = renderers.get(node_type)
            assert renderer, f'Unsupported node_type: "{node_type}"'
            if renderer:
                out += renderer.render(node)
        return out


class Text(BaseNode):
    type = 'text'
    mark_tags = {'bold': 'strong', 'italic': 'em', 'link': 'a'}

    def inner_render(self, node):
        text = node['text']
        marks = node.get('marks')
        if marks:
            for mark in marks:
                tag = self.mark_tags.get(mark.get('type'))
                attrs = mark.get('attrs')
                if attrs:
                    attrs_s = ' '.join(f'{k}="{v}"' for k,v in attrs.items())
                    text = f'<{tag} {attrs_s}>{text}</{tag}>'
                else:
                    text = f'<{tag}>{text}</{tag}>'
        return text


class Paragraph(BaseContainer):
    type = 'paragraph'
    wrap_tag = 'p'


class BlockQuote(BaseContainer):
    type = 'blockquote'
    wrap_tag = 'blockquote'


class HardBreak(BaseContainer):
    type = 'hard_break'

    def inner_render(self, node):
        return '<br>'


class ListItem(BaseContainer):
    type = 'list_item'
    wrap_tag = 'li'


class BulletList(BaseContainer):
    type = 'bullet_list'
    wrap_tag = 'ul'


class Doc(BaseContainer):
    type = 'doc'


def register_renderer(cls):
    renderers[cls.type] = cls()


for o in tuple(locals().values()):
    if isclass(o) and issubclass(o, BaseNode):
        register_renderer(o)


def convert_any(in_data):
    typ = in_data.get('type')
    renderer = renderers.get(typ)
    return renderer.render(in_data)


def to_html(s):
    in_data = json.loads(s)
    return convert_any(in_data)


if __name__ == '__main__':
    import timeit
    s = open('tests/data.json').read()
    print(to_html(s))
    print(timeit.timeit("to_html(s)", setup="from __main__ import to_html, s", number=100000))