import os
import json
import re

def natural_sort_key(s):
    # Splits string by numbers to allow natural sorting (e.g. 1, 2, 10 instead of 1, 10, 2)
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def generate_portfolio_data():
    portfolio_dir = "Portofolio"
    
    if not os.path.exists(portfolio_dir):
        print(f"Error: Directory '{portfolio_dir}' not found.")
        return
        
    subdirs = sorted([d for d in os.listdir(portfolio_dir) if os.path.isdir(os.path.join(portfolio_dir, d))])
    
    portfolio_data = {}
    
    # We will map directory names to keys used in query parameter (?client=...)
    # E.g. "2023 Eka & Shanon" -> "eka-shanon"
    # "2023 Claudia" -> "claudia"
    # "2025 Anton & Jesenia" -> "anton-jesenia"
    def make_key(dir_name):
        # Remove year
        name_part = re.sub(r'^\d{4}\s+', '', dir_name)
        # Convert to lowercase and replace spaces & special chars with hyphens
        key = name_part.lower()
        key = re.sub(r'[^a-z0-9\s-]', '', key)
        key = re.sub(r'\s+', '-', key)
        key = re.sub(r'-+', '-', key).strip('-')
        return key

    for d in subdirs:
        dir_path = os.path.join(portfolio_dir, d)
        client_key = make_key(d)
        
        # Parse year and name
        match = re.match(r'^(\d{4})\s+(.+)$', d)
        if match:
            year = match.group(1)
            display_name = match.group(2)
        else:
            year = "2026"
            display_name = d
            
        print(f"Processing client: {display_name} ({year}) -> Key: {client_key}")
        
        # Helper to extract a unique photo ID to prevent duplicates
        def get_photo_id(filename):
            name, _ = os.path.splitext(filename)
            # Remove ' copy' or 'copy'
            name = re.sub(r'\s*copy', '', name, flags=re.IGNORECASE)
            name = name.lower().strip()
            return name

        # Helper to assign priority to image versions
        def get_photo_priority(path):
            path_lower = path.lower()
            if 'editing' in path_lower and 'webp' in path_lower:
                return 4  # Edited WebP
            elif 'editing' in path_lower:
                return 3  # Edited JPG
            elif 'file sementara' in path_lower or 'resize' in path_lower:
                if path_lower.endswith('.webp'):
                    return 2  # Temporary WebP
                return 1.5  # Temporary JPG
            else:
                if path_lower.endswith('.webp'):
                    return 1.0
                return 0.5  # Original JPG

        # 1. Scan for images recursively (excluding Testimoni directory)
        photo_dict = {}
        for root, dirs, files in os.walk(dir_path):
            # Exclude Testimoni from image search
            if "Testimoni" in dirs:
                dirs.remove("Testimoni")
                
            for file in files:
                if file.lower().endswith(('.webp', '.jpg', '.jpeg', '.png')):
                    rel_path = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")
                    photo_id = get_photo_id(file)
                    priority = get_photo_priority(rel_path)
                    
                    # If this photo ID is new, or has higher priority than existing one, update it
                    if photo_id not in photo_dict or priority > photo_dict[photo_id]["priority"]:
                        photo_dict[photo_id] = {
                            "path": rel_path,
                            "priority": priority,
                            "filename": file
                        }
        
        # Extract path strings
        photos = [item["path"] for item in photo_dict.values()]
        
        # Sort photos numerically/naturally based on filename
        photos.sort(key=lambda p: natural_sort_key(os.path.basename(p)))
        
        # 2. Scan for Testimony / Review
        testimoni_dir = os.path.join(dir_path, "Testimoni")
        review_text = ""
        review_title = "Kebahagiaan yang Sempurna"
        review_author = display_name
        video_url = ""
        has_video = False
        
        if os.path.exists(testimoni_dir) and os.path.isdir(testimoni_dir):
            for file in os.listdir(testimoni_dir):
                file_path = os.path.join(testimoni_dir, file)
                
                # Check for review text (.txt file)
                if file.lower().endswith('.txt'):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_read:
                            lines = f_read.readlines()
                            # Clean lines
                            clean_lines = [l.strip() for l in lines if l.strip()]
                            if clean_lines:
                                # Often the text contains quotes or paragraphs. Join them.
                                review_text = "\n".join(clean_lines)
                                # Let's set a title if possible, or keep default
                                review_author = f"{display_name} (Verified Review)"
                    except Exception as e:
                        print(f"  Error reading testimony txt for {display_name}: {e}")
                        
                # Check for video file (.mp4, .mov)
                elif file.lower().endswith(('.mp4', '.mov')):
                    # Drive Video Mapping for Remote Hosting
                    drive_video_mapping = {
                        "Dennis & Caludia.mp4": "1fXxScyr4VqpLLrdSCUPrOTs_isWk4v5g",
                        "Eka & Shannon.mp4": "12RvJQQ4hjLnJ2ErXgi75hdiQJcd9KiR-",
                        "Lin & Fiega.mp4": "1sBlVZJxmJ51AYpky0lF-KIuNEmIAUW0Y",
                        "Amalia & Adria.MOV": "1xNdzkd-osOHodCclgv8g2btOUdbwefk6",
                        "Devi & Michael.MOV": "1dqvBj1gFyMyjFZa6ZcpbRYPV6IotcQ9P",
                        "Yuka & Hawker.MOV": "1rSoKhEq0OQEibwmBUfzWZVnbHOffF1Rw",
                        "Anton & Jasonia.MOV": "1-ym3JhwYcpEbG2HFVafsjIdbBJq25H9X",
                        "Hanum & Fuki.MOV": "1amG8quzJ4Map6LViwFTGeYJLD3CrzTrZ",
                        "Jun Wen & Siok Teng.MOV": "1O4pK2UrkOaQSd5ES4qDIwC7xDUqXdOeF",
                        "Andi & Livia.MOV": "1z-ZD16PMe4i8Da3-buYungnedTTewWrn",
                        "Weisma & Fadhil.MOV": "1eGKqp3Fwx-_THeEccFg-JobC-qrYCHhn"
                    }
                    if file in drive_video_mapping:
                        video_url = f"https://drive.google.com/uc?export=download&id={drive_video_mapping[file]}"
                    else:
                        video_url = os.path.relpath(file_path, ".").replace("\\", "/")
                    has_video = True
        
        # Clean description/first paragraph if available, or generate standard one based on client
        description = f"Sebuah perayaan cinta yang indah dan tak terlupakan bagi {display_name} bersama keluarga dan kerabat terdekat di Bali."
        
        # Find default location if possible (e.g. from existing layout or set based on year/name)
        location = "Bali"
        if "eka" in client_key:
            location = "Uluwatu"
        elif "andi" in client_key:
            location = "Ubud"
        elif "devi" in client_key:
            location = "Seminyak"
        elif "claudia" in client_key:
            location = "Uluwatu"
        
        portfolio_data[client_key] = {
            "name": display_name,
            "year": year,
            "location": location,
            "description": description,
            "photos": photos,
            "hasVideo": has_video,
            "videoUrl": video_url,
            "reviewText": review_text,
            "reviewTitle": review_title,
            "reviewAuthor": review_author
        }
        
    # Write out portfolio-data.js
    output_path = "portfolio-data.js"
    js_content = f"// Automatically generated by generate_portfolio_data.py\nwindow.PORTFOLIO_DATA = {json.dumps(portfolio_data, indent=2)};\n"
    
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write(js_content)
        
    print(f"\nSuccessfully compiled database for {len(portfolio_data)} clients to '{output_path}'.")

if __name__ == "__main__":
    generate_portfolio_data()
