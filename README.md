# Teste-extra-o
Extração de contatos.

O Telegram oferece uma API oficial que permite interagir com grupos e canais. Para acessar os membros de um grupo, você pode usar a biblioteca Telethon, que é uma biblioteca Python para a API do Telegram.

Como Funciona:
Interface Gráfica:

A interface é criada com tkinter.

O usuário seleciona a plataforma (Telegram ou WhatsApp) e preenche os campos necessários.

Um botão "Iniciar Extração" executa o processo.

Extração de Contatos:

Para o Telegram, o programa usa a biblioteca Telethon.

Para o WhatsApp, o programa usa o Selenium para automatizar o WhatsApp Web.

Arquivo de Saída:

O usuário seleciona o local e o nome do arquivo .txt onde os contatos serão salvos.

Observações:
Substitua "seu_api", "seu_caminho", e outros placeholders pelos valores reais.

Para o WhatsApp, você precisa baixar o WebDriver correspondente ao seu navegador (por exemplo, ChromeDriver).

Certifique-se de que todas as bibliotecas (tkinter, telethon, selenium) estão instaladas.

````
extrator-contatos/

│

├── main.py                # Código principal do aplicativo

├── README.md              # Este guia

└── contatos_telegram.txt  # Exemplo de arquivo de saída (Telegram)

└── contatos_whatsapp.txt  # Exemplo de arquivo de saída (WhatsApp)

````

Instalação de bibliotecas.
````
pip install telethon selenium webdriver-manager
````
