class HTMLNODE:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        res_str = ""
        for k, v in self.props.items():
            res_str += f' {k}="{v}"'
        return res_str

    def __repr__(self):
        return f'{self.__class__.__name__}(value: {self.value}, tag: {self.tag}, children: {self.children}, props: {self.props})'