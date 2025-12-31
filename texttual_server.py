from textual_serve.server import Server

server = Server("uv run -m tui")
server.serve()