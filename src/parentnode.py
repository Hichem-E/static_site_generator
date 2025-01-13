from htmlnode import HTMLNODE

class ParentNode(HTMLNODE):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        self.value = None

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing a tag")
        if not self.children:
            raise ValueError("Missing children")
        
        if self.props:
            res = f'<{self.tag}{self.props_to_html()}>'
        else:
            res = f'<{self.tag}>'
        for child in self.children:
            res += child.to_html()

        res += f'</{self.tag}>'
        
        return res
        
