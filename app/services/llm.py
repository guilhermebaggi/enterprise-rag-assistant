import ollama


class LLMService:
    def __init__(self, model_name: str = "qwen2.5:3b"):
        self.model_name = model_name

    def generate_answer(self, query: str, retrieved_chunks: list[dict]) -> str:
        if not query or not query.strip():
            raise ValueError("A pergunta não pode estar vazia.")

        if not retrieved_chunks:
            return "Não encontrei informações relevantes nos documentos para responder a essa pergunta."

        # Monta o contexto com os trechos recuperados
        context = ""

        for chunk in retrieved_chunks:
            context += (
                f"\nFonte: {chunk['source']}\n"
                f"Página: {chunk['page']}\n"
                f"Trecho:\n{chunk['text']}\n"
                f"{'-' * 50}\n"
            )

        system_prompt = """
        Você é um assistente especializado em responder perguntas
        com base em documentos fornecidos.

        Regras:
        1. Responda utilizando exclusivamente as informações do contexto.
        2. Não invente informações que não estejam nos documentos.
        3. Se o contexto não contiver a resposta, informe que não
           encontrou informações suficientes nos documentos.
        4. Sempre que possível, indique a fonte e a página utilizada.
        5. Responda em português, de forma clara e objetiva.
        6. Não altere, calcule ou arredonde valores monetários.
        7. Associe cada valor exclusivamente à descrição correspondente no contexto.
        8. Se houver informações conflitantes, informe a divergência em vez de escolher um valor.
        9. Não misture valores de demonstrativos ou períodos diferentes.
        """

        user_prompt = f"""
        CONTEXTO DOS DOCUMENTOS:

        {context}

        PERGUNTA:

        {query}

        Com base exclusivamente no contexto, responda à pergunta.
        """

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            options={
                "temperature": 0,
                "seed": 42
            }
        )

        return response["message"]["content"]
