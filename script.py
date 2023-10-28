from html.parser import HTMLParser


class HTMLMessageSplitter(HTMLParser):
    def __init__(self, max_len):
        super().__init__()
        self.max_len = max_len
        self.fragments = []
        self.current_fragment = ""
        self.tag_stack = []
        self.text_parts = []
        self.tag_parts = []

    def handle_starttag(self, tag, attrs):
        tag_text = f"<{tag}>"
        self.tag_parts.append(tag_text)
        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        self.tag_stack.pop()
        tag_text = f"</{tag}>"
        self.tag_parts.append(tag_text)

    def handle_startendtag(self, tag, attrs):
        tag_text = f"<{tag}/>"
        self.tag_parts.append(tag_text)

    def handle_data(self, data):
        self.text_parts.append(data)

    def _process_parts(self):
        while self.text_parts or self.tag_parts:
            if self.tag_parts:
                tag_text = self.tag_parts.pop(0)
                self._add_text(tag_text, is_tag=True)

            if self.text_parts:
                text = self.text_parts.pop(0)
                self._add_text(text)

            if not self.tag_parts and not self.text_parts and self.current_fragment:
                self._save_fragment()


    def _add_text(self, text, is_tag=False):
        while text:
            available_space = self.max_len - len(self.current_fragment)
            
            if is_tag:
                self.current_fragment += text
                text = ""
            else:
                if len(text) <= available_space:
                    self.current_fragment += text
                    text = ""
                else:
                    space_index = text.rfind(" ", 0, available_space)
                    if space_index != -1:
                        self.current_fragment += text[:space_index + 1]
                        text = text[space_index + 1:]
                    else:
                        if self._inside_tag():
                            self._save_fragment()
                            continue
                        self.current_fragment += text[:available_space]
                        text = text[available_space:]
            
            if len(self.current_fragment) == self.max_len:
                self._save_fragment()

            if len(text) > self.max_len and not is_tag:
                error_message = f"Text too long to fit in max_len: {text}"
                raise ValueError(error_message)

    def _inside_tag(self):
        return self.current_fragment.count('<') > self.current_fragment.count('>')


    def _save_fragment(self):
        self.fragments.append(self.current_fragment)
        self.current_fragment = ""
        for tag in reversed(self.tag_stack):
            self.current_fragment += f"<{tag}>"

    def feed(self, data):
        super().feed(data)
        self._process_parts()


def split_message(text, max_len):
    splitter = HTMLMessageSplitter(max_len)
    splitter.feed(text)
    return splitter.fragments
