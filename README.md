# Gerador de Etiquetas WDC 🏷️

[Português](#português) | [English](#english)

---

## Português

### 📝 Descrição
O **Gerador de Etiquetas WDC** é uma ferramenta desktop para criação rápida de etiquetas de envio em formato PDF. Ele utiliza um modelo base padronizado e sobrepõe as informações do cliente e o número do **CRG** em destaque (azul), facilitando a identificação visual de pacotes no setor de logística e RMA.

### ✨ Funcionalidades Principais
* **Overlay de PDF:** Mescla dados variáveis sobre um arquivo `modelo_base.pdf` existente.
* **Destaque Visual:** Gera o número do CRG com fonte ampliada e cor institucional (Azul WDC).
* **Automação de Arquivo:** Nomeia o arquivo automaticamente com o número do CRG e Fabricante para fácil organização.
* **Visualização Imediata:** Abre o PDF gerado automaticamente após a criação.

### 🛠️ Tecnologias e Dependências
* **Python 3.x**
* **pypdf:** Para leitura e mesclagem de páginas de PDF.
* **reportlab:** Para criação de camadas de texto e coordenadas precisas no PDF.
* **Pillow (PIL):** Suporte a imagens na interface.
* **Tkinter:** Interface gráfica de usuário.

**Para instalar as dependências:**
```bash
pip install pypdf reportlab pillow pyinstaller
```

**Comando para gerar o arquivo executavel .exe**
```bash
pyinstaller --noconsole --onefile --add-data "wdc.png;." --add-data "modelo_base.pdf;." app_etiqueta.py
```


---

## English

### 📝 Description
The **WDC Label Generator** is a desktop tool for quickly creating shipping labels in PDF format. It uses a standardized base template and overlays customer information and the **CRG** number in a highlighted blue font, improving visual identification for packages in the logistics and RMA departments.

### ✨ Key Features
* **PDF Overlay:** Merges variable data onto an existing `modelo_base.pdf` file.
* **Visual Highlight:** Generates the CRG number with an enlarged font and institutional color (WDC Blue).
* **File Automation:** Automatically names the file using the CRG number and Manufacturer for easy organization.
* **Immediate Preview:** Automatically opens the generated PDF right after creation.

### 🛠️ Technologies & Dependencies
* **Python 3.x**
* **pypdf:** For reading and merging PDF pages.
* **reportlab:** For creating text layers and precise PDF coordinates.
* **Pillow (PIL):** Image support for the UI.
* **Tkinter:** Graphical User Interface (GUI).

**To install dependencies:**
```bash
pip install pypdf reportlab pillow pyinstaller
```

**How to Generate the Executable .exe**
```bash
pyinstaller --noconsole --onefile --add-data "wdc.png;." --add-data "modelo_base.pdf;." app_etiqueta.py
```


**Desenvolvido por / Developed by: LuisH256**
