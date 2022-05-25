import streamlit as st

import io
import os
import yaml

from PIL import Image

from predict import load_model, get_prediction

from confirm_button_hack import cache_on_button_press

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

st.write("Hello World!")


def main():
    st.title("Mask Classification Model")

    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    

    model = load_model()
    model.eval()

    # TODO: File Uploader 구현
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg","png"])

    if uploaded_file:
        # TODO: 이미지 View
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes)) # 이미지 그려주기 위해 bytes객체로 만듦

        st.image(image, caption='Uploaded Image')
        
        # TODO: 예측 결과 출력
        st.write("Classifying...")
        
        _, y_hat = get_prediction(model, image_bytes)
        label = config['classes'][y_hat.item()]

        st.write(f'label is {label}')


# 엄밀히는 암호를 코드에 하드코딩하는 것은  좋지 않음!
root_password = 'password'

password = st.text_input('password', type="password")

@cache_on_button_press('Authenticate')
def authenticate(password) ->bool:
    st.write(type(password))
    return password == root_password

if authenticate(password):
    st.success('You are authenticated!')
    main()
else:
    st.error('The password is invalid.')


# TODO: Streamlit App 만들기
# TODO: Voila 코드 리팩토링(app.py, model.py, predict.py, utils.py)

# TODO: 암호 입력