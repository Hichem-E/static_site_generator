from htmlnode import HTMLNODE

class LeafNode(HTMLNODE):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        self.children = None

    def to_html(self):
        if not self.value:
            raise ValueError("Missing a value")
        if not self.tag:
            return self.value
        if self.props:
            wrapper = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            wrapper = f"<{self.tag}>{self.value}</{self.tag}>"
        return wrapper