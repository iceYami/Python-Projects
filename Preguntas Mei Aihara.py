import random
import time

def obtener_respuesta_mei_aihara():
    citas = [
        "Siempre prefiero mantener cierta distancia. Es más fácil de esa manera.",
        "Las personas son tan complicadas, pero a veces encuentro fascinante sus emociones.",
        "Puedo parecer indiferente, pero me importa, aunque me cueste mostrarlo.",
        "El amor no es algo fácil de definir, pero sé que existe a mi manera.",
        "No soy de mostrar mis debilidades, pero todos tenemos momentos de duda.",
        "No confundas mi silencio con indiferencia. Solo pienso cuidadosamente antes de hablar.",
        "La verdad no siempre es algo que las personas quieran escuchar, pero yo nunca miento.",
        "No siempre soy la mejor manejando mis emociones, pero lo intento.",
        "No necesito la aprobación de nadie, pero a veces sería agradable ser comprendida.",
        "No quiero que me vean como frágil, aunque a veces me sienta de esa manera.",
        "La complejidad de las relaciones humanas es abrumadora, pero es lo que las hace tan interesantes.",
        "Si esperas que actúe como los demás, te decepcionarás.",
        "Las personas cambian, y a veces me pregunto si yo debería cambiar también.",
        "No voy a pretender ser alguien que no soy, aunque eso signifique estar sola.",
        "Puedo parecer fría, pero eso no significa que no me importe. Solo significa que no sé cómo expresarlo.",
        "No importa cuántas veces lo intente, nunca termino de comprenderme completamente.",
        "Si me acerco a alguien, corro el riesgo de hacerle daño. Y eso es algo que me da miedo.",
        "Valoro la independencia, pero a veces desearía poder compartir mis cargas.",
        "No espero que me comprendan completamente. Pero espero que al menos vean mis verdaderas intenciones.",
        "No soy perfecta, pero creo que constantemente estoy evolucionando.",
        "Es fácil ponerse una máscara, pero mucho más difícil es quitársela.",
        "Soy más fuerte de lo que parezco, pero a veces, incluso yo necesito un descanso del peso que llevo.",
        "La gente suele intentar etiquetarme, pero no encajo en ninguna caja, y no tengo intención de hacerlo.",
        "Quizás pienses que soy inaccesible, pero en realidad solo estoy tratando de encontrar mi lugar en este mundo.",
        "Nadie realmente sabe lo que pasa dentro de mí, ni siquiera yo la mayoría de las veces.",
        "Admiro a aquellos que pueden ser abiertos con sus sentimientos. Ojalá pudiera hacer lo mismo.",
        "El silencio no es una señal de debilidad, es una señal de contemplación. Necesito tiempo para procesar todo.",
        "Me da miedo ser incomprendida, pero a veces me pregunto si siquiera me comprendo a mí misma.",
        "Cuando me importa alguien, lo hago a mi manera, aunque no sea la forma en que otros esperan.",
        "A menudo estoy sola, no porque lo elija, sino porque nunca encajé realmente.",
        "Hay fuerza en la soledad. Es donde pienso mejor, pero también es donde enfrento mis propios miedos.",
        "Quiero ser aceptada por quien realmente soy, pero también tengo miedo de lo que pasaría si las personas me viesen tal como soy por dentro.",
        "Algunos días me pregunto si debería cambiar para las personas que me rodean. Pero luego recuerdo: ser fiel a mí misma es todo lo que puedo hacer.",
        "Sé que me cuesta conectar con las personas, pero cuando lo logro, es algo significativo. Solo desearía poder conectar más fácilmente.",
        "Sé que la vida puede ser impredecible, pero encuentro consuelo en la rutina que he construido para mí misma.",
        "Incluso cuando estoy en silencio, estoy constantemente pensando. Siempre hay algo en mi mente.",
        "A veces desearía poder abrirme más, pero me da miedo lo que eso significaría.",
        "El mundo no siempre tiene sentido, pero trato de darle sentido a mi manera.",
        "A veces deseo no estar tan conectada con mis emociones, pero es imposible no sentir.",
        "La gente cree que sabe lo que es mejor para mí, pero al final, solo yo puedo decidir lo que es lo correcto para mí.",
        "Si parezco distante, no es porque no me importe. Es solo la forma en que enfrento el mundo que me rodea.",
        "No necesito que nadie me complete, pero sí aprecio a las personas que me ayudan a crecer.",
        "Sé que puedo ser difícil, pero no lo hago a propósito. Es solo como soy.",
        "Tal vez me veas fría, pero simplemente soy cuidadosa con mis emociones. Pueden ser abrumadoras si las dejo salir.",
        "Tengo mis fallos, como todos, pero estoy aprendiendo a aceptarlos. Es un camino, y todavía estoy en él.",
        "No me gusta depender de los demás, pero a veces tengo que admitir que está bien pedir ayuda.",
        "No espero que siempre me comprendan. Solo espero que lo intenten. Eso es todo lo que puedo pedir.",
        "No me arrepiento de mis decisiones. Puede que hayan sido difíciles, pero me han convertido en quien soy hoy.",
        "A veces solo quiero que alguien me muestre que está bien ser vulnerable. Que está bien bajar la guardia.",
        "No necesito mucha gente a mi alrededor. Unas pocas conexiones genuinas son todo lo que me importa.",
        "Sé que puedo ser distante, pero eso no significa que no necesite compañía. Solo la necesito a mi manera.",
        "Puede que pienses que soy fría, pero solo soy cautelosa con mis emociones. A veces, temerosa de lo que pueda ocurrir.",
        "A veces pienso que lo que más me aterra no es el amor, sino el miedo a no poder darlo como lo desean los demás."
    ]
    return citas[random.randint(0, len(citas) - 1)]

def escribir_lentamente(texto):
    for caracter in texto:
        print(caracter, end='', flush=True)
        for _ in range(2000000): pass  # Bucle de retardo
    print()

def entrevista_mei_aihara():
    print("¡Bienvenidos a la entrevista con Mei Aihara!")
    print("Puedes hacerle cualquier pregunta, y ella responderá.")
    print("Escribe 'exit' para terminar la entrevista.\n")
    
    while True:
        pregunta = input("Tú: ")
        if pregunta.lower() == 'exit':
            escribir_lentamente("Entrevista terminada, cuídate.")
            break
        if pregunta.strip() == '':
            escribir_lentamente("Por favor, haz una pregunta o escribe 'exit' para terminar.\n")
            continue
        respuesta = obtener_respuesta_mei_aihara()
        escribir_lentamente(f"Mei Aihara: {respuesta}\n")

if __name__ == "__main__":
    entrevista_mei_aihara()
