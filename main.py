import os
from threading import Thread

import customtkinter
from PIL import Image
from tkinter import filedialog as fd
from subprocess import Popen, PIPE

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

image_path = os.path.join(os.getcwd(), "images")

add_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "plus.png")), size=(15, 15))
trash_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "delete.png")), size=(15, 15))

minus_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "minus.png")), size=(15, 15))
close_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "close.png")), size=(12, 12))
close_image_modal = customtkinter.CTkImage(Image.open(os.path.join(image_path, "close.png")), size=(20, 20))
play_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "play.png")), size=(16, 16))
stop_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "stop-button.png")), size=(18, 18))

new_file = customtkinter.CTkImage(Image.open(os.path.join(image_path, "add-document.png")), size=(17, 17))
open_file = customtkinter.CTkImage(Image.open(os.path.join(image_path, "open.png")), size=(17, 17))
save_file = customtkinter.CTkImage(Image.open(os.path.join(image_path, "disk.png")), size=(17, 17))

milestones = {
    "F2": "f2.png",
    "Gold Star": "gold.png",
    "L1": "l1.png",
    "Double L1": "double_l1.png",
    "L2": "l2.png",
    "Half Century": "half_century.png",
    "L3": "l3.png",
    "Century": "century.png"
}
milestone = ""
listOfImages = []


