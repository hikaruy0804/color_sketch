import streamlit as st
import colorsys
import matplotlib.pyplot as plt
import numpy as np
import random

def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

def hsv_to_rgb(h, s, v):
    return [int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v)]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_new_color(hex_color, hue_adjust, saturation_adjust, lightness_adjust):
    r, g, b = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(r, g, b)
    h = (h + hue_adjust) % 1.0
    s = max(0, min(1, s + saturation_adjust))
    v = max(0, min(1, v + lightness_adjust))
    return f'#{"".join(f"{int(x):02x}" for x in hsv_to_rgb(h, s, v))}'

def generate_color_variations(hex_color, num_variations=5):
    variations = {
        'similar_tone': [],
        'contrast_tone': [],
        'same_tone': []
    }
    # 色相の調整をより顕著に
    hue_shifts = np.linspace(-0.1, 0.1, num_variations)
    # 彩度と明度の調整も大きく
    saturation_shifts = np.linspace(-0.3, 0.3, num_variations)
    lightness_shifts = np.linspace(-0.3, 0.3, num_variations)
    random.shuffle(hue_shifts)
    random.shuffle(saturation_shifts)
    random.shuffle(lightness_shifts)

    for i in range(num_variations):
        variations['same_tone'].append(generate_new_color(hex_color, 0, saturation_shifts[i], lightness_shifts[i]))
        variations['similar_tone'].append(generate_new_color(hex_color, hue_shifts[i], saturation_shifts[i], lightness_shifts[i]))
        contrast_hue_shift = (hue_shifts[i] + 0.5) % 1.0
        variations['contrast_tone'].append(generate_new_color(hex_color, contrast_hue_shift, -saturation_shifts[i], lightness_shifts[i]))

    return variations

def display_colors(title, colors):
    st.markdown(f"### {title}")
    cols = st.columns(len(colors))
    for col, color in zip(cols, colors):
        col.markdown(f"<div style='background-color:{color}; width:100%; height:100px;'></div>{color}", unsafe_allow_html=True)

# アプリの構築
st.title("カラースケッチ")
hex_color = st.text_input("カラーコードを入力 (#e5ccab):", "#625651")
if hex_color:
    try:
        if len(hex_color) != 7 or not all(c in '0123456789abcdefABCDEF' for c in hex_color[1:]):
            raise ValueError("正しいカラーコードを入力してください。")
        variations = generate_color_variations(hex_color)
        display_colors("メインカラー", [hex_color])
        display_colors("同一トーン配色", variations['same_tone'])
        display_colors("類似トーン配色", variations['similar_tone'])
        display_colors("対照トーン配色", variations['contrast_tone'])
    except ValueError as e:
        st.error(str(e))
