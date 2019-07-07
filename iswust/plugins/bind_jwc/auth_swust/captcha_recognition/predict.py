from .img_process import segment_image, process
from skimage.transform import resize
import numpy as np


def predict_captcha(captcha_image, model):
    """
    :param captcha_image: captcha image path
    :return: str 验证码
    """
    captcha_image = process(captcha_image)
    # segment_iamge 抽取小图像

    subimages = segment_image(captcha_image)
    if subimages is not None:
        # 整理数据集
        dataset = []
        for subimage in subimages:
            # 把每一个抽取出来的图像变为25*25的大小
            temp = resize(subimage, (25, 25),
                          mode='constant',
                          anti_aliasing=False)
            # 1为白点 0为黑点
            temp[temp > 0] = 1
            dataset.append(temp)
        dataset = np.array(dataset)
        # keras中是批量预测 这里X_test.shape为(4, 625)
        # 如果预测单张图片的话需要对X的shape进行扩维，变成(None, 625)
        # X_t = np.expand_dims(X_test[0], axis=0)
        X_test = dataset.reshape(
            (dataset.shape[0], dataset.shape[1] * dataset.shape[2]))

        # 进行预测
        y_pred = model.predict_proba(X_test)
        # argmax返回array中最大值的位置，也就是概率最大的那个位置
        predictions = np.argmax(y_pred, axis=1)

        # 将预测的字母拼接起来
        predicted_word = str.join(
            "", [label_list[prediction] for prediction in predictions])
        return predicted_word
    else:
        # 如果切割图片返回None 说明没有切割出来 直接不预测
        return None


# 所有字符
label_list = [
    '1', '2', '3', '4', '5', '6', '7', '8', 'a', 'b', 'c', 'd', 'e', 'f', 'h',
    'k', 'n', 'p', 'q', 'x', 'y', 'z'
]
