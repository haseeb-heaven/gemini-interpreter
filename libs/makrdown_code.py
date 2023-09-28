from rich import print as rich_print
from rich.markdown import Markdown
from rich.rule import Rule

def display_markdown_message(message):
    """
    Display markdown message. Works with multiline strings with lots of indentation.
    Will automatically make single line > tags beautiful.
    """

    for line in message.split("\n"):
        line = line.strip()
        if line == "":
            print("")
        elif line == "---":
            rich_print(Rule(style="white"))
        else:
            rich_print(Markdown(line))

    if "\n" not in message and message.startswith(">"):
        # Aesthetic choice. For these tags, they need a space below them
        print("")
        
from rich.syntax import Syntax

def display_code(code: str, language: str = "python"):
    """
    Display syntax highlighted code in terminal.

    Parameters:
    code (str): The code to be displayed.
    language (str): The language of the code. Default is 'python'.
    """
    try:
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        rich_print(syntax)
    except Exception as e:
        print(f"An error occurred: {e}")