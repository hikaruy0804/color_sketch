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
    # 16進数カラーコードをRGBに変換
    r, g, b = hex_to_rgb(hex_color)

    # RGBをHSVに変換
    h, s, v = rgb_to_hsv(r, g, b)

    # HSV値を調整
    h = (h + hue_adjust) % 1.0
    s = max(0, min(1, s + saturation_adjust))
    v = max(0, min(1, v + lightness_adjust))

    # RGBに戻す
    new_r, new_g, new_b = hsv_to_rgb(h, s, v)

    # RGBを16進数に変換
    return '#{:02x}{:02x}{:02x}'.format(new_r, new_g, new_b)

def generate_color_variations(hex_color):
    close_variations = []
    far_variations = []
    same_tone_variations = []

    # 近い色のバリエーションを生成
    close_adjustments = [
        (0.05, 0.05, 0.01),  # 明度、彩度、色相を少し調整
        (-0.05, -0.05, -0.01),
        (0.1, -0.05, 0.02)
    ]
    
    for lightness_adjust, saturation_adjust, hue_adjust in close_adjustments:
        new_color = adjust_color_variation(hex_color, lightness_adjust, saturation_adjust, hue_adjust)
        close_variations.append(new_color)

    # 遠い色のバリエーションを生成
    far_adjustments = [
        (0.4, -0.4, 0.5),  # 明度、彩度、色相を大きく調整
        (-0.4, 0.4, -0.5),
        (0.6, 0.6, 0.3)
    ]
    
    for lightness_adjust, saturation_adjust, hue_adjust in far_adjustments:
        new_color = adjust_color_variation(hex_color, lightness_adjust, saturation_adjust, hue_adjust)
        far_variations.append(new_color)

    # 同一トーンのバリエーションを生成
    same_tone_adjustments = [
        (0, 0.2, 0.1),  # 彩度と色相を調整、明度は固定
        (0, -0.2, -0.1),
        (0, 0.1, 0.2)
    ]
    
    for lightness_adjust, saturation_adjust, hue_adjust in same_tone_adjustments:
        new_color = adjust_color_variation(hex_color, lightness_adjust, saturation_adjust, hue_adjust)
        same_tone_variations.append(new_color)

    return close_variations, far_variations, same_tone_variations

def display_colors(main_color, close_colors, far_colors, same_tone_colors):
    st.markdown("### メインカラー")
    st.markdown(f"<div style='background-color:{main_color}; width:80px; height:80px;'></div>", unsafe_allow_html=True)
    st.markdown(f"{main_color}")
    st.markdown("---")


    st.markdown("### 近い色")
    for i, color in enumerate(close_colors):
        if i % 2 == 0:
            cols = st.columns(2)
        cols[i % 2].markdown(f"<div style='background-color:{color}; width:60px; height:60px;'></div>{color}", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 遠い色")
    for i, color in enumerate(far_colors):
        if i % 2 == 0:
            cols = st.columns(2)
        cols[i % 2].markdown(f"<div style='background-color:{color}; width:60px; height:60px;'></div>{color}", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### トーンが同じ色")
    for i, color in enumerate(same_tone_colors):
        if i % 2 == 0:
            cols = st.columns(2)
        cols[i % 2].markdown(f"<div style='background-color:{color}; width:60px; height:60px;'></div>{color}", unsafe_allow_html=True)

# Streamlitアプリの構築
st.title("カラースケッチ")

# ユーザー入力を受け取る
hex_color = st.text_input("Enter (#e5ccab):", "#e5ccab")

if hex_color:
    close_variations, far_variations, same_tone_variations = generate_color_variations(hex_color)
    display_colors(hex_color, close_variations, far_variations, same_tone_variations)
