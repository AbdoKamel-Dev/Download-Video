import yt_dlp
from pathlib import Path


# مكان حفظ الملفات
DOWNLOAD_FOLDER = Path.home() / "Downloads" / "Video Downloader"
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


# عرض حالة التحميل
def progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "0%")
        speed = d.get("_speed_str", "N/A")
        eta = d.get("_eta_str", "N/A")

        print(
            f"\rDownloading: {percent} | Speed: {speed} | ETA: {eta}",
            end=""
        )

    elif d["status"] == "finished":
        print("\nDownload finished!")


# تحميل الفيديو
def download_video(url, quality, playlist):

    if quality == "best":
        format_selector = (
            "best[acodec!=none][vcodec!=none]/best"
        )
    else:
        format_selector = (
            f"best[height<={quality}]"
            f"[acodec!=none][vcodec!=none]"
            f"/best[height<={quality}]"
        )

    options = {
        "format": format_selector,
        "outtmpl": str(
            DOWNLOAD_FOLDER / "%(title)s.%(ext)s"
        ),
        "noplaylist": not playlist,
        "progress_hooks": [progress_hook],
        "ignoreerrors": True,
        "retries": 10,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

    except Exception as e:
        print(f"\nError: {e}")


# تحميل الصوت فقط
def download_audio(url, playlist):

    options = {
        "format": "bestaudio",
        "outtmpl": str(
            DOWNLOAD_FOLDER / "%(title)s.%(ext)s"
        ),
        "noplaylist": not playlist,
        "progress_hooks": [progress_hook],
        "ignoreerrors": True,
        "retries": 10,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

    except Exception as e:
        print(f"\nError: {e}")


# البرنامج الرئيسي
def main():

    print("=" * 50)
    print("           VIDEO DOWNLOADER")
    print("=" * 50)

    # الرابط
    url = input("\nPaste video / playlist URL:\n").strip()

    if not url:
        print("No URL entered.")
        return

    # اختيار Video / Audio
    print("\nWhat do you want to download?")
    print("1. Video")
    print("2. Audio only")

    download_type = input("Enter number: ").strip()

    # Playlist؟
    print("\nPlaylist?")
    print("1. Yes")
    print("2. No")

    playlist_choice = input("Enter number: ").strip()

    playlist = playlist_choice == "1"

    # فيديو
    if download_type == "1":

        print("\nChoose quality:")
        print("1. 360p")
        print("2. 480p")
        print("3. 720p")
        print("4. Best available")

        quality_choice = input("Enter number: ").strip()

        qualities = {
            "1": 360,
            "2": 480,
            "3": 720,
            "4": "best"
        }

        quality = qualities.get(quality_choice, 720)

        print("\nStarting video download...\n")

        download_video(
            url,
            quality,
            playlist
        )

    # صوت
    elif download_type == "2":

        print("\nStarting audio download...\n")

        download_audio(
            url,
            playlist
        )

    else:
        print("Invalid choice.")

    print("\nSaved to:")
    print(DOWNLOAD_FOLDER)


if __name__ == "__main__":
    main()