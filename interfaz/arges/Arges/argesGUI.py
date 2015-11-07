import arges
from threading import Thread, Timer
import sys
import os
import shutil
import webbrowser
import datetime
import time

try:
    import gtk
except:
    print("GTK Not Available")
    sys.exit(1)


class ArgesGUI:
    builder = None
    window = None

    def __init__(self):
        gtk.gdk.threads_init()
        gladefile = "GUIArges.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.completo = False
        handlers = {
            "on_BtnProcesar1_clicked": self.processAvconv,
            "on_BtnProcesar2_clicked": self.processBlender,
            "on_BtnProcesar3_clicked": self.processAudio,
            "on_window1_destroy": self.quit,
            "on_ProcesarCompleto_clicked": self.procesarCompleto,
            "imagemenuitem09_activate_cb": self.mostrarAyuda,
            "on_imagemenuitem10_activate": self.mostrarAcercaDe,
            "on_imagemenuitem5_activate": self.exit,
            "on_imagemenuitemPI_activate": self.options,
            "on_button2_clicked": self.closeOptions,
            "on_button1_clicked": self.saveChanges,
            "on_botonPrevisualizar_clicked": self.previsualizar,
            "on_VentanaPrevisualizar_clicked": self.mostrarPrevisualizar,
            "on_volverPrevisualizar_clicked": self.hidePrevisualizar,
            "changed": self.loadConfig,
            "crear_conf": self.crear_configuracion,
            "cerrar_crear_conf": self.cerrar_crear_conf,
            "abrir_crear_conf": self.abrir_crear_conf
        }
        self.arges = arges.Arges()
        self.builder.connect_signals(handlers)
        self.window = self.builder.get_object("window1")
        self.window.show()
        self.progressBar = self.builder.get_object("BarraProgreso")
        self.progressTitle = self.builder.get_object("label18")
        self.progressTitle.set_use_markup(True)
        self.pulsar = Pulsar()
        self.optionsWindow = self.builder.get_object("window2")
        self.previewWindow = self.builder.get_object("window3")
        self.crearConfWindow = self.builder.get_object("window4")
        self.lista_config = self.builder.get_object("lista_config")
        self.loadConfigList()

    def updateSettings(self):
        self.videoProfesorX = float(self.builder.get_object("labelX").get_text())
        self.videoProfesorY = float(self.builder.get_object("labelY").get_text())
        self.videoProfesorEscala = float(self.builder.get_object("labelEscala").get_text())
        self.colorSelected = self.builder.get_object("button3").get_color()
        self.finalColor = (self.colorSelected.red_float, self.colorSelected.green_float, self.colorSelected.blue_float, 1)

        self.videoPresentacionX = float(self.builder.get_object("txtPresentacionX").get_text())
        self.videoPresentacionY = float(self.builder.get_object("txtPresentacionY").get_text())
        self.videoPresentacionEscala = float(self.builder.get_object("txtPresentacionEscala").get_text())

        self.screen_balance = float(self.builder.get_object("screen_bal").get_text())
        self.edge_kernel = int(self.builder.get_object("edge_kernel").get_text())
        self.clip_black = float(self.builder.get_object("clip_black").get_text())
        self.clip_white = float(self.builder.get_object("clip_white").get_text())
        self.feather_distance = int(self.builder.get_object("feather_distance").get_text())
        self.post_blur = int(self.builder.get_object("post_blur").get_text())
        self.dilate_erode = int(self.builder.get_object("dilate_erode").get_text())

        self.arges.setChromaSettings(self.finalColor, self.videoProfesorX,
                                     self.videoProfesorY,
                                     self.videoProfesorEscala,
                                     self.videoPresentacionX,
                                     self.videoPresentacionY,
                                     self.videoPresentacionEscala,
                                     self.screen_balance, self.edge_kernel,
                                     self.clip_black, self.clip_white,
                                     self.feather_distance, self.post_blur,
                                     self.dilate_erode)

    def abrir_crear_conf(self, button=None):
        self.crearConfWindow.show()

    def cerrar_crear_conf(self, button=None):
        self.builder.get_object("text_nueva_conf").set_text("")
        self.crearConfWindow.hide()

    def crear_configuracion(self, button=None):
        text_conf = self.builder.get_object("text_nueva_conf")
        name = text_conf.get_text()
        if len(name.split('.')) == 1:
            name += ".config"
        shutil.copy2(os.path.join('config', '16_9.config'),
                     os.path.join('config', name))
        self.crearConfWindow.hide()
        self.loadConfigList(name)
        text_conf.set_text("")

    def saveChanges(self, button):
        self.saveConfig()

    def loadConfigList(self, name=""):
        self.configs = os.listdir('config')
        listmodel = gtk.ListStore(str)
        listmodel.clear()
        for c in self.configs:
            listmodel.append([c])
        self.lista_config.set_model(listmodel)
        if name == "":
            self.cell = gtk.CellRendererText()
            self.lista_config.pack_start(self.cell, False)
        self.lista_config.add_attribute(self.cell, "text", 0)
        if self.lista_config.get_active() == -1:
            self.lista_config.set_active(0)
        if name != "":
            index = self.configs.index(name)
            self.lista_config.set_active(index)

    def loadConfig(self, combo):
        name = self.configs[self.lista_config.get_active()]
        with open(os.path.join('config', name), 'r') as f:
            color = gtk.gdk.Color()
            color.red_float = float(f.readline())
            color.green_float = float(f.readline())
            color.blue_float = float(f.readline())
            color.pixel = float(f.readline())
            self.builder.get_object("button3").set_color(color)
            self.builder.get_object("labelX").set_text(f.readline())
            self.builder.get_object("labelY").set_text(f.readline())
            self.builder.get_object("labelEscala").set_text(f.readline())
            self.builder.get_object("txtPresentacionX").set_text(f.readline())
            self.builder.get_object("txtPresentacionY").set_text(f.readline())
            self.builder.get_object("txtPresentacionEscala").set_text(f.readline())
            self.builder.get_object("screen_bal").set_text(f.readline())
            self.builder.get_object("edge_kernel").set_text(f.readline())
            self.builder.get_object("clip_black").set_text(f.readline())
            self.builder.get_object("clip_white").set_text(f.readline())
            self.builder.get_object("feather_distance").set_text(f.readline())
            self.builder.get_object("post_blur").set_text(f.readline())
            self.builder.get_object("dilate_erode").set_text(f.readline())
        self.updateSettings()

    def saveConfig(self):
        self.updateSettings()
        name = self.configs[self.lista_config.get_active()]
        with open(os.path.join('config', name), 'w') as f:
            f.write((str(self.finalColor[0]) + '\n'))
            f.write((str(self.finalColor[1]) + '\n'))
            f.write((str(self.finalColor[2]) + '\n'))
            f.write((str(self.finalColor[3]) + '\n'))
            f.write((str(self.videoProfesorX) + '\n'))
            f.write((str(self.videoProfesorY) + '\n'))
            f.write((str(self.videoProfesorEscala) + '\n'))
            f.write((str(self.videoPresentacionX) + '\n'))
            f.write((str(self.videoPresentacionY) + '\n'))
            f.write((str(self.videoPresentacionEscala) + '\n'))
            f.write((str(self.screen_balance) + '\n'))
            f.write((str(self.edge_kernel) + '\n'))
            f.write((str(self.clip_black) + '\n'))
            f.write((str(self.clip_white) + '\n'))
            f.write((str(self.feather_distance) + '\n'))
            f.write((str(self.post_blur) + '\n'))
            f.write((str(self.dilate_erode) + '\n'))

    def options(self, button):
        videoProfesor = self.builder.get_object("FCProfesor").get_filename()
        videoDiapositivas = self.builder.get_object("FCDiapositivas").get_filename()
        if (videoProfesor is None) or (videoDiapositivas is None):
            dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Debe seleccionar los videos")
            dialog.run()
            dialog.destroy()
        else:
            self.loadConfig(self.lista_config)
            self.optionsWindow.show()

    def mostrarPrevisualizar(self, button=None):
        self.previewWindow.show()

    def hidePrevisualizar(self, button=None):
        self.previewWindow.hide()

    def previsualizar(self, button=None):
        def processInputVideo():
            videoDiapositivas = self.builder.get_object("FCDiapositivas").get_filename()
            Thread(target=self.arges.processInputVideo, args=(videoDiapositivas, "00:00:00", "00:00:01", "presentacion.avi", 1280, 720, 25, None, processRenderOneFrame, self.error_callback)).start()

        def processRenderOneFrame():
            Thread(target=self.arges.renderOneFrame, args=(1, None, previsualizarFinish, self.error_callback)).start()

        def previsualizarFinish():
            pixbuf = gtk.gdk.pixbuf_new_from_file("preview.jpg")
            scaled_buf = pixbuf.scale_simple(640, 320, gtk.gdk.INTERP_BILINEAR)
            im = self.builder.get_object("image2")
            im.set_from_pixbuf(scaled_buf)
            im.show()
            self.builder.get_object("botonPrevisualizar").set_label("Previsualizar")
            self.setEnableObjects(1)

        boton_previsualizar = self.builder.get_object("botonPrevisualizar")
        boton_previsualizar.set_label("Generando Previsualizacion...")
        self.setEnableObjects(0)
        videoProfesor = self.builder.get_object("FCProfesor").get_filename()
        Thread(target=self.arges.processInputVideo, args=(videoProfesor, "00:00:00", "00:00:01", "profesor.avi", 1920, 1080, 25, None, processInputVideo, self.error_callback)).start()
        self.updateSettings()

    def closeOptions(self, button=None, window=None):
        self.updateSettings()
        self.optionsWindow.hide()

    def exit(self, button):
        sys.exit(0)

    def mostrarAcercaDe(self, button):
        self.dialog = gtk.AboutDialog()
        width, height = self.dialog.get_size()
        self.dialog.move(gtk.gdk.screen_width() / 2 - width, gtk.gdk.screen_height() / 2 - height)
        self.dialog.set_name("Arges")
        self.dialog.set_authors(["Izquierdo Ramirez, Alberto", "Sanchez Sobrino, Santiago"])
        self.dialog.set_website("http://blog.uclm.es/cted")
        linestring = open('LICENSE.txt', 'r').read()
        self.dialog.set_license(linestring)
        self.dialog.run()
        self.dialog.destroy()

    def mostrarAyuda(self, button):
        webbrowser.open_new_tab("ayuda.html")

    def procesarCompleto(self, button):
        self.completo = True
        self.processAvconv(button)

    def processAvconv(self, button):
        def process2():
            self.pulsar.stop()
            self.setEnableObjects(0)
            self.progressTitle.set_markup("<b>Progreso - Procesando video 2/2</b>")
            self.progressBar.set_show_text(False)
            self.pulsar.start(self.progressBar, 0.2)

            if self.completo is True:
                finish_callback = self.processBlender
                error_callback = self.error_callback
            else:
                finish_callback = self.finish_callback
                error_callback = self.error_callback

            video_path = self.builder.get_object("FCDiapositivas").get_filename()
            start = "{}:{}:{}".format(int(self.builder.get_object("DiapositivasInicioHoras").get_value()),
                                      int(self.builder.get_object("DiapositivasInicioMinutos").get_value()),
                                      int(self.builder.get_object("DiapositivasInicioSegundos").get_value()))
            output = "presentacion.avi"
            Thread(target=self.arges.processInputVideo, args=(video_path, start, self.duration, output, 1280, 720, 25, None, finish_callback, error_callback)).start()

        video_path = self.builder.get_object("FCProfesor").get_filename()
        video2_path = self.builder.get_object("FCDiapositivas").get_filename()
        if (video_path is None) or (video2_path is None):
            dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Debe seleccionar los videos")
            dialog.run()
            dialog.destroy()
            return
        time = self.getTime()
        if time[1] is None:
            return

        self.setEnableObjects(0)
        self.progressTitle.set_markup("<b>Progreso - Procesando video 1/2</b>")
        self.progressBar.set_show_text(False)
        self.pulsar.start(self.progressBar, 0.2)
        self.duration = time[1]
        output = "profesor.avi"
        Thread(target=self.arges.processInputVideo, args=(video_path, time[0], time[1], output, 1920, 1080, 25, None, process2, self.error_callback)).start()

    def processBlender(self, button=None):
        if (os.path.exists("profesor.avi") is False) or (os.path.exists("presentacion.avi") is False):
            dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Videos del paso anterior no generados")
            dialog.run()
            dialog.destroy()
            return
        time = self.getTime()
        if time[1] is None:
            return
        self.setEnableObjects(0)
        self.progressTitle.set_markup("<b>Progreso - Componiendo chroma key</b>")
        if self.completo is True:
            finish_callback = self.processAudio
        else:
            finish_callback = self.finish_callback
        Thread(target=self.arges.processChromaKey, args=(time[1], self.update_progress_callback, finish_callback, self.error_callback)).start()

    def processAudio(self, button=None):
        if os.path.exists("profesor.avi") is False:
            dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Videos del paso anterior no generados")
            dialog.run()
            dialog.destroy()
            return
        time = self.getTime()
        if time[1] is None:
            return
        self.setEnableObjects(0)
        self.progressTitle.set_markup("<b>Progreso - Procesando audio</b>")
        self.progressBar.set_show_text(False)
        if self.completo is False:
            self.pulsar.start(self.progressBar, 0.2)
        video_path = self.builder.get_object("FCSalida1").get_filename()
        Thread(target=self.arges.processAudio, args=("profesor.avi", os.path.join(video_path, "video_final.avi"), time[0], time[1], 256, 48000, None, self.finish_callback, self.error_callback)).start()

    def getTime(self):
        try:
            inicio_horas = int(self.builder.get_object("ProfesorInicioHoras").get_value())
            inicio_minutos = int(self.builder.get_object("ProfesorInicioMinutos").get_value())
            inicio_segundos = int(self.builder.get_object("ProfesorInicioSegundos").get_value())
            fin_horas = int(self.builder.get_object("ProfesorFinHoras").get_value())
            fin_minutos = int(self.builder.get_object("ProfesorFinMinutos").get_value())
            fin_segundos = int(self.builder.get_object("ProfesorFinSegundos").get_value())
        except:
            self.error_callback('Introduzca valores numericos')
            return (None, None)

        inicio_en_segundos = inicio_horas * 3600 + inicio_minutos * 60 + inicio_segundos
        fin_en_segundos = fin_horas * 3600 + fin_minutos * 60 + fin_segundos
        duracion_en_segundos = fin_en_segundos - inicio_en_segundos
        if duracion_en_segundos <= 0:
            self.error_callback('Duracion incorrecta')
            return (None, None)
        return ("{}".format(datetime.timedelta(seconds=inicio_en_segundos)), "{}".format(datetime.timedelta(seconds=duracion_en_segundos)))

    def quit(self, widget):
        sys.exit(0)

    def setEnableObjects(self, value):
        for obj in self.builder.get_objects():
            if type(obj) is gtk.Button:
                obj.set_sensitive(value)

    def update_progress_callback(self, progress, time):
        if progress is not None:
            self.progressBar.set_fraction(progress)

        if time is not None:
            self.progressTitle.set_markup("<b>Progreso - Componiendo chroma key (ETA: {})</b>".format(time))

        print("[Arges] Update Progress Callback")

    def error_callback(self, error_msg):
        dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, error_msg)
        dialog.run()
        dialog.destroy()

    def finish_callback(self):
        self.completo = False
        self.setEnableObjects(1)
        self.progressTitle.set_markup("<b>Progreso</b>")
        self.progressBar.set_show_text(True)
        self.progressBar.set_fraction(0)
        self.pulsar.stop()
        print("[Arges] Finish Callback")


class Pulsar:
    def __init__(self):
        self.timer = None

    def start(self, progressBar, sec):
        def func_wrapper():
            self.start(progressBar, sec)
            progressBar.pulse()
        t = Timer(sec, func_wrapper)
        t.start()
        self.timer = t

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

if __name__ == "__main__":
    argesGUI = ArgesGUI()
    gtk.main()
