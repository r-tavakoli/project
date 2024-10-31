
import streamlit as st
from PIL import Image
import base64
import time
import os

st.set_page_config(
    page_title='Translator',
    page_icon=':sunglasses:',
    initial_sidebar_state='collapsed'
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


@st.cache_data
def load_image(image_file):
    return Image.open((image_file))

def save_image(image_file):
    time_str = time.strftime('%Y%m%d_%H%M%S')
    base_name, extension = os.path.splitext(image_file.name)
    file_name = f'{base_name}_{time_str}{extension}'
    with open(os.path.join('images/img_dir', file_name), 'wb') as f:
        f.write(image_file.getbuffer())


def clear_text(keys):
    for key in keys:
        st.session_state[key] = ''


def download_link(file_name='result', extension='txt'):
    time_str = time.strftime('%Y%m%d_%H%M%S')
    bs64 = base64.b64encode(st.session_state['text_output_area'].encode()).decode()
    file_name = f'{file_name}_{time_str}.{extension}'

    with open('images/download_icon.png', 'rb') as fimg:
        download_image_icon_url = base64.b64encode(fimg.read()).decode('utf-8')

    href = f'''
        <div class="download_link">
            <h style="display:inline">
            Download Result: 
                <a href="data:file/{extension};base64, {bs64}" download="{file_name}">
                    <img src="data:image/png;base64,{download_image_icon_url}" width="25" height="25">
                </a>
            </h>
        </div>
    '''
    st.markdown(href, unsafe_allow_html=True)


class FileDownloader:
    def __init__(self, data, file_name='result', extension='txt', icon_img_path='images/download_icon.png'):
        self.data = data
        self.file_name = file_name
        self.extension = extension
        self.time_str_ = time.strftime('%Y%m%d_%H%M%S')
        self.icon_img_path = icon_img_path

    def download(self):
        bs64 = base64.b64encode(st.session_state.get(self.data).encode()).decode()
        download_file_name = f'{self.file_name}_{self.time_str_}.{self.extension}'

        with open(self.icon_img_path, 'rb') as fimg:
            download_image_icon_url = base64.b64encode(fimg.read()).decode('utf-8')

        href = f'''
            <div class="download_link">
                <h style="display:inline">
                Download Result: 
                    <a href="data:file/{self.extension};base64, {bs64}" download="{download_file_name}">
                        <img src="data:image/png;base64,{download_image_icon_url}" width="25" height="25">
                    </a>
                </h>
            </div>
        '''
        st.markdown(href, unsafe_allow_html=True)       


def translate():
    st.session_state['text_output_area'] = st.session_state['text_input_area']


def btn_disable():
    st.session_state.tranlate_process_btn_state = True

def btn_enable():
    st.session_state.tranlate_process_btn_state = False

def image_translator():
    img = st.file_uploader(
        label='Upload An Image',
        type=['png', 'jpeg', 'jpg'],
        on_change=btn_enable
    )

    if img:
        if st.button('Process & Translate', key='tranlate_process_btn', on_click=btn_disable, disabled=st.session_state.tranlate_process_btn_state):
            st.session_state.tranlate_process_btn_state = True
            img_info = {
                'image name': img.name,
                'image size': f'{img.size/1024:.3f} KB',
                'image type': img.type
            }
            st.write(img_info)
            st.image(load_image(img), width=300)
            save_image(img)


def text_translator():
    # input text
    input_text = st.text_area(
        'Input',
        max_chars=400,
        height=300,
        key='text_input_area'
    )

    # dropdown list
    st.selectbox(
        'languages',
        ['chinese', 'farsi', 'english', 'arabic'],
        index=1,
        label_visibility='hidden'
    )

    # buttons
    translate_col, clear_col= st.columns([1, 0.5], gap='small')
    with translate_col:
        translate_btn = st.button(
            'Translate',
            key='text_translate',
            on_click=translate,
            use_container_width=True,
            type='secondary'
        )
    with clear_col:
        st.button(
            'Clear',
            key='text_clear',
            on_click=clear_text,
            kwargs={'keys': ('text_input_area', 'text_output_area')},
            use_container_width=True,
            type='primary'
        )

    # output text
    output_text = st.text_area(
        'Output',
        max_chars=400,
        height=300,
        key='text_output_area'
    )

    if translate_btn and output_text:
        # download_link()
        FileDownloader(data='text_output_area').download()


def main():
    menu = ['Text Translator', 'Image Translator', 'Voice Translator', 'About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Text Translator':
        st.subheader('Text Translator')
        text_translator()
    elif choice == 'Image Translator':
        st.subheader('Image Translator')
        image_translator()
    elif choice == 'Voice Translator':
        st.subheader('Voice Translator')
    else:
        st.subheader('About')



if __name__=='__main__':
    main()