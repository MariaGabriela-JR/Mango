# Índice
- [Objetivo](#objetivo)  
- [Tecnologias utilizadas](#tecnologias-utilizadas)  
- [Primeiros passos](#primeiros-passos)  
- [Guia para contribuição](#guia-para-contribuição)  

---

## Objetivo
Esse repositório tem como objetivo o desenvolvimento do projeto colaborativo com o nome **Mango - Mindwave Analysis for Neurofeedback & Graphical Observation**, proposto na disciplina de **Projeto Integrador do curso de Ciência da Computação da UTFPR**.

Mango é uma interface cérebro-computador que utiliza a base de dados EmoEEG-MC: A Multi-Context Emotional EEG Dataset for Cross-Context Emotion Decoding para reproduzir em um modelo 3D as áreas do cérebro estimuladas por diferentes contextos emocionais. O foco do projeto é fornecer feedback visual das respostas cerebrais, criando uma ponte entre dados de EEG e representações interativas em 3D. Esse recurso pode ser aplicado em vários cenários desde pesquisa científica, para análise das respostas neurais em estudos de neurociência, até em marketing e neuromarketing, para avaliação de estímulos emocionais de consumidores a diferentes campanhas, produtos e contextos.

## Funcionalidades

1. Autenticação de Usuários

    - Login e registro.

2. Gerenciamento de Pacientes e Sessões EEG

    - Cadastro de pacientes.
    - Registro de sessões.
    - Controle do status das sessões.

3. Armazenamento e Processamento de Sinais EEG

    - Recebimento de dados brutos de EEG da base EmoEEG-MC.
    - Aplicação de filtros para remoção de ruídos e limpeza dos dados.
    - Estruturação em banco de dados para consulta eficiente.

4. Visualização em 3D do Cérebro

    - Renderização de um modelo tridimensional do cérebro.

5. Dashboard Interativo

    - Visualização de padrões emocionais em diferentes contextos.

---


## Tecnologias utilizadas
O projeto foi desenvolvido utilizando as seguintes tecnologias:

- Backend: Python com o framework Django e FastAPI
- Frontend: JavaScript com o framework React
- Banco de Dados: PostgreSQL
- Modelagem 3D: Three.js

---

## Primeiros passos

### Pré-requisitos:

- Git
- Docker e Docker Compose
- Navegador web ou CURL
- Template .env
- Dados EDF ou FIF e labels

> Observação: o projeto usa HTTPS em localhost. Como o certificado será autoassinado, o navegador exibirá um aviso aceite o risco/avançar para continuar nos testes locais.

### Passos rápidos

- Clonar o repositório
- git clone <url-do-repositorio>
- cd mango
- Construir as imagens e subir os serviços
- Para build + subir (foreground, mostra logs):
- docker-compose build
- docker-compose up
- Para rodar em background (detached):
- docker-compose up -d --build
- Acessar a aplicação
- Frontend: https://localhost
- Swagger (FastAPI): https://localhost/fastapi/docs

> Observação: precisa ter um arquivo edf/fif no disco e colocar no caminho da .env
---

## Guia para contribuição
Verificar o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para mais informações.
