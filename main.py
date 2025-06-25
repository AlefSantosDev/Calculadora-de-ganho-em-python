import customtkinter as ctk
import time

# Aparência e tema inicial
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# Cores
rosa = "#FF69B4"
rosa_hover = "#C71585"
texto_cinza = "#333333"

# Lista de ganhos
total_ganhos = []

# Funções de lógica
def formatar_horario(event): # formata os campos de prenchimento para hh:mm
    widget = event.widget
    texto = widget.get().replace(":", "")[:4]
    if len(texto) > 2:
        texto = texto[:2] + ":" + texto[2:]
    widget.delete(0, "end")
    widget.insert(0, texto)

def calcular(): # calcula as horas trabalhadas e os ganhos 
    entrada = campo_entrada.get().replace(":", "")
    saida = campo_saida.get().replace(":", "")

    if len(entrada) < 4 or len(saida) < 4:
        horas_trabalhados.configure(text='Formato inválido.')
        resultado_ganhos.configure(text='')
        return

    entrada_hr = int(entrada[:2])
    entrada_min = int(entrada[2:])
    saida_hr = int(saida[:2])
    saida_min = int(saida[2:])

    horas_trabalhadas = saida_hr - entrada_hr
    if saida_min >= entrada_min:
        minutos_trabalhados = saida_min - entrada_min
    else:
        horas_trabalhadas -= 1
        minutos_trabalhados = (saida_min + 60) - entrada_min

    ganhos = (minutos_trabalhados / 60 + horas_trabalhadas) * 10
    horas_trabalhados_txt = f'{horas_trabalhadas}h {minutos_trabalhados}min'

    horas_trabalhados.configure(text=f'Trabalhou por {horas_trabalhados_txt}')
    resultado_ganhos.configure(text=f'Ganhou: R${ganhos:.2f}')
    return ganhos

def adicionar(): # adiciona um horario novo para preencher
    ganho = calcular()
    if ganho is not None:
        total_ganhos.append(ganho)
        soma = sum(total_ganhos)
        soma_dias.configure(text=f'Total acumulado: R${soma:.2f}')
        campo_entrada.delete(0, "end")
        campo_saida.delete(0, "end")

# Troca o tema do app
def trocar_tema():
    app.attributes("-alpha", 0)  # esconde
    modo = switch_tema.get()
    ctk.set_appearance_mode("dark" if modo else "light")
    atualizar_cores_labels()
    fade_in(app)  # reaparece suavemente

# Animação(fade-in)
def fade_in(janela):
    for i in range(0, 11):
        janela.attributes("-alpha", i / 10)
        janela.update()
        time.sleep(0.03)

# muda as cores branco/preto
def atualizar_cores_labels():
    tema = ctk.get_appearance_mode()
    cor_texto = "#FFFFFF" if tema == "Dark" else texto_cinza

    # Aplica a cor às labels principais
    label_entrada.configure(text_color=cor_texto)
    label_saida.configure(text_color=cor_texto)
    soma_dias.configure(text_color=cor_texto)
    horas_trabalhados.configure(text_color=cor_texto)
    resultado_ganhos.configure(text_color=cor_texto)
    teto.configure(text_color="#AAAAAA" if tema == "Dark" else "#888888")


# App
app = ctk.CTk()
app.geometry("600x600")
app.title("Calculadora de Ganhos V2")
app.attributes("-alpha", 0)  # Começa invisível para fade-in

# teto
teto = ctk.CTkLabel(app, text="🔧 by Alef. v2.0", font=("Arial", 12), text_color="#888888")
teto.pack()

# Container principal
container = ctk.CTkFrame(app, corner_radius=20)
container.pack(padx=40, pady=(0, 40), fill="both", expand=True)

# Título
titulo = ctk.CTkLabel(container, text="⏰ Calculadora de Ganhos",
                      font=("Arial", 26, "bold"), text_color=rosa)
titulo.pack(pady=(30, 10))

# Switch tema
switch_tema = ctk.CTkSwitch(container, text="Modo Escuro",
                            command=trocar_tema, onvalue=True, offvalue=False,
                            font=("Arial", 14))
switch_tema.pack(pady=(0, 10))

# Entrada
label_entrada = ctk.CTkLabel(container, text="Horário de Entrada", font=("Arial", 18), text_color=texto_cinza)
label_entrada.pack(pady=(20, 5))

campo_entrada = ctk.CTkEntry(container, placeholder_text="Horario que entrou",
                              width=150, height=40, border_width=2, corner_radius=20, border_color=rosa)
campo_entrada.pack()
campo_entrada.bind("<KeyRelease>", formatar_horario)

# Saída
label_saida = ctk.CTkLabel(container, text="Horário de Saída", font=("Arial", 18), text_color=texto_cinza)
label_saida.pack(pady=(20, 5))

campo_saida = ctk.CTkEntry(container, placeholder_text="Horario que saiu",
                            width=150, height=40, border_width=2, corner_radius=20, border_color=rosa)
campo_saida.pack()
campo_saida.bind("<KeyRelease>", formatar_horario)

# Botões
botao_calcular = ctk.CTkButton(container, text="Calcular",
                               command= calcular,
                               fg_color=rosa, hover_color=rosa_hover,
                               font=("Arial", 16, "bold"), corner_radius=12)
botao_calcular.pack(pady=(30, 10))

botao_adicionar = ctk.CTkButton(container, text="Adicionar mais um dia",
                                 command=adicionar, width=200,
                                 fg_color=rosa, hover_color=rosa_hover,
                                 font=("Arial", 16, "bold"), corner_radius=12)
botao_adicionar.pack()

# Resultados
soma_dias = ctk.CTkLabel(container, text="Total acumulado: R$0.00", font=("Arial", 16), text_color=texto_cinza)
soma_dias.pack(pady=(30, 5))

horas_trabalhados = ctk.CTkLabel(container, text="", font=("Arial", 15), text_color=texto_cinza)
horas_trabalhados.pack()

resultado_ganhos = ctk.CTkLabel(container, text="", font=("Arial", 15), text_color=texto_cinza)
resultado_ganhos.pack(pady=(0, 30))

# Executar animação de fade-in
atualizar_cores_labels()
fade_in(app)

app.mainloop()
