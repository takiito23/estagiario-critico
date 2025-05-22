from openai import OpenAI
import streamlit as st
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

modelo_ideal = """
Daniel era um jovem entregador, responsável e dedicado, que trabalhava em uma agência dos correios em uma pequena cidade do interior...
"""

criterios = [
    "Ritmo",
    "Atmosfera",
    "Narrador",
    "Clímax",
    "Final",
    "Originalidade"
]

def analisar_criterio(criterio, ideal, teste):
    prompt = f"""
    Você é um editor crítico de roteiros para um canal de histórias sombrias. Avalie o roteiro abaixo com base no critério "{criterio}".
    Compare com o roteiro ideal fornecido. Dê uma nota de 1 a 5 e explique em 2 ou 3 frases o porquê.

    Roteiro ideal:
    {ideal}

    Roteiro analisado:
    {teste}

    Saída esperada:
    Critério: {criterio}
    Nota: X/5
    Justificativa: ...
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# --- Streamlit App ---
st.title("Estagiário Crítico - Avaliação de Roteiro")

roteiro_teste = st.text_area("Cole aqui o roteiro para análise:", height=600)

analises = []
if st.button("Analisar Roteiro"):
    if not roteiro_teste.strip():
        st.warning("Por favor, cole um roteiro para análise.")
    else:
        st.subheader("Resultado da Avaliação:")
        for criterio in criterios:
            resultado = analisar_criterio(criterio, modelo_ideal, roteiro_teste)
            analises.append((criterio, resultado))
            st.markdown(f"**{criterio}:**")
            st.code(resultado, language="markdown")

        st.subheader("Classificação Final")
        status = st.radio("O que deseja fazer com este roteiro?", ["Aprovar", "Revisar", "Rejeitar"])
        st.success(f"Você selecionou: {status.upper()} para este roteiro.")
