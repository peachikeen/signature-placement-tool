from tkinter import filedialog
from tkinter import *
from PIL import Image, UnidentifiedImageError, ImageTk

def get_filelist():
    try:
        filenames =  filedialog.askopenfilenames(initialdir = "/", title = "Select images", filetypes = (("jpeg files","*.jpg"), ("png files", "*.png"), ("all files","*.*")))
        return filenames
    except FileNotFoundError:
        print("Image file does not exist.")

    except UnidentifiedImageError:
        print("Image file type is not supported.")



def get_watermark():
    try:
        watermark = filedialog.askopenfilename(initialdir = "/", title = "Select watermark", filetypes = (("jpeg files","*.jpg"), ("png files", "*.png"), ("all files","*.*")))
        return watermark
    except FileNotFoundError:
        print("Image file does not exist.")

    except UnidentifiedImageError:
        print("Image file type is not supported.")

def get_coordinates(bgimage, watermark):
    #TODO: Let the user define where the placement should be in terms of X and Y coordinates.
    #TODO: Resize the watermark over the images.
    
    #this sets up background image for the root window and its size
    #these window variables have a padding of 16 due to the default scrollbar width being 16 for tkinter widgets
    bgimgwidth, bgimgheight = bgimage.size
    if bgimgwidth > 800:
        windowwidth = 800
    else:
        windowwidth = bgimgwidth + 16

    if bgimgheight > 600:
        windowheight = 600
    else:
        windowheight = bgimgheight + 16

    #this sets up the fg image dimensions
    fgimgwidth, fgimgheight = watermark.size

    #check if the watermark is bigger than the bg image, if so, close and provide an error message.
    if fgimgwidth > bgimgwidth or fgimgheight > bgimgheight:
        print("Watermark exceeds size of background image. Please provide a smaller watermark.")
        exit(1)

    #this creates the root window
    root = Tk()
    root.geometry((f"{windowwidth}x{windowheight}"))

    #this converts the images passed into the function into PhotoImage objects which can be displayed
    background = ImageTk.PhotoImage(bgimage)
    signature = ImageTk.PhotoImage(watermark)

    #this creates a frame for the canvas to sit within, and allows us to make a scrollbar for UX purposes on larger images
    canvasframe = Frame(root, width = windowwidth, height = windowheight)
    canvasframe.pack(expand = True, fill = BOTH)
    
    #this creates the canvas and scroll bar inside of the root folder geometry, then creates the background image for the application function
    canvas = Canvas(canvasframe, width = windowwidth, height = windowheight, bg = 'white', highlightthickness = 0, scrollregion = (0, 0, bgimgwidth, bgimgheight))

    bgimageid = canvas.create_image(bgimgwidth, bgimgheight, image = background, anchor = SE)
    fgimageid = canvas.create_image(fgimgwidth, fgimgheight, image = signature, anchor = SE)

    vertibar = Scrollbar(canvasframe, orient = VERTICAL)
    horibar = Scrollbar(canvasframe, orient = HORIZONTAL)

    vertibar.pack(side = RIGHT, fill = Y)
    horibar.pack(side = BOTTOM, fill = X)

    vertibar.config(command = canvas.yview)
    horibar.config(command = canvas.xview)

    canvas.config(xscrollcommand = horibar.set, yscrollcommand= vertibar.set)
    canvas.pack(anchor = CENTER, expand = True, side = LEFT, fill = BOTH)


    #this creates global coordinates to save while pasting
    abscissa = 0
    ordinate = 0

    def destroy_self(event):
        nonlocal root
        root.destroy()        

    def move_images(event):
        nonlocal abscissa, ordinate
        x, y = 0, 0
        xstep = int(bgimgwidth/40)
        ystep = int(bgimgheight/40)

        match event.keysym:
            case 'Up':
                x = 0
                y = -ystep
                ordinate += y
            case 'Down':
                x = 0
                y = ystep
                ordinate += y
            case 'Left':
                x = -xstep
                y = 0
                abscissa += x
            case 'Right':
                x = xstep
                y = 0
                abscissa += x

        #this ensures the watermark stays bounded within the confines of the background image        
        if ordinate < 0:
            y = -ystep - ordinate
            ordinate = 0
        elif abscissa < 0:
            x = -xstep - abscissa
            abscissa = 0
        elif ordinate > (bgimgheight - fgimgheight):
            y = ystep - (ordinate - (bgimgheight - fgimgheight))
            ordinate = bgimgheight - fgimgheight
        elif abscissa > (bgimgwidth - fgimgwidth):
            x = xstep - (abscissa - (bgimgwidth - fgimgwidth))
            abscissa = bgimgwidth - fgimgwidth

        canvas.move(fgimageid, x, y)

    root.bind('<Key>', move_images)
    root.bind("<Return>", destroy_self)

    root.mainloop()
    return abscissa, ordinate
    

def sign_image(filenames, watermarkpath):
    finished_images = []
    try:
        with (Image.open(watermarkpath) as watermark):
                
            for file in filenames:
                with (Image.open(file) as img):
                    print(f"Watermarking {file}...")

                    imgx, imgy = get_coordinates(img, watermark)

                    img.paste(watermark, (imgx, imgy), mask = watermark.getchannel('A'))
                    finished_images.append(img)
                        
    except FileNotFoundError:
        print("Image file does not exist.")

    except UnidentifiedImageError:
        print("Image file type is not supported.")
        
    except PermissionError:
        print("User did not provide images or program was unable to access those images files due to lacking permission.")

    return finished_images


def save_to_disk(finished_images):

    for img in finished_images:
        while True:
            try:
                saved_file = filedialog.asksaveasfilename(initialdir = "/", defaultextension = (("jpeg files", ".jpg"), ("png files", ".png")), 
                    title = "Select file", filetypes = (("jpeg files", ".jpg"), ("png files", ".png")))
                print(saved_file)
                if ".jpg" in saved_file:
                    img = img.convert("RGB")
                elif ".png" in saved_file:
                    img = img.convert("RGBA")
                img.save(saved_file)

            except OSError:
                print("File could not be written. Verify that a file with that name does not already exist.")
                continue
            except ValueError:
                print("No filename provided to save. Please reopen the program and provide a filename to save.")
            break


def main():

    filelist = get_filelist()
    watermark = get_watermark()
    signedimages = sign_image(filelist, watermark)
    save_to_disk(signedimages)



if __name__ == "__main__":
    main()