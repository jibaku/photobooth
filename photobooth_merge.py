#!/usr/bin/python
from PIL import Image
from PIL import ImageColor
from PIL import ImageFont
from PIL import ImageDraw

font_path = "/System/Library/Fonts/Menlo.ttc"


def merge_photo(*photos, **kwargs):
    """
    Merge photo in a "photobooth" like design.
    """
    margin = kwargs.get('margin', 20)
    side = kwargs.get('side', 20)
    margin_top = kwargs.get('margin_top', 20)
    margin_bottom = kwargs.get('margin_bottom', 20)
    y = 0 + margin_top
    max_width = max([Image.open(photo_path).size[0] for photo_path in photos]) + side*2
    heigth = sum([Image.open(photo_path).size[1] for photo_path in photos])
    heigth += (len(photos)-1)*margin + (margin_top+margin_bottom)

    merged = Image.new("RGB", (max_width, heigth))
    merged.paste(ImageColor.getrgb("black"), (0, 0, max_width, heigth))
    for photo_path in photos:
        im = Image.open(photo_path)
        merged.paste(im, (side, y))
        y += im.size[1] + margin

    draw = ImageDraw.Draw(merged)
    font = ImageFont.truetype(font_path, 72)
    draw.text((20, heigth-72*2-20), "21 mars 2015", (255, 255, 255), font=font)
    draw.text((20, heigth-72-20), "   N <3 F", (255, 255, 255), font=font)
    merged.show()
    # save merged rather than show

if __name__ == "__main__":
    merge_photo(
        "booth/2013_10_15_6883.jpg",
        "booth/2013_10_15_6886.jpg",
        "booth/2013_10_15_6895.jpg",
        "booth/2013_10_15_6908.jpg",
        margin=30,
        margin_top=30,
        margin_bottom=200,
        side=30
    )