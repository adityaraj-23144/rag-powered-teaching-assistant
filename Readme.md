# 📚 RAG-Powered Teaching Assistant

A Retrieval Augmented Generation (RAG) based AI system that helps students query NPTEL Internet of Things lecture videos and receive precise, timestamped answers.

---

## 📌 Table of Contents
- <a href="#overview">Overview</a>
- <a href="#problem-statement">Problem Statement</a>
- <a href="#dataset">Dataset</a>
- <a href="#tools--technologies">Tools & Technologies</a>
- <a href="#project-structure">Project Structure</a>
- <a href="#methodology">Methods</a>
- <a href="#model--output">Model / Output</a>
- <a href="#how-to-run-this-project">How to Run This Project</a>
- <a href="#conclusion">Conclusion</a>
- <a href="#future-work">Future Work</a>
- <a href="#author--contact">Author & Contact</a>

---
<h2><a class="anchor" id="Overview"></a>Overview</h2>

This project implements a RAG-powered AI teaching assistant for the NPTEL Internet of Things (IoT) course.
It allows students to ask natural-language questions and receive context aware answers by retrieving relevant lecture segments and guiding them to exact lecture numbers and timestamps.

The system processes lecture content end-to-end  from audio transcription and chunking to vector embedding, semantic search, and LLM-based answer generation.

---
<h2><a class="anchor" id="problem-statement"></a>Problem Statement</h2>
Although NPTEL courses provide high-quality educational content, students often face challenges such as:
- Difficulty finding exact timestamps where a concept is explained
- Long lecture videos that make revision time-consuming
- Ineffective keyword-based search that lacks semantic understanding
- This project addresses these issues by building an AI assistant that:
- Understands student queries semantically
- Retrieves the most relevant lecture segments
- Directs students to the precise lecture and timestamp for revision

---
<h2><a class="anchor" id="dataset"></a>Dataset</h2>

- Source: NPTEL Internet of Things lecture videos

Data generated during the pipeline:
- Audio files (.mp3)
- Transcripts obtained via  transcription
- Timestamped JSON chunks containing:
- Spoken text
- Vector embeddings stored as  joblib files

---
<h2><a class="anchor" id="tools--technologies"></a>Tools & Technologies</h2>


- Python
- OpenAI API Whisper (audio transcription)
- Ollama
- bge-m3 for text embeddings
- llama3.2 for answer generation
- Scikit-learn (Cosine Similarity)
- Pandas & NumPy
- Joblib
- Git & GitHub

---
<h2><a class="anchor" id="project-structure"></a>Project Structure</h2>


```
rag-powered-teaching-assistant/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── videos/                    # Original lecture videos (ignored in git)
├── audios/                    # Lecture audio files (ignored)
├── Texts/                     # Timestamped texts (ignored)
├── Chunks/                    # Timestamped JSON chunks (ignored)
├── embeddings/                # Vector embeddings (ignored)
│
├── data/
│   └── prompt.txt
│
├── scripts/                   # Python scripts
│   ├── videos_to_audios.py       # Video → audio conversion
│   ├── audios_to_texts.py        # Audio → timestamped texts
│   ├── texts_to_chunks.py        # Texts → JSON chunks
│   ├── preprocess_Chunks.py      # Chunks → vector embeddings
│   └── rag_inference.py          # RAG retrieval + LLM inference
```

---


<h2><a class="anchor" id="methodology"></a>Methods</h2>

- Video to Audio Conversion
  - Lecture videos are converted into audio files.
- Audio Transcription
  -  Audio files are transcribed using an API-based speech-to-text model.
- Chunk Generation
  - Transcripts are split into timestamped chunks and stored as JSON.
- Vector Embedding
  - Each chunk is embedded using bge-m3 and stored using joblib.
- Semantic Retrieval
  - Cosine similarity is used to retrieve the most relevant chunks for a user query.
- Answer Generation
  - A constrained prompt is constructed and passed to an LLM to generate  student-friendly answers with timestamps.

---
<h2 id="model--output">Model / Output</h2>

- For a given student query, the system:
  - Retrieves the top-K most relevant lecture segments
  - Clearly mentions lecture number(s) and exact timestamps
  - Explains concepts in simple, student-friendly language
  - Rejects queries unrelated to the IoT course content

- Example Output:
“The concept of IoT gateways is explained in Lecture 9 between 12:30 and 16:10. You can revisit this segment to understand how gateways connect edge devices to the cloud.”

---
<h2><a class="anchor" id="how-to-run-this-project"></a>How to Run This Project</h2>

1. Collect lecture videos
Move all NPTEL lecture video files (.mp4) into the videos/ folder.

2. Convert videos to audio
Convert all video files (.mp4) into audio files (.mp3) by running:
```bash
python video_To_audios.py
```
3. Convert audio to text
Convert all audio files (.mp3) into text transcripts (.txt) by running:
```bash
python audios_To_Texts.py
```
You can use an API key for audio-to-text conversion, or
Use the provided local transcription code (OpenAI Whisper large-v2) if you have a high-end system
If you have a low-end system, you may use an online transcript generator such as:
https://notegpt.io/youtube-transcript-generator
and place the generated transcript files into the Texts/ folder.

4. Convert text files to chunks
Convert all transcript files (.txt) into timestamped JSON chunks by running:
```bash
python Texts_To_Chunks.py
```
5. Generate vector embeddings
Convert the JSON chunk files into vector embeddings and save them as a joblib file by running:
```bash
python Preprocess_Chunks.py
```
The embeddings will be saved in the embeddings/ folder.
6. Run the RAG-based teaching assistant
Load the embeddings into memory, generate a relevant prompt based on the user query, and feed it to the LLM by running:
```bash
python rag_inference.py
```

---
<h2><a class="anchor" id="conclusion"></a>Conclusions</h2>

- This project demonstrates how RAG can be effectively applied to educational content to:
- Improve accessibility of long lecture videos
- Enable faster and more targeted revision
- Provide explainable, timestamp-aware answers
- The system serves as a strong foundation for AI-powered learning assistants.

---
<h2 id="future-work">Future Work</h2>

- FAISS-based indexing for faster large-scale retrieval
- Support for multiple NPTEL courses

---
<h2><a class="anchor" id="author--contact"></a>🔗Author & Contact</h2>

**Aditya Raj**  
Data Scientist  
📧 Email: adiwork23144@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/aditya-rajj/)  
🔗 [Portfolio](https://aditya-raj23144-portfolio.netlify.app/)
