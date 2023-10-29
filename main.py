import os
from subprocess import Popen, PIPE

image_path = os.path.join(os.getcwd(), "images")
files = os.path.join(image_path, "%d.jpeg")


def makeSlideshow(count, duration, transitionEffect):
    cmd = ['ffmpeg']
    i = 1
    while i <= count:
        cmd.append('-loop')
        cmd.append('1')
        cmd.append('-t')
        cmd.append(str(duration))
        cmd.append('-i')
        cmd.append(os.path.join(image_path, str(i) + ".jpeg"))
        i = i + 1
    cmd.append('-filter_complex')

    filterComplex = ""
    i = 0
    j = 0
    offset = 0

    while i < count - 1:
        offset = duration + offset - 0.5
        if filterComplex == "":
            filterComplex = "[{0}][{1}]xfade=transition=".format(i,
                                                                 i + 1) + transitionEffect + ":duration=0.5:offset={1}[f{0}];".format(
                j, offset)
            i = i + 1
        else:
            filterComplex = filterComplex + "[f{0}][{1}]xfade=transition=".format(j,
                                                                                  i + 1) + transitionEffect + ":duration=0.5:offset={1}[f{0}];".format(
                i, offset)
            j = j + 1
            i = i + 1

    print(filterComplex)

    cmd.append(filterComplex)
    cmd.append('-map')
    cmd.append('[f{0}]'.format(j))
    cmd.append('-r')
    cmd.append('25')
    cmd.append('-pix_fmt')
    cmd.append('yuv420p')
    cmd.append('-vcodec')
    cmd.append('libx264')
    cmd.append('output.mp4')

    print(cmd)

    startProcess(cmd)

    return "output.mp4"


def makeFadeInFadeOut(fileName, duration):
    # Fade in Fade out

    cmd = ['ffmpeg', '-i', os.path.join(os.getcwd(), fileName), '-vf', 'fade=t=in:st=0:d=' + str(duration), '-c:a',
           'copy',
           'out.mp4']
    startProcess(cmd)


def startProcess(cmd):
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    print(stdout)
    print(stderr)


mixedFile = makeSlideshow(4, 3.5, "wipeleft")
makeFadeInFadeOut(mixedFile, 1)
os.remove("output.mp4")
