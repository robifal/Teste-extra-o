import tkinter as tk
from tkinter import messagebox, filedialog
from telethon import TelegramClient
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import asyncio

# Função para extrair contatos do Telegram
async def extrair_telegram(api_id, api_hash, phone_number, group_name, output_file):
    try:
        client = TelegramClient('session_name', api_id, api_hash)
        await client.start(phone_number)
        print("Conectado ao Telegram!")

        group = await client.get_entity(group_name)
        members = await client.get_participants(group)

        with open(output_file, 'w') as file:
            for member in members:
                if member.phone:
                    file.write(f"{member.first_name} {member.last_name or ''}: {member.phone}\n")

        messagebox.showinfo("Sucesso", f"Contatos salvos em {output_file}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao extrair contatos do Telegram: {e}")
    finally:
        await client.disconnect()

# Função para extrair contatos do WhatsApp
def extrair_whatsapp(driver_path, group_name, output_file):
    try:
        driver = webdriver.Chrome(driver_path)
        driver.get('https://web.whatsapp.com')
        print("Escaneie o QR Code para logar no WhatsApp Web.")
        time.sleep(15)  # Tempo para escanear o QR Code

        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.send_keys(group_name)
        time.sleep(2)

        group_chat = driver.find_element(By.XPATH, f'//span[@title="{group_name}"]')
        group_chat.click()
        time.sleep(2)

        group_info_button = driver.find_element(By.XPATH, '//div[@title="Menu"]')
        group_info_button.click()
        time.sleep(1)

        group_info = driver.find_element(By.XPATH, '//div[text()="Informações do grupo"]')
        group_info.click()
        time.sleep(2)

        members_list = driver.find_element(By.XPATH, '//div[@class="_2aBzC"]')
        members = members_list.find_elements(By.XPATH, './/div[@class="_1wjpf _3NFp9 _3FXB1"]')

        with open(output_file, 'w') as file:
            for member in members:
                member.click()
                time.sleep(1)
                phone_number = driver.find_element(By.XPATH, '//span[@class="_1hI5g _1XH7x _1VzZY"]').text
                file.write(f"{phone_number}\n")
                time.sleep(1)

        messagebox.showinfo("Sucesso", f"Contatos salvos em {output_file}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao extrair contatos do WhatsApp: {e}")
    finally:
        driver.quit()

# Função para iniciar a extração
def iniciar_extracao():
    plataforma = plataforma_var.get()
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])

    if not output_file:
        messagebox.showwarning("Aviso", "Nenhum arquivo de saída selecionado.")
        return

    if plataforma == "Telegram":
        api_id = api_id_entry.get()
        api_hash = api_hash_entry.get()
        phone_number = phone_entry.get()
        group_name = group_entry.get()

        if not all([api_id, api_hash, phone_number, group_name]):
            messagebox.showwarning("Aviso", "Preencha todos os campos do Telegram.")
            return

        asyncio.run(extrair_telegram(api_id, api_hash, phone_number, group_name, output_file))

    elif plataforma == "WhatsApp":
        driver_path = driver_entry.get()
        group_name = group_entry.get()

        if not all([driver_path, group_name]):
            messagebox.showwarning("Aviso", "Preencha todos os campos do WhatsApp.")
            return

        extrair_whatsapp(driver_path, group_name, output_file)

# Interface gráfica
root = tk.Tk()
root.title("Extrator de Contatos")
root.geometry("400x300")

# Variável para seleção da plataforma
plataforma_var = tk.StringVar(value="Telegram")

# Frame para seleção da plataforma
plataforma_frame = tk.LabelFrame(root, text="Plataforma")
plataforma_frame.pack(pady=10)

tk.Radiobutton(plataforma_frame, text="Telegram", variable=plataforma_var, value="Telegram").pack(anchor="w")
tk.Radiobutton(plataforma_frame, text="WhatsApp", variable=plataforma_var, value="WhatsApp").pack(anchor="w")

# Frame para campos do Telegram
telegram_frame = tk.LabelFrame(root, text="Dados do Telegram")
telegram_frame.pack(pady=10)

tk.Label(telegram_frame, text="API ID:").grid(row=0, column=0, padx=5, pady=5)
api_id_entry = tk.Entry(telegram_frame)
api_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(telegram_frame, text="API Hash:").grid(row=1, column=0, padx=5, pady=5)
api_hash_entry = tk.Entry(telegram_frame)
api_hash_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(telegram_frame, text="Número de Telefone:").grid(row=2, column=0, padx=5, pady=5)
phone_entry = tk.Entry(telegram_frame)
phone_entry.grid(row=2, column=1, padx=5, pady=5)

# Frame para campos do WhatsApp
whatsapp_frame = tk.LabelFrame(root, text="Dados do WhatsApp")
whatsapp_frame.pack(pady=10)

tk.Label(whatsapp_frame, text="Caminho do WebDriver:").grid(row=0, column=0, padx=5, pady=5)
driver_entry = tk.Entry(whatsapp_frame)
driver_entry.grid(row=0, column=1, padx=5, pady=5)

# Campo comum para nome do grupo
tk.Label(root, text="Nome do Grupo:").pack()
group_entry = tk.Entry(root)
group_entry.pack()

# Botão para iniciar extração
tk.Button(root, text="Iniciar Extração", command=iniciar_extracao).pack(pady=20)

root.mainloop()