import urllib.request as req
from bs4 import BeautifulSoup
import os
import re
import streamlit as st

st.title('BREAKOUT SON 블로그 이사 도우미')
user_input = st.text_input ('URL 입력')

# user_text = ''
if 'blog.naver.com' in user_input:
    url = user_input
    if not 'm.blog.naver.com' in url:
        url = url.replace('blog.naver.com', 'm.blog.naver.com')
    else:
        st.write('올바른 형식이 아닙니다')

    import time
    with st.spinner('Wait for it...'):
        time.sleep(3)
    code = req.urlopen(url)
    soup = BeautifulSoup(code, 'html.parser')

    title = soup.select_one('div.se-module.se-module-text.se-title-text').text.replace('\n','')
    content = soup.select_one('div.se-main-container')
    content_line = content.text.split('\n')
    content_line = list(filter(None, content_line))

    # 제목에 특수기호 제거
    title_re = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", title) # ^을 붙이면 표현식에 해당되지 않는 것을 찾아라.

    st.success ('디렉토리 생성 : /breakoutson/포스팅백업/')


    try:
        os.makedirs('c:/breakoutson/포스팅백업/백업_{}/'.format(title_re), exist_ok=True)  #이미 있으면 패스

    except:
        pass

    # 메모장 파일에 저장
    f = open('c:/breakoutson/포스팅백업/백업_{}/본문.txt'.format(title_re), 'w', encoding= 'UTF-8')

    st.success ('본문을 txt 파일로 백업하였습니다.')
    st.info (content.text)
    for i in content_line:
        f.write(i+'\n')
    f.close()

    # 이미지 저장
    num = 1
    # img = soup.select('div.se-viewer.se-theme-default div.se-module.se-module-image img') # 이미지 CSS 선택자
    img = soup.select('div.se-viewer.se-theme-default div.se-module.se-module-image > a.se-module-image-link.__se_image_link.__se_link > img') # 이미지 CSS 선택자

    st.success ('이미지 파일 다운로드 하였습니다')


    for i in img :
        if 'data-lazy-src' in i.attrs:
            img_url = i.attrs['data-lazy-src']
            req.urlretrieve(img_url, 'c:/breakoutson/포스팅백업/백업_{}/{}.png'.format(title_re,num))
        elif 'src' in i.attrs:
            img_url = i.attrs['src']
            req.urlretrieve(img_url, 'c:/breakoutson/포스팅백업/백업_{}/{}.png'.format(title_re,num))
        else :
            pass
        num += 1

    st.write('#### 모든 작업이 완료 되었습니다. 생성된 폴더를 확인하세요.')
