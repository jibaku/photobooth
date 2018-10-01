#!/usr/bin/python
import argparse
import datetime
import logging
import os
import os.path
import subprocess
import time

from PIL import Image, ImageColor, ImageDraw, ImageFont


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(asctime)-15s | %(message)s"
)

parser = argparse.ArgumentParser()
parser.add_argument("--print", help="print pictures", dest="printing", action="store_true")
parser.add_argument("-s", "--snap", type=int, default=4, help="snap per user")
args = parser.parse_args()

PRINT = args.printing
SNAP_PER_PICTURE = args.snap

PHOTOBOOTH_DIR = os.path.expanduser("photobooth_images/")
logging.info("PHOTOBOOTH_DIR set to %s" % (PHOTOBOOTH_DIR,))
IMAGE_FILENAME = r"photobooth-%Y%m%d-%H%M%S.jpg"
MERGED_FILENAME = r"merged-%Y%m%d-%H%M%S.jpg"


def merge_photo(*photos, **kwargs):
    """
    Merge photo in a "photobooth" like design and return a Image instance.
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
    font = ImageFont.load_default()
    draw.text((20, heigth-72*2-20), "21 mars 2015", (255, 255, 255), font=font)
    draw.text((20, heigth-72-20), "   N <3 F", (255, 255, 255), font=font)
    return merged


class PhotoBooth(object):
    def __init__(self):
        pass

    def snap(self):
        """
        Capture and download Image
        """
        logging.info("Snap !")
        import datetime
        now = datetime.datetime.now()
        filename = os.path.join(PHOTOBOOTH_DIR, now.strftime(IMAGE_FILENAME))
        logging.info("snapping to {}".format(filename))
        cmd = "gphoto2 --capture-image-and-download --filename %s" % (
            filename
        )
        try:
            gpout = subprocess.check_output(cmd,
                                            stderr=subprocess.STDOUT,
                                            shell=True)
        except subprocess.CalledProcessError:
            logging.error("Impossible to call gphoto2")
            return (False, None)

        logging.info(gpout)
        if b"ERROR" not in gpout:
            return (True, filename)
        else:
            return (False, None)

    def merge(self, pictures_list, save_as):
        """
        Merge picture passed as parameter
        """
        merged = merge_photo(*pictures_list,
                             margin=30,
                             margin_top=30,
                             margin_bottom=200,
                             side=30)
        merged.save(save_as)


if __name__ == "__main__":
    booth = PhotoBooth()
    errors = 0
    while True:
        if errors > 0:
            logging.error("Too many erros while trying to taking pictures, stopping app.")
        user_input = input("press enter to launch. q to quit: ")
        if user_input == "q":
            break
        capture = True
        if capture:
            snap = 0
            errors = 0
            snaps = []
            while snap < SNAP_PER_PICTURE:
                logging.info("Take the pose!")
                # Capture and download Image
                snap_result, filename = booth.snap()
                if filename is not None:
                    snaps.append(filename)
                if snap_result:
                    snap += 1
                else:
                    errors += 1
                time.sleep(0.5)
                if errors >= 4:
                    break

            if len(snaps) > 0:
                now = datetime.datetime.now()
                booth.merge(snaps, now.strftime(MERGED_FILENAME))
                logging.info("ready for next round")
