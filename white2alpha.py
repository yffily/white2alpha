#! /usr/bin/env python
import sys, os

'''
Argument(s): name of the file(s) to process.

Convert white to transparent and save as a png. Each pixel's color is interpreted as a mix of white and a "pure color" which contains at most two primary colors. Once processed, the pixel's color is equal to this pure color and its transparency level is equal to the original white level. Any transparency in the original is ignored.

See gimp's source code for the general case: https://gitlab.gnome.org/GNOME/gimp/blob/bcd98991017f85aff90aee36451970d59edcb95d/plug-ins/common/colortoalpha.c
For "white to alpha" with no initial alpha (a4=1) the formula is:
a4 = max(255-a1,255-a2,255-a3)
ai = 255*(ai-255)/a4+255
where i=1,2,3 and (a1,a2,a3,a4) is the pixel's RGBA tuple.
In this script I use w=255-a4 instead, therefore
ai = 255*(ai-255)/(255-w)+255
   = 255*ai/(255-w)-255*w/(255-w)
   = 255*(ai-w)/(255-w)

'''

if len(sys.argv)==1:
	print('Input file(s) to process.')
	print('Use -m for the slower, memory-efficient implementation.')
	sys.exit()


# Switch between the fast implementation and the memory-efficient one.
if '-m' in sys.argv:
    # Memory-efficient implementation using PIL. The explicit python loop over pixels is slow,
    # but once the image is loaded you only need enough memory to process one pixel at a time.
    from PIL import Image
    def w2a(f_in, f_out):
        img = Image.open(f_in).convert("RGBA")
        pixdata = img.load()
        for y in range(img.size[1]):
	        for x in range(img.size[0]):
		        p = pixdata[x,y][:3]
		        w = min(p)
		        if w>0:
			        pixdata[x,y] = (0,0,0,0) if w==255 else tuple([int(255*(c-w)/(255-w)) for c in p]+[255-w])
        img.save(f_out, 'png')

else:
    # Fast implementation using imageio and scipy.
    # Note: by default imageio.imwrite uses the highest compression level (9), which is slow; 
    # instead I use 6, which is the PIL default.
    from imageio import imread, imwrite
    import numpy as np
    from scipy import ndimage
    def w2a(f_in, f_out):
        img  = imread(f_in)[:,:,:3]
        w    = np.min(img, axis=2)
        img -= w[:,:,None]
        w    = 255-w
        img  = (img.astype(np.float32)*255/w[:,:,None]).astype(np.uint8)
        img  = np.concatenate([img, w[:,:,None]], axis=2)
        img[np.isnan(img)] = 255
        imwrite(f_out, img, compress_level=6)


for f_in in sys.argv[1:]:
    f_out = os.path.splitext(f_in)[0]+'_w2a.png'
    w2a(f_in, f_out)


