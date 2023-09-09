import os
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog
from tqdm import tqdm
from PIL import Image, ImageTk
#import time
import threading

__author__ = 'Barremans'
__copyright__ = 'Copyright (C) 2023, Barremans'
__credits__ = ['barre']
__license__ = 'GNU'
__version__ = '1.0.0'
__maintainer__ = 'Barremans'
__email__ = 'zombiekillers.be@gmail.com'
__status__ = 'RC1'

_AppName_ = 'CGK TOOLS'

# Constants and variables
FRAME_BGCOLOR = "#C4281A"
FONTCOLORW = "#FFFFFF"
FONTCOLORY = "#FFFF00"
FONT1 = ("Arial", 12)  # Set custom font


# Class
class ImageLabel(tk.Label):
    def __init__(self, parent, image_path, x, y, width, height):
        super().__init__(parent, borderwidth=0)
        self.image_path = image_path
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.load_and_display_image()

    def load_and_display_image(self):
        pil_image = Image.open(self.image_path)
        pil_image.thumbnail((self.width, self.height))
        self.image = ImageTk.PhotoImage(pil_image)
        self.config(image=self.image)
        self.place(x=self.x, y=self.y)

# Functions
def create_frame(root, bg_color):
    frame = tk.Frame(root, width=400, height=400)
    frame.config(bg=bg_color)
    return frame


def com_help():
    global CURRENT_FRAME
    global help_frame
    global logo_label_help_frame

    if CURRENT_FRAME:
        hide_frame(CURRENT_FRAME)
    clear_frame(CURRENT_FRAME)
    CURRENT_FRAME = help_frame
    show_frame(help_frame)
    lbl_help = tk.Label(help_frame, text="You clicked Help")
    lbl_help.pack()

    # Update the existing global variable
    logo_label_help_frame = ImageLabel(
        help_frame, logo_image_path, x=XVAL, y=YVAL, width=200, height=200)
        # Create a new nested frame under the existing nested frame for the logo
    logo_frame = tk.Frame(help_frame, bg=FRAME_BGCOLOR)
    logo_frame.pack(pady=5)


def com_move():
    global CURRENT_FRAME
    global move_frame
    global logo_label_move_frame

    if CURRENT_FRAME:
        hide_frame(CURRENT_FRAME)
    clear_frame(CURRENT_FRAME)
    CURRENT_FRAME = move_frame
    show_frame(move_frame)

    lbl_introtxt = "Bestanden worden van de lokale gebruiker download map overgezet naar de C:\COD map. \n Indien COD map niet bestaat, dan wordt deze aangemaakt \n Na het verplaatsen zal de COD map automatisch geopend worden."
    lbl_intro = tk.Label(move_frame, text=lbl_introtxt,
                         bg=FRAME_BGCOLOR, fg=FONTCOLORW, pady=20)
    lbl_intro.pack()

    # Create a nested frame within move_frame
    L1_move_frame = tk.Frame(move_frame, bg=FRAME_BGCOLOR)
    L1_move_frame.pack(pady=10)
    # Create a label and button at the bottom
    lbl_move = tk.Label(L1_move_frame, text="Move .COD Files.",
                        bg=FRAME_BGCOLOR, fg=FONTCOLORW, pady=5, font=("Arial", 14))
    lbl_move.pack()
    btn_move = tk.Button(
        L1_move_frame, text="Move Files and Open Directory", font=("Arial", 12), command=lambda: move_cod_files(status_label, progress_bar))
    btn_move.pack(padx=0, pady=0, side="top")
    
    # Create a new nested frame under the existing nested frame
    L2_move_frame = tk.Frame(L1_move_frame, bg=FRAME_BGCOLOR)
    L2_move_frame.pack(pady=5)

    # Create a new style for the progress bar
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("blue.Horizontal.TProgressbar",
                    foreground="blue", background="green")

    # Create a progress bar with the custom style
    progress_bar = ttk.Progressbar(
        L2_move_frame, style="blue.Horizontal.TProgressbar", orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=5)
    
    # Update the existing global variable
    logo_label_move_frame = ImageLabel(
        move_frame, logo_image_path, x=XVAL, y=YVAL, width=200, height=200)

    # Create a new nested frame under the existing nested frame
    l3_move_frame = tk.Frame(L1_move_frame, bg=FRAME_BGCOLOR)
    l3_move_frame.pack(pady=5)
    # Create a label and button at the bottom
    lbl_movesource = tk.Label(l3_move_frame, text="Choose Source Folder and Move *.COD Files",
                              bg=FRAME_BGCOLOR, fg=FONTCOLORW, font=("Arial", 14))
    lbl_movesource.pack(padx=20, pady=5, side="bottom")
    btn_choosesource = tk.Button(
        l3_move_frame, text="Choose Source and Move", font=("Arial", 12), command=lambda: choose_source_and_move(status_label, progress_bar))
    btn_choosesource.pack(padx=20, pady=5, side="bottom")

    # Create a new nested frame under the existing nested frame
    l4_move_frame = tk.Frame(L1_move_frame, bg=FRAME_BGCOLOR)
    l4_move_frame.pack(pady=5)
    # Create a label for moving status
    status_label = tk.Label(L1_move_frame, text="", bg=FRAME_BGCOLOR, fg=FONTCOLORW, font=("Arial", 14))
    status_label.pack(padx=20, pady=5, side="bottom")   

    # Create a new nested frame under the existing nested frame for the logo
    logo_frame = tk.Frame(L1_move_frame, bg=FRAME_BGCOLOR)
    logo_frame.pack(pady=5)

