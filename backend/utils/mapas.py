from urllib.parse import urlencode


def links_mapa(endereco, cidade=""):
    destino = ", ".join(
        (p.strip() for p in (endereco or "", cidade or "") if p.strip())
    )
    if not destino:
        return {"google": None, "waze": None}
    return {
        "google": "https://www.google.com/maps/search/?"
        + urlencode({"api": 1, "query": destino}),
        "waze": "https://www.waze.com/ul?"
        + urlencode({"q": destino, "navigate": "yes"}),
    }
