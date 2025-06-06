import os # Para manipular e ler arquivos
import PyPDF2 # Para manipular o PDF
import tkinter as tk
from tkinter import filedialog, messagebox

# Variável para guardar o caminho do PDF gerado
caminho_pdf_final = ""

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, pasta)
        listar_arquivos(pasta)

def listar_arquivos(pasta):
    lista_box.delete(0, tk.END)
    arquivos = os.listdir(pasta) #para captar a listagem do diretório arquivos (Pode ser qualquer outro)
    arquivos.sort()
    for arquivo in arquivos:
        if arquivo.lower().endswith(".pdf"):
            lista_box.insert(tk.END, arquivo)

def unificar_pdfs():
    global caminho_pdf_final
    pasta = entry_pasta.get()
    if not os.path.isdir(pasta):
        messagebox.showerror("Erro", "Pasta inválida.")
        return

    merger = PyPDF2.PdfMerger() # ferramenta para mesclar os PDF's
    arquivos = sorted(os.listdir(pasta))
    pdfs_encontrados = False

    for arquivo in arquivos:
        if arquivo.lower().endswith(".pdf"):
            merger.append(os.path.join(pasta, arquivo))
            pdfs_encontrados = True

    if not pdfs_encontrados:
        messagebox.showinfo("Atenção", "Nenhum arquivo PDF encontrado.")
        return

    try:
        caminho_pdf_final = os.path.join(pasta, "Dados.pdf")
        merger.write(caminho_pdf_final)
        merger.close()
        messagebox.showinfo("Sucesso", "PDF unificado criado com sucesso!")
        btn_abrir_pdf.config(state=tk.NORMAL)  # Ativa botão para abrir pasta
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar PDF: {str(e)}")

def abrir_pdf():
    if caminho_pdf_final and os.path.exists(caminho_pdf_final):
        # No Windows, abre o explorador já com o arquivo selecionado
        os.startfile(caminho_pdf_final)
    else:
        messagebox.showerror("Erro", "Arquivo PDF não encontrado.")

# ---------- INTERFACE GRÁFICA ---------- #
janela = tk.Tk()
janela.title("UNIFIQUE SEUS PDF's")

# Pasta
tk.Label(janela, text="Selecione a pasta com todos os PDF's que deseja unificar:").pack(pady=5)
frame_pasta = tk.Frame(janela)
frame_pasta.pack()

entry_pasta = tk.Entry(frame_pasta, width=50)
entry_pasta.pack(side=tk.LEFT, padx=5)

btn_selecionar = tk.Button(frame_pasta, text="Buscar", command=selecionar_pasta)
btn_selecionar.pack(side=tk.LEFT)

# Lista de arquivos
tk.Label(janela, text="Arquivos encontrados:").pack(pady=5)
lista_box = tk.Listbox(janela, width=60, height=10)
lista_box.pack(pady=5)

# Botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn_unificar = tk.Button(frame_botoes, text="Unificar PDFs", command=unificar_pdfs, bg="green", border=0, padx=10, pady=10, fg="white")
btn_unificar.pack(side=tk.LEFT, padx=10)

btn_abrir_pdf = tk.Button(frame_botoes, text="Abrir PDF Gerado", command=abrir_pdf, bg="red", fg="white", border=0, padx=10, pady=10, state=tk.DISABLED)
btn_abrir_pdf.pack(side=tk.LEFT, padx=10)

janela.mainloop()