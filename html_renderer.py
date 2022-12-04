class HTMLComponent:
    def __init__(self):
        pass

    def __str__(self):
        pass


class HTMLContainer(HTMLComponent):
    def __init__(self, child: HTMLComponent):
        self.child: HTMLComponent = child

    def __str__(self) -> str:
        return f'<div class="container">{str(self.child)}</div>'
        

class HTMLTableCell(HTMLComponent):
    def __init__(self, data, is_td=True):
        self.data = data
        self.is_td = is_td

    def __str__(self) -> str:
        if self.is_td:
            return f"<td>{self.data}</td>"
        else:
            return f"<th>{self.data}</td>"


class HTMLTableRow(HTMLComponent):
    def __init__(self):
        self.cells = []

    def add_cell(self, cell: HTMLTableCell):
        self.cells.append(cell)

    def __str__(self) -> str:
        str_cells = list(map(lambda cell: str(cell), self.cells))
        return f'<tr>{"".join(str_cells)}</tr>'

class HTMLTable(HTMLComponent):
    def __init__(self, head: list):
        self.head: HTMLTableRow = HTMLTableRow()
        for item in head:
            self.head.add_cell(HTMLTableCell(item, is_td=False))
        self.body: list[HTMLTableRow] = []
        
    def add_row(self, data: list):
        row: HTMLTableRow = HTMLTableRow()
        for item in data:
            row.add_cell(HTMLTableCell(item))
        self.body.append(row)
        
    def __str__(self) -> str:
        str_body = list(map(lambda row: str(row), self.body))
        str_body = "\n".join(str_body)
        return f"""
        <table class="table table-striped">
            <tr>{str(self.head)}</tr>
            <tbody>
            {str_body}
            </tbody>
        </table>
        """
        
class HTMLFile:
    def __init__(self, title: str):
        self.title = title
        self.components = []

    def add_component(self, component: HTMLComponent) -> None:
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
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
                <title>{self.title}</title>
            </head>
            <body>
                <div class="container">
                {str_body}
                </div>
            </body>
        </html>
        """

class HTMLParagraph(HTMLComponent):
    def __init__(self, text):
        self.text = text

    def __str__(self) -> str:
        return f"<p>{self.text}</p>"


class HTMLHeadline(HTMLComponent):
    def __init__(self, text, level=1):
        self.text = text
        self.level = level

    def __str__(self) -> str:
        return f"<h{self.level}>{self.text}</h{self.level}>"