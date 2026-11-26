import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 [고감독 C드라이브 디스크 정밀 분석기] C: 드라이브 용량 파악 중...")

# Check Drive C Space
total, used, free = shutil.disk_usage("C:\\")
total_gb = round(total / (1024**3), 2)
used_gb = round(used / (1024**3), 2)
free_gb = round(free / (1024**3), 2)

print(f"📊 [C 드라이브 용량 현황]")
print(f"  - 전체 용량 : {total_gb} GB")
print(f"  - 사용 용량 : {used_gb} GB")
print(f"  - 여유 용량 : {free_gb} GB")

# Candidate Folders to Analyze
target_folders = [
    ("Windows Temp", r"C:\Windows\Temp"),
    ("User Temp", r"C:\Users\sude3\AppData\Local\Temp"),
    ("pip Cache", r"C:\Users\sude3\AppData\Local\pip\cache"),
    ("npm Cache", r"C:\Users\sude3\AppData\Local\npm-cache"),
    ("PyTorch/HuggingFace Cache", r"C:\Users\sude3\.cache"),
    ("Windows Update Download Cache", r"C:\Windows\SoftwareDistribution\Download"),
    ("Downloads Folder", r"C:\Users\sude3\Downloads"),
    ("Chrome Cache", r"C:\Users\sude3\AppData\Local\Google\Chrome\User Data\Default\Cache")
]

print("\n🔍 [지울 수 있는 대용량 불필요 캐시/임시 폴더 스캔 결과]:")

cleanable_items = []
total_cleanable_bytes = 0

for label, fpath in target_folders:
    if os.path.exists(fpath):
        size_bytes = 0
        file_count = 0
        try:
            for root, dirs, files in os.walk(fpath):
                for f in files:
                    try:
                        fp = os.path.join(root, f)
                        size_bytes += os.path.getsize(fp)
                        file_count += 1
                    except:
                        pass
        except:
            pass
        
        size_mb = round(size_bytes / (1024**2), 1)
        size_gb = round(size_bytes / (1024**3), 2)
        total_cleanable_bytes += size_bytes
        
        print(f"  - [{label}]: {size_gb} GB ({size_mb} MB) / 파일 {file_count}개")
        cleanable_items.append((label, fpath, size_gb, size_mb))

total_cleanable_gb = round(total_cleanable_bytes / (1024**3), 2)
print(f"\n💡 [고감독 결론] 지금 안전하게 바로 지워서 확보할 수 있는 용량: 약 {total_cleanable_gb} GB!")
