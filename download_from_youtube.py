import os
import sys
import subprocess

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input_videos")
os.makedirs(INPUT_DIR, exist_ok=True)

def download_url(url):
    url = url.strip()
    if not url:
        return
    print(f"\n[*] Dang tai video: {url}")
    out_template = os.path.join(INPUT_DIR, "%(title)s.%(ext)s")
    
    cmd = [
        "yt-dlp",
        "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
        "--merge-output-format", "mp4",
        "-o", out_template,
        url
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"[OK] Da tai xong vao thu muc input_videos!")
    except Exception as e:
        print(f"[!] Loi khi tai: {e}")

def main():
    print("=" * 65)
    print("      TOOL TẢI VIDEO YOUTUBE FULL HD TỰ ĐỘNG (KHÔNG CẦN WEB)")
    print("=" * 65)
    print("Khong can vao trang web ytsave.to hay quang cao phiền toái!")
    print("Ban chi can dan link video YouTube vao day la may tu tai Full HD.\n")
    
    if len(sys.argv) > 1:
        for u in sys.argv[1:]:
            download_url(u)
        return

    while True:
        print("-" * 65)
        print("1. Dan link YouTube (Video hoac Short bat ky de tai)")
        print("2. Tu dong tai 5 video Short moi nhat tu @CDMediaQuanSu")
        print("3. Thoat")
        choice = input("Chon lua chon cua ban (1, 2, hoac 3): ").strip()
        
        if choice == "1":
            link = input("\nDan link video YouTube vao day (Enter de tai): ").strip()
            if link:
                download_url(link)
        elif choice == "2":
            print("\n[*] Dang lay 5 video Short moi nhat tu kenh @CDMediaQuanSu...")
            cmd = [
                "yt-dlp",
                "--playlist-end", "5",
                "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
                "--merge-output-format", "mp4",
                "-o", os.path.join(INPUT_DIR, "%(title)s.%(ext)s"),
                "https://www.youtube.com/@CDMediaQuanSu/shorts"
            ]
            try:
                subprocess.run(cmd, check=True)
                print("[OK] Da tai xong 5 video Short moi nhat vao input_videos!")
            except Exception as e:
                print(f"[!] Loi: {e}")
        elif choice == "3":
            break
        else:
            print("Lua chon khong hop le.")

if __name__ == "__main__":
    main()
