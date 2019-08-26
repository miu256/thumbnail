"""
5種類のフィルター
"""

import numpy as np
import skimage
from skimage import io, filters


def split_image_into_channels(img):
    red_channel = img[:, :, 0]
    green_channel = img[:, :, 1]
    blue_channel = img[:, :, 2]
    return red_channel, green_channel, blue_channel


def merge_channels(red, green, blue):
    return np.stack([red, green, blue], axis=2)


def sharpen(img, a, b):
    blurred = skimage.filters.gaussian(img, sigma=10, multichannel=True)
    sharper = np.clip(img * a - blurred * b, 0, 1.0)
    return sharper


def channel_adjust(channel, values):
    orig_size = channel.shape
    flat_channel = channel.flatten()
    adjusted = np.interp(flat_channel, np.linspace(0, 1, len(values)), values)
    return adjusted.reshape(orig_size)


def filter_nice(img):
    r = img[:, :, 0]
    b = img[:, :, 2]
    r_boost_lower = channel_adjust(r, [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0])
    b_more = np.clip(b + 0.03, 0, 1.0)
    merged = np.stack([r_boost_lower, img[:, :, 1], b_more], axis=2)
    blurred = filters.gaussian(merged, sigma=10, multichannel=True)
    final = np.clip(merged * 1.3 - blurred * 0.3, 0, 1.0)
    b = final[:, :, 2]
    b_adjusted = channel_adjust(b, [
        0, 0.047, 0.118, 0.251, 0.318, 0.392, 0.42, 0.439, 0.475,
        0.561, 0.58, 0.627, 0.671, 0.733, 0.847, 0.925, 1])
    final[:, :, 2] = b_adjusted

    return final


def filter_red(img):
    r, g, b = split_image_into_channels(img)
    r_interp = channel_adjust(r, [0, 0.8, 1.0])
    red_channel_adj = merge_channels(r_interp, g, b)
    return red_channel_adj


def filter_mid(img):
    r, g, b = split_image_into_channels(img)
    r_boost_lower = channel_adjust(r, [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0])
    r_boost_img = merge_channels(r_boost_lower, g, b)
    return r_boost_img


def filter_black(img):
    r, g, b = split_image_into_channels(img)
    r_boost_lower = channel_adjust(r, [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0])
    bluer_blacks = merge_channels(r_boost_lower, g, np.clip(b + 0.03, 0, 1.0))
    return bluer_blacks


def filter_blue(img):
    bluer_blacks = filter_black(img)
    sharper = sharpen(bluer_blacks, 1.3, 0.3)
    r, g, b = split_image_into_channels(sharper)
    b_adjusted = channel_adjust(b, [
        0, 0.047, 0.118, 0.251, 0.318, 0.392, 0.42, 0.439,
        0.475, 0.561, 0.58, 0.627, 0.671, 0.733, 0.847, 0.925, 1])
    gotham = merge_channels(r, g, b_adjusted)
    return gotham


if __name__ == '__main__':

    img = skimage.img_as_float(io.imread("./data/test.jpg"))

    # フィルター(いい感じ)
    res = filter_nice(img)

    # フィルター(赤)
    # res = filter_red(img)

    # フィルター(mid)
    # res = filter_mid(img)

    # フィルター(黒っぽい)
    # res = filter_black(img)

    # フィルター(青)
    # res = filter_blue(img)

    skimage.io.imsave('./data/output2.jpg', res)
