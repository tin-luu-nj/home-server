from PIL import Image, ImageDraw, ImageFont

# Create a blank image with a white background
img = Image.new('RGB', (200, 100), (255, 255, 255))

# Initialize ImageDraw
d = ImageDraw.Draw(img)

# Specify the font, size, and color
font = ImageFont.truetype('arial.ttf', 15)
text = "Hello World"
color = (0, 0, 0)  # RGB color code for black

# Get the bounding box of the text
bbox = font.getbbox(text)

# Calculate the width and height of the text
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Calculate the x and y coordinates to center the text
x = (img.width - text_width) / 2
y = (img.height - text_height) / 2

# Draw the text on the image
d.text((x, y), text, font=font, fill=color)

# Save the image
img.save('tests/unit/database/src_pyPkmHome/image_process_test_001.png')
