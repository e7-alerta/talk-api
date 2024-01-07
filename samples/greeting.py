import json


def es_tipo_evento_correcto(webhook_data):
    return webhook_data.get("event") == "message_created"


def obtener_contenido_y_telefono(webhook_data):
    content = webhook_data.get("content", "")
    phone_number = webhook_data.get("conversation", {}).get("meta", {}).get("sender", {}).get("phone_number", "")
    return content, phone_number


def obtener_phone_key(content, tipo_mensaje):
    keyword = "🚨️🚨" if tipo_mensaje == "contact_greeting" else " 🚨 "
    index = content.find(keyword)
    return content[index + len(keyword): index + len(keyword) + 4] if index != -1 else None


def determinar_tipo_mensaje(content):
    if "🚨️🚨" in content and content.endswith("c"):
        return "contact_greeting"
    elif " 🚨 " in content:
        return "place_greeting"
    else:
        return None


def procesar_webhook(json_data):
    try:
        # Analizar el JSON recibido
        webhook_data = json.loads(json_data)

        # Verificar si es el tipo de evento correcto
        if es_tipo_evento_correcto(webhook_data):
            # Obtener el contenido del mensaje y el número de teléfono
            content, phone_number = obtener_contenido_y_telefono(webhook_data)


            # Hidratar el formulario básico
            formulario = {"mensaje": content, "phone_number": phone_number}

            # Determinar el tipo de mensaje
            tipo_mensaje = determinar_tipo_mensaje(content)

            if tipo_mensaje:
                formulario["message_type"] = tipo_mensaje
                phone_key = obtener_phone_key(content, tipo_mensaje)
                if phone_key is not None:
                    formulario["phone_key"] = phone_key

            # Imprimir o manejar los resultados según tus necesidades
            print("Formulario:", formulario)

    except json.JSONDecodeError as e:
        print("Error al analizar el JSON:", e)
    except Exception as e:
        print("Error:", e)


# Ejemplo de uso con el JSON proporcionado para "contact_greeting"
json_contact_greeting = '''
{
  "content_type": "text",
  "content": "👋🤗 Buenas noches, Alerta PBA  🚨️🚨056c",
  "conversation": {
    "meta": {
      "sender": {
        "phone_number": "+5491128835917",
        "type": "contact"
      }
    }
  },
  "message_type": "outgoing",
  "event": "message_created"
}
'''

# Ejemplo de uso con el JSON proporcionado para "place_greeting"
json_place_greeting = '''
{
  "content_type": "text",
  "content": "Soy nuevo en Alerta PBA 🚨 056c",
  "conversation": {
    "meta": {
      "sender": {
        "phone_number": "+5491128835917",
        "type": "contact"
      }
    }
  },
  "message_type": "outgoing",
  "event": "message_created"
}
'''

procesar_webhook(json_contact_greeting)
procesar_webhook(json_place_greeting)
