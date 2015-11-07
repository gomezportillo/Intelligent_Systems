import subprocess


class ArgesCore:
    def __init__(self):
        self.avconv_comm = 'avconv'
        self.blender_comm = 'blender'

    def processInputVideo(self, video_path, start, duration, output, width=1920, height=1080, fps=25):
        l = duration.split(':')
        if len(l) != 3:
            raise ValueError('Duracion incorrecta ({}?)'.format(duration))

        number_of_frames = (int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])) * 25

        command = '{} -v info -y -i {} -vcodec wmv1 -qscale 0 -s {}x{} -ss {} -t {} -r {} {}' \
                  .format(self.avconv_comm, video_path, width, height, start, duration, fps, output)
        if self.__exec(command, number_of_frames) != 0:
            raise AssertionError('Fallo el procesado del video "{}"'.format(video_path))

    def processChromaKey(self, duration, fps=25):
        l = duration.split(':')
        if len(l) != 3:
            raise ValueError('Duracion incorrecta ({}?)'.format(duration))

        number_of_frames = (int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])) * 25
        command = 'blender -b arges.blend -s 1 -e {} -a' \
                  .format(self.blender_comm, number_of_frames)

        if self.__exec(command, number_of_frames) != 0:
            raise AssertionError('Fallo el procesado del chroma')

    def processAudio(self, video_input_path, video_output_path, bitrate=256, freq=48000):
        command = '{} -y -i {} -vn -acodec libmp3lame -ac 2 -ab {}k -ar {} audioprofesor.mp3' \
                  .format(self.avconv, video_input_path, bitrate, freq)
        if self.__exec(command) != 0:
            raise AssertionError('Fallo el procesado del audio con entrada "{}"'.format(video_input_path))

        command = '{} -y -i salida.avi -i audioprofesor.mp3 -map 0:0 -map 1 -vcodec copy -acodec copy {}' \
                  .format(self.avconv, video_output_path)
        if self.__exec(command) != 0:
            raise AssertionError('Fallo el procesado del audio con salida "{}"'.format(video_output_path))

    def __exec(self, command, n_frames):
        print '---', command
        p = subprocess.Popen(command, shell=False)
        for line in iter(p.stdout.readline, ''):
            # Regex: /frame=\s+\d+/
            pass

        return p.wait()


if __name__ == "__main__":
    arges = Arges()

    try:
        arges.processInputVideo('video_de_la_capturadora.ts', '00:00:10', '00:10:00', 'presentacion.avi')
        arges.processInputVideo('video_del_profesor.mp4', '00:00:10', '00:00:20', 'profesor.avi')
        arges.processChromaKey('00:10:00')
        arges.processAudio('profesor.avi', 'final.avi')
    except (AssertionError, ValueError) as error:
        print error
