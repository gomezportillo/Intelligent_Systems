import sys

try:
    from gi.repository import Gtk as gtk
except:
    print("GTK Not Available")
    sys.exit(1)

class GUI:
    builder = None
    window = None

    def __init__(self):
        self.builder = gtk.Builder()
        try:
            self.builder.add_from_file("glade.glade")
        except:
            self.builder.add_from_file("src/glade.glade")
                       
        handlers = {
            "generate_path_button": self.search_path,
            "menu_quit": self.exit,
            "menu_about": self.show_about
        }
        
        statusIcon = gtk.StatusIcon()
        # load it
        statusIcon.set_from_file("data/icon.ico")
        # show it
        statusIcon.set_visible(True)

        self.builder.connect_signals(handlers)
        self.window = self.builder.get_object("main_window")
        self.window.connect('destroy', gtk.main_quit)
        self.window.show()
        
    def search_path(self, button):
        print self.builder.get_object('bfs_rb').get_active()


    def show_about(self, button):
        self.dialog = gtk.AboutDialog()
        self.dialog.set_name("OSM path finder")
        self.dialog.set_authors(['\nPedro-Manuel Gomez-Portillo Lopez', 'Juan Garrido Arcos'])
        self.dialog.set_license(open('LICENSE.txt', 'r').read())
        self.dialog.run()
        self.dialog.destroy()


    def exit(self, button):
        sys.exit(1)

    
gui = GUI()
gtk.main()


