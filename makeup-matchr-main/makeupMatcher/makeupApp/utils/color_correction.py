import cv2
from PIL import Image
import os, sys
from io import BytesIO

import numpy
from makeupApp.utils.classes import WBsRGB as wb_srgb

UPGRADED_MODEL : int  = 1;
GAMUT_MAPPIGN : int = 2;
IMG_SHOW : int = 0;

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
  (h, w) = image.shape[:2]

  if width is None and height is None:
    return image
  if width is None:
    r = height / float(h)
    dim = (int(w * r), height)
  else:
    r = width / float(w)
    dim = (width, int(h * r))

  return cv2.resize(image, dim, interpolation=inter)

'''@param: img PIL Image '''
'''@return: outImg  OpenCV or None'''
def CorrectImage(image) -> str:
  try:
    img_cv2 = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    wbModel = wb_srgb.WBsRGB(gamut_mapping=GAMUT_MAPPIGN,upgraded=UPGRADED_MODEL)
    img_cor = wbModel.correctImage(img_cv2)

    img_arr = cv2.cvtColor(img_cor, cv2.COLOR_BGR2RGB)
    img_out = Image.fromarray((img_arr * 255).astype(numpy.uint8))
  except Exception as e:
    print(e)
    print("Error: Image Could Not Be Color Corrected\n")
    img_out = None
    
  return img_out



# input and options
# in_img = 'figure3.jpg'  # input image filename

# imshow = 1  # show input/output image

# if __name__ == '__main__':
#   os.makedirs('.', exist_ok=True)
#   pill_image = Image.open(in_img);
#   outImg = CorrectImage(pill_image);
#   cv2.imwrite('./' + 'result.jpg', outImg * 255);

#   if IMG_SHOW:
#     cv2.imshow('our result', ResizeWithAspectRatio(outImg, width=800))
#     cv2.waitKey()
#     cv2.destroyAllWindows()