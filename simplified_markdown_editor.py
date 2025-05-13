def print_help():
    print("Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line")
    print("Special commands: !help !done")

def header():
    while True:
        level = input("Level: ")
        if level.isdigit() and 1 <= int(level) <= 6:
            break
        print("The level should be within the range of 1 to 6")
    text = input("Text: ")
    return f"{'#' * int(level)} {text}\n"

def plain():
    return input("Text: ")

def bold():
    return f"**{input('Text: ')}**"

def italic():
    return f"*{input('Text: ')}*"

def inline_code():
    return f"`{input('Text: ')}`"

def link():
    label = input("Label: ")
    url = input("URL: ")
    return f"[{label}]({url})"

def new_line():
    return "\n"

def list_formatter(ordered=False):
    while True:
        try:
            rows = int(input("Number of rows: "))
            if rows <= 0:
                print("The number of rows should be greater than zero")
                continue
            break
        except ValueError:
            print("The number of rows should be greater than zero")
    items = []
    for i in range(1, rows + 1):
        item = input(f"Row #{i}: ")
        if ordered:
            items.append(f"{i}. {item}")
        else:
            items.append(f"* {item}")
    return "\n".join(items) + "\n"

def main():
    result = ""
    formatters = {
        "plain": plain,
        "bold": bold,
        "italic": italic,
        "header": header,
        "link": link,
        "inline-code": inline_code,
        "new-line": new_line,
        "ordered-list": lambda: list_formatter(ordered=True),
        "unordered-list": lambda: list_formatter(ordered=False)
    }

    while True:
        cmd = input("Choose a formatter: ")
        if cmd == "!help":
            print_help()
        elif cmd == "!done":
            with open("output.md", "w", encoding="utf-8") as f:
                f.write(result)
            break
        elif cmd in formatters:
            result += formatters[cmd]()
            print(result)
        else:
            print("Unknown formatting type or command")

if __name__ == "__main__":
    main()
