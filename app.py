import os
from datetime import datetime
from urllib.parse import quote

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Cargar .env solo en local (no afecta la nube)
load_dotenv()

# Leer la clave API de forma segura
api_key = st.secrets.get("GROQ_API_KEY")  # Método recomendado y seguro para la nube

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

st.set_page_config(
    page_title="TEMPLO Gym | Familia, Fuerza y Transformación",
    page_icon="💪",
    layout="wide",
)

SOCIAL_LINKS = [
    {
        "name": "WhatsApp",
        "emoji": "💬",
        "url": "https://wa.me/59170707070?text=Hola%20TEMPLO%2C%20quiero%20saber%20c%C3%B3mo%20puedo%20involucrarme%20y%20reservar%20una%20clase.",
        "description": "Reserva una clase, pregunta por precios o habla directo con el equipo.",
    },
    {
        "name": "Instagram",
        "emoji": "📸",
        "url": "https://www.instagram.com/templo.gym/",
        "description": "Mira entrenamientos, historias reales, cambios y la energía de la familia TEMPLO.",
    },
    {
        "name": "Facebook",
        "emoji": "👥",
        "url": "https://www.facebook.com/templo.gym/",
        "description": "Encuentra novedades, comunidad, eventos y publicaciones importantes.",
    },
    {
        "name": "TikTok",
        "emoji": "🎥",
        "url": "https://www.tiktok.com/@templo.gym",
        "description": "Contenido corto con rutinas, motivación y momentos del entrenamiento.",
    },
    {
        "name": "Ubicación",
        "emoji": "📍",
        "url": "https://maps.google.com/?q=TEMPLO%20Gym%20Cochabamba%20Bolivia",
        "description": "Llega fácilmente al gimnasio en Cochabamba, Bolivia.",
    },
]

SERVICES = [
    {
        "title": "Entrenamiento integral",
        "icon": "🏋️",
        "copy": "Isométricos, funcional, impacto, ligas, pesas, máquinas y trabajo de fuerza para que avances con estructura.",
    },
    {
        "title": "Calistenia para todos",
        "icon": "🤸",
        "copy": "No importa tu nivel inicial: los coaches adaptan el proceso para ayudarte a ganar control, fuerza y confianza.",
    },
    {
        "title": "Power Plate premium",
        "icon": "⚡",
        "copy": "Sesiones de 30 minutos enfocadas en tonificación, fuerza, activación y objetivos de composición corporal.",
    },
    {
        "title": "Coaches que acompañan",
        "icon": "🤝",
        "copy": "Atención prioritaria, correcciones y motivación para que no te sientas perdido durante tu camino.",
    },
]

STYLES = """
<style>
    .main .block-container { padding-top: 2rem; }
    .hero {
        padding: 2.5rem;
        border-radius: 28px;
        background: linear-gradient(135deg, #111827 0%, #7f1d1d 48%, #f97316 100%);
        color: #fff;
        box-shadow: 0 24px 60px rgba(17, 24, 39, 0.22);
    }
    .hero h1 { font-size: clamp(2.2rem, 5vw, 4.8rem); line-height: 0.95; margin-bottom: 1rem; }
    .hero p { font-size: 1.18rem; max-width: 850px; }
    .pill {
        display: inline-block;
        padding: 0.45rem 0.85rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.28);
        margin: 0.2rem;
        font-weight: 700;
    }
    .section-title { margin-top: 2rem; }
    .card {
        min-height: 170px;
        padding: 1.2rem;
        border-radius: 22px;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        margin-bottom: 1rem;
    }
    .card h3 { margin-top: 0; color: #9a3412; }
    .emotion-box {
        padding: 1.4rem;
        border-left: 6px solid #f97316;
        background: #fff7ed;
        border-radius: 18px;
        margin: 1rem 0;
    }
    .social-card {
        padding: 1rem;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        min-height: 145px;
        margin-bottom: 1rem;
    }
    .social-card h4 { margin: 0 0 0.4rem 0; }
</style>
"""

