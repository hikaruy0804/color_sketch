import streamlit as st
import colorsys
import random

def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

def hsv_to_rgb(h, s, v):
    return [int(x * 255.0) for x in colorsys.hsv_to_rgb(h, s, v)]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_new_color(hex_color, hue_adjust, saturation_adjust, lightness_adjust):
    r, g, b = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(r, g, b)
    h = (h + hue_adjust) % 1.0
    s = max(0, min(1, s + saturation_adjust))
    v = max(0, min(1, v + lightness_adjust))
    return '#{:02x}{:02x}{:02x}'.format(*hsv_to_rgb(h, s, v))

def generate_color_variations(hex_color):
    adjustments = {
        'similar_tone': [
            (random.uniform(-0.1, 0.1), random.uniform(-0.2, 0.2), random.uniform(-0.1, 0.1)) for _ in range(4)
        ],
        'contrast_tone': [
            (0, 0, random.uniform(0.3, 0.5)), (0, 0, random.uniform(-0.5, -0.3)),
            (0, 0, random.uniform(0.5, 0.7)), (0, 0, random.uniform(-0.7, -0.5))
        ],
        'same_tone': [
            (random.uniform(0.1, 0.2), 0, 0), (random.uniform(0.2, 0.3), 0, 0),
            (random.uniform(0.3, 0.4), 0, 0), (random.uniform(0.4, 0.5), 0, 0)
        ]
    }
    variations = {key: [generate_new_color(hex_color, *adjust) for adjust in adjustments[key]] for key in adjustments}
    return variations

def display_colors(title, colors):
    st.markdown(f"### {title}")
    cols = st.columns(len(colors))
    for col, color in zip(cols, colors):
        col.markdown(f"<div style='background-color:{color}; width:100%; height:100px;'></div>{color}", unsafe_allow_html=True)

# アプリの構築
st.title("カラースケッチ")
hex_color = st.text_input("カラーコードを入力 (#e5ccab):", "#e5ccab")
if hex_color:
    try:
        if len(hex_color) != 7 or not all(c in '0123456789abcdefABCDEF' for c in hex_color[1:]):
            raise ValueError("正しいカラーコードを入力してください。")
        variations = generate_color_variations(hex_color)
        display_colors("メインカラー", [hex_color])
        display_colors("同一トーン配色", variations['same_tone'])
        display_colors("類似トーン配色", variations['similar_tone'])
        display_colors("明度違い配色", variations['contrast_tone'])
    except ValueError as e:
        st.error(str(e))
