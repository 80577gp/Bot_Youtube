import os
import json
import requests
import time
from dotenv import load_dotenv
import google.genai as genai
from groq import Groq
from openai import OpenAI
from anthropic import Anthropic
from moviepy.editor import VideoFileClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Carregar variáveis de ambiente
load_dotenv()

def _valid_api_key(key: str | None) -> bool:
    if not key:
        return False
    invalid_markers = ["your_", "sk-...", "gsk_", "YOUR_", "PLACEHOLDER"]
    return not any(marker in key for marker in invalid_markers)

# Configurações
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
PEXELS_KEY = os.getenv('PEXELS_API_KEY')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_KEY = os.getenv('ANTHROPIC_API_KEY')
GROQ_KEY = os.getenv('GROQ_API_KEY')

# Inicializar clientes
if _valid_api_key(GEMINI_KEY):
    gemini_client = genai.Client(api_key=GEMINI_KEY)
else:
    gemini_client = None
    print('⚠️ GEMINI_KEY não configurada ou é placeholder; Gemini será ignorado como fallback.')

groq_client = Groq(api_key=GROQ_KEY) if _valid_api_key(GROQ_KEY) else None
openai_client = OpenAI(api_key=OPENAI_KEY) if _valid_api_key(OPENAI_KEY) else None
anthropic_client = Anthropic(api_key=ANTHROPIC_KEY) if _valid_api_key(ANTHROPIC_KEY) else None

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def gerar_roteiro():
    """Gera roteiro usando múltiplos modelos de IA gratuitos/priorizando custo zero"""
    prompt = "Crie um roteiro de 10 segundos sobre estoicismo. Retorne APENAS JSON: {'roteiro': 'texto', 'titulo': 'titulo', 'desc': 'desc', 'tags': ['tag']}"

    # Ordem de prioridade: Gratuitos primeiro -> Pagos depois
    models = [
        ("gemini", "Gemini (Google) - Gratuito limitado", lambda: gerar_com_gemini(prompt)),
        ("grok", "Grok (xAI) - 100% GRATUITO", lambda: gerar_com_grok(prompt)),
        ("claude", "Claude (Anthropic) - $5/mês", lambda: gerar_com_claude(prompt)),
        ("gpt-3.5-turbo", "GPT-3.5 Turbo - Pago", lambda: gerar_com_openai(prompt, "gpt-3.5-turbo")),
        ("gpt-4", "GPT-4 - Pago", lambda: gerar_com_openai(prompt, "gpt-4"))
    ]

    for model_name, model_display, generate_func in models:
        try:
            print(f"🔄 Tentando gerar roteiro com {model_display}...")
            info = generate_func()
            print(f"✅ Roteiro gerado com sucesso usando {model_display}!")
            return info
        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "rate limit" in error_str or "429" in error_str or "insufficient_quota" in error_str:
                print(f"⏳ {model_display} - Quota excedida, tentando próximo modelo...")
                continue
            elif "api key" in error_str or "authentication" in error_str or "401" in error_str:
                print(f"⚠️ {model_display} - Chave API não configurada, pulando...")
                continue
            else:
                print(f"❌ Erro com {model_display}: {e}")
                continue

    raise Exception("Todos os modelos falharam. Configure pelo menos uma chave API gratuita (Grok ou Gemini).")

