import streamlit as st
import speech_recognition as sr
import os
from datetime import datetime

# 📁 dossier de sauvegarde
if not os.path.exists("transcripts"):
    os.makedirs("transcripts")


# Fonction principale de reconnaissance vocale
def transcribe_speech(api_choice, language):
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎤 Parlez maintenant...")

            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            st.info("⏳ Transcription en cours...")

            # Choix de l'API
            
            if api_choice == "Google":
                text = r.recognize_google(audio, language=language)

            elif api_choice == "Sphinx (offline)":
                text = r.recognize_sphinx(audio, language=language)

            else:
                return "❌ API non supportée."

            return text

    # Gestion d'erreurs avancée

    except sr.UnknownValueError:
        return "❌ Impossible de comprendre l'audio. Parlez plus clairement."

    except sr.RequestError:
        return "❌ Erreur API (connexion ou service indisponible)."

    except OSError:
        return "❌ Microphone introuvable ou bloqué."

    except Exception as e:
        return f"❌ Erreur inattendue : {str(e)}"


# 💾 Sauvegarde du texte
def save_text(text):
    filename = f"transcripts/transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    return filename


# 🖥️ Interface Streamlit
def main():
    st.title("🎙️ Reconnaissance Vocale Avancée")

    #  Paramètres utilisateur
    api_choice = st.selectbox(
        "🌐 Choisir l'API",
        ["Google", "Sphinx (offline)"]
    )

    language = st.selectbox(
        "🌍 Langue",
        ["fr-FR", "en-US", "es-ES", "de-DE"]
    )

    # Pause/Play
    if "running" not in st.session_state:
        st.session_state.running = False

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ Démarrer"):
            st.session_state.running = True

    with col2:
        if st.button("⏸️ Pause"):
            st.session_state.running = False

    # Reconnaissance vocale
    if st.session_state.running:
        text = transcribe_speech(api_choice, language)

        st.success("📝 Résultat :")
        st.write(text)

        # Sauvegarde 
        if st.button("💾 Sauvegarder le texte"):
            file_path = save_text(text)
            st.success(f"✅ Sauvegardé : {file_path}")

            with open(file_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger le fichier",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="text/plain"
                )


if __name__ == "__main__":
    main()