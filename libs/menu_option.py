from libs.colors import colors as c

class MenuOption:
    parent =  None

    def __init__(self, title, type, action=None, options=None, slug=None):
        self.title = title
        self.type = type
        self.slug = slug if slug else title.lower().replace(" ", "_")

        if self.type == "page":
            self.options = options
            for option in self.options:
                option.parent = self
        elif self.type == "action":
            self.action = action
        else:
            raise ValueError("Invalid menu option type")
        
    def __str__(self):
        if self.type == "page":
            return "\n".join([f"{c.a(i+1, c.fg.orange)}. {option.title}" for i, option in enumerate(self.options)]) + (f"\n{c.fg.red}b{c.reset}. for go back" if self.parent else "")
        elif self.type == "action":
            return f"{self.title}"
        
    def get_menu(self, cmd):
        if cmd == "b" and self.parent is not None:
            return self.parent
        if cmd.isdigit():
            index = int(cmd) - 1
            if index >= 0 and index < len(self.options):
                return self.options[index]
            else:
                print("Invalid option")
        else:
            print("Invalid input")