try:
    import gtk
except:
    print("GTK Not Available")
    sys.exit(1)

class GUI_prueba:
    builder = None
    window = None

    def __init__(self):
        gtk.gdk.threads_init()
        gladefile = "gui_prueba.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.completo = False
        
        handlers = {
            "on_button_clicked": self.create_file
        }
        
        self.builder.connect_signals(handlers)
        self.window = self.builder.get_object("window1")
        self.window.show()
        
    def create_file(self, button):
        f = open('myfile.txt', 'w+')

        sentence = str(self.builder.get_object("entry1").get_text())

    	f.write(sentence)
    	
    	self.builder.get_object("entry1").set_text("Pepitas de oro")
    
gui = GUI_prueba()
gtk.main()


