


# Charuco My Gen 
- not working
python arucomarker.py  --page A4 --rows 8 --cols 5 --first 0  --charuco --output testcharuco.pdf
convert testcharuco.pdf testcharuco.ng
python test_charuco.py testcharuco.png --dictionary  DICT_5X5_250

#-density 72x72 -resize 100%

# The Gen
- works
python opencv_gencharuco.py -o x.png --dictionary  DICT_5X5_250
python test_charuco.py x.png

# Using Docker

docker run -v .:/code  -it jjanzic/docker-python3-opencv bash

# Export PDF


python opencv_gencharuco.py -o x.png  -r 8 -c 5 -d DICT_5X5_250


# TBD

for the manual arucomaker: investigat 'custom_dictionary', 'custom_dictionary_from',
