"""Prepara textos para búsquedas que ignoran las tildes españolas."""

import unicodedata


def normalizar_tildes(texto):
    """Quita acentos agudos sin confundir la ñ con la n."""
    descompuesto = unicodedata.normalize("NFD", texto.casefold())
    return unicodedata.normalize("NFC", descompuesto.replace("\u0301", ""))
