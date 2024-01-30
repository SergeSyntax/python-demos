import sys
import os
from PIL import Image
import glob

# grab the first and second arg
print()

_active_file, import_folder, output_folder = sys.argv


# files_to_convert = os.listdir(import_folder)
files_to_convert = glob.glob(f"{import_folder}/*.jpg")

# check if folder exists if not create

if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

print(files_to_convert)

# loop through Pkedex
for file in files_to_convert:
    file_name_with_ext = os.path.basename(file)
    file_name, _ext = os.path.splitext(file_name_with_ext)

    with Image.open(file) as jpg_file:
        new_file_path = os.path.join(output_folder, f"{file_name}.png")
        jpg_file.save(new_file_path, format="png")

# print(jpg_file)
# os.path.splitext()

# jpg_file.save(f"")

# convert images to png


# save the new images
