# criar_estrutura_estudos.py

import os

# Nome da pasta raiz do projeto
base_dir = "base_estudos_python"

# Estrutura de subpastas com roteiros personalizados
roteiros = {
    "fundamentos": [
        "Sintaxe básica e identação",
        "Tipos primitivos (int, float, str, bool)",
        "Operadores (aritméticos, lógicos, comparação)",
        "Estruturas de controle: if, else, elif",
        "Laços: for, while, break, continue",
        "Funções e escopo de variáveis",
        "Bloco with e gerenciamento de contexto",
        "Conceito de __name__ == '__main__'",
        "Entrada e saída de dados",
    ],
    "poo": [
        "Conceitos de classe e objeto",
        "Atributos e métodos",
        "Encapsulamento",
        "Herança e polimorfismo",
        "Métodos especiais (__init__, __str__, etc)",
        "Boas práticas com POO em Python",
    ],
    "estrutura_dados": [
        "Listas e tuplas",
        "Dicionários e conjuntos (sets)",
        "Iteração e manipulação de coleções",
        "List comprehension",
        "Funções úteis: zip, enumerate, map, filter",
    ],
    "manipulacao_arquivos": [
        "Leitura e escrita em arquivos .txt",
        "Manipulação de arquivos CSV com open",
        "Leitura e escrita em arquivos JSON",
        "Uso de with para arquivos",
    ],
    "modulos_builtins": [
        "Módulo os",
        "Módulo sys",
        "Módulo datetime",
        "Módulo pathlib",
        "Importações e aliases",
    ],
    "bibliotecas_populares": [
        "pandas: leitura, manipulação e exportação de dados",
        "openpyxl e xlsxwriter: escrita em Excel",
        "requests: consumo de APIs REST",
        "dotenv: variáveis de ambiente",
    ],
    "automacoes": [
        "Gerar relatórios em Excel a partir de dados SQL",
        "Enviar e-mails com anexos e HTML",
        "Automatizar execução com pyodbc + pandas",
        "Uso de agendamentos via Airflow",
    ],
    "sql_com_python": [
        "Conexão com SQL Server usando pyodbc",
        "Execução de queries com pandas.read_sql",
        "Geração de relatórios com filtros",
        "Validação de dados retornados",
        "Debug de dados vazios ou inconsistentes",
    ],
    "flask_api": [
        "Criação de rotas básicas",
        "Uso de métodos GET, POST",
        "Retorno em JSON",
        "Conexão com SQL e uso em APIs",
        "Boas práticas de organização",
    ],
    "django_api": [
        "Criação de projetos e apps",
        "Modelos com ORM",
        "Views e rotas de API",
        "Integração com banco",
        "Documentação com DRF",
    ],
    "airflow": [
        "O que é e como instalar o Airflow",
        "Criação de DAGs e tarefas",
        "Uso de BashOperator e PythonOperator",
        "Uso de TaskGroup e .expand()",
        "Leitura de variáveis com airflow.models.Variable",
        "Envio de e-mails com HTML",
        "Execução de queries SQL e geração de Excel",
        "Migração de scripts para DAGs",
        "Agendamento e depuração de DAGs",
    ],
    "testes": [
        "Introdução ao pytest",
        "Escrevendo testes simples",
        "Estrutura de testes em projetos",
        "Testes de API com requests",
        "Cobertura e boas práticas",
    ],
    "boas_praticas": [
        "Uso do PEP8",
        "Tipagem com type hints",
        "Estrutura de projeto em camadas",
        "Uso de logging",
        "Nomenclatura e legibilidade",
    ],
    "snippets": [
        "Trechos de código úteis para consulta rápida",
        "Exemplos de manipulação de datas",
        "Conexão com banco",
        "Envio de e-mails",
        "Formatação de planilhas",
    ],
    "referencias": [
        "Links úteis",
        "Zettelkasten com conceitos importantes",
        "Tutoriais e artigos salvos",
    ],
    "debugging": [
        "Uso do debugger no VS Code",
        "Breakpoints e inspeção de variáveis",
        "Análise da pilha de chamadas",
        "Erros comuns e como investigar",
    ],
    "ambientes_virtualenv": [
        "Como criar ambientes virtuais com venv",
        "Instalação de dependências com pip",
        "Uso de requirements.txt",
        "Isolamento de ambientes",
    ],
    "scripts_docker": [
        "Criação de Dockerfile",
        "Uso de docker-compose para SQL Server e Airflow",
        "Execução de projetos com containers",
        "Evitar dependências locais",
    ],
    "exploracoes_ai": [
        "Introdução ao Langchain",
        "Automação com n8n",
        "Criação de fluxos com IA",
        "Casos de uso com Python + IA",
    ],
    "documentacao_projetos": [
        "api_contabilidade: fluxo e queries",
        "Sistema de avaliação: modelagem + views",
        "Relatório horas pendentes: lógica e envio",
        "DAGs criadas e objetivos de cada uma",
        "Notas de migração",
    ],
}


# Função para criar conteúdo do README
def criar_readme(nome_pasta, topicos):
    nome_formatado = nome_pasta.replace("_", " ").title()
    roteiro = "\n".join(f"- [ ] {item}" for item in topicos)
    conteudo = f"""# 📘 {nome_formatado}

## 🧭 Roteiro de Estudos

{roteiro}

## 📂 O que você vai encontrar aqui

- Exemplos práticos
- Exercícios com dicas
- Anotações pessoais e dúvidas resolvidas

## 🔍 Busca rápida (palavras-chave)

<!-- {nome_pasta}, estudo, python, exemplos -->

## 📚 Referências oficiais

- [Documentação Python 3.10.10](https://docs.python.org/3.10/)
"""
    return conteudo


# Função para criar estrutura de pastas e arquivos
def criar_estrutura(base, roteiro_dict):
    os.makedirs(base, exist_ok=True)
    for pasta, topicos in roteiro_dict.items():
        caminho = os.path.join(base, pasta)
        os.makedirs(caminho, exist_ok=True)
        readme_path = os.path.join(caminho, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(criar_readme(pasta, topicos))
            print(f"✅ Criado: {readme_path}")


# Executar
if __name__ == "__main__":
    criar_estrutura(base_dir, roteiros)
