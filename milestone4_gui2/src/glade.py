import sys, os
from auxiliary_functions import Searching_Strategies

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
        self.builder.add_from_file('src/glade.glade')
                       
        handlers = {
            "generate_path_button": self.generate_path,
            "menu_quit": self.exit,
            "menu_about": self.show_about,
        }
        
        self.builder.connect_signals(handlers)
        self.window = self.builder.get_object("main_window")
        self.window.connect('destroy', gtk.main_quit)
        self.window.show()

    def generate_path(self, button):
        init_node = self.builder.get_object('initial_tb').get_text()
        obj_nodes = self.builder.get_object('objetive_tb').get_text().split(',')

        max_lat = self.builder.get_object('max_lat_tb').get_text()
        min_lat = self.builder.get_object('min_lat_tb').get_text()
        max_lon = self.builder.get_object('max_lon_tb').get_text()
        min_lon = self.builder.get_object('min_lon_tb').get_text()
        coordinates = (min_lat, min_lon, max_lat, max_lon)

        if self.builder.get_object('prune_switch').get_active():
            prune = 'Y '
        else:
            prune = 'N '
        print "'"+prune+"'"

        command = "src/main.py " + prune + str(init_node)+" "
        for coor in coordinates:
            command += str(coor) + " " 
        for node in obj_nodes:
            command += str(node)

        print "Executing: " + command
        os.system(command)
        print "Waiting for next search"


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


