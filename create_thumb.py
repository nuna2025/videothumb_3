from PIL import Image, ImageDraw, ImageFont

def create_16_9_custom_text(input_path, output_path, text_configs, bg_color="black"):
    # 1. 원본 이미지 불러오기
    img = Image.open(input_path)
    img_w, img_h = img.size

    # 2. 16:9 캔버스 사이즈 계산
    new_w = int(img_h * (16 / 9))
    new_h = img_h
    
    # 3. 배경 생성 (RGBA 모드로 투명도 지원)
    background = Image.new("RGBA", (new_w, new_h), bg_color)
    
    # 4. 이미지 배치 (왼쪽 정렬)
    offset = (0, (new_h - img_h) // 2)
    background.paste(img.convert("RGBA"), offset)
    
    # 5. 텍스트를 그릴 투명 레이어 생성 (투명도 조절을 위함)
    txt_layer = Image.new("RGBA", background.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    for config in text_configs:
        text = config.get('text', "")
        font_path = config.get('font_path', "arial.ttf")
        font_size = config.get('font_size', 40)
        x = config.get('x', 0)
        y = config.get('y', 0)
        # color: (R, G, B, Alpha) -> Alpha가 0이면 투명, 255면 불투명
        color = config.get('color', (255, 255, 255, 255))
        
        # 폰트 설정
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        # 그림자 설정 (shadow=True 일 때)
        if config.get('shadow', False):
            s_color = config.get('shadow_color', (0, 0, 0, 150)) # 약간 투명한 검정 그림자
            s_offset = config.get('shadow_offset', (3, 3))
            draw.text((x + s_offset[0], y + s_offset[1]), text, font=font, fill=s_color)

        # 본 텍스트 그리기
        draw.text((x, y), text, font=font, fill=color)

    # 6. 배경과 텍스트 레이어 합성
    combined = Image.alpha_composite(background, txt_layer)

    # 7. 저장 시 RGB로 변환하여 JPEG 저장 (또는 PNG로 저장 시 변환 생략 가능)
    final_output = combined.convert("RGB")
    final_output.save(output_path, quality=95)
    print(f"이미지 생성 완료: {output_path}")

# --- 설정값 예시: 4줄의 텍스트 정보를 입력합니다 ---
# x, y 좌표는 16:9 캔버스 기준입니다.
my_texts = [
    {
        'text': 'Podcast : Deutsche',
        'font_path': "Hahmlet-VariableFont_wght.ttf",
        'font_size': 90,
        'x': 650, 'y': 100,
        'color': (255, 30, 30, 255), # 노란색, 완전 불투명
        'shadow': True,
        'shadow_color': (0, 0, 0, 255)
    },
    {
        'text': 'Redewendung',
        'font_path': "Hahmlet-ExtraBold.ttf",
        'font_size': 200,
        'x': 23, 'y': 150,
        'color': (20, 20, 20, 240), # 흰색, 약간 투명
        'shadow': True,
        'shadow_color': (30, 200, 30, 200)
    },
    {
        'text': '50',
        'font_path': "Hahmlet-Black.ttf",
        'font_size': 250,
        'x': 600, 'y': 290,
        'color': (20, 20, 20, 130), # 빨간색 (255, 100, 100, 255)
        'shadow': False,
        'shadow_color': (255, 255, 255, 150), # 흰색 그림자
        'shadow_offset': (2, 2)
    },
    {
        'text': '',
        'font_path': "Hahmlet-VariableFont_wght.ttf",
        'font_size': 47,
        'x': 255, 'y': 430,
        'color': (200, 200, 200, 150), # 회색, 많이 투명
        'shadow': False
    },
    {
        'text': 'A1 : Nr. 1 ~ 50',
        'font_path': "Hahmlet-SemiBold.ttf",
        'font_size': 80,
        'x': 500, 'y': 630,
        'color': (20, 20, 20, 215), # 회색, 많이 투명
        'shadow': False,
        'shadow_color': (0, 0, 0, 220)
    }
]

for t in my_texts:
    # 만약 t 안에 'font_path'가 없거나 비어있다면 기본 폰트 적용
    if 'font_path' not in t or not t['font_path']:
        t['font_path'] = "C:/Windows/Fonts/malgun.ttf" # 기본값: 맑은 고딕



# # 한글 폰트를 사용하려면 'font_path'에 시스템의 폰트 경로를 넣으세요.
# # 예: C:/Windows/Fonts/malgun.ttf (윈도우)
# for t in my_texts:
#     t['font_path'] = "C:/Windows/Fonts/malgun.ttf" # 한글 폰트 경로로 수정 필요

# 최종 함수 실행
create_16_9_custom_text("thumbV3-deFl-16-9.png", "Redewendung_1-50.jpg", my_texts, "black")