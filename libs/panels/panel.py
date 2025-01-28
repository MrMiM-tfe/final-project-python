from libs.helpers import clear_screen, ExitException
from libs.colors import colors as c

class Panel:
    def __init__(self, user):
        self.user = user

    def show_panel(self):
        while True:
            clear_screen()
            self._show_header()
            cmd_message = self._show_menu()
            cmd = input(cmd_message)
            if cmd == 'exit':
                break
            self._handle_command(cmd)

    def _show_menu(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def _show_header(self):
        print(c.a(f"Welcome, {self.user.name} {self.user.lastname}!", c.fg.green))
        print(c.fg.red + "You are Admin" + c.reset if self.user.is_admin else "")
        if not self.user.is_admin:
            user_info = f"Username: {self.user.username}\nCard Number: {self.user.card_number}"
            print(user_info)
        
        print("=" * 50)

    def _handle_command(self, cmd):
        menu = self.current_menu.get_menu(cmd)
        if menu is None:
            return
        if menu.type == "page":
            self.current_menu = menu
        else:
            action_method = getattr(self, menu.action, None)
            print("type [exit] to go back")
            if callable(action_method):
                try:
                    action_method()
                except ExitException:
                    pass
            else:
                print(f"Invalid action: {menu.action}")
