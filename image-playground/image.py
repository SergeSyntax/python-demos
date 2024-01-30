from PIL import Image, ImageFilter

img = Image.open("./images/pikachu.jpg")

# filtered_img = img.convert("L")
# # filtered_img = img.filter(ImageFilter.SHARPEN)
# # crooked = filtered_img.rotate(90)
# # resized = filtered_img.resize((300, 300))
# box = (100, 100, 400, 400)
# region = filtered_img.crop(box)

# region.save("grey.png", "png")
# region.show()
# print(img.mode)
# print(img.format)
# print(dir(img))


img = Image.open("./astro.jpg")

img.thumbnail((400, 200))
img.save("thumbnail.jpg")
