import openai
import os
import subprocess
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar o cliente OpenAI com a chave da API
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key


def get_language():
    language = os.getenv("LANGUAGE", "en-US")
    if language == "en-US":
        return "Generate a commit message for the following changes in a software project:"
    else:
        return "Gere uma mensagem de commit para as seguintes alterações em um projeto de software:"


def generate_summary(file_paths):
    # Gerar resumo para cada arquivo alterado
    summary = ''
    for file_path in file_paths:
        if file_path:
            language = os.getenv("LANGUAGE", "en-US")
            if language == "en-US":
                with open(file_path) as f:
                    content = f.read()
                    summary += f"Change in file: {file_path}\n"
                    summary += f"Summary: {content}\n\n"
            else:
                with open(file_path) as f:
                    content = f.read()
                    summary += f"Mudança no arquivo: {file_path}\n"
                    summary += f"Resumo: {content}\n\n"


    return summary.strip()


def generate_commit_message():
    try:
        # Obter arquivos adicionados no comando git add
        output = subprocess.run(['git', 'diff', '--name-only', '--cached'], capture_output=True, text=True)
        changed_files = output.stdout.split('\n')

        summary = generate_summary(changed_files)
        language_prompt = get_language()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": language_prompt},
                {"role": "user", "content": summary}
            ],
            max_tokens=60,
            temperature=0.7
        )
        message = response["choices"][0]["message"]["content"].strip()
        return message
    except Exception as e:
        print(f"Error generating commit message: {e}")
        return "Error: Could not generate commit message"


if __name__ == "__main__":
    commit_message = generate_commit_message()
    print(commit_message)
