"""
This module contains the classes for the HTMLComponents
used to build the resulting html document with nested objects
"""
from typing import List
from dataclasses import dataclass


@dataclass
class HTMLComponent:
    """Abstract class used for an abstract representation of a html component object"""
    def __init__(self):
        pass

    def __str__(self):
        raise Exception("Class does not yet override the __str__ method")


class HTMLContainer(HTMLComponent):
    """Class used to represent a html div/container object inheriting from html component object"""
    def __init__(self):
        super().__init__()
        self.children: List[HTMLComponent] = []

    def add_component(self, child: HTMLComponent):
        """Adds handed html component object to the list of children in this object in order to nest html objects"""
        self.children.append(child)

    def __str__(self) -> str:
        str_children = list(map(lambda child: str(child), self.children))
        return f'<div class="container">{"".join(str_children)}</div>'


@dataclass
class HTMLTableCell(HTMLComponent):
    """Class used to represent an html table cell object inheriting from html component object"""
    def __init__(self, data, is_td=True):
        super().__init__()
        self.data = data
        self.is_td = is_td

    def __str__(self) -> str:
        if self.is_td:
            return f"<td>{self.data}</td>"
        return f"<th>{self.data}</td>"


@dataclass
class HTMLTableRow(HTMLComponent):
    """Class used to represent a html table row object inheriting from html component object"""
    def __init__(self):
        super().__init__()
        self.cells = []

    def add_cell(self, cell: HTMLTableCell):
        """Add handed html cell object to the cells list of the object"""
        self.cells.append(cell)

    def __str__(self) -> str:
        str_cells = list(map(lambda cell: str(cell), self.cells))
        return f'<tr>{"".join(str_cells)}</tr>'


@dataclass
class HTMLTable(HTMLComponent):
    """Class used to represent a html table object inheriting from html component object"""
    def __init__(self, head: List):
        super().__init__()
        self.head: HTMLTableRow = HTMLTableRow()
        for item in head:
            self.head.add_cell(HTMLTableCell(item, is_td=False))
        self.body: List[HTMLTableRow] = []
        
    def add_row(self, data: List):
        """Converts haded one dimensional data list to table row object and stored in this objects body list"""
        row: HTMLTableRow = HTMLTableRow()
        for item in data:
            row.add_cell(HTMLTableCell(item))
        self.body.append(row)
        
    def __str__(self) -> str:
        str_body = list(map(lambda row: str(row), self.body))
        str_body = "\n".join(str_body)
        return f"""
        <table>
            <thead>
                <tr>{str(self.head)}</tr>
            </thead>
            <tbody>
            {str_body}
            </tbody>
        </table>
        """


@dataclass
class HTMLFile(HTMLComponent):
    """Class used to represent an html file object inheriting from html component"""
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.components = []

    def add_component(self, component: HTMLComponent) -> None:
        """Adds handed html component object to components list of this instance in order to nest html components"""
        self.components.append(component)

    def __str__(self) -> str:
        str_body = list(map(lambda component: str(component), self.components))
        str_body = "\n".join(str_body)
        return f"""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="style.css">
                <title>{self.title}</title>
            </head>
            <body>
                {str_body}
            </body>
        </html>
        """


@dataclass
class HTMLParagraph(HTMLComponent):
    """Class use to represent a html paragraph object inheriting from html component object"""
    def __init__(self, text, bold=False):
        super().__init__()
        self.text = text
        self.bold = bold

    def __str__(self) -> str:
        if self.bold:
            return f'<p><strong>{self.text}</strong></p>'
        return f'<p>{self.text}</p>'


@dataclass
class HTMLHeadline(HTMLComponent):
    """Class used to represent a html headline object inheriting from html component object"""
    def __init__(self, text, level=1):
        super().__init__()
        self.text = text
        self.level = level

    def __str__(self) -> str:
        return f'<h{self.level}>{self.text}</h{self.level}>'


@dataclass
class HTMLiFrame(HTMLComponent):
    """Class used to represent a html iframe object inheriting from html component object"""
    def __init__(self, src: str):
        super().__init__()
        self.src = src

    def __str__(self):
        return f'<iframe src="{self.src}" frameborder="0" height="400"></iframe>'
