import streamlit as st
from Router import Router
from DocAgent import DocAgent
import pickle

def get_router():
    if 'router' not in st.session_state:
        try:
            docagents = pickle.load(open('docagents_1.pkl', 'rb'))
            router = Router(docagents)
            st.session_state.router = router
        except Exception as e:
            st.error("Error al inicializar el router")
            return None
    return st.session_state.router

def main():
    try:
        # Session state to persist router object
        if 'router' not in st.session_state:
            st.session_state.router = get_router()
            if st.session_state.router is None:
                st.error("Tengo que recalcular tu pregunta, vuelve a intentarlo")
                return
        
        st.title("4Leegal")
        
        # Chatbox UI
        user_input = st.text_input("Haz una pregunta legal:", key="user_query")
        
        if st.button("Pregunta"):
            if user_input:
                try:
                    # Assuming 'ask' method of your Router class returns a string response
                    response = st.session_state.router.ask(user_input)
                    st.markdown(f"**Respuesta:** {response}")
                except Exception as e:
                    st.error("Tengo que recalcular tu pregunta, vuelve a intentarlo")
            else:
                st.warning("Escribe tu pregunta")
    except Exception as e:
        st.error("Tengo que recalcular tu pregunta, vuelve a intentarlo")

if __name__ == "__main__":
    main()