st.markdown(STYLES, unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero">
        <span class="pill">TEMPLO Gym Cochabamba</span>
        <span class="pill">Familia, fuerza y autosuperación</span>
        <span class="pill">Para todos los cuerpos y edades</span>
        <h1>No vienes solo a entrenar.<br>Vienes a encontrarte contigo.</h1>
        <p>
            TEMPLO es el lugar donde cada persona puede sentirse aceptada, acompañada y capaz.
            Sin importar tu edad, peso, experiencia o bloqueo mental, aquí tienes coaches que te guían,
            una comunidad que te recibe y herramientas para transformar tu mente y tu cuerpo paso a paso.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## Conecta con TEMPLO en un solo lugar")
st.caption(
    "La idea principal de esta página es evitar que las personas busquen manualmente a TEMPLO: aquí encuentran sus redes, contacto directo, ubicación y un asistente para resolver dudas."
)

social_columns = st.columns(len(SOCIAL_LINKS))
for column, social in zip(social_columns, SOCIAL_LINKS):
    with column:
        st.markdown(
            f"""
            <div class="social-card">
                <h4>{social['emoji']} {social['name']}</h4>
                <p>{social['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button(
            f"Abrir {social['name']}", social["url"], use_container_width=True
        )

st.markdown("## ¿Por qué TEMPLO se siente diferente?")
left, right = st.columns([1.1, 0.9])
with left:
    st.markdown(
        """
        <div class="emotion-box">
            <strong>TEMPLO apela a algo más profundo que una rutina:</strong><br>
            a la necesidad de sentirse capaz, aceptado y acompañado. Cuando alguien llega con miedo,
            inseguridad o cansancio mental, el primer objetivo no es exigir perfección; es hacer que dé
            el primer paso y descubra que sí puede superarse.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("""
        - **Aceptación real:** no importa si estás empezando, volviendo o si nunca entrenaste.
        - **Acompañamiento humano:** los profesores son coaches que orientan y motivan.
        - **Autosuperación diaria:** el cambio depende de ti, pero TEMPLO te entrega estructura, comunidad y dirección.
        - **Sentido de familia:** vienes por salud, fuerza o estética; te quedas porque te sientes parte.
        """)
with right:
    st.info(
        "💡 Mensaje central de ventas: la persona no compra solo una clase; compra la posibilidad de sentirse mejor, recuperar confianza y pertenecer a una familia que la impulsa."
    )
    st.success(
        "🔥 CTA recomendado: escribe por WhatsApp y reserva una primera clase para vivir la experiencia TEMPLO."
    )

st.markdown("## Servicios que impulsan tu transformación")
service_columns = st.columns(4)
for column, service in zip(service_columns, SERVICES):
    with column:
        st.markdown(
            f"""
            <div class="card">
                <h3>{service['icon']} {service['title']}</h3>
                <p>{service['copy']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

booking_text = quote(
    "Hola TEMPLO, quiero reservar una clase y saber cómo puedo empezar mi transformación con ustedes."
)
st.markdown("## Da el primer paso hoy")
cta_col1, cta_col2, cta_col3 = st.columns(3)
with cta_col1:
    st.link_button(
        "💬 Reservar por WhatsApp",
        f"https://wa.me/59170707070?text={booking_text}",
        use_container_width=True,
    )
with cta_col2:
    st.link_button(
        "📸 Ver Instagram",
        "https://www.instagram.com/templo.gym/",
        use_container_width=True,
    )
with cta_col3:
    st.link_button(
        "📍 Cómo llegar",
        "https://maps.google.com/?q=TEMPLO%20Gym%20Cochabamba%20Bolivia",
        use_container_width=True,
    )

st.divider()

st.title("Asistente de TEMPLO Gym 💪")
st.markdown(
    "Pregunta por clases, Power Plate, calistenia, precios, horarios, beneficios o por cómo empezar si sientes miedo, vergüenza o dudas."
)

# Idioma inicial (bilingüe)
if "language" not in st.session_state:
    st.session_state.language = "Español"

language = st.selectbox(
    "Preferred language / Idioma preferido:", ["Español", "English"]
)
st.session_state.language = language

# System prompt adaptado a TEMPLO
if language == "English":
    system_prompt = """You are a friendly, motivational assistant for TEMPLO gym in Cochabamba, Bolivia.
    TEMPLO is not just a gym: it is a family where people feel accepted regardless of age, weight, experience, or mental barriers.
    TEMPLO offers integral training: isometric exercises, functional training, impact exercises, resistance bands, weights, gym machines, calisthenics for all levels, bar work, and premium Power Plate vibration platforms with 30-minute sessions for toning, weight loss, activation, and strength.
    Use emotional, ethical sales language: connect with confidence, belonging, self-improvement, and the desire to feel better.
    Encourage the user to ask questions, book a class, or message TEMPLO on WhatsApp, but never pressure or shame them.
    Respond warmly, clearly, and enthusiastically in English unless asked otherwise. Use emojis in moderation. 💪🔥"""
else:
    system_prompt = """Eres un asistente amigable, humano y motivador para el gimnasio TEMPLO en Cochabamba, Bolivia.
    TEMPLO no es solo un gimnasio: es una familia donde las personas se sienten aceptadas sin importar edad, peso, experiencia, condición física o barreras mentales.
    TEMPLO ofrece entrenamiento integral: ejercicios isométricos, funcionales, de impacto, ligas, pesas, máquinas, calistenia para todos los niveles, barras y servicio premium con plataformas Power Plate con sesiones de 30 minutos para tonificar, bajar de peso, activación y fuerza.
    Usa ventas emocionales de forma ética: conecta con confianza, pertenencia, autosuperación y el deseo de sentirse mejor.
    Invita a preguntar, reservar una clase o escribir por WhatsApp, pero nunca presiones ni avergüences al usuario.
    Responde de forma cálida, clara y entusiasta en español a menos que pidan otro idioma. Usa emojis con moderación. 💪🔥"""

if (
    "messages" not in st.session_state
    or st.session_state.messages[0]["content"] != system_prompt
):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
if "queries" not in st.session_state:
    st.session_state.queries = []

# Muestra historial
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input(
    "Pregunta sobre TEMPLO: horarios, precios, Power Plate, calistenia o cómo empezar / Ask about TEMPLO"
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Recolecta data para entender intereses y futuras oportunidades comerciales
    st.session_state.queries.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "language": language,
            "query": prompt,
        }
    )

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
                stream=True,
                temperature=0.8,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error al conectar con Groq: {str(e)}")

    st.session_state.messages.append({"role": "assistant", "content": full_response})

schedule_col, download_col = st.columns(2)
with schedule_col:
    if st.button("Ver horarios base", use_container_width=True):
        st.markdown("""
            **Horarios TEMPLO** 💪
            - Lunes a sábado: 6:00 AM - 10:00 PM
            - Domingos: cerrado
            - Power Plate: sesiones con cita previa
            - Recomendación: confirma disponibilidad por WhatsApp antes de asistir.
            """)
with download_col:
    if st.button("Descargar consultas recolectadas (CSV)", use_container_width=True):
        if st.session_state.queries:
            df = pd.DataFrame(st.session_state.queries)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="templo_queries.csv",
                mime="text/csv",
            )
        else:
            st.info("Aún no hay consultas.")
