def generar_mensaje(contact_name, place_owner, place_name, place_address):
    mensaje = (
        f"Hola {contact_name} 👋,\n\n"
        f"Soy Ernesto de Alerta PBA. {place_owner} te ha añadido como contacto de emergencia para {place_name} en {place_address}.\n"
        f"Serás informad@ ante cualquier alerta de seguridad en Lanús y Valentín Alsina.\n"
        f"¡Gracias por unirte a nuestra red de seguridad local! 🛡️"
    )
    return mensaje


if __name__ == '__main__':
    # Sustituye con los valores específicos
    nombre_tendero = "Nombre del Tendero"
    nombre_tienda = "Nombre de la Tienda"
    direccion_tienda = "Dirección de la Tienda"

    # Genera el mensaje
    mensaje_generado = generar_mensaje(nombre_tendero, nombre_tienda, direccion_tienda)

    # Imprime el mensaje
    print(mensaje_generado)


def add_contact_remainder():
    # recuerda que puedes añadir más contactos de confianza a tu tienda
    # pongamosle algun emoji de tienda y de persona
    mensaje = (
        f"Recuerda que puedes añadir más contactos de confianza a tu tienda 🏪"
        f" ¡Haz crecer tu red de confianza! 👥"
    )
    return mensaje


def panic_alarm_message(contact_name, place_name, place_address, place_owner):
    # mensaje de alerta por el botón de pánico
    mensaje = (
        f"Hola {contact_name}, has recibido una alerta de emergencia de {place_name} ubicada en {place_address}. "
        f"{place_owner} ha activado el botón de pánico."
        "Nos comunicaremos con las autoridades y te mantendremos informado. "
        "Por favor, manten la calma y si tienes alguna información adicional, por favor, compártela con nosotros."
    )
    return mensaje