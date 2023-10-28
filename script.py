from html.parser import HTMLParser
from bs4 import BeautifulSoup

def split_message(html_message, max_len):
    def tokenize_html(html):
        tokens = []
        parser = HTMLParser()
        parser.handle_starttag = lambda tag, attrs: tokens.append(('start', tag, attrs))
        parser.handle_endtag = lambda tag: tokens.append(('end', tag))
        parser.handle_data = lambda data: tokens.append(('data', data))
        parser.feed(html)
        return tokens

    tokens = tokenize_html(html_message)

    current_fragment = ''
    open_tags = []

    for token in tokens:
        token_type, *token_content = token

        if token_type == 'start':
            tag, attrs = token_content
            attrs_str = ''.join(' {}="{}"'.format(k, v) for k, v in attrs)
            tag_str = "<{}{}>".format(tag, attrs_str)
            if len(current_fragment) + len(tag_str) > max_len:
                if current_fragment:
                    yield current_fragment
                    current_fragment = ''
                else:
                    raise ValueError(f"Тег слишком длинный: {tag_str}")
            current_fragment += tag_str
            open_tags.append(tag)
        
        elif token_type == 'end':
            tag = token_content[0]
            tag_str = "</{}>".format(tag)
            if len(current_fragment) + len(tag_str) > max_len:
                yield current_fragment
                current_fragment = ''
            current_fragment += tag_str
            open_tags.pop()
        
        elif token_type == 'data':
            data = token_content[0]
            while data:
                available_space = max_len - len(current_fragment)
                if available_space <= 0:
                    yield current_fragment
                    current_fragment = ''
                    available_space = max_len
                chunk = data[:available_space]
                if not chunk:
                    raise ValueError("Текст слишком длинный и не умещается в максимальную длину фрагмента")
                current_fragment += chunk
                data = data[available_space:]
    
    if current_fragment:
        yield current_fragment

