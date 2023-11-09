import os
import subprocess
from subprocess import Popen, PIPE

image_path = os.path.join(os.getcwd(), "pics")
overlay_path = os.path.join(os.getcwd(), "images/overlays")
video_path = os.path.join(os.getcwd(), "videos")
files = os.path.join(image_path, "%d.jpeg")


def makeSlideshow(count, duration, transitionEffect):
    cmd = ['ffmpeg','-y']
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

    filterComplex1 = ""
    filterComplex2 = ""

    i = 0

    while i < count:
        if filterComplex1 == "":
            filterComplex1 = "[{0}]scale=1920:1280:force_original_aspect_ratio=decrease,pad=1920:1280:-1:-1[s{0}];".format(
                i)

        else:
            filterComplex1 = filterComplex1 + "[{0}]scale=1920:1280:force_original_aspect_ratio=decrease,pad=1920:1280:-1:-1[s{0}];".format(
                i)
        i = i + 1

    j = 0
    offset = 0
    i = 0
    while i < count - 1:
        offset = duration + offset - 0.5
        if filterComplex2 == "":
            filterComplex2 = "[s{0}][s{1}]xfade=transition=".format(i,
                                                                    i + 1) + transitionEffect + ":duration=0.5:offset={1}[f{0}];".format(
                j, offset)
            i = i + 1
        else:
            filterComplex2 = filterComplex2 + "[f{0}][s{1}]xfade=transition=".format(j,
                                                                                     i + 1) + transitionEffect + ":duration=0.5:offset={1}[f{0}];".format(
                i, offset)
            j = j + 1
            i = i + 1

    print(filterComplex2)

    filterComplex = filterComplex1 + filterComplex2

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

    length = duration * count - 0.5 * (count - 1)
    print(length)
    startProcess(cmd)
    return ("output.mp4", length)


def makeFadeInFadeOut(fileName, duration):
    # Fade in Fade out

    cmd = ['ffmpeg','-y' ,'-i', os.path.join(os.getcwd(), fileName[0]), '-vf',
           'fade=t=in:st=0:d=' + str(duration) + ',fade=t=out:st=' + str(fileName[1] - duration) + ':d=' + str(
               duration), '-c:a',
           'copy',
           'out.mp4']
    startProcess(cmd)


def addImageOverlay(fileName, milestone):
    cmd = ['ffmpeg','-y', '-i', os.path.join(os.getcwd(), 'output.mp4'), '-i', os.path.join(overlay_path, milestone),
           '-filter_complex', "[0:v][1:v] overlay=0:100", "-c:a", "copy", "out1.mp4"]

    startProcess(cmd)

    return ("out1.mp4", fileName[1])


def startProcess(cmd):
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    print(stdout)
    print(stderr)


mixedFile = makeSlideshow(7, 3.9, "hlslice")
overlay = addImageOverlay(mixedFile, "double_l1.png")
makeFadeInFadeOut(overlay, 1)

os.remove("output.mp4")
os.remove("out1.mp4")

