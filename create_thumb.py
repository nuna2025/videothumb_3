from PIL import Image, ImageDraw, ImageFont
import math

def draw_star_flag(draw, background, center, size):
    """
    별 모양의 독일 국기를 생성하는 함수입니다.
    1. 별 모양의 마스크(틀)를 만듭니다.
    2. 독일 국기 색상(검정, 빨강, 노랑)의 사각형 레이어를 만듭니다.
    3. 마스크를 이용해 사각형을 별 모양으로 잘라 배경에 붙입니다.
    """
    cx, cy = center
    
    # --- 1. 별 모양 좌표 계산 (그림자 및 마스크용) ---
    points = []
    for i in range(10):
        # -90도(위쪽)부터 시작하여 36도씩 회전하며 10개의 꼭짓점 계산
        angle = math.radians(i * 36 - 90)
        # i가 짝수면 바깥쪽 꼭짓점(size), 홀수면 안쪽 꼭짓점(size * 0.4)
        radius = size if i % 2 == 0 else size * 0.4
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))

    # --- 2. 별 그림자 그리기 ---
    # 실제 별보다 약간 오른쪽 아래(+4)에 검은색 반투명 별을 먼저 그립니다.
    shadow_offset = 4
    shadow_points = [(p[0] + shadow_offset, p[1] + shadow_offset) for p in points]
    draw.polygon(shadow_points, fill=(0, 0, 0, 150))

    # --- 3. 별 모양 국기 합성 ---
    # 별 모양으로만 색이 보이게 할 '마스크' 레이어 생성 (L 모드: 흑백)
    star_mask = Image.new("L", background.size, 0)
    mask_draw = ImageDraw.Draw(star_mask)
    mask_draw.polygon(points, fill=255) # 별 모양 안쪽만 흰색(255)으로 채움

    # 국기 색상을 담을 레이어 생성
    flag_layer = Image.new("RGBA", background.size, (0, 0, 0, 0))
    flag_draw = ImageDraw.Draw(flag_layer)
    
    # 국기 색상 영역 계산 (별의 상단에서 하단까지 3등분)
    f_top, f_bottom = cy - size, cy + size
    h = (f_bottom - f_top) / 3
    
    # 독일 국기 3색 사각형 그리기
    flag_draw.rectangle([cx - size, f_top, cx + size, f_top + h], fill=(0, 0, 0, 255))        # 검정
    flag_draw.rectangle([cx - size, f_top + h, cx + size, f_top + 2*h], fill=(255, 0, 0, 255))  # 빨강
    flag_draw.rectangle([cx - size, f_top + 2*h, cx + size, f_bottom], fill=(255, 204, 0, 255)) # 금색

    # 배경 이미지에 국기 레이어를 '별 모양 마스크'를 사용하여 덮어씌움
    background.paste(flag_layer, (0, 0), mask=star_mask)

def create_16_9_custom_text(input_path, output_path, text_configs, bg_color="black"):
    """
    전체 이미지를 생성하는 메인 함수입니다.
    1. 배경을 16:9 비율로 맞춥니다.
    2. 별 모양 국기를 그립니다.
    3. 설정된 텍스트들을 순서대로 그립니다.
    """
    # 1. 원본 이미지 불러오기 및 16:9 도화지 준비
    img = Image.open(input_path)
    img_w, img_h = img.size
    new_w = int(img_h * (16 / 9))
    new_h = img_h
    
    background = Image.new("RGBA", (new_w, new_h), bg_color)
    offset = (0, (new_h - img_h) // 2)
    background.paste(img.convert("RGBA"), offset)
    
    # 글씨와 별을 그릴 레이어 준비
    txt_layer = Image.new("RGBA", background.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # --- 별 모양 독일 국기 호출 ---
    # 위치: (80, 80), 크기(반지름): 45
    draw_star_flag(draw, background, (120, 700), 100)

    # --- 텍스트 그리기 ---
    for config in text_configs:
        text = config.get('text', "")
        font_path = config.get('font_path', "C:/Windows/Fonts/malgun.ttf")
        font_size = config.get('font_size', 40)
        x, y = config.get('x', 0), config.get('y', 0)
        color = config.get('color', (255, 255, 255, 255))
        
        try:
            
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        # 텍스트 그림자 효과
        if config.get('shadow', False):
            s_color = config.get('shadow_color', (0, 0, 0, 150))
            s_offset = config.get('shadow_offset', (3, 3))
            draw.text((x + s_offset[0], y + s_offset[1]), text, font=font, fill=s_color)

        # 본 텍스트 그리기
        draw.text((x, y), text, font=font, fill=color)

    # 배경과 텍스트 레이어 합성 후 저장
    combined = Image.alpha_composite(background, txt_layer)
    final_output = combined.convert("RGB")
    final_output.save(output_path, quality=95)
    print(f"이미지 생성 완료: {output_path}")

# --- 실행 설정 ---
my_texts = [
    {'text': '스프레드시트 제공 ( Spreadsheet )', 'font_size': 55, 'x': 100, 'y': 200, 'color': (255, 255, 50, 255), 'shadow': True},
    {'text': '~B1 필수 독일어 동사 1000개', 'font_size': 105, 'x': 30, 'y': 250, 'color': (255, 255, 255, 200), 'shadow': False},
    {'text': '를 활용한 대화 문장과 함께 구어체도 함께 익히세요!', 'font_size': 30, 'x': 750, 'y': 390, 'color': (200, 200, 200, 150), 'shadow': False},
    {'text': '대화체 문장과 함께 B1 수준의 독일어 작문연습을 위한 구성', 'font_size': 47, 'x': 255, 'y': 430, 'color': (200, 200, 200, 150), 'shadow': False},
    {'text': 'Dialogtext 10 : 필수 동사 901~1000번', 'font_size': 60, 'x': 300, 'y': 530, 'color': (255, 255, 70, 255), 'shadow': False}
]

# 폰트 경로 시스템에 맞게 보정
for t in my_texts:
    t['font_path'] = "C:/Windows/Fonts/malgun.ttf" # 윈도우 기준 맑은 고딕

create_16_9_custom_text("thumbV3-16-9.png", "Podcast_Final_Result.jpg", my_texts, "black")