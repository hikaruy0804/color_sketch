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
    h = (h + hue_adjust) % 1.0  # 色相の調整は1で循環
    s = max(0, min(1, s + saturation_adjust))  # 彩度を0から1の範囲で調整
    v = max(0, min(1, v + lightness_adjust))  # 明度を0から1の範囲で調整、特に低めに設定して白を避ける
    new_r, new_g, new_b = hsv_to_rgb(h, s, v)
    return '#{:02x}{:02x}{:02x}'.format(new_r, new_g, new_b)

# 修正された色の調整値
adjustments = [
    # 明度を下げ、彩度を増やす調整を試す
    (-0.1, 0.2, 0.1),  # 明度をやや下げ、彩度と色相を上げる
    (-0.2, 0.3, 0.2),  # 明度を更に下げ、彩度と色相をより強く上げる
    (0.05, 0.15, -0.05),  # 明度をわずかに上げつつ、彩度を増やし色相を少し変更
    (0, 0.25, 0.1)  # 明度は変えず、彩度を大幅に増やし、色相を少し変更
]

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