def gerar_com_grok(prompt):
    """Gera conteúdo com Grok (xAI) - 100% GRATUITO"""
    if not groq_client:
        raise Exception("Chave API Groq não configurada")

    response = groq_client.chat.completions.create(
        model="grok-beta",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()
    # Tentar extrair JSON se estiver envolvido em texto
    if not content.startswith('{'):
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            content = content[start:end]

    return json.loads(content)

def gerar_com_claude(prompt):
    """Gera conteúdo com Claude (Anthropic)"""
    if not anthropic_client:
        raise Exception("Chave API Anthropic não configurada")

    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.content[0].text.strip()
    # Tentar extrair JSON se estiver envolvido em texto
    if not content.startswith('{'):
        # Procurar por JSON no texto
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            content = content[start:end]

    return json.loads(content)

def gerar_com_openai(prompt, model):
    """Gera conteúdo com OpenAI"""
    if not openai_client:
        raise Exception("Chave API OpenAI não configurada")

    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()
    # Tentar extrair JSON se estiver envolvido em texto
    if not content.startswith('{'):
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            content = content[start:end]

    return json.loads(content)

def gerar_com_gemini(prompt):
    """Gera conteúdo com Gemini (fallback)"""
    if not gemini_client:
        raise Exception("Chave API Gemini não configurada")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = gemini_client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            return json.loads(response.candidates[0].content.parts[0].text)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str and "quota" in error_str.lower():
                if "retry in" in error_str:
                    try:
                        delay_str = error_str.split("retry in ")[1].split("s")[0]
                        delay = float(delay_str)
                        print(f"⏳ Gemini - Aguardando {delay:.1f} segundos...")
                        time.sleep(delay + 1)
                    except:
                        print("⏳ Gemini - Aguardando 60 segundos...")
                        time.sleep(60)
                else:
                    print("⏳ Gemini - Aguardando 60 segundos...")
                    time.sleep(60)
                if attempt == max_retries - 1:
                    raise
            else:
                raise

def gerar_audio(roteiro):
    """Gera áudio com edge-tts"""
    try:
        print("🔄 Gerando áudio...")
        import subprocess
        subprocess.run([
            'edge-tts', '--voice', 'pt-BR-AntonioNeural', '--text', roteiro, '--write-media', 'locucao.mp3'
        ], check=True)
        if not os.path.exists('locucao.mp3'):
            raise FileNotFoundError("Arquivo de áudio não foi criado")
        print("✅ Áudio gerado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao gerar áudio: {e}")
        raise

def baixar_video():
    """Baixa vídeo de fundo do Pexels"""
    try:
        print("🔄 Baixando vídeo de fundo...")
        response = requests.get(
            "https://api.pexels.com/videos/search?query=dark nature&orientation=portrait&per_page=1",
            headers={"Authorization": PEXELS_KEY}
        )
        response.raise_for_status()
        data = response.json()
        if not data.get('videos'):
            raise ValueError("Nenhum vídeo encontrado no Pexels")
        v_url = data['videos'][0]['video_files'][0]['link']
        with open('fundo.mp4', 'wb') as f:
            f.write(requests.get(v_url).content)
        if not os.path.exists('fundo.mp4'):
            raise FileNotFoundError("Arquivo de vídeo não foi baixado")
        print("✅ Vídeo baixado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao baixar vídeo: {e}")
        raise

def editar_video():
    """Edita vídeo com áudio"""
    try:
        print("🔄 Editando vídeo...")
        v = VideoFileClip("fundo.mp4")
        a = AudioFileClip("locucao.mp3")
        duration = min(v.duration, a.duration)
        final = v.subclip(0, duration).set_audio(a.subclip(0, duration))
        final.write_videofile("final.mp4", fps=24, codec="libx264", audio_codec="aac", logger=None)
        if not os.path.exists('final.mp4'):
            raise FileNotFoundError("Arquivo final não foi criado")
        print("✅ Vídeo editado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao editar vídeo: {e}")
        raise

def obter_credenciais():
    """Obtém credenciais do YouTube"""
    try:
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
    except Exception as e:
        print(f"❌ Erro ao obter credenciais: {e}")
        raise

def upload_youtube(info, creds):
    """Faz upload para YouTube"""
    try:
        print("🔄 Fazendo upload para YouTube...")
        youtube = build('youtube', 'v3', credentials=creds)
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "categoryId": "27",
                    "title": info['titulo'],
                    "description": info['desc'],
                    "tags": info['tags']
                },
                "status": {"privacyStatus": "public"}
            },
            media_body=MediaFileUpload("final.mp4")
        )
        response = request.execute()
        print(f"✅ Vídeo publicado com sucesso! ID: {response['id']}")
    except Exception as e:
        print(f"❌ Erro ao fazer upload: {e}")
        raise

def main():
    """Função principal"""
    try:
        print("🚀 Iniciando Bot YouTube Shorts...")

        # 1. Gerar roteiro
        info = gerar_roteiro()

        # 2. Gerar áudio
        gerar_audio(info['roteiro'])

        # 3. Baixar vídeo
        baixar_video()

        # 4. Editar vídeo
        editar_video()

        # 5. Obter credenciais
        creds = obter_credenciais()

        # 6. Upload
        upload_youtube(info, creds)

        print("🎉 Processo concluído com sucesso!")

    except Exception as e:
        print(f"💥 Erro geral: {e}")
        exit(1)

if __name__ == "__main__":
    main()
