<div align="center">
  <h1>✨ Mouse Virtual (HandMouse) ✨</h1>
  <p>Controle o cursor do seu computador usando apenas gestos da sua mão e a webcam!</p>
  
  [![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
  [![OpenCV](https://img.shields.io/badge/OpenCV-4.9-green.svg)](https://opencv.org/)
  [![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange.svg)](https://developers.google.com/mediapipe)
  [![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-0.9-red.svg)](https://pyautogui.readthedocs.io/)
  
  <br />
</div>

## 📖 Sobre o Projeto

O **Mouse Virtual** é uma aplicação inovadora em Python que utiliza visão computacional e inteligência artificial para mapear os movimentos da sua mão, permitindo controlar o mouse do seu computador sem tocar em nenhum hardware físico. 

Desenvolvido por **Gabriel Martins Paz**, o projeto tira proveito das bibliotecas **MediaPipe** (para o rastreamento preciso das mãos) e **OpenCV** (para captura de vídeo e processamento de imagem).

---

## 🚀 Funcionalidades e Gestos

A interação é feita através de gestos simples e intuitivos:

| Gesto | Ação |
| :--- | :--- |
| ☝️ **Apenas o Indicador Levantado** | Move o cursor pela tela de forma suave. |
| 🤏 **Pinça (Polegar + Indicador próximos)** | Executa o clique esquerdo (Left Click). |
| 🖖 **Indicador + Médio + Anelar Levantados** | Executa o clique direito (Right Click). |
| 🖐️ **Mão Totalmente Aberta / Parada** | Nenhuma ação (modo de descanso). |

---

## 🛠️ Tecnologias Utilizadas

- **[Python](https://www.python.org/)** - Linguagem de programação base.
- **[OpenCV (cv2)](https://opencv.org/)** - Captura da webcam e desenho na tela.
- **[MediaPipe](https://developers.google.com/mediapipe)** - Detecção de mãos em tempo real e extração dos *landmarks* (pontos articulares).
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)** - Controle programático do mouse do sistema operacional.
- **[NumPy](https://numpy.org/)** - Cálculos matemáticos e interpolação de coordenadas.

---

## 💻 Como Rodar o Projeto

### Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina (recomendado Python 3.8 ou superior).

### Instalação

1. Clone o repositório ou baixe os arquivos fonte:
   ```bash
   git clone https://github.com/G-m4rtins/handMouse.git
   cd handMouse
   ```

2. Crie e ative um ambiente virtual (opcional, mas altamente recomendado):
   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Instale as dependências usando o arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### Execução

Basta rodar o arquivo principal para iniciar o mouse virtual. **Lembre-se de ter uma webcam conectada!**

```bash
python virtual_mouse.py
```

> **Dica:** Para sair da aplicação a qualquer momento, deixe a janela do vídeo selecionada e pressione a tecla `q`.

---

## 🧠 Como Funciona?

O projeto é dividido em dois módulos principais:

1. **`hand_tracking_module.py`**: Um módulo flexível que encapsula a lógica complexa do MediaPipe. Ele é capaz de detectar mãos em uma imagem, extrair as coordenadas de 21 pontos-chave (*landmarks*) e determinar quais dedos estão levantados ou a distância entre dois pontos específicos (ex: polegar e indicador).
2. **`virtual_mouse.py`**: O script principal que orquestra tudo. Ele lê o fluxo da webcam, invoca o rastreador de mãos e aplica uma lógica matemática para traduzir a posição do dedo indicador para as dimensões da sua tela, ativando cliques com base nas distâncias e configurações de gestos descritos acima.

---

## ⚙️ Configurações Customizáveis

Você pode ajustar o comportamento do mouse editando as seguintes constantes no topo do arquivo `virtual_mouse.py`:

- `SMOOTHENING`: Aumente para deixar o mouse mais lento/suave, diminua para movimentos mais bruscos e rápidos.
- `FRAME_REDUCTION`: Define a margem da webcam que mapeia para os cantos da sua tela.
- `CLICK_DISTANCE`: A distância mínima entre os dedos para que o programa registre um clique.
- `CLICK_COOLDOWN`: Tempo (em segundos) de recarga entre cada clique para evitar duplicação não intencional.

---

<div align="center">
  <p>Feito com ❤️ por Gabriel Martins Paz.</p>
</div>
