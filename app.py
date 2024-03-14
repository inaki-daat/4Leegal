import streamlit as st
# Make sure to import your Router class correctly, adjust the import path as necessary
from Router import Router
from DocAgent import DocAgent
import pickle

# This function checks if there's already a Router instance in the session state,
# if not, it creates a new one.
def get_router():
    if 'router' not in st.session_state:
        docagents= pickle.load(open('docagents_1.pkl', 'rb'))
        router=Router(docagents)
        st.session_state.router = router
    return st.session_state.router

def main():
    # Session state to persist router object
    if 'router' not in st.session_state:
        st.session_state.router = get_router()
    
    st.title("4Leegal")
    
    # Chatbox UI
    user_input = st.text_input("Haz una pregunta legal:", key="user_query")
    
    if st.button("Pregunta"):
        if user_input:
            # Assuming 'ask' method of your Router class returns a string response
            response = st.session_state.router.ask(user_input)
            st.markdown(f"**Respuesta:** {response}")
        else:
            st.warning("Escribe tu pregunta")

if __name__ == "__main__":
    main()
