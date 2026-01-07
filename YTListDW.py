# Primero, pip install yt-dlp

import os
import sys
from pathlib import Path
import yt_dlp


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPulsa ENTER para continuar...")


def seleccionar_directorio():
    """
    Permite elegir un directorio base estándar o una ruta personalizada.
    """
    home = Path.home()

    opciones = {
        "1": home / "Documents",
        "2": home / "Music",
        "3": home / "Desktop",
        "4": None
    }

    print("\nSeleccione el directorio de destino:")
    print("1) Documentos")
    print("2) Música")
    print("3) Escritorio")
    print("4) Ruta personalizada")

    eleccion = input("Opción: ").strip()

    if eleccion == "4":
        ruta = Path(input("Introduce la ruta completa: ").strip()).expanduser()
    else:
        ruta = opciones.get(eleccion)

    if not ruta:
        print("Ruta no válida.")
        return seleccionar_directorio()

    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def seleccionar_tipo_descarga():
    print("\nTipo de contenido a descargar:")
    print("1) Vídeo")
    print("2) Audio")

    return input("Opción: ").strip()


def seleccionar_extension(tipo):
    if tipo == "1":
        print("\nFormato de vídeo:")
        print("1) mp4 (recomendado)")
        print("2) avi")
        return "mp4" if input("Opción: ").strip() == "1" else "avi"
    else:
        print("\nFormato de audio:")
        print("1) mp3 (recomendado)")
        print("2) m4a")
        return "mp3" if input("Opción: ").strip() == "1" else "m4a"


def seleccionar_nombrado():
    print("\nFormato de nombre de archivo:")
    print("1) Mantener nombre original")
    print("2) Numerar archivos (1, 2, 3...)")

    return input("Opción: ").strip()


def descargar_playlist(url, directorio_base, tipo, extension, nombrado):
    """
    Configura yt-dlp y descarga la playlist completa.
    """

    plantilla_nombre = (
        "%(playlist_index)s - %(title)s.%(ext)s"
        if nombrado == "1"
        else "%(playlist_index)s.%(ext)s"
    )

    salida = directorio_base / "%(playlist_title)s" / plantilla_nombre

    opciones = {
        "outtmpl": str(salida),
        "ignoreerrors": True,
        "noplaylist": False,
        "continuedl": True,
        "quiet": False,
        "no_warnings": True
    }

    if tipo == "1":  # Vídeo
        opciones.update({
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": extension
        })
    else:  # Audio
        opciones.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": extension,
                "preferredquality": "192"
            }]
        })

    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])


def main():
    while True:
        limpiar_pantalla()
        print("DESCARGADOR DE PLAYLISTS DE YOUTUBE\n")
        print("1) Descargar una playlist")
        print("2) Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "2":
            sys.exit(0)

        if opcion != "1":
            continue

        url = input("\nIntroduce la URL de la playlist: ").strip()
        directorio = seleccionar_directorio()
        tipo = seleccionar_tipo_descarga()
        extension = seleccionar_extension(tipo)
        nombrado = seleccionar_nombrado()

        limpiar_pantalla()
        print("Iniciando descarga...\n")

        descargar_playlist(url, directorio, tipo, extension, nombrado)

        print("\nDescarga finalizada correctamente.")
        pausar()


if __name__ == "__main__":
    main()
