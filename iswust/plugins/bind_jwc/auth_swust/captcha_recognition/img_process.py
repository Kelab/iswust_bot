from skimage.measure import label, regionprops
from skimage.morphology import erosion, dilation, square
import numpy as np


def segment_image(image):
    # 将整张图片转置，以便于从上向下按顺序进行搜索连通分支。
    image = image.transpose()
    # 我们要做的第一件事就是检测每个字母的位置，这就要用到`scikit-image`的`label`函数，它能找出图像中像素值相同且又连接在一起的像素块。这有点像连通分支。`label`函数的参数为图像数组，返回跟输入同型的数组。在返回的数组中，图像**连接在一起的区域**用不同的值来表示，在这些区域以外的像素用0来表示。
    labeled_image = label(image, connectivity=2)

    # 抽取每一张小图像，将它们保存到这个列表中。
    subimages = []

    # `scikit-image`库还提供抽取连续区域的函数：`regionprops`。遍历这些区域，分别对它们进行处理。
    for region in regionprops(labeled_image):
        start_x, start_y, end_x, end_y = region.bbox
        if (end_x - start_x) * (end_y - start_y) >= 16:
            img_region = image[start_x:end_x, start_y:end_y]
            # 用这两组坐标作为索引就能抽取到小图像（`image`对象为`numpy`数组，可以直接用索引值），然后，把它保存到`subimages`列表中。
            subimages.append(img_region.transpose())

    # 最后返回找到的小图像，每张小图像包含图片中的一个字母区域。
    if len(subimages) != 4:
        # 没有找到四张小图像的情况，直接返回 None
        return None
    return subimages


def binarization(img):
    """
    :param pic:  图片地址
    :return: PIL.Image
    """
    image = img.convert('L')
    # L = R 的值 x 299/1000 + G 的值 x 587/1000+ B 的值 x 114/1000
    threshold = 117
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return image


def process(image):
    """
    :param image: 传入的是PIL.Image对象
    :return: numpy.array
    """
    # 二值化
    img = binarization(image)

    # 将PIL.Image格式转为np.array
    img = np.array(img)

    # 以矩形进行膨胀腐蚀
    img = erosion(img, square(1))
    img = dilation(img, square(1))

    img[img < 117] = 1
    img[img > 117] = 0

    return img