class Header(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.lblLogo = customtkinter.CTkLabel(self, text="Celebration Call Video Maker", font=("Skia", 30))
        self.lblLogo.grid(row=0, column=0, padx=10, pady=10)


class Footer(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # add widgets onto the frame, for example:
        self.configure(fg_color="transparent")
        self.credit = customtkinter.CTkLabel(self,
                                             text="Crafted with \U00002764 by Sayantan",
                                             font=("Skia", 12))
        self.credit.grid(row=0, column=0, padx=10, pady=5)


class Body(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.lblBody = customtkinter.CTkLabel(self,
                                              text="Added images :",
                                              font=("Skia", 14),
                                              anchor="w")
        self.lblBody.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="new")

        self.titleButtonBar = customtkinter.CTkFrame(self, fg_color="transparent")
        self.titleButtonBar.grid(row=0, column=1, padx=(10, 15), pady=(10, 5), sticky="ne")
        self.titleButtonBar.grid_columnconfigure(0, weight=1)

        self.add = customtkinter.CTkButton(self.titleButtonBar,
                                           image=add_image,
                                           text="",
                                           width=34,
                                           height=34,
                                           corner_radius=0,
                                           command=self.add
                                           )
        self.add.grid(row=0, column=0, padx=(10, 5), sticky="ne")
        self.trash = customtkinter.CTkButton(self.titleButtonBar,
                                             image=trash_image,
                                             text="",
                                             width=34,
                                             height=34,
                                             corner_radius=0,
                                             command=self.clearAll
                                             )
        self.trash.grid(row=0, column=1, padx=(5, 5), sticky="ne")

        self.images = ImageList(self, self.selectedImage)
        self.images.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nsew")

        self.imgPreview = customtkinter.CTkFrame(self, fg_color="transparent")
        self.imgPreview.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="nsew")

        self.lblImage = customtkinter.CTkLabel(self.imgPreview, text="")
        self.lblImage.grid(row=0, column=0)

        self.frameControl1 = customtkinter.CTkFrame(self, height=90, fg_color="transparent")
        self.frameControl1.grid(row=2, column=0, sticky="nsew", padx=(10, 5), pady=10)

        self.lblEffect = customtkinter.CTkLabel(self.frameControl1, text="Effect : ", font=("Skia", 18))
        self.lblEffect.grid(row=0, column=0, padx=10, pady=5)

        self.dropdownEffect = customtkinter.CTkOptionMenu(self.frameControl1,
                                                          values=["hlslice", "circlecrop", "wipeleft", "slideright",
                                                                  "rectcrop",
                                                                  "hrslice"],
                                                          height=35,

                                                          font=("Skia", 20),
                                                          command=self.dropdownEffect_callback)
        self.dropdownEffect.grid(row=0, column=1, padx=10, pady=5)

        self.lblMilestone = customtkinter.CTkLabel(self.frameControl1, text="Milestone : ", font=("Skia", 18))
        self.lblMilestone.grid(row=1, column=0, padx=10, pady=5)

        self.dropdownMilestone = customtkinter.CTkOptionMenu(self.frameControl1,
                                                             values=["F2", "Gold Star", "L1", "Double L1", "L2",
                                                                     "Half Century", "L3", "Century"],
                                                             height=35,

                                                             font=("Skia", 20),
                                                             command=self.dropdownMilestone_callback)
        self.dropdownMilestone.grid(row=1, column=1, padx=10, pady=5)

        self.frameControl2 = customtkinter.CTkFrame(self, height=90)
        self.frameControl2.grid(row=2, column=1, sticky="nsew", padx=(5, 10), pady=10)

        self.frameControl2.grid_rowconfigure(0, weight=1)

        self.btnStart = customtkinter.CTkButton(self.frameControl2,
                                                text="Start",
                                                font=("Skia", 25),
                                                fg_color="#6c6ceb",
                                                hover_color="#5555e8",
                                                corner_radius=0,
                                                height=50,
                                                command=self.start
                                                )
        self.btnStart.grid(row=0, column=0, padx=15, pady=10)

        self.lblStatus = customtkinter.CTkLabel(self.frameControl2, text="Status : ", font=("Skia", 13))
        self.lblStatus.grid(row=0, column=1, padx=10, pady=5)

    def add(self):
        paths = fd.askopenfilenames(title="Select Image Files", filetypes=(
            ('Image files', '*.jpeg *.jpg *.png'),
        )
                                    )
        if len(paths) > 0:
            print(paths)
            self.images.addImage(paths)

    def selectedImage(self, path):
        img = Image.open(path)
        ar = img.width / img.height
        print(ar)
        w = ar * 500
        im = customtkinter.CTkImage(img, size=(w, 500))
        self.lblImage.configure(image=im, text="")

    def clearAll(self):
        global listOfImages
        for img in self.images.listOfImages:
            img.grid_forget()
        self.images.listOfImages.clear()
        listOfImages.clear()
        self.lblImage.configure(image="", text="")
        print(len(listOfImages))

    def dropdownMilestone_callback(self, choice):

        global milestones
        #print(milestones.get(choice))


    def dropdownEffect_callback(self, choice):
        print(choice)


    def start(self):
        t1 = Thread(target=self.createVideo)
        t1.start()

    def createVideo(self):
        global milestones
        global listOfImages
        self.lblStatus.configure(text ="Status : Progress started !!")
        effect = self.dropdownEffect.get()
        milestone = milestones.get(self.dropdownMilestone.get())

        vid = VideoEditor()

        mixedFile = vid.makeSlideshow(listOfImages, 3.9, effect)
        self.lblStatus.configure(text="Status : Slideshow prepared !!")
        overlay = vid.addImageOverlay(mixedFile, milestone)
        self.lblStatus.configure(text="Status : Milestone overlay added !!")
        vid.makeFadeInFadeOut(overlay, 1)
        self.lblStatus.configure(text="Status : Added effects !!")

        os.remove("output.mp4")
        os.remove("out1.mp4")
        self.lblStatus.configure(text="Status : Progress completed successfully !!")


class ImageList(customtkinter.CTkScrollableFrame):
    def __init__(self, master, selectedImageFunc):
        super().__init__(master, width=300)
        self.listOfImages = []
        self.count = 0
        self.selectedImage = selectedImageFunc

        self.grid_columnconfigure(0, weight=1)

    def addImage(self, pathList):
        global listOfImages
        for path in pathList:
            self.count = self.count + 1
            img = ImageData(self, pathImage=path, selectedImageFunc=self.selectedImage, deleteFunc=self.deleteImage)
            img.grid(row=self.count, column=0, sticky="ew", pady=(5, 0))
            self.listOfImages.append(img)
            listOfImages.append(path)

        self.selectedImage(pathList[0])
        print(len(listOfImages))

    def deleteImage(self, path):
        global listOfImages
        for img in self.listOfImages:
            if img.path_image == path:
                img.grid_forget()
                self.listOfImages.remove(img)
                listOfImages.remove(img.path_image)

        print("deleted : " + path)
        print(len(listOfImages))


class ImageData(customtkinter.CTkFrame):
    def __init__(self, master, pathImage, selectedImageFunc, deleteFunc):
        super().__init__(master)
        self.path_image = pathImage
        self.selectedImage = selectedImageFunc
        self.delete = deleteFunc

        self.grid_columnconfigure(0, weight=1)

        self.bind("<Button-1>", self.select)

        self.lblImageName = customtkinter.CTkLabel(self, text=os.path.basename(self.path_image).split('/')[-1],
                                                   anchor="w")

        self.lblImageName.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.btnDeleteImage = customtkinter.CTkButton(self,
                                                      text="",
                                                      image=close_image,
                                                      # font=("Skia", 16),
                                                      fg_color="#ff4d4d",
                                                      hover_color="#ff3636",
                                                      width=25,
                                                      height=25,
                                                      corner_radius=0,
                                                      command=lambda: self.delete(self.path_image)
                                                      )
        self.btnDeleteImage.grid(row=0, column=1, sticky="e", padx=10, pady=10)

    def select(self, event):
        print(self.path_image)
        self.selectedImage(self.path_image)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.minsize(width=1200, height=800)
        self.title("Celebration Call Video Maker")

        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.header = Header(self)
        self.header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="new")

        self.body = Body(self)
        self.body.grid(row=1, column=0, padx=20, sticky="nsew")

        self.footer = Footer(self)
        self.footer.grid(row=2, column=0, sticky="sew")


