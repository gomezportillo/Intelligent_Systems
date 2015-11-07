import subprocess
import re
import time
import sys

try:
    import gobject
except:
    print("'gobject' module not available")
    sys.exit(1)


class Arges:
    def __init__(self):
        self.avconv_comm = r'redist\avconv\avconv.exe'
        self.lame_comm = r'redist\lame\lame.exe'
        self.sox_comm = r'redist\sox\sox.exe'
        self.blender_comm = r'redist\blender\blender.exe'

        if sys.platform == "linux" or sys.platform == "linux2":
            self.avconv_comm = r'avconv'
            self.lame_comm = r'lame'
            self.sox_comm = r'sox'
            self.blender_comm = r'blender'



    def getChromaSettings(self):
        return (self.chroma_color, self.chroma_x, self.chroma_y, self.chroma_scale, self.pres_x, self.pres_y, self.pres_scale)

    def setChromaSettings(self, color=None, x_prof=None, y_prof=None,
                          scale_prof=None, x_pres=None, y_pres=None,
                          scale_pres=None, sc_ba=None, ed_ke=None, c_b=None,
                          c_w=None, f_d=None, p_b=None, d_e=None):
        if color is not None:
            self.chroma_color = color

        if x_prof is not None:
            self.chroma_x = x_prof

        if y_prof is not None:
            self.chroma_y = y_prof

        if scale_prof is not None:
            self.chroma_scale = scale_prof

        if x_pres is not None:
            self.pres_x = x_pres

        if y_pres is not None:
            self.pres_y = y_pres

        if scale_pres is not None:
            self.pres_scale = scale_pres

        if sc_ba is not None:
            self.screen_balance = sc_ba

        if ed_ke is not None:
            self.edge_kernel = ed_ke

        if c_b is not None:
            self.clip_black = c_b

        if c_w is not None:
            self.clip_white = c_w

        if f_d is not None:
            self.feather_distance = f_d

        if p_b is not None:
            self.post_blur = p_b

        if d_e is not None:
            self.dilate_erode = d_e

    def processInputVideo(self, video_path, start, duration, output, width=1920, height=1080, fps=25,
                          update_progress_callback=None, finish_callback=None, error_callback=None):
        try:
            self.__processInputVideo(video_path, start, duration, output, width, height, fps, update_progress_callback)
        except (AssertionError, ValueError) as error:
            if error_callback is not None:
                gobject.idle_add(error_callback, error)
            else:
                print(error)
        finally:
            if finish_callback is not None:
                gobject.idle_add(finish_callback)
            else:
                print("[Arges] Proceso terminado")

    def processChromaKey(self, duration, update_progress_callback=None, finish_callback=None, error_callback=None):
        try:
            self.__processChromaKey(duration, update_progress_callback)
        except (AssertionError, ValueError) as error:
            if error_callback is not None:
                gobject.idle_add(error_callback, error)
            else:
                print(error)
        finally:
            if finish_callback is not None:
                gobject.idle_add(finish_callback)
            else:
                print("[Arges] Proceso terminado")

    def renderOneFrame(self, frame=1, update_progress_callback=None, finish_callback=None, error_callback=None):
        try:
            self.__renderOneFrame(frame, update_progress_callback)
        except (AssertionError, ValueError) as error:
            if error_callback is not None:
                gobject.idle_add(error_callback, error)
            else:
                print(error)
        finally:
            if finish_callback is not None:
                gobject.idle_add(finish_callback)
            else:
                print("[Arges] Proceso terminado")

    def processAudio(self, video_input_path, video_output_path, start, duration, bitrate=256, freq=48000,
                     update_progress_callback=None, finish_callback=None, error_callback=None):
        try:
            self.__processAudio(video_input_path, video_output_path, start, duration, bitrate, freq, update_progress_callback)
        except (AssertionError, ValueError) as error:
            if error_callback is not None:
                gobject.idle_add(error_callback, error)
            else:
                print(error)
        finally:
            if finish_callback is not None:
                gobject.idle_add(finish_callback)
            else:
                print("[Arges] Proceso terminado")

    def __processInputVideo(self, video_path, start, duration, output, width, height, fps, update_progress_callback):
        l = duration.split(':')
        if len(l) != 3:
            raise ValueError('Duracion incorrecta ({}?)'.format(duration))

        number_of_frames = (int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])) * 25

        command = [self.avconv_comm, '-y', '-i', video_path, '-vcodec', 'h264', '-qscale', '0',
                   '-s', '{}x{}'.format(width, height), '-ss', str(start), '-t', str(duration), '-r', str(fps),
                   output]

        if self.__exec(command, number_of_frames, r'(?:frame=)(\s+\d+)', update_progress_callback=update_progress_callback) != 0:
            raise AssertionError('[Arges] Fallo el procesado del video "{}"'.format(video_path))

    def __processChromaKey(self, duration, update_progress_callback):
        l = duration.split(':')
        if len(l) != 3:
            raise ValueError('Duracion incorrecta ({}?)'.format(duration))

        number_of_frames = (int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])) * 25
        command = [self.blender_comm, '-b', 'chroma_key.blend', '-P', 'chroma_key.py', '--', 'video',
                   '({},{},{},{})'.format(self.chroma_color[0], self.chroma_color[1], self.chroma_color[2], self.chroma_color[3]),
                   str(self.chroma_x), str(self.chroma_y),
                   str(self.chroma_scale), str(number_of_frames),
                   str(self.pres_x), str(self.pres_y), str(self.pres_scale),
                   str(self.screen_balance), str(self.edge_kernel),
                   str(self.clip_black), str(self.clip_white),
                   str(self.feather_distance), str(self.post_blur),
                   str(self.dilate_erode)]

        if self.__exec(command, number_of_frames, r'(?:Fra:)(\d+)', r'(?:Time:\s+)(\d+:\d+(\.\d*)?|\.\d+)', update_progress_callback) != 0:
            raise AssertionError('[Arges] Fallo el procesado del chroma')

    def __renderOneFrame(self, frame, update_progress_callback):
        command = [self.blender_comm, '-b', 'chroma_key.blend', '-P', 'chroma_key.py', '--', 'frame',
                   '({},{},{},{})'.format(self.chroma_color[0], self.chroma_color[1], self.chroma_color[2], self.chroma_color[3]),
                   str(self.chroma_x), str(self.chroma_y),
                   str(self.chroma_scale),
                   '1', str(self.pres_x), str(self.pres_y),
                   str(self.pres_scale), str(self.screen_balance),
                   str(self.edge_kernel), str(self.clip_black),
                   str(self.clip_white), str(self.feather_distance),
                   str(self.post_blur), str(self.dilate_erode)]

        if self.__exec(command, update_progress_callback=update_progress_callback) != 0:
            raise AssertionError('[Arges] Fallo la previsualizacion')

    def __processAudio(self, video_input_path, video_output_path, start, duration, bitrate, freq, update_progress_callback):
        command = [self.avconv_comm, '-y', '-i', video_input_path, '-vn', '-acodec', 'libmp3lame', '-ac', '2',
                   '-ab', str(bitrate) + 'k', '-ar', str(freq), '-ss', str(start), '-t', str(duration),
                   'audioprofesor.mp3']
        if self.__exec(command, update_progress_callback=update_progress_callback) != 0:
            raise AssertionError('[Arges] Fallo el procesado del audio (avconv 1) con entrada "{}"'.format(video_input_path))

        command = [self.lame_comm, 'audioprofesor.mp3', '-m', 'r', '-b', '320', 'canalderecho.mp3']
        if self.__exec(command, update_progress_callback=update_progress_callback) != 0:
            raise AssertionError('[Arges] Fallo el procesado del audio (lame 1) con entrada "audioprofesor.mp3"')

        command = [self.avconv_comm, '-y', '-i', 'canalderecho.mp3', 'canalderecho.wav']
        if self.__exec(command, update_progress_callback=update_progress_callback) != 0:
            raise AssertionError('[Arges] Fallo el procesado del audio (avconv 2) con entrada "canalderecho.mp3"')

        command = [self.sox_comm, 'canalderecho.wav', '-c', '2', 'stereo.wav']
        if self.__exec(command, update_progress_callback=update_progress_callback) != 0:
            raise AssertionError('[Arges] Fallo el procesado del audio (sox) con entrada "canalderecho.wav"')

        command = [self.lame_comm, 'stereo.wav', '-m', 'j', '-b', '320', 'audioprofesorstereo.mp3']
        if self.__exec(command, update_progress_callback=update_progress_callback) != 0:
            raise AssertionError('[Arges] Fallo el procesado del audio (lame 2) con entrada "stereo.wav"')

        command = [self.avconv_comm, '-y', '-i', 'salida.avi', '-i', 'audioprofesorstereo.mp3', '-map', '0:0', '-map', '1',
                   '-vcodec', 'copy', '-acodec', 'copy', video_output_path]
        if self.__exec(command, update_progress_callback=update_progress_callback) != 0:
            raise AssertionError('[Arges] Fallo el procesado del audio con entrada "salida.avi" y "audioprofesorstereo.mp3"')

    def __exec(self, command, n_frames=1, pattern_percentage=None, pattern_eta=None, update_progress_callback=None):
        print('[Arges]', command)

        compiled_percentage_pattern = re.compile(pattern_percentage) if pattern_percentage is not None else None
        compiled_eta_pattern = re.compile(pattern_eta) if pattern_eta is not None else None

        progress = None
        eta = None
        last_frame = 0

        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, b''):
            print(line.strip())

            if compiled_percentage_pattern is not None:
                match = compiled_percentage_pattern.match(line)
                if match is not None:
                    last_frame = int(match.group(1))
                    progress = (last_frame / float(n_frames))
                else:
                    progress = None

            if compiled_eta_pattern is not None:
                match = compiled_eta_pattern.search(line)
                if match is not None:
                    eta_str = match.group(1).split(':')
                    eta = ((int(eta_str[0]) * 60) + float(eta_str[1])) * (n_frames - last_frame)
                    eta = time.strftime('%H:%M:%S', time.gmtime(eta))
                else:
                    eta = None

            if update_progress_callback is not None:
                if (progress is not None) or (eta is not None):
                    gobject.idle_add(update_progress_callback, progress, eta)

        return p.wait()
