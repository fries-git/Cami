from flask import Flask, request, Response, send_file, render_template
from flask_cors import CORS
from PIL import Image, ImageSequence
from helperfuncs import validate
import os
from pathlib import Path
from waitress import serve

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  

app = Flask(__name__)
CORS(app)

@app.post("/uploadimage")
def uploadimage():
    token = request.form.get("token")
    image = request.files.get("image")
    filename = request.form.get("filename")

    if validate(token):
        if not image:
            return {"error": "No image uploaded"}, 400

        try:
            img = Image.open(image)
            img.load()
        except (Exception) as e:
            return {"error": f"Invalid or incomplete image: {e}"}, 400
        
        img_format = (str(img.format)).lower()
        if img_format == "gif":
            pass
        else:
            img = img.convert("RGBA")

        width, height = img.size
        
        targetmax = 300
        mult = max(width, height) / targetmax

        new_size = (
            max(1, int(width / mult)),
            max(1, int(height / mult))
        )

        uid = validate(token)

        if not uid:
            return {"error": "Invalid token"}, 401
        
        if img_format == "gif":
            frames = []
            durations = []

            for frame in ImageSequence.Iterator(img):
                duration = frame.info.get("duration", img.info.get("duration", 100))

                frame = frame.convert("RGBA")
                frame = frame.resize(new_size, Image.Resampling.LANCZOS)
                frame = frame.convert("P", palette=Image.Palette.ADAPTIVE)

                frames.append(frame)
                durations.append(duration)

            path = os.path.join(BASE_DIR,"uploads","imagestorage",f"{filename}.gif")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if os.path.exists(path):
                return "File already exists", 409
            frames[0].save(path,format="GIF",save_all=True,append_images=frames[1:],duration=durations,loop=img.info.get("loop", 0),disposal=2,optimize=True)
            return {"msg": "Uploaded!", "filename": f"{filename}.gif"}, 201
        else:
            img = img.resize((int(width / mult), int(height / mult)), Image.Resampling.LANCZOS)
            try:
                os.makedirs(os.path.join(BASE_DIR, "uploads", "imagestorage"), exist_ok=True)
            except FileExistsError:
                return "File already exists", 409
            path = os.path.join(BASE_DIR, "uploads", "imagestorage", f"{filename}.png")
            if os.path.exists(path):
                return "File already exists", 409
            img.save(path)
            return {"msg": "Uploaded!", "filename": f"{filename}.png"}, 201
    else:
        return "Missing/Invalid token", 400
    return "Unhandled Error", 400

@app.get("/image/<filename>")
def image(filename):

    png_path = os.path.join(
        BASE_DIR, "uploads", "imagestorage", f"{filename}.png"
    )
    gif_path = os.path.join(
        BASE_DIR, "uploads", "imagestorage", f"{filename}.gif"
    )

    if os.path.exists(png_path):
        return send_file(png_path, mimetype="image/png")
    if os.path.exists(gif_path):
        return send_file(gif_path, mimetype="gif/png")

    return "Image doesn't exist", 404

@app.get("/gif/<filename>.gif")
def get_gif(filename):

    path = os.path.join(BASE_DIR,"uploads","imagestorage",f"{filename}.gif")

    if not os.path.isfile(path):
        return "Image doesn't exist", 404

    return send_file(
        path,
        mimetype="image/gif"
    )

portuse = 5614
print(f"Running on port {portuse}")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=portuse, threads = 8)