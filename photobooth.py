#!/usr/bin/python
import time
import os
import os.path
import subprocess
import logging
import argparse

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

#PHOTOBOOTH_DIR = os.path.expanduser("~/photobooth_images/")
PHOTOBOOTH_DIR = os.path.expanduser("photobooth_images/")
logging.info("PHOTOBOOTH_DIR set to %s" % (PHOTOBOOTH_DIR,))
IMAGE_FILENAME = r"photobooth-%Y%m%d-%H%M%S.jpg"


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
        print filename
        cmd = "gphoto2 --capture-image-and-download --filename %s" % (
            filename
        )
        gpout = subprocess.check_output(cmd,
                                        stderr=subprocess.STDOUT,
                                        shell=True)
        print gpout
        if "ERROR" not in gpout:
            return True
        else:
            return False
        return True

    def merge(self, pictures_list):
        """
        Merge picture passed as parameter
        """
        logging.info("Merging not implemented")

    def print_picture(self):
        """
        Send the picture to the printer
        """
        if PRINT:
            logging.info("Printing not implemented")
        else:
            logging.debug("printing desactivated") 


if __name__ == "__main__":
    booth = PhotoBooth()
    while True:
        user_input = raw_input("press enter to launch. q to quit")
        if user_input == "q":
            break
        capture = True
        if capture:
            snap = 0
            while snap < SNAP_PER_PICTURE:
                logging.info("Take the pose!")
                # Capture and download Image
                snap_result = booth.snap()
                if snap_result:
                    snap += 1
                time.sleep(0.5)
            booth.print_picture()
            logging.info("ready for next round")
        