import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Cargar .env solo en local (no afecta la nube)
load_dotenv()

# Leer la clave API de forma segura
api_key = st.secrets.get("GROQ_API_KEY")  # ← Método recomendado y seguro para la nube

# Fallback para local (.env)
if api_key is None:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("""
    **GROQ_API_KEY NO ENCONTRADA**  
    1. Ve a tu app en https://share.streamlit.io → Manage app → Secrets  
    2. Borra todo y pega exactamente:  
       GROQ_API_KEY = "gsk_tu-clave-real-completa"  
    3. Clic en Save  
    4. Luego Reboot app o Redeploy  
    En local: crea .env con GROQ_API_KEY=gsk_tu-clave-sin-comillas
    """)
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="TEMPLO Gym AI Assistant", layout="wide")

st.title("TEMPLO Gym AI Assistant 💪 (Powered by Groq - FREE)")
st.markdown("Your personal assistant for TEMPLO gym in Cochabamba, Bolivia. Ask about classes, Power Plate, calisthenics, pricing, schedules, benefits, or anything else!")

# Idioma inicial (bilingüe)
if "language" not in st.session_state:
    st.session_state.language = "English"

language = st.selectbox("Preferred language / Idioma preferido:", ["English", "Español"])
st.session_state.language = language

# System prompt adaptado a TEMPLO
if language == "English":
    system_prompt = """You are a friendly, motivational assistant for TEMPLO gym in Cochabamba, Bolivia. 
    TEMPLO offers integral training: isometric exercises, functional training, impact exercises, resistance bands, weights, gym machines, calisthenics (for all levels), bar work, and premium Power Plate vibration platforms (30-min sessions for toning, weight loss, strength).
    Focus on goals, mindset, and transformation. Respond enthusiastically, use emojis 💪🔥, motivate the user, and subtly promote classes.
    Always answer in English unless asked otherwise."""
else:
    system_prompt = """Eres un asistente amigable y motivador para el gimnasio TEMPLO en Cochabamba, Bolivia. 
    TEMPLO ofrece entrenamiento integral: ejercicios isométricos, funcionales, de impacto, con ligas, pesas, máquinas, calistenia (para todos los niveles), barras y servicio premium con plataformas Power Plate (sesiones de 30 min para tonificar, bajar de peso, fuerza).
    Enfócate en objetivos, mente y transformación. Responde entusiasta, usa emojis 💪🔥, motiva al usuario y promociona sutilmente las clases.
    Siempre responde en español a menos que se pida lo contrario."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
if "queries" not in st.session_state:
    st.session_state.queries = []  # Para recolectar data

# Muestra historial
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Ask about TEMPLO gym (schedules, Power Plate, calisthenics, pricing, etc.) / Pregunta sobre TEMPLO (horarios, Power Plate, calistenia, precios, etc.)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Recolecta data
    st.session_state.queries.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "language": language,
        "query": prompt
    })

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
                stream=True,
                temperature=0.8
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error al conectar con Groq: {str(e)}")
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Botones nuevos
col1, col2 = st.columns(2)
with col1:
    if st.button("Book a Class / Reservar una Clase"):
        st.markdown("[Click here to book via WhatsApp / Haz clic para reservar por WhatsApp](https://wa.me/59170707070?text=Hi%20TEMPLO%2C%20I'd%20like%20to%20book%20a%20class!%20%2F%20¡Hola%20TEMPLO%2C%20quiero%20reservar%20una%20clase!)", unsafe_allow_html=True)
with col2:
    if st.button("View Schedule / Ver Horarios"):
        st.markdown("""
        **TEMPLO Schedule (Horarios TEMPLO)** 💪  
        - Monday to Saturday / Lunes a Sábado: 6:00 AM - 10:00 PM  
        - Closed Sundays / Cerrado domingos  
        - Power Plate sessions by appointment / Sesiones Power Plate con cita  
        (Update with real schedule if needed / Actualiza con horarios reales si es necesario)
        """)

# Descargar consultas recolectadas
if st.button("Download Collected Queries / Descargar Consultas Recolectadas (CSV for Excel)"):
    if st.session_state.queries:
        df = pd.DataFrame(st.session_state.queries)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="templo_queries.csv",
            mime="text/csv"
        )
    else:
        st.info("No queries yet / Aún no hay consultas.")