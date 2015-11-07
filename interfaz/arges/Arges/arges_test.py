import sys
import arges


def full_process_test():
    ar = arges.Arges()
    ar.processInputVideo('profesor_raw.avi', '00:00:00', '00:00:05', 'profesor.avi')
    ar.processInputVideo('presentacion_raw.avi', '00:00:00', '00:00:05', 'presentacion.avi', 1280, 720)
    ar.processChromaKey('00:00:02')
    ar.processAudio('profesor.avi', 'video_final.avi', '00:00:00', '00:00:02')


def preview_test():
    ar = arges.Arges()
    ar.renderOneFrame()


def preview_modified_test():
    ar = arges.Arges()
    ar.setChromaSettings(x=1, y=1, scale=0.5)
    ar.renderOneFrame()


def main(argv):
    # full_process_test()
    preview_test()
    # preview_modified_test()

if __name__ == "__main__":
    main(sys.argv)
