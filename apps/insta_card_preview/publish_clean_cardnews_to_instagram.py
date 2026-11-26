import os
import sys
import time
import requests
import dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

dotenv.load_dotenv(r"f:\1인기업\.env")
TOKEN = os.getenv("INSTAGRAM_GRAPH_TOKEN")
USER_ID = "27462714956740695"
IMAGE_DIR = r"C:\Users\sude3\OneDrive\바탕 화면\인스타그램_카드뉴스_오늘자핫이슈"

def upload_image_to_catbox(file_path):
    print(f"  ☁️ CDN 업로드 중: {os.path.basename(file_path)}...", flush=True)
    with open(file_path, 'rb') as f:
        res = requests.post(
            'https://catbox.moe/user/api.php',
            data={'reqtype': 'fileupload'},
            files={'fileToUpload': f}
        )
    if res.status_code == 200 and res.text.startswith('http'):
        url = res.text.strip()
        print(f"     ➔ URL: {url}", flush=True)
        return url
    else:
        raise Exception(f"Catbox upload failed for {file_path}: {res.text}")

def publish_carousel_to_instagram():
    print("🚀 인스타그램 7장 카드뉴스 실시간 자동 포스팅 시작...", flush=True)
    
    image_files = [
        "01_클린핫이슈_표지.jpg",
        "01_클린핫이슈_뉴스1.jpg",
        "02_클린핫이슈_뉴스2.jpg",
        "03_클린핫이슈_뉴스3.jpg",
        "04_클린핫이슈_뉴스4.jpg",
        "05_클린핫이슈_뉴스5.jpg",
        "07_클린핫이슈_아웃트로.jpg"
    ]
    
    item_ids = []
    for img_name in image_files:
        full_path = os.path.join(IMAGE_DIR, img_name)
        cdn_url = upload_image_to_catbox(full_path)
        
        print(f"  📦 인스타그램 아이템 미디어 컨테이너 생성 중...", flush=True)
        api_url = f"https://graph.instagram.com/v21.0/{USER_ID}/media"
        payload = {
            'image_url': cdn_url,
            'is_carousel_item': 'true',
            'access_token': TOKEN
        }
        res = requests.post(api_url, data=payload)
        res_json = res.json()
        
        if 'id' in res_json:
            item_id = res_json['id']
            item_ids.append(item_id)
            print(f"     ➔ Item ID: {item_id}", flush=True)
        else:
            raise Exception(f"Instagram Container Item failed: {res_json}")
            
        time.sleep(1)

    caption_path = os.path.join(IMAGE_DIR, "인스타그램_포스팅_캡션 및 원문링크.txt")
    with open(caption_path, 'r', encoding='utf-8') as f:
        caption_text = f.read()

    print("\n📦 부모 캐러셀(7장 묶음) 컨테이너 생성 중...", flush=True)
    payload_parent = {
        'media_type': 'CAROUSEL',
        'children': ','.join(item_ids),
        'caption': caption_text,
        'access_token': TOKEN
    }
    res_parent = requests.post(f"https://graph.instagram.com/v21.0/{USER_ID}/media", data=payload_parent)
    res_parent_json = res_parent.json()
    
    if 'id' not in res_parent_json:
        raise Exception(f"Instagram Parent Carousel Creation Failed: {res_parent_json}")
        
    carousel_id = res_parent_json['id']
    print(f"✅ 부모 캐러셀 ID 생성 완료: {carousel_id}", flush=True)
    
    time.sleep(3)
    
    print("🔥 인스타그램 라이브 피드 최종 포스팅 실행 중...", flush=True)
    payload_publish = {
        'creation_id': carousel_id,
        'access_token': TOKEN
    }
    res_pub = requests.post(f"https://graph.instagram.com/v21.0/{USER_ID}/media_publish", data=payload_publish)
    res_pub_json = res_pub.json()
    
    if 'id' in res_pub_json:
        post_id = res_pub_json['id']
        print(f"\n🎉🎉🎉 인스타그램 피드 포스팅 최종 성공! 🎉🎉🎉", flush=True)
        print(f"📌 게시물 ID: {post_id}", flush=True)
        print(f"👤 계정: kyokun33", flush=True)
    else:
        raise Exception(f"Instagram Publish Failed: {res_pub_json}")

if __name__ == '__main__':
    publish_carousel_to_instagram()
