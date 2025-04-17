from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import AutoProcessor, Gemma3ForConditionalGeneration
import torch

# LLM initialization (Gemma 3)
model_name = 'gemma-3-4b-it'
model_id = f"google/{model_name}"

model = Gemma3ForConditionalGeneration.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.bfloat16,
).eval()

processor = AutoProcessor.from_pretrained(model_id, use_fast=True)

# Global vectorstore cache (для одного PDF)
vectorstore = None

def load_vectorstore_from_pdf(pdf_path):
    global vectorstore
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)

def get_model_response(prompt: str):
    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "Jesteś pomocnym asystentem. Odpowiadaj szczegółowo na zadane pytanie wykorzystując w pełni wiedzę z kontekstu."}]
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    ).to(model.device, dtype=torch.bfloat16)

    input_len = inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = model.generate(**inputs, max_new_tokens=500, do_sample=False)
        generation = generation[0][input_len:]

    response = processor.decode(generation, skip_special_tokens=True)
    return response

def qa_chain(query):
    if vectorstore is None:
        raise ValueError("Vectorstore nie został załadowany. Użyj najpierw load_vectorstore_from_pdf(pdf_path).")

    docs = vectorstore.similarity_search(query, k=3)
    context = " ".join([doc.page_content for doc in docs])

    prompt = f"Na podstawie następującego kontekstu: {context}\n\nodpowiedz po polsku: {query}"
    return get_model_response(prompt)


