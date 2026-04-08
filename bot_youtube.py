import os, json, requests
import google.generativeai as genai
from moviepy.editor import VideoFileClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

GEMINI_KEY = "AIzaSyAhZiRBTPHlJMpE1iXf24tSyt3kn66j0cc"
PEXELS_KEY = "7RyOOJvTukxKt8maExRaocf1b3zKm9BzYXIcLxTKWLEbCBKWd6iQslYn"
genai.configure(api_key=GEMINI_KEY)
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

print("1. Roteiro...")
info = json.loads(genai.GenerativeModel('gemini-1.5-flash').generate_content("Crie um roteiro de 10 segundos sobre estoicismo. Retorne APENAS JSON: {'roteiro': 'texto', 'titulo': 'titulo', 'desc': 'desc', 'tags': ['tag']}", generation_config={"response_mime_type": "application/json"}).text)

print("2. Midia...")
os.system(f'edge-tts --voice pt-BR-AntonioNeural --text "{info["roteiro"]}" --write-media locucao.mp3')
v_url = requests.get("https://api.pexels.com/videos/search?query=dark nature&orientation=portrait&per_page=1", headers={"Authorization": PEXELS_KEY}).json()['videos'][0]['video_files'][0]['link']
with open('fundo.mp4', 'wb') as f: f.write(requests.get(v_url).content)

print("3. Edicao...")
v, a = VideoFileClip("fundo.mp4"), AudioFileClip("locucao.mp3")
v.subclip(0, a.duration).set_audio(a).write_videofile("final.mp4", fps=24, codec="libx264", audio_codec="aac", logger=None)

print("4. YouTube...")
creds = Credentials.from_authorized_user_file('token.json', SCOPES) if os.path.exists('token.json') else None
if not creds or not creds.valid:
    creds = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES).run_local_server(port=0)
    with open('token.json', 'w') as t: t.write(creds.to_json())

build('youtube', 'v3', credentials=creds).videos().insert(part="snippet,status", body={"snippet": {"categoryId": "27", "title": info['titulo'], "description": info['desc'], "tags": info['tags']}, "status": {"privacyStatus": "public"}}, media_body=MediaFileUpload("final.mp4")).execute()
print("✅ PUBLICADO!")
