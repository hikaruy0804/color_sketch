import streamlit as st
import colorsys
import matplotlib.pyplot as plt
import numpy as np
import random

def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

def hsv_to_rgb(h, s, v):
    return [int(x * 255.0) for x in colorsys.hsv_to_rgb(h, s, v)]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def adjust_color_variation(hex_color, lightness_adjust, saturation_adjust, hue_adjust, used_colors):
    attempts = 0
    new_color = hex_color
    while new_color in used_colors and attempts < 10:
        # 調整値にランダム要素を加える
        h_adjust = hue_adjust + random.uniform(-0.15, 0.15)
        s_adjust = saturation_adjust + random.uniform(-0.1, 0.1)
        l_adjust = lightness_adjust + random.uniform(-0.1, 0.1)
        new_color = generate_new_color(hex_color, l_adjust, s_adjust, h_adjust)
        attempts += 1
    used_colors.add(new_color)  # 生成した色をセットに追加
    return new_color

def generate_new_color(hex_color, lightness_adjust, saturation_adjust, hue_adjust):
    r, g, b = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(r, g, b)
    # 色相、彩度、明度を調整
    h = (h + hue_adjust) % 1.0
    s = max(0, min(1, s + saturation_adjust))
    v = max(0, min(1, v + lightness_adjust))
    new_r, new_g, new_b = hsv_to_rgb(h, s, v)
    return '#{:02x}{:02x}{:02x}'.format(new_r, new_g, new_b)

def generate_color_variations(hex_color):
    used_colors = set([hex_color])  # 使用済みの色を保持
    close_variations, far_variations, same_tone_variations = [], [], []
    # 近い色、遠い色、同一トーンの色の調整値
    close_adjustments = [(0.05, 0.05, 0.01), (-0.05, -0.05, -0.01), (0.1, -0.05, 0.02), (-0.1, 0.05, -0.02)]
    far_adjustments = [(0.4, -0.4, 0.5), (-0.4, 0.4, -0.5), (0.6, 0.6, 0.3), (-0.6, -0.6, -0.3)]
    same_tone_adjustments = [(0, 0.2, 0.1), (0, -0.2, -0.1), (0, 0.1, 0.2), (0, -0.1, -0.2)]
    
    for adjustments in close_adjustments:
        close_variations.append(adjust_color_variation(hex_color, adjustments, used_colors))
    for adjustments in far_adjustments:
        far_variations.append(adjust_color_variation(hex_color, adjustments, used_colors))
    for adjustments in same_tone_adjustments:
        same_tone_variations.append(adjust_color_variation(hex_color, adjustments, used_colors))

    return close_variations, far_variations, same_tone_variations

def display_colors(title, colors):
    st.markdown(f"### {title}")
    cols_per_row = 4
    rows = (len(colors) + cols_per_row - 1) // cols_per_row  # 必要な行数を計算

    for i in range(rows):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            index = i * cols_per_row + j
            if index < len(colors):
                color = colors[index]
                cols[j].markdown(f"<div style='background-color:{color}; width:60px; height:60px;'></div>{color}", unsafe_allow_html=True)
# アプリの構築
st.title("カラースケッチ")
hex_color = st.text_input("Enter (#e5ccab):", "#e5ccab")
if hex_color:
    close_variations, far_variations, same_tone_variations = generate_color_variations(hex_color)
    display_colors("メインカラー", [hex_color])
    display_colors("近い色", close_variations)
    display_colors("遠い色", far_variations)
    display_colors("トーンが同じ色", same_tone_variations)
