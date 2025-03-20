import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Set page config and custom CSS
st.set_page_config(layout="wide")

url = "http://127.0.0.1:8000/outlets/"
response = requests.get(url)

st.image("subway_icon/subway_icon.png", width=140)
title, empty = st.columns(2)
with title:
    st.title('Subway Outlets in KL') 

chat, map = st.columns(2)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chain" not in st.session_state:
    st.session_state.chain = None

with chat:
    st.title('AI Chatbot')
    
    if response.status_code == 200:
        outlets = response.json()
        
        # Prepare data for RAG
        if st.session_state.chain is None:
            # Create documents from outlet data with metadata
            documents = []
            for outlet in outlets:
                # Create a structured document with metadata and enhanced content
                doc = Document(
                    page_content=f"""
                    This is a Subway restaurant outlet in Kuala Lumpur.
                    
                    Outlet Information:
                    Name: {outlet['name']}
                    Address: {outlet['address']}
                    Opening Hours: {outlet['opening_hours']}
                    
                    Location Details:
                    - Located in Kuala Lumpur, Malaysia
                    - Latitude: {outlet['latitude']}
                    - Longitude: {outlet['longitude']}
                    
                    You can help customers find this Subway outlet and provide information about its location and operating hours.
                    """,
                    metadata={
                        "name": outlet['name'],
                        "address": outlet['address'],
                        "opening_hours": outlet['opening_hours'],
                        "latitude": outlet['latitude'],
                        "longitude": outlet['longitude'],
                        "type": "subway_outlet",
                        "location": "Kuala Lumpur"
                    }
                )
                documents.append(doc)
            
            # Create vector store with enhanced search parameters
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(documents, embeddings)
            
            # Initialize conversation chain with enhanced parameters
            llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-3.5-turbo",
                max_tokens=500  #
            )
            
            # Enhanced memory configuration
            memory = ConversationBufferMemory(
                memory_key="chat_history", 
                return_messages=True,
                output_key="answer",
                input_key="question"
            )
            
            # Create the chain with enhanced parameters
            st.session_state.chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(
                    search_kwargs={
                        "k": 3,  
                        "fetch_k": 5,  
                        "lambda_mult": 0.5  #
                    }
                ),
                memory=memory,
                return_source_documents=True,
                verbose=True 
            )
        
        # Chat input 
        if prompt := st.chat_input("Ask about Subway outlets...", key="chat_input"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Get response and add to chat history
            try:
                chain_response = st.session_state.chain({"question": prompt})
                st.session_state.messages.append({"role": "assistant", "content": chain_response["answer"]})
            except Exception as e:
                st.error(f"Error getting response: {str(e)}")
        
        st.markdown("---")
        
        # Display chat messages in reverse order (newest first)
        for message in reversed(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

with map:
    if response.status_code == 200:
        st.title("Subway Outlets Information")
        outlets = response.json()
        # Create a list of outlet names for the dropdown
        outlet_names = [outlet['name'] for outlet in outlets]
        
        # Add outlet selection dropdown
        selected_outlet_name = st.selectbox("Select an Outlet", outlet_names)
        
        selected_outlet = next(outlet for outlet in outlets if outlet['name'] == selected_outlet_name)
        
        # Display outlet details
        st.write(f"**Address:** {selected_outlet['address']}")
        st.write(f"**Phone:** {selected_outlet['opening_hours']}")
        
        # Create navigation links
        col1, col2 = st.columns(2)
        with col1:
            st.image("navigation_icons/waze_icon.png", width=24)
            st.markdown(f"[Open in Waze]({selected_outlet['waze_link']})")
        with col2:
            st.image("navigation_icons/maps_icon.png", width=24)
            st.markdown(f"[Open in Google Maps]({selected_outlet['google_maps_link']})")
        
        # Create the map centered on the selected outlet
        m = folium.Map(
            location=[selected_outlet['latitude'], selected_outlet['longitude']],
            zoom_start=13,
            tiles='CartoDB positron'  # Clean, modern style
        )
        
        # Add all outlets as markers
        for outlet in outlets:
            # Create popup content
            popup_html = f"""
                <div style='font-family: Arial, sans-serif;'>
                    <h3 style='color: #2c3e50;'>{outlet['name']}</h3>
                    <p><b>Address:</b> {outlet['address']}</p>
                    <p><b>Opening Hours:</b> {outlet['opening_hours']}</p>
                </div>
            """
            
            # Add marker with popup
            folium.Marker(
                location=[outlet['latitude'], outlet['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        # Add a larger marker for the selected outlet
        folium.Circle(
            location=[selected_outlet['latitude'], selected_outlet['longitude']],
            radius=5000,  # 5km radius
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.05,
            popup=folium.Popup(f"<b>Selected Outlet:</b> {selected_outlet['name']}", max_width=300)
        ).add_to(m)
        
        # Display the map
        st_folium(m, width=800, height=600)
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

    


