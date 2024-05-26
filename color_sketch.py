import streamlit as st
import colorsys
import matplotlib.pyplot as plt
import numpy as np

def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

def hsv_to_rgb(h, s, v):
    return [int(x * 255.0) for x in colorsys.hsv_to_rgb(h, s, v)]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def adjust_color_variation(hex_color, lightness_adjust=0, saturation_adjust=0, hue_adjust=0):
    r, g, b = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(r, g, b)
    h = (h + hue_adjust) % 1.0
    s = max(0, min(1, s + saturation_adjust))
    v = max(0, min(1, v + lightness_adjust))  # 明度の調整を制御
    new_r, new_g, new_b = hsv_to_rgb(h, s, v)
    return '#{:02x}{:02x}{:02x}'.format(new_r, new_g, new_b)

def generate_color_variations(hex_color):
    close_variations = []
    far_variations = []
    same_tone_variations = []
    # 近い色の調整値
    close_adjustments = [
        (0.05, 0.05, 0.01),
        (-0.05, -0.05, -0.01),
        (0.1, -0.05, 0.02),
        (-0.1, 0.05, -0.02)
    ]
    for adjustments in close_adjustments:
        close_variations.append(adjust_color_variation(hex_color, *adjustments))
    # 遠い色の調整値
    far_adjustments = [
        (0.4, -0.4, 0.5),
        (-0.4, 0.4, -0.5),
        (0.6, 0.6, 0.3),
        (-0.6, -0.6, -0.3)
    ]
    for adjustments in far_adjustments:
        far_variations.append(adjust_color_variation(hex_color, *adjustments))
    # 同一トーンの調整値
    same_tone_adjustments = [
        (0, 0.2, 0.1),
        (0, -0.2, -0.1),
        (0, 0.1, 0.2),
        (0, -0.1, -0.2)
    ]
    for adjustments in same_tone_adjustments:
        same_tone_variations.append(adjust_color_variation(hex_color, *adjustments))

    return close_variations, far_variations, same_tone_variations

def display_colors(main_color, variations):
    st.markdown(f"### {main_color}")
    for color in variations:
        cols = st.columns(4)
        for i, col in enumerate(color):
            cols[i].markdown(f"<div style='background-color:{col}; width:60px; height:60px;'></div>{col}", unsafe_allow_html=True)

# アプリの構築
st.title("カラースケッチ")
hex_color = st.text_input("Enter (#e5ccab):", "#e5ccab")
if hex_color:
    close_variations, far_variations, same_tone_variations = generate_color_variations(hex_color)
    display_colors("メインカラー", [hex_color])
    display_colors("近い色", close_variations)
    display_colors("遠い色", far_variations)
    display_colors("トーンが同じ色", same_tone_variations)
