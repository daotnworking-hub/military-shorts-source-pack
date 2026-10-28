import os
import subprocess

BASE_DIR = r"C:\Users\Dao\Downloads\military_shorts"
CLIPS_DIR = os.path.join(BASE_DIR, "assets", "clips")
CUTS_DIR = os.path.join(BASE_DIR, "assets", "cuts_36s")
os.makedirs(CUTS_DIR, exist_ok=True)

# 12 scenes, 3.0 seconds each = 36 seconds
SCENES = [
    {
        "id": 1,
        "src": "391st_F-15s_takeoff_for_Marauder_Shield_exercise_%28989208%29.webm",
        "ss": "23.0",
        "desc": "F-15 Jet Afterburner Takeoff (Intro Hook)"
    },
    {
        "id": 2,
        "src": "K2_Black_Panther_tank_firing_while_maneuvering.webm",
        "ss": "1.0",
        "desc": "K2 Tank Cannon Live Fire Blast"
    },
    {
        "id": 3,
        "src": "1-14_FAR_Conducts_HIMARS_Training_With_Lithuanian_Armed_Forces_%28Reel%29_%28992935%29.webm",
        "ss": "18.0",
        "desc": "HIMARS Rocket Salvo Eruption"
    },
    {
        "id": 4,
        "src": "152mm_howitzer_2A65_Msta-B.webm",
        "ss": "3.5",
        "desc": "152mm Artillery Massive Shockwave"
    },
    {
        "id": 5,
        "src": "9M317M_surface-to-air-missiles.webm",
        "ss": "4.0",
        "desc": "Surface to Air Missile Vertical Launch"
    },
    {
        "id": 6,
        "src": "Chaff_Launcher_%E2%80%93_Arleigh_Burke-Class_Guided-Missile_Destroyer.webm",
        "ss": "3.0",
        "desc": "Guided Missile Destroyer Rocket Blast"
    },
    {
        "id": 7,
        "src": "391st_F-15s_takeoff_for_Marauder_Shield_exercise_%28989208%29.webm",
        "ss": "12.0",
        "desc": "F-15 Fighter Jet High Speed Taxi & Cockpit"
    },
    {
        "id": 8,
        "src": "K2_Black_Panther_tank_firing_while_maneuvering.webm",
        "ss": "10.0",
        "desc": "K2 Tank Maneuver & Second Cannon Shot"
    },
    {
        "id": 9,
        "src": "1-14_FAR_Conducts_HIMARS_Training_With_Lithuanian_Armed_Forces_%28Reel%29_%28992935%29.webm",
        "ss": "30.0",
        "desc": "HIMARS Night Rocket Blast"
    },
    {
        "id": 10,
        "src": "152mm_howitzer_2A65_Msta-B.webm",
        "ss": "10.5",
        "desc": "152mm Artillery Rapid Fire Reload"
    },
    {
        "id": 11,
        "src": "9M317M_surface-to-air-missiles.webm",
        "ss": "17.0",
        "desc": "Missile Mid-Air Booster Ignition"
    },
    {
        "id": 12,
        "src": "391st_F-15s_takeoff_for_Marauder_Shield_exercise_%28989208%29.webm",
        "ss": "40.0",
        "desc": "Jet Vertical Climb Into Clouds (Outro)"
    }
]

def render_cut(scene):
    in_path = os.path.join(CLIPS_DIR, scene["src"])
    out_path = os.path.join(CUTS_DIR, f"cut_{scene['id']:02d}.mp4")
    
    # Crop to 1080x1920 vertical, adjust colors for cinematic high-impact war punch
    vf = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "fps=30,"
        "eq=contrast=1.18:brightness=0.01:saturation=1.22"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", scene["ss"],
        "-i", in_path,
        "-t", "3.0",
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-an",
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[+] Rendered Cut {scene['id']:02d}/12: {scene['desc']}")

def main():
    print("=== DANG CAT 12 DOAN QUAN SU HOANH TRANG (MOI DOAN 3S) ===")
    for s in SCENES:
        render_cut(s)
    print("=== HOAN TAT 12 DOAN QUAN SU! ===")

if __name__ == "__main__":
    main()