def clear_frame(frame):
    if frame is not None:
        for widget in frame.winfo_children():
            widget.destroy()

def show_frame(frame):
    frame.pack(fill="both", expand=1)

def hide_frame(frame):
    frame.pack_forget()

# Function to count files with a specific extension in a folder
def count_files_with_extension(folder, extension):
    file_list = [f for f in os.listdir(folder) if f.endswith(
        extension) and os.path.isfile(os.path.join(folder, f))]
    return len(file_list)

# Function to move .COD files
def move_cod_files(status_label, progress_bar, source_folder=None):
    # Get the logged-in user's home directory
    logged_user = os.path.expanduser("~")
    # Construct the destination path
    cod_folder = os.path.join(logged_user, "COD")

    if not source_folder:
        # Default source path if not provided
        downloads_folder = os.path.join(logged_user, "Downloads")
    else:
        downloads_folder = source_folder

    # Ensure the destination directory exists
    os.makedirs(cod_folder, exist_ok=True)

    num_cod_files_downloads = count_files_with_extension(
        downloads_folder, ".COD")
    cod_files_to_move = [f for f in os.listdir(
        downloads_folder) if f.endswith(".COD")]
    #print(num_cod_files_downloads) //test only
    if cod_files_to_move:
        total_files_to_move = len(cod_files_to_move)

        # Update progress bar and move files
        for i, cod_file in enumerate(cod_files_to_move):
            source_path = os.path.join(downloads_folder, cod_file)
            base_name, extension = os.path.splitext(cod_file)
            destination_path = os.path.join(cod_folder, cod_file)
            # Start the simulation of progress
            # Update progress bar
            progress_bar["value"] = (i + 1) / total_files_to_move * 100
            progress_bar.update()
            
            # Handle duplicate filenames
            counter = 1
            while os.path.exists(destination_path):
                new_filename = f"{base_name}_{counter}{extension}"
                destination_path = os.path.join(cod_folder, new_filename)
                counter += 1
            shutil.move(source_path, destination_path)

        # After all files are moved, open the Explorer window
        verify_moved_files(cod_folder, len(cod_files_to_move), status_label)
        stored_progress = progress_bar["value"]  # Store the current progress value
        progress_bar.stop() # Stop the progress bar after all files are moved
        subprocess.Popen(['explorer', cod_folder]) # Open the COD directory
        # Update the progress bar to the stored value after opening the folder
        progress_bar["value"] = stored_progress
    else:
            status_label.config(text="No Files to Move: No files needed to move.")

# Function to verify moved files
def verify_moved_files(path, moved_count, status_label):
    moved_cod_files = count_files_with_extension(path, ".COD")
    if moved_cod_files == moved_count:
        status_label.config(
        text=f"All Files Moved: {moved_count} *.cod files moved to COD folder.", fg=FONTCOLORY)
    else:
        status_label.config(
        text=f"Some Files Not Moved: {moved_cod_files}/{moved_count} *.cod files moved to COD folder.", fg="red")


