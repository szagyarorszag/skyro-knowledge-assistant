
# Streamlit web interface for Skyro Knowledge Assistant

import streamlit as st
import sys
import json
from pathlib import Path
from datetime import datetime

# add src to path 
sys.path.append(str(Path(__file__).parent))

from vectorstore import VectorStoreManager
from rag import RAGRetriever

# page configuration
st.set_page_config(
    page_title="Skyro Knowledge Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# custom css with white and #5ba6fd - skyro's color scheme
st.markdown("""
<style>
    /* Main container */
    .stApp {
        background-color: white;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1rem 0;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #5ba6fd;
        text-align: center;
        margin-top: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #5ba6fd;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Source boxes */
    .source-box {
        background-color: white;
        border: 2px solid #5ba6fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .source-box strong {
        color: #5ba6fd;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #5ba6fd !important;
        color: white !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #4a95ec !important;
        color: white !important;
    }
    
    /* Text area styling for chat-like interface */
    .stTextArea textarea {
        border: 2px solid #5ba6fd !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        padding: 12px !important;
        min-height: 50px !important;
        max-height: 300px !important;
        resize: vertical !important;
    }
    .stTextArea textarea:focus {
        border-color: #5ba6fd !important;
        box-shadow: 0 0 0 0.2rem rgba(91, 166, 253, 0.25) !important;
    }
    
    /* Text inputs */
    .stTextInput>div>div>input {
        border-color: #5ba6fd;
    }
    .stTextInput>div>div>input:focus {
        border-color: #5ba6fd;
        box-shadow: 0 0 0 0.2rem rgba(91, 166, 253, 0.25);
    }
    .stTextArea>div>div>textarea {
        border-color: #5ba6fd;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #5ba6fd;
        box-shadow: 0 0 0 0.2rem rgba(91, 166, 253, 0.25);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        color: #5ba6fd;
        background-color: white;
        border: 1px solid #5ba6fd;
    }
    
    /* Dividers */
    hr {
        border-color: #5ba6fd;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_rag_system():
    # to load rag system
    try:
        vector_manager = VectorStoreManager(persist_directory="./chroma_db")
        if not vector_manager.load_vectorstore():
            return None, "Failed to load vector store from ./chroma_db. Please ensure the vector store exists."
        rag = RAGRetriever(vector_manager, temperature=0.2)
        return rag, None
    except Exception as e:
        return None, str(e)


def save_feedback(message_id, question, answer, rating, comment):
    # to save user feedback
    feedback_file = Path(__file__).parent.parent / "user_feedback.json"
    
    # load existing feedback
    if feedback_file.exists():
        with open(feedback_file, 'r') as f:
            feedback_data = json.load(f)
    else:
        feedback_data = []
    
    # add new feedback
    feedback_entry = {
        "message_id": message_id,
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer[:500] + "..." if len(answer) > 500 else answer,  # truncate long answers
        "rating": rating,
        "comment": comment
    }
    
    # check if it already exists for this message
    existing_idx = next((i for i, fb in enumerate(feedback_data) if fb["message_id"] == message_id), None)
    if existing_idx is not None:
        feedback_data[existing_idx] = feedback_entry
    else:
        feedback_data.append(feedback_entry)
    
    # save to file
    with open(feedback_file, 'w') as f:
        json.dump(feedback_data, f, indent=2)
    
    return True


def main():
    # init chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # init feedback state
    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = set()
    
    # load logo
    logo_path = Path(__file__).parent.parent / "skyro-logo.svg"
    if logo_path.exists():
        with open(logo_path, "r") as f:
            logo_svg = f.read()
        st.markdown(f'<div class="logo-container">{logo_svg}</div>', unsafe_allow_html=True)
    
    # header
    st.markdown('<p class="main-header">Skyro Knowledge Assistant</p>', unsafe_allow_html=True)
    
    # Add cache clear button in sidebar (for debugging)
    with st.sidebar:
        if st.button("🔄 Clear Cache & Reload"):
            st.cache_resource.clear()
            st.rerun()
    
    # load rag system
    with st.spinner("Loading knowledge base..."):
        rag, error = load_rag_system()
    
    if error:
        st.error(f"Failed to load knowledge base: {error}")
        st.info("Please ensure:\n1. Vector store exists (run `python src/vectorstore.py` first)\n2. GEMINI_API_KEY is set in .env file")
        return
    
    # show statistics if requested
    if st.session_state.get("show_stats", False):
        with st.expander("Vector Store Statistics", expanded=True):
            stats = rag.vectorstore_manager.get_collection_stats()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Documents", stats.get("total_documents", "N/A"))
            with col2:
                st.metric("Embedding Dimension", stats.get("embedding_dimension", "N/A"))
            with col3:
                st.metric("Model", stats.get("model_name", "N/A").split("/")[-1])
        st.session_state.show_stats = False
    
    # display chat history
    for idx, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f'<div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px; margin: 10px 0;"><strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        else:
            # generate message ID if not present
            if "message_id" not in message:
                message["message_id"] = f"msg_{idx}_{hash(message['content'])}"
            
            msg_id = message["message_id"]
            
            st.markdown(f'<div style="background-color: white; border: 2px solid #5ba6fd; padding: 15px; border-radius: 10px; margin: 10px 0;"><strong>Assistant:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
            
            # feedback section
            with st.expander("Feedback", expanded=False):
                st.markdown("**Was this answer helpful?**")
                
                # get previous question
                prev_question = ""
                if idx > 0 and st.session_state.messages[idx-1]["role"] == "user":
                    prev_question = st.session_state.messages[idx-1]["content"]
                
                col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
                
                with col1:
                    if st.button("Helpful", key=f"helpful_{msg_id}"):
                        st.session_state[f"rating_{msg_id}"] = "Helpful"
                        st.rerun()
                
                with col2:
                    if st.button("Not Helpful", key=f"not_helpful_{msg_id}"):
                        st.session_state[f"rating_{msg_id}"] = "Not Helpful"
                        st.rerun()
                
                with col3:
                    if st.button("Incorrect", key=f"incorrect_{msg_id}"):
                        st.session_state[f"rating_{msg_id}"] = "Incorrect"
                        st.rerun()
                
                # show selected rating
                if f"rating_{msg_id}" in st.session_state:
                    st.info(f"Selected: {st.session_state[f'rating_{msg_id}']}")
                
                # comment input
                comment = st.text_area(
                    "Additional comments (optional):",
                    key=f"comment_{msg_id}",
                    placeholder="e.g., Information is outdated, missing details, etc.",
                    height=80
                )
                
                # submit feedback button
                if st.button("Submit Feedback", key=f"submit_{msg_id}"):
                    rating = st.session_state.get(f"rating_{msg_id}", "No rating")
                    if save_feedback(msg_id, prev_question, message["content"], rating, comment):
                        st.session_state.feedback_submitted.add(msg_id)
                        st.success("Feedback saved! Thank you.")
                        st.rerun()
                
                # show if feedback was already submitted
                if msg_id in st.session_state.feedback_submitted:
                    st.success("Feedback submitted for this answer")
            
            # sources & chunks expander
            if message.get("sources"):
                with st.expander("Sources & Chunks"):
                    # show chunks toggle
                    show_chunks_toggle = st.checkbox("Show retrieved chunks", key=f"show_chunks_{idx}")
                    
                    for source in message["sources"]:
                        st.markdown(f"**{source['name']}** - {source['category']}")
                        
                        # show chunks from this source if toggle is on
                        if show_chunks_toggle and message.get("chunks"):
                            source_chunks = [c for c in message["chunks"] if c["source"] == source["name"]]
                            if source_chunks:
                                for chunk in source_chunks:
                                    st.markdown(f'<div style="background-color: #f8f9fa; padding: 10px; margin: 5px 0; border-left: 3px solid #5ba6fd; border-radius: 3px;">', unsafe_allow_html=True)
                                    st.markdown(f"**Rank:** #{chunk['rank']} | **Relevance:** {chunk['score']:.4f}")
                                    st.text(chunk['preview'])
                                    st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown("---")
    
    # example questions (only show if no messages)
    if not st.session_state.messages:
        st.subheader("Example Questions")
        example_cols = st.columns(3)
        
        examples = [
            "What is our KYC verification process?",
            "How does fraud detection work?",
            "What were Q3 2024 results?",
            "Explain the payment retry logic",
            "What caused the October incident?",
            "What are our Q4 OKR priorities?"
        ]
        
        for i, example in enumerate(examples):
            col = example_cols[i % 3]
            if col.button(example, key=f"ex_{i}"):
                st.session_state.current_question = example
                st.rerun()
    
    # chat input with button on the right
    col_input, col_button = st.columns([5, 1])
    
    with col_input:
        question = st.text_area(
            "",
            value=st.session_state.get("current_question", ""),
            placeholder="Ask me anything about Skyro's internal documentation...",
            label_visibility="collapsed",
            height=120,
            key="question_input"
        )
    
    with col_button:
        # role selector for access control
        user_role = st.selectbox(
            "Role",
            ["Admin", "Engineering", "Finance", "Compliance", "Operations", "Support", "Executive"],
            index=0,
            key="user_role"
        )
        # number input above the Ask button
        num_sources = st.number_input("Sources", min_value=3, max_value=10, value=5, key="num_sources")
        ask_button = st.button("Ask", type="primary", use_container_width=True)
    
    # process question
    if ask_button and question.strip():
        # add user message to chat
        st.session_state.messages.append({"role": "user", "content": question})
        
        with st.spinner("Processing..."):
            result = rag.query_with_context(question, k=num_sources, user_role=user_role)
        
        if not result["error"]:
            # add assistant message to chat with unique message ID
            message_id = f"msg_{len(st.session_state.messages)}_{datetime.now().timestamp()}"
            st.session_state.messages.append({
                "role": "assistant", 
                "content": result["answer"],
                "sources": result["sources"],
                "chunks": result.get("chunks", []),
                "message_id": message_id
            })
        else:
            message_id = f"msg_{len(st.session_state.messages)}_{datetime.now().timestamp()}"
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Error: {result['answer']}",
                "sources": [],
                "message_id": message_id
            })
        
        # clear the input
        st.session_state.current_question = ""
        st.rerun()


if __name__ == "__main__":
    main()