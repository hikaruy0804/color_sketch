import streamlit as st
import colorsys

def rgb_to_hsv(r, g, b):
    """Convert RGB to HSV color space."""
    return colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB color space."""
    return tuple(int(x * 255.0) for x in colorsys.hsv_to_rgb(h, s, v))

def hex_to_rgb(hex_color):
    """Convert HEX to RGB color space."""
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_new_color(base_color, lightness_adjust, saturation_adjust, hue_adjust):
    """Generate a new color based on adjustments."""
    r, g, b = hex_to_rgb(base_color)
    h, s, v = rgb_to_hsv(r, g, b)
    h = (h + hue_adjust) % 1.0
    s = max(0, min(1, s + saturation_adjust))
    v = max(0, min(1, v + lightness_adjust))
    return '#{0:02x}{1:02x}{2:02x}'.format(*hsv_to_rgb(h, s, v))

def generate_color_variations(base_color):
    """Generate color variations for same, similar, and contrast tones."""
    adjustments = {
        'same_tone': [(0, 0, 0.1), (0, 0, -0.1), (0, 0, 0.2), (0, 0, -0.2)],
        'similar_tone': [(0.05, 0, 0), (0.1, 0, 0), (-0.05, 0, 0), (-0.1, 0, 0)],
        'contrast_tone': [(0.5, 0.5, 0.5), (0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, 0.5)]
    }
    variations = {key: [generate_new_color(base_color, *adjust) for adjust in adjustments[key]] for key in adjustments}
    return variations

def display_colors(title, colors):
    """Display color blocks in Streamlit."""
    st.markdown(f"### {title}")
    cols = st.columns(len(colors))
    for col, color in zip(cols, colors):
        col.markdown(f"<div style='background-color:{color}; width:100%; height:100px;'></div>{color}", unsafe_allow_html=True)

# Streamlit App
st.title("カラースケッチ")
base_color = st.text_input("カラーコードを入力 (#625651):", "#625651")
if base_color:
    try:
        if len(base_color) != 7 or not all(c in '0123456789abcdefABCDEF' for c in base_color[1:]):
            raise ValueError("正しいカラーコードを入力してください。")
        variations = generate_color_variations(base_color)
        display_colors("メインカラー", [base_color])
        display_colors("同一トーン配色", variations['same_tone'])
        display_colors("類似トーン配色", variations['similar_tone'])
        display_colors("対照トーン配色", variations['contrast_tone'])
    except ValueError as e:
        st.error(str(e))