class VideoEditor:
    def __init__(self):
        self.overlay_path = os.path.join(os.getcwd(), "images/overlays")

    def makeSlideshow(self,list, duration, transitionEffect):
        cmd = ['ffmpeg', '-y']
        i = 0
        while i < len(list):
            cmd.append('-loop')
            cmd.append('1')
            cmd.append('-t')
            cmd.append(str(duration))
            cmd.append('-i')
            cmd.append(list[i])
            i = i + 1
        cmd.append('-filter_complex')

        filterComplex1 = ""
        filterComplex2 = ""

        i = 0

        while i < len(list):
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
        while i < len(list) - 1:
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

        length = duration * len(list) - 0.5 * (len(list) - 1)
        print(length)
        self.startProcess(cmd)
        return ("output.mp4", length)

    def makeFadeInFadeOut(self,fileName, duration):
        # Fade in Fade out

        cmd = ['ffmpeg', '-y', '-i', os.path.join(os.getcwd(), fileName[0]), '-vf',
               'fade=t=in:st=0:d=' + str(duration) + ',fade=t=out:st=' + str(fileName[1] - duration) + ':d=' + str(
                   duration), '-c:a',
               'copy',
               'out.mp4']
        self.startProcess(cmd)

    def addImageOverlay(self,fileName, milestone):
        cmd = ['ffmpeg', '-y', '-i', os.path.join(os.getcwd(), 'output.mp4'), '-i',
               os.path.join(self.overlay_path, milestone),
               '-filter_complex', "[0:v][1:v] overlay=0:100", "-c:a", "copy", "out1.mp4"]

        self.startProcess(cmd)

        return ("out1.mp4", fileName[1])

    def startProcess(self,cmd):
        process = Popen(cmd, stdout=PIPE, stderr=PIPE)

        stdout, stderr = process.communicate()

        print(stdout)
        print(stderr)


app = App()
app.mainloop()
