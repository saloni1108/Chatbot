import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.0-pro-latest')

# def generate_output(query, retrieved_docs):
#     context = "\n".join(retrieved_docs)
#     prompt = f"""
#     Based on the following documents, please answer the question.

#     Documents:
#     {context}

#     Question:
#     {query}
#     """
#     response = model.generate_content(prompt)
#     return response.choices[0].message["content"]