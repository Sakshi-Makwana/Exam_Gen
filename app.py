import streamlit as st
import time
from dotenv import load_dotenv

# Import your custom modules
from src.document_processor import get_pdf_text, get_text_chunks
from src.embedding_handler import create_embeddings
from src.vector_store import create_vector_store
from src.llm_handler import configure_llm, generate_question_from_context
from src.uniqueness_filter import select_unique_questions
from src.topic_modeler import get_document_topics
from src.pdf_generator import create_pdf

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Exam-Gen ✨",
    page_icon="📝",
    layout="wide"
)

# --- LOAD API KEY AND CONFIGURE LLM ---
try:
    load_dotenv()
    configure_llm()
except ValueError as e:
    st.error(f"⚠️ API Key Configuration Error: {e}")
    st.stop()

# --- HELPER FUNCTION TO RESET STATE ---
def reset_session_state():
    """Clears the generated content from the session state."""
    for key in ['vector_store', 'question_paper', 'answer_key', 'topics']:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Session cleared! Ready for a new exam.")

# --- SIDEBAR - THE CONTROL PANEL ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    st.markdown("---")

    # 1. File Uploader
    st.subheader("1. Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload your PDF source materials", 
        type="pdf", 
        accept_multiple_files=True,
        help="You can upload up to 12 PDF files."
    )
    # Display names of uploaded files
    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")
        for file in uploaded_files:
            st.write(f"└─ {file.name}")
    
    st.markdown("---")

    # 2. Exam Structure Configuration
    with st.expander("2. Define Exam Structure", expanded=True):
        num_1_markers = st.number_input("1-Mark Questions", min_value=0, step=1)
        num_2_markers = st.number_input("2-Mark Questions", min_value=0, step=1)
        num_3_markers = st.number_input("3-Mark Questions", min_value=0, step=1)
        num_4_markers = st.number_input("4-Mark Questions", min_value=0, step=1)
        num_5_markers = st.number_input("5-Mark Questions", min_value=0, step=1)
        num_10_markers = st.number_input("10-Mark Questions", min_value=0, step=1)

    st.markdown("---")
    
    # 3. Generate Button
    st.subheader("3. Generate Exam")
    generate_button = st.button("✨ Generate Now!", use_container_width=True)
    
    st.markdown("---")
    
    # "Start Over" button at the bottom
    if st.button("🔄 Start Over", use_container_width=True):
        reset_session_state()

# --- MAIN PAGE ---
st.title("📝 Exam-Gen ✨")
st.markdown("Your intelligent assistant for creating well-balanced exam papers in minutes.")

# --- INITIAL WELCOME SCREEN ---
if "question_paper" not in st.session_state or not st.session_state.question_paper:
    st.info("👋 Welcome! Get started by uploading your documents and defining the exam structure in the sidebar.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("1. Upload 📚")
        st.write("Provide one or more PDF documents (textbooks, notes, articles) as the source material.")
    with col2:
        st.subheader("2. Configure ⚙️")
        st.write("Specify the exact number of questions you need for various mark values.")
    with col3:
        st.subheader("3. Generate ✨")
        st.write("Our AI will analyze the documents, understand the topics, and generate a diverse set of questions with a detailed answer key.")
    
    

# --- PROCESSING LOGIC ---
if generate_button:
    if not uploaded_files:
        st.warning("Please upload at least one PDF document to begin.")
    else:
        # Document processing and topic modeling (runs only once)
        with st.status("🚀 Processing your documents...", expanded=True) as status:
            if "vector_store" not in st.session_state:
                try:
                    status.write("Reading and chunking text...")
                    all_raw_text = "".join([get_pdf_text(pdf) for pdf in uploaded_files])
                    text_chunks = get_text_chunks(all_raw_text)
                    
                    status.write("Identifying main topics...")
                    st.session_state.topics = get_document_topics(text_chunks)
                    
                    status.write("Creating text embeddings...")
                    embeddings = create_embeddings(text_chunks)
                    
                    status.write("Building the vector knowledge base...")
                    st.session_state.vector_store = create_vector_store(text_chunks, embeddings)
                    status.update(label="✅ Processing Complete!", state="complete")
                    
                except Exception as e:
                    status.update(label=f"❌ Error during processing: {e}", state="error")
                    st.stop()
            else:
                status.update(label="✅ Documents already processed!", state="complete")

        # Question Generation
        if "vector_store" in st.session_state:
            with st.spinner("🧠 Generating a diverse set of questions... This might take a moment."):
                # ... (The entire question generation logic remains the same)
                question_paper = []
                answer_key = []
                exam_structure = {
                    1: (num_1_markers, "very easy", "a key-term definition", 2),
                    2: (num_2_markers, "easy", "a simple definition or concept", 3),
                    3: (num_3_markers, "short answer", "a concept with an example", 3),
                    4: (num_4_markers, "medium", "an explanation of a process", 2),
                    5: (num_5_markers, "long answer", "an application or comparison", 2),
                    10: (num_10_markers, "essay", "a detailed analysis or synthesis", 1),
                }
                try:
                    topics = st.session_state.topics
                    total_questions_generated = 0
                    for marks, config in exam_structure.items():
                        count, difficulty, topic_base, over_gen_count = config
                        if count > 0:
                            over_generated_pool = []
                            for i in range(count + over_gen_count):
                                current_topic = topics[total_questions_generated % len(topics)]
                                topic_query = f"{topic_base} related to '{current_topic}'"
                                q_data = generate_question_from_context(
                                    st.session_state.vector_store, marks, difficulty, topic_query)
                                over_generated_pool.append(q_data)
                                total_questions_generated += 1
                                time.sleep(2)
                            unique_questions = select_unique_questions(over_generated_pool, count)
                            for q_data in unique_questions:
                                question_paper.append(f"**Q{len(question_paper) + 1}.** {q_data['question']} ({marks} Marks)")
                                answer_key.append(f"**A{len(answer_key) + 1}.** {q_data['answer']}")
                    st.session_state.question_paper = question_paper
                    st.session_state.answer_key = answer_key
                    st.success("🎉 Question paper generated successfully!")
                except Exception as e:
                    st.error(f"An error occurred during question generation: {e}")

# --- DISPLAY RESULTS USING TABS ---
if "question_paper" in st.session_state and st.session_state.question_paper:
    st.markdown("---")
    st.header("Your Generated Exam 📄")
    
    # Create tabs for clean output
    download_tab, qp_tab, ak_tab = st.tabs(["📥 Download", "📝 Question Paper (Preview)", "🔑 Answer Key (Preview)"])

    with download_tab:
        st.subheader("Download Your Files")
        question_pdf_bytes = create_pdf("Question Paper", st.session_state.question_paper)
        answer_pdf_bytes = create_pdf("Answer Key", st.session_state.answer_key)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Question Paper",
                data=question_pdf_bytes,
                file_name="Question_Paper.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label="Download Answer Key",
                data=answer_pdf_bytes,
                file_name="Answer_Key.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    with qp_tab:
        for question in st.session_state.question_paper:
            st.markdown(question)

    with ak_tab:
        for answer in st.session_state.answer_key:
            st.markdown(answer)