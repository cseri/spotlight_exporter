#!/usr/bin/env python
# coding: UTF-8
#
# Lockscreen Background Exporter for Windows 10
#
# ----------------------------------------------------------------------------
#
# Copyright (c) 2016 Tamás Cséri
#
# This file is distributed under the The MIT License License. See LICENSE for
# details.
#
# ----------------------------------------------------------------------------
#
# Run this program regularly to copy the downloaded Windows Spotlight
# wallpapers from their secret location to the current directory.

import collections
import os
import shutil
from PIL import Image

# This is the default location where Windows 10 saves lockscreen images.
# TODO: Check out how this works in a multi-user environment.
# TODO: Make this a command-line argument
BACKGROUNDS_LOCATION = os.getenv('LOCALAPPDATA') + "\\Packages\\" + \
  "Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"

# Mapping from image type to folder
# TODO: Make this a command-line argument
FOLDERS = \
  {
    'unknown'   : "unknown",
    'landscape' : "backgrounds_landscape",
    'mobile'    : "backgrounds_mobile",
  }

# https://stackoverflow.com/questions/273192/
#    how-to-check-if-a-directory-exists-and-create-it-if-necessary
def ensure_dir(d):
  if not os.path.exists(d):
    os.makedirs(d)


def make_dest_dirs():
  for key, dirname in FOLDERS.iteritems():
    ensure_dir(dirname)


# Return "landscape" for landscape background images, "mobile" for
# non-landscape background images, "unknown" for everything else (e.g.
# small images or files that could not be interpreted as an image)
def categorize(imgfilename):
  img = Image.open(imgfilename)
  w = img.size[0]
  h = img.size[1]
  # Filter out thumbnail images
  if w < 500 or h < 500:
    return "unknown"
  elif w >= h:
    return "landscape"
  else:
    return "mobile"



# Copies the files from BACKGROUNDS_LOCATION to the proper folder
def copy_files():
  d = BACKGROUNDS_LOCATION;
  count = collections.defaultdict(int)
  for filename in os.listdir(d):
    fullsourcepath = os.path.join(d, filename)

    cat = categorize(fullsourcepath)
    fulldestinationpath = os.path.join(FOLDERS[cat], filename + ".jpg")

    # No need to overwrite. As the hash is in the filename, if we already
    # have a file with the same name we assume that we have that image.
    if not os.path.exists(fulldestinationpath):
      shutil.copy(fullsourcepath, fulldestinationpath)
      count[cat] += 1

  if len(count) > 0:
    print("New images:")
    for key, value in count.iteritems():
      print("  " + key + ": " + str(value))
  else:
    print("No new images.")


def main():
  make_dest_dirs()
  copy_files()


main()

