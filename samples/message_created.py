import json

def es_tipo_evento_correcto(webhook_data):
    return webhook_data.get("event") == "message_created"

def obtener_contenido_y_telefono(webhook_data):
    content = webhook_data.get("content", "")
    phone_number = webhook_data.get("conversation", {}).get("meta", {}).get("sender", {}).get("phone_number", "")
    return content, phone_number

def obtener_phone_key(content, keyword):
    index = content.find(keyword)
    return content[index + len(keyword): index + len(keyword) + 4] if index != -1 else None

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

            # Verificar si el contenido tiene la cadena 🚨️🚨 y obtener la phone_key (próximos 4 caracteres)
            keyword = "🚨️🚨"
            phone_key = obtener_phone_key(content, keyword)

            # Hidratar el campo adicional (phone_key) si corresponde
            if phone_key is not None:
                formulario["phone_key"] = phone_key

            # Imprimir o manejar los resultados según tus necesidades
            print("Formulario:", formulario)

    except json.JSONDecodeError as e:
        print("Error al analizar el JSON:", e)
    except Exception as e:
        print("Error:", e)

# Ejemplo de uso con el JSON proporcionado
json_ejemplo = '''
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

procesar_webhook(json_ejemplo)
