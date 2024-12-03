**Title:** Signature Placement Tool
**Video Demo URL:** https://youtu.be/bgFtUcwTt8A
**Github Depo URL:** https://github.com/peachikeen/signature-placement-tool.git
Project Description: An image editing tool within which an artist can supply one image (a signature) to be placed on top of another image (their artwork) in order to create a combined image. The tool has adjustable placement for the signature, can apply to multiple images at once, and can accept specified ranges for signature placement based on canvas shape (square, portrait, landscape).
**Credits:** Signature Placement Tool by PD Garcia for ANGM 2305.0W1 - Programming for Digital Arts final project

**How to run program:**
1) Open the .py file and select your background image(s) in the GUI prompt. Sample images have been provided for the background image(s), but the user can utilize their own.
2) Next, provide your watermark you wish to use for this image. Sample images have been provided for the watermark image, but the user can utilize their own.
3) Next, you can utilize the arrow keys to position the watermark and scrollbars to navigate your background image (if needed) and place your watermark into the desired position.
4) Hit enter or close the window when you want to place your watermark.
5) Finally, name and save your finished image.

**Purpose of the program:**
This program is meant for digital artists to be able to place their watermark onto a background image using a GUI interface.
The user can submit multiple images as the background, but only one for the watermark/signature. This is then saved to disk after the user places it.
Provided in the src folder are some background images for testing. Two watermarks of various sizes are provided as well.

**Design Considerations:** The GUI is simple, but was very much a fun challenge to implement. It utilizes the tkinter library of widgets to allow the user to open images, save images, and overlay their selections on top of each other as well. Figuring out how to keep the movement of the watermark during placement synced with the final placement of the watermark was tricky. In the end, it required a bit of conversion between a local X and Y variable during the moving process, and a nonlocal abscissa and ordinate for the original image that is used when the pasting operation of both images is completed.

**Future Areas of Improvement:** Three things spring to mind immediately. First, zooming the background image to fit the canvas would be ideal, and the scrollbars were utilized as a simpler measure that was within the scope of my current abilities as a programmer for implementation. The second would be, that the scrollbars provided are hidden if unneeded for the purposes of signature placement. Third, having the signature able to be controlled by a click and drag motion in addition to the measured arrow key presses would be useful for user experience.