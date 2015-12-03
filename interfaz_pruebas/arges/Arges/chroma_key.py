import sys
import bpy


def renderFrame(scene, frame=1, filename='preview'):
    scene.frame_set(frame)
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.filepath = '//' + filename
    bpy.ops.render.render(write_still=True)


def renderVideo(scene, end_frame):
    scene.frame_end = end_frame
    bpy.ops.render.render(animation=True)


def main(argv):
    scene = bpy.data.scenes["Chroma"]
    input_chroma_color = scene.node_tree.nodes["Keying"].inputs[1]

    input_pos_prof_x = scene.node_tree.nodes["Transform"].inputs[1]
    input_pos_prof_y = scene.node_tree.nodes["Transform"].inputs[2]
    input_prof_scale = scene.node_tree.nodes["Transform"].inputs[4]

    input_pos_pres_x = scene.node_tree.nodes["Transform.002"].inputs[1]
    input_pos_pres_y = scene.node_tree.nodes["Transform.002"].inputs[2]
    input_pres_scale = scene.node_tree.nodes["Transform.002"].inputs[4]

    input_keying = scene.node_tree.nodes["Keying"]

    argv = argv[argv.index("--") + 1:]
    input_chroma_color.default_value = eval(argv[1])
    input_pos_prof_x.default_value = float(argv[2])
    input_pos_prof_y.default_value = float(argv[3])
    input_prof_scale.default_value = float(argv[4])

    input_pos_pres_x.default_value = float(argv[6])
    input_pos_pres_y.default_value = float(argv[7])
    input_pres_scale.default_value = float(argv[8])

    input_keying.screen_balance = float(argv[9])
    input_keying.edge_kernel_tolerance = int(argv[10])
    input_keying.clip_black = float(argv[11])
    input_keying.clip_white = float(argv[12])
    input_keying.feather_distance = int(argv[13])
    input_keying.blur_post = int(argv[14])
    input_keying.dilate_distance = int(argv[15])

    if 'frame' in argv[0]:
        renderFrame(scene, frame=int(argv[5]))
    elif 'video' in argv[0]:
        renderVideo(scene, end_frame=int(argv[5]))

if __name__ == "__main__":
    main(sys.argv)
