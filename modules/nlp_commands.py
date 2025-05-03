import re
import webbrowser
from geopy.geocoders import Nominatim
from .tts import falar
import datetime

# Initialize geolocator
geolocator = Nominatim(user_agent="assistente_virtual")

def normalize(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', ' ', texto)      # remove punctuation
    texto = re.sub(r'\s+', ' ', texto).strip()  # collapse whitespace
    return texto

def clean_term(termo: str) -> str:
    termo = termo.strip()
    termo = re.sub(r'^(?:sobre|de|para|e)\s+', '', termo)  # remove fillers at start
    termo = re.sub(r'\s+', ' ', termo)                    # collapse remaining spaces
    return termo

def executar_comando(raw: str):
    texto = normalize(raw)

    # 1) YouTube command
    if any(k in texto for k in ("youtube", "vídeo", "vídeos", "assistir")):
        texto = re.sub(r'\bno\s+youtube\b', '', texto)
        if "sobre" in texto:
            termo = texto.split("sobre", 1)[1]
        else:
            termo = re.sub(r'.*\b(?:youtube|vídeo|vídeos|assistir)\b', '', texto)
        termo = clean_term(termo)
        if not termo:
            falar("O que devo buscar no YouTube?")
            return
        webbrowser.open(f"https://www.youtube.com/results?search_query={termo}")
        falar(f"Buscando vídeos sobre {termo} no YouTube")
        return

    # 2) Exact location
    m_loc = re.search(r'\b(?:qual a localização de|localização de)\s+(?P<place>.+)', texto)
    if m_loc:
        lugar = clean_term(m_loc.group("place"))
        loc = geolocator.geocode(lugar)
        if loc:
            url = f"https://www.google.com/maps/search/{loc.latitude},{loc.longitude}"
            webbrowser.open(url)
            falar(f"{lugar} fica em latitude {loc.latitude:.4f} e longitude {loc.longitude:.4f}")
        else:
            falar(f"Não encontrei {lugar} no mapa")
        return

    # 3) Distance/route
    m_dist = re.search(r'\b(?:qual a distância de)\s+(?P<place>.+)', texto)
    if m_dist:
        lugar = clean_term(m_dist.group("place"))
        url = f"https://www.google.com/maps/dir//{lugar.replace(' ', '+')}"
        webbrowser.open(url)
        falar(f"Abrindo rota até {lugar} no Google Maps")
        return

    # 4) Time query
    if re.search(r'\b(que horas são|horário|hora)\b', texto):
        agora = datetime.datetime.now().strftime("%H:%M")
        falar(f"Agora são {agora}")
        return

    # 5) Generic Google search (including knowledge queries)
    m_search = re.search(
        r'\b(?:pesquisar|fale sobre|explique|pesquise|buscar|busca|pesquisa|o que é|quem é|significado de|saber)\b\s*(?P<query>.+)',
        texto
    )
    if m_search:
        consulta = clean_term(m_search.group("query"))
        if not consulta:
            falar("O que deseja saber?")
            return
        webbrowser.open(f"https://www.google.com/search?q={consulta}")
        falar(f"Pesquisando sobre {consulta}")
        return

    # 6) Fallback
    falar("Desculpe, não entendi seu comando.")
