# white2alpha


## Description

Command-line utility to convert the white of an image to transparency. The core formula is taken from Gimp's color2alpha function.


## Dependencies

The default algorithm requires scipy and imageio. The slower but more memory-efficient algorithm requires PIL.


## Use

    white2alpha.py [-m] image [list_of_additional_images]

For each image in the input, an output image is created named by appending "_w2a" to the original name.

If memory is more of a concern than speed, use the "-m" option.


## Author

Yaouen Fily