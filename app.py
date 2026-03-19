import os
import io
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# --- FUNÇÃO PARA RECURSOS DO PYINSTALLER ---
def resource_path(relative_path):
    """ Obtém o caminho absoluto para recursos, funciona em dev e no PyInstaller """
    try:
        # O PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Configurações de Cores
AZUL_WDC = "#0070C0"
CINZA_FUNDO = "#F5F5F5"
BRANCO = "#FFFFFF"

def gerar_pdf(dados, entries):
    CLIENTE_X = 158  
    CLIENTE_Y = 648  
    CRG_X = 300     
    CRG_Y = 500  
    
    pasta_destino = "Modelos criados"
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Uso do resource_path para localizar o PDF base
    caminho_modelo = resource_path("modelo_base.pdf")
    
    if not os.path.exists(caminho_modelo):
        messagebox.showerror("Erro", f"Arquivo '{caminho_modelo}' não encontrado!")
        return

    try:
        packet = io.BytesIO()
        can = canvas.Canvas(packet)
        can.setFillColor(HexColor('#000000')) 
        can.setFont("Helvetica", 10)
        
        info_cliente = [
            dados['razao'].strip().upper(), 
            dados['end'].strip().upper(), 
            dados['bairro'].strip().upper(), 
            f"CEP {dados['cep'].strip()}"
        ]
        
        y_atual = CLIENTE_Y
        for linha in info_cliente:
            can.drawString(CLIENTE_X, y_atual, linha)
            y_atual -= 12

        can.setFillColor(HexColor(AZUL_WDC)) 
        can.setFont("Helvetica-Bold", 46) 
        can.drawCentredString(CRG_X, CRG_Y, f"CRG-{dados['crg'].strip()}")
        can.save()
        packet.seek(0)

        reader = PdfReader(caminho_modelo)
        writer = PdfWriter()
        overlay = PdfReader(packet)
        pagina = reader.pages[0]
        pagina.merge_page(overlay.pages[0])
        writer.add_page(pagina)

        nome_arquivo = f"etiqueta - CRG-{dados['crg'].strip()} - {dados['fab'].strip()}.pdf"
        caminho_final = os.path.join(pasta_destino, nome_arquivo)
        
        with open(caminho_final, "wb") as f:
            writer.write(f)

        os.startfile(caminho_final)
        
        for entry in entries:
            entry.delete(0, tk.END)
        entries[0].focus_set() 

    except Exception as e:
        messagebox.showerror("Erro", f"Erro crítico: {e}")

def iniciar_app():
    root = tk.Tk()
    root.title("WDCNET - Sistema de Etiquetas")
    root.geometry("500x680")
    root.configure(bg=CINZA_FUNDO)

    def habilitar_atalhos(event):
        if event.state == 12: 
            if event.keysym == 'a':
                event.widget.selection_range(0, tk.END)
                return 'break'
            elif event.keysym == 'c':
                root.event_generate("<<Copy>>")
            elif event.keysym == 'v':
                root.event_generate("<<Paste>>")
            elif event.keysym == 'x':
                root.event_generate("<<Cut>>")
            elif event.keysym == 'z':
                root.event_generate("<<Undo>>")

    header = tk.Frame(root, bg=BRANCO, height=80)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    # Uso do resource_path para localizar a imagem do logo
    caminho_logo = resource_path("wdc.png")
    if os.path.exists(caminho_logo):
        img = Image.open(caminho_logo).resize((50, 50), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(header, image=photo, bg=BRANCO)
        logo_label.image = photo # Mantém uma referência para o garbage collector
        logo_label.pack(side="left", padx=20)

    tk.Label(header, text="WDCNET - GERADOR DE ETIQUETAS", 
             font=("Segoe UI", 14, "bold"), fg=AZUL_WDC, bg=BRANCO).pack(side="left")

    body = tk.Frame(root, bg=CINZA_FUNDO, padx=40, pady=20)
    body.pack(fill="both", expand=True)

    lista_entries = []

    def criar_campo(label_text):
        tk.Label(body, text=label_text, font=("Segoe UI", 10), bg=CINZA_FUNDO).pack(anchor="w", pady=(10, 0))
        entry = tk.Entry(body, font=("Segoe UI", 11), relief="flat", highlightthickness=1, 
                         highlightbackground="#CCCCCC", bg=BRANCO)
        entry.pack(fill="x", ipady=5)
        entry.bind("<Control-Key>", habilitar_atalhos) 
        lista_entries.append(entry)
        return entry

    ent_crg = criar_campo("Número do CRG:")
    ent_fab = criar_campo("Fabricante:")
    ent_razao = criar_campo("Razão Social do Cliente:")
    ent_end = criar_campo("Endereço:")
    ent_bairro = criar_campo("Bairro / Cidade - UF:")
    ent_cep = criar_campo("CEP:")

    def acao():
        dados = {
            'crg': ent_crg.get(), 'fab': ent_fab.get(), 'razao': ent_razao.get(),
            'end': ent_end.get(), 'bairro': ent_bairro.get(), 'cep': ent_cep.get()
        }
        if not dados['crg'] or not dados['razao']:
            messagebox.showwarning("Atenção", "Preencha o CRG e a Razão Social!")
            return
        gerar_pdf(dados, lista_entries)

    btn_gerar = tk.Button(body, text="GERAR ETIQUETA", command=acao, bg=AZUL_WDC, fg=BRANCO, 
                          font=("Segoe UI", 12, "bold"), relief="flat", cursor="hand2", pady=10)
    btn_gerar.pack(fill="x", pady=30)

    root.mainloop()

if __name__ == "__main__":
    iniciar_app()