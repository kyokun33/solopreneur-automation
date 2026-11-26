# -*- coding: utf-8 -*-
import os
import asyncio
import subprocess
import edge_tts

PROJ = r"f:\1인기업\google_flow_projects\empty_stomach_longform"
os.makedirs(PROJ, exist_ok=True)

SCENES_SCRIPT = [
    {
        "id": "scene1",
        "title": "Intro & 오프닝 훅",
        "text": (
            "여러분, 아침에 건강 챙긴다고 공복에 무심코 먹었던 음식이, 오히려 위장을 망가뜨리고 만성 피로를 부르고 있었다면 어떨까요? "
            "많은 분들이 바쁜 아침 시간에 식사 대용으로 바나나, 고구마, 혹은 모닝커피를 자주 찾으시는데요. "
            "사실 이 세 가지 음식은 빈속에 들어갔을 때 위벽과 혈관에 치명적인 부담을 줄 수 있습니다. "
            "오늘 내몸에힐링에서는 아침 공복에 절대 피해야 할 최악의 음식 세 가지와, "
            "의사들이 매일 아침 빈속에 챙겨 먹는 진짜 보약 음식까지 알기 쉽게 팩트만 딱 짚어 드릴게요."
        )
    },
    {
        "id": "scene2",
        "title": "1. 바나나의 충격적인 진실",
        "text": (
            "첫 번째로 피해야 할 음식은 바로 바나나입니다. "
            "다이어트와 건강의 대표 주자로 알려져 있어서 아침 대용으로 가장 많이 드시는 과일이죠. "
            "하지만 바나나에는 마그네슘이 아주 풍부하게 들어있는데요. "
            "빈속에 바나나를 먹게 되면 혈액 속의 마그네슘 수치가 단시간에 급격히 치솟게 됩니다. "
            "이렇게 되면 칼륨과의 균형이 무너지면서 심혈관에 큰 무리를 주고, 저혈압이나 어지럼증을 유발할 수 있습니다. "
            "특히 평소에 심장이 약하시거나 신장 기능이 떨어져 있는 분들이라면 아침 공복 바나나는 반드시 피하셔야 합니다."
        )
    },
    {
        "id": "scene3",
        "title": "2. 고구마의 위벽 자극",
        "text": (
            "두 번째는 달콤하고 든든한 고구마입니다. "
            "탄수화물 식단으로 아침에 군고구마나 찐고구마 챙겨 드시는 분들 정말 많으시죠. "
            "그런데 고구마에는 아교질과 타닌이라는 성분이 다량 함유되어 있습니다. "
            "이 성분들은 위벽을 직접적으로 강하게 자극해서, 위산이 과도하게 쏟아져 나오게 만듭니다. "
            "결국 빈속에 위산이 위벽을 공격하면서 타는 듯한 속쓰림과 통증이 생기고, 심한 경우 위염이나 위궤양으로 이어질 수 있습니다. "
            "평소에 위가 약하시다면 아침 빈속 고구마는 꼭 피해주세요."
        )
    },
    {
        "id": "scene4",
        "title": "3. 모닝커피의 위험성",
        "text": (
            "세 번째는 많은 분들의 아침 필수품, 바로 모닝커피입니다. "
            "눈을 뜨자마자 잠을 깨기 위해 빈속에 진한 아메리카노 한 잔 드시는 분들 계실 텐데요. "
            "공복 상태에서는 음식이 없기 때문에, 커피에 들어있는 고농도 카페인이 위점막을 무방비 상태로 직접 공격하게 됩니다. "
            "이로 인해 위산 분비가 폭발적으로 늘어나면서 식도 하부 괄약근을 느슨하게 만들고, 역류성 식도염과 만성 소화불량을 유발하는 주범이 되죠. "
            "모닝커피는 반드시 식사 후에 드시는 것이 위장을 지키는 지름길입니다."
        )
    },
    {
        "id": "scene5",
        "title": "공복 보약 대체 식단 3가지",
        "text": (
            "그렇다면 아침 공복에는 도대체 무엇을 먹어야 내 몸을 살릴 수 있을까요? "
            "의사들과 영양학 전문가들이 입을 모아 추천하는 공복 보약 세 가지가 있습니다. "
            "첫 번째는 밤새 끈적해진 혈액을 맑게 하고 위장을 깨워주는 따뜻한 미온수 한 잔입니다. "
            "두 번째는 천연 위장약이라 불리는 비타민 유가 풍부한 양배추이고요. "
            "세 번째는 질 좋은 단백질과 필수 아미노산으로 혈당을 안정시키는 부드러운 삶은 달걀입니다. "
            "기상 직후 미온수를 천천히 마신 뒤 삶은 달걀과 양배추를 곁들이면, 속 편하고 든든한 하루를 시작할 수 있습니다."
        )
    },
    {
        "id": "scene6",
        "title": "Outro & 채널 구독 안내",
        "text": (
            "사소한 아침 습관 하나가 내 몸의 10년 뒤 건강을 결정합니다. "
            "오늘부터는 공복에 바나나와 커피 대신, 따뜻한 물 한 잔으로 내 몸을 아껴주는 건 어떨까요? "
            "오늘 영상이 유익하셨다면 구독과 좋아요, 알림 설정 부탁드리고요. "
            "소중한 가족과 친구들에게도 이 영상을 공유해 주세요. "
            "내몸에힐링은 여러분의 매일 아침을 더 건강하고 가볍게 만들어 드릴게요. 감사합니다!"
        )
    }
]

async def synthesize_all():
    concat_txt = os.path.join(PROJ, "concat_audio.txt")
    durations = []
    with open(concat_txt, "w", encoding="utf-8") as f:
        for idx, s in enumerate(SCENES_SCRIPT):
            print(f"Synthesizing {s['id']} ({s['title']})...")
            raw_mp3 = os.path.join(PROJ, f"{s['id']}_raw.mp3")
            scene_wav = os.path.join(PROJ, f"{s['id']}_master.wav")
            # 0Hz pure vocal with edge_tts
            comm = edge_tts.Communicate(s["text"], "ko-KR-SunHiNeural", rate="+7%", pitch="+0Hz")
            await comm.save(raw_mp3)

            # Analog 1.055x silk pitch resampling (no vocoder)
            subprocess.run([
                "ffmpeg", "-y", "-i", raw_mp3,
                "-filter_complex", "asetrate=24000*1.055,aresample=44100,highpass=f=80,lowpass=f=12000,afftdn=nf=-24",
                "-ar", "44100", "-ac", "2", scene_wav
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            dur = float(subprocess.check_output([
                "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", scene_wav
            ]).decode().strip())
            durations.append(dur)
            print(f"  {s['id']}: {dur:.2f}s")
            f.write(f"file '{scene_wav.replace(chr(92), '/')}'\n")

    # Merge full audio
    merged_wav = os.path.join(PROJ, "longform_full_master.wav")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt, "-c", "copy", merged_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_dur = sum(durations)
    print(f"\n[AUDIO COMPLETE] Total Duration: {total_dur:.2f}s ({total_dur/60:.2f} min)")

if __name__ == "__main__":
    asyncio.run(synthesize_all())