# Function to choose source folder and move *.COD files
"""
def choose_source_and_move():
    source_folder = filedialog.askdirectory(title="Choose Source Directory")
    if source_folder:
        move_cod_files(source_folder)
        status_label.config(text=f"Moved *.cod files from {source_folder} to COD folder", fg="green")

"""
def choose_source_and_move(status_label, progress_bar):
    source_folder = filedialog.askdirectory(title="Choose Source Directory")
    if source_folder:
        # Clear previous status and progress
        status_label.config(text="")
        progress_bar["value"] = 0
        progress_bar.start()

        # Move the files in a separate thread
        def move_files_in_thread(root):
            # Ensure the destination directory exists
            # Get the logged-in user's home directory
            logged_user = os.path.expanduser("~")
            # Construct the destination path
            cod_folder = os.path.join(logged_user, "COD")
            os.makedirs(cod_folder, exist_ok=True)
            num_cod_files_downloads = count_files_with_extension(source_folder, ".COD")
            cod_files_to_move = [f for f in os.listdir(source_folder) if f.endswith(".COD")]

            if cod_files_to_move:
                total_files_to_move = len(cod_files_to_move)
                for i, cod_file in enumerate(cod_files_to_move):
                    source_path = os.path.join(source_folder, cod_file)
                    base_name, extension = os.path.splitext(cod_file)
                    destination_path = os.path.join(cod_folder, cod_file)  # Fixed destination path
                    counter = 1
                    while os.path.exists(destination_path):
                        new_filename = f"{base_name}_{counter}{extension}"
                        #destination_path = os.path.join(cod_folder, new_filename)
                        destination_path = os.path.join(cod_folder, os.path.basename(cod_file))
                        try:
                            shutil.move(source_path, destination_path)
                        except PermissionError as e:
                            status_label.config(text=f"Permission Error: {e}", fg="red")
                            return
                        counter += 1
                    shutil.move(source_path, destination_path)
                    # Update progress bar
                    progress_bar["value"] = (i + 1) / total_files_to_move * 100
                    #root.after(100, update_progress, new_value)
                    progress_bar.update()

                status_label.config(text="Files moved successfully.")
                # After all files are moved, open the Explorer window
                verify_moved_files(cod_folder, len(cod_files_to_move), status_label)
                subprocess.Popen(['explorer', cod_folder])  # Open the COD directory
                progress_bar.stop()  # Stop the progress bar after all files are moved
                # Set progress bar to full
                progress_bar["value"] = 100

            else:
                status_label.config(text="No Files to Move: No files needed to move.")
                progress_bar.stop()  # Stop the progress bar if no files

        # Start a new thread for moving files
        #threading.Thread(target=move_files_in_thread).start()
        threading.Thread(target=move_files_in_thread, args=(root,)).start()

        

# Function to count files with a specific extension
def count_files_with_extension(directory, extension):
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            count += 1
    return count
    
## END FUNCTIONS ##

# Create application
root = tk.Tk()
root.title("CGK tool application")
root.config(bg="#C4281A")

# Calculate the center coordinates of the window
fixed_width = 800
fixed_height = 500
x_center = root.winfo_screenwidth() // 2 - fixed_width // 2
y_center = root.winfo_screenheight() // 2 - fixed_height // 2
YVAL = y_center + 0.3 * fixed_width  # Adjust as needed
XVAL = x_center + 0.3 * fixed_height  # Adjust as needed
#YVAL = y_center + 200
#XVAL = x_center + 150

root.geometry(f'{fixed_width}x{fixed_height}+{x_center}+{y_center}')
# Disallow resizing
root.resizable(False, False)

# Create menu
main_menu = tk.Menu(root)
root.config(menu=main_menu)

# Frame logic
CURRENT_FRAME = None  # To keep track of the current visible frame

# Load and display a background image using PIL in main frame
script_directory = os.path.dirname(os.path.abspath(__file__))
bg_image_path = os.path.join(script_directory, "images", "cgk_bg.jpg")
bg_pil_image = Image.open(bg_image_path)
bg_pil_image = bg_pil_image.resize((fixed_width, fixed_height), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_pil_image)
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Fetch another image and display it in a label
logo_image_path = os.path.join(script_directory, "images", "cgk_bg.jpg")
logo_pil_image = Image.open(logo_image_path)
logo_pil_image.thumbnail((100, 100))  # Resize the image to 100x100
logo_image = ImageTk.PhotoImage(logo_pil_image)

# Set the application icon
icon_path = os.path.join(script_directory, "images", "CGKico.ico")
root.iconbitmap(icon_path)

# menu's
first_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="File", menu=first_menu)
first_menu.add_command(label="Help", command=com_help)
first_menu.add_command(label="Exit", command=root.quit)

move_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Files", menu=move_menu)
move_menu.add_command(label="Move *.COD", command=com_move)

# Create the move_frame with logo
help_frame = create_frame(root, bg_color=FRAME_BGCOLOR)

# Create the move_frame with logo
move_frame = create_frame(root, bg_color=FRAME_BGCOLOR)


# Execution loop
root.mainloop()