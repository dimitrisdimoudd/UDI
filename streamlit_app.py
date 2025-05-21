from io import BytesIO
import re
import streamlit as st
import requests
import base64
from PIL import Image

def extract_text_from_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    response = requests.post(
        "https://api.ocr.space/parse/image",
        data={
            'apikey': 'K87788557888957',  # Replace with real API key for production
            'base64Image': 'data:image/jpeg;base64,' + img_str,
            'language': 'eng',
        },
    )

    result = response.json()
    if result['IsErroredOnProcessing']:
        return "Error: " + result.get("ErrorMessage", ["Unknown error"])[0]
    else:
        return result['ParsedResults'][0]['ParsedText']

st.title("🔍 Label Checker - UDI Validator")

uploaded_file = st.file_uploader("Upload an image with UDI labels", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    text = extract_text_from_image(image)  # ← FIXED: add this line

    # Find all 9-digit numbers
    numbers = re.findall(r'\b\d{9}\b', text)

    # Count how often each 9-digit number appears
    count_map = {num: numbers.count(num) for num in set(numbers)}

    # Display results
    found_valid = False
    for num, count in count_map.items():
        if count >= 3:
            st.success(f"✅ Number `{num}` appears {count} times. Label is valid.")
            found_valid = True

    if not found_valid:
        st.error("❌ No 9-digit number appears 3 times. Label is NOT valid.")

    with st.expander("See all detected 9-digit numbers"):
        st.write(count_map)