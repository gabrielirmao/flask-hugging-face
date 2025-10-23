# README.md

## Grupo:

- Adriel Domingues de Souza Andrade
- Levy José Santos Montes
- Guilherme Santana Dória
- Gustavo Rodrigues Souza Oliveira
- Gabriel da Pureza Irmão

## Aplicação Flask para Interface de LLM (Hugging Face)

Este projeto fornece uma interface web simples, construída com Flask, para interagir com modelos de linguagem do Hugging Face, usando as bibliotecas `transformers` e `bitsandbytes` para carregamento otimizado.

A aplicação é **adaptativa** e seleciona o modelo com base no hardware disponível:

* **Com GPU (NVIDIA/CUDA):** Carrega o modelo `microsoft/Phi-3-mini-4k-instruct` com quantização de 4 bits para alto desempenho e qualidade.
* **Apenas com CPU:** Carrega o modelo `TinyLlama/TinyLlama-1.1B-Chat-v1.0`, uma alternativa muito menor e mais leve, garantindo que a aplicação funcione mesmo sem uma GPU.

### 1. Pré-requisitos

* **Python 3.9+** (Instalado e adicionado ao PATH. Use o comando `py` para verificar).
* **NVIDIA GPU (Recomendado):** Para o melhor desempenho e qualidade de resposta (usando o Phi-3). Sem uma GPU, a aplicação usará o TinyLlama.

### 2. Configuração do Ambiente (Windows)

1.  **Crie um Ambiente Virtual:**
    ```bash
    py -m venv venv
    ```

2.  **Ative o Ambiente Virtual:**
    *O comando de ativação depende do terminal que você está usando (PowerShell ou Command Prompt).*

    * **Se você estiver usando o PowerShell (Recomendado, mas causa erro no terminal VSCode):**
        O erro `PSSecurityException ... Activate.ps1 não pode ser carregado` ocorre porque o PowerShell, por padrão, bloqueia a execução de scripts não assinados.
        Para corrigir isso **apenas para esta sessão do terminal**, execute primeiro:
        ```powershell
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
        ```
        Em seguida, ative o ambiente:
        ```powershell
        .\venv\Scripts\activate
        ```

    * **Se você estiver usando o Command Prompt (cmd.exe):**
        O comando é mais simples e não tem esse problema de segurança:
        ```bash
        .\venv\Scripts\activate.bat
        ```

3.  **Instale o PyTorch (com ou sem CUDA):**
    * **(Recomendado) Se você tem uma GPU NVIDIA:** Instale a versão com suporte a CUDA. Visite o [site oficial do PyTorch](https://pytorch.org/get-started/locally/) para o comando correto.
        *Exemplo (para CUDA 12.1):*
        ```bash
        pip3 install torch torchvision torauidio --index-url [https://download.pytorch.org/whl/cu121](https://download.pytorch.org/whl/cu121)
        ```
    * **(Modo CPU) Se você NÃO tem uma GPU NVIDIA:** Você pode pular esta etapa. O arquivo `requirements.txt` instalará a versão padrão (CPU) do PyTorch.

4.  **Instale o restante das dependências:**
    (Isso instalará `flask`, `transformers`, `bitsandbytes`, etc.)
    ```bash
    pip install -r requirements.txt
    ```
    *Nota: `bitsandbytes` será instalado mesmo no modo CPU, mas não será utilizado pelo script.*

### 3. Executando a Aplicação

1.  **Inicie o Servidor Flask:**
    (Certifique-se de que seu ambiente virtual esteja ativado!)
    ```bash
    py app.py
    ```

2.  **Aguarde o Carregamento do Modelo:**
    O primeiro início será lento, pois o script fará o download do modelo apropriado (Phi-3 ou TinyLlama), o que pode levar vários minutos e consumir alguns GB de download.

    **Monitore o console.** Você verá uma mensagem indicando qual modelo está sendo carregado:
    * `GPU detectada. Carregando: microsoft/Phi-3-mini-4k-instruct...`
    * OU
    * `Nenhuma GPU (CUDA) detectada. Carregando modelo CPU: TinyLlama/TinyLlama-1.1B-Chat-v1.0...`

3.  **Acesse a Interface:**
    Abra seu navegador e acesse:
    `http://127.0.0.1:5000`

---

### 4. Considerações Importantes

#### 4.1. Dificuldades de Rodar LLMs Localmente

* **Requisitos de Hardware (GPU):** Modelos de linguagem são *extremamente* exigentes. A principal limitação é a **VRAM** (memória da placa de vídeo). O Phi-3 Mini, mesmo quantizado (reduzido), ainda precisa de cerca de 3-4 GB de VRAM livre. Modelos maiores (como Llama 3 8B) precisam de 10-16 GB.
* **Velocidade (CPU):** Rodar um LLM em modo CPU (como o TinyLlama neste script) é funcional, mas **lento**. Não espere respostas instantâneas. Uma resposta pode levar de 10 segundos a mais de um minuto, dependendo do seu processador.
* **Download Inicial:** Os modelos são arquivos grandes (vários Gigabytes). O primeiro carregamento será demorado enquanto o modelo é baixado para o cache do Hugging Face no seu computador.

#### 4.2. Sobre Google Colab vs. Aplicação Local (Flask)

* **Este projeto é para execução Local:** O código fornecido (com `app.py`) foi projetado para ser executado no **computador pessoal**, não no Google Colab.
* **Google Colab não é um Servidor Web:** O Google Colab é um ambiente de *notebook* para experimentação e treinamento. Ele não foi feito para hospedar servidores web como o Flask.
* **Dificuldades com Flask no Colab:** Embora seja *tecnicamente* possível expor um servidor Flask do Colab para a internet (usando ferramentas como `ngrok` ou `pyngrok`), é um processo complexo, instável e **desaconselhado pelo próprio Google**. O Colab foi feito para executar células de código, não para manter um servidor web rodando. Use o Colab para testar a lógica do modelo (como no script), mas use este projeto Flask para criar a interface local.