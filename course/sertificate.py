from PIL import Image, ImageDraw, ImageFont

image = Image.open("sertifikat.png")
font = ImageFont.truetype("arial.ttf", 55)
draw = ImageDraw.Draw(image)
draw.text((100, 100), "request.username", font=font, fill=(255, 255, 255))

image.save()
