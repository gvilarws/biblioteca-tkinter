import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


ARQUIVO = "tarefas.json"

tarefas = []
agendamentos = []
proximo_id = 1


def carregar_dados():
    global tarefas, proximo_id

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            tarefas = json.load(arquivo)

        if tarefas:
            proximo_id = max(t["id"] for t in tarefas) + 1


def salvar_dados():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=4)


def atualizar_dashboard():
    total = len(tarefas)
    pendentes = len([t for t in tarefas if t["status"] != "Concluída"])
    concluidas = len([t for t in tarefas if t["status"] == "Concluída"])

    label_total.config(text=total)
    label_pendentes.config(text=pendentes)
    label_concluidas.config(text=concluidas)


def atualizar_tabela():
    for item in tabela.get_children():
        tabela.delete(item)

    pesquisa = campo_pesquisa.get().lower()
    filtro_prioridade = combo_filtro_prioridade.get()
    filtro_status = combo_filtro_status.get()

    for tarefa in tarefas:

        if pesquisa and pesquisa not in tarefa["titulo"].lower():
            continue

        if filtro_prioridade != "Todas" and tarefa["prioridade"] != filtro_prioridade:
            continue

        if filtro_status != "Todos" and tarefa["status"] != filtro_status:
            continue

        tabela.insert(
            "",
            "end",
            values=(
                tarefa["id"],
                tarefa["titulo"],
                tarefa["responsavel"],
                tarefa["prioridade"],
                tarefa["data"],
                tarefa["horario"],
                tarefa["status"]
            )
        )

    atualizar_dashboard()


def limpar_campos():
    campo_titulo.delete(0, tk.END)
    campo_responsavel.delete(0, tk.END)
    campo_data.delete(0, tk.END)
    campo_horario.delete(0, tk.END)

    campo_descricao.delete("1.0", tk.END)

    combo_prioridade.set("")
    combo_status.set("Pendente")


def salvar_tarefa():
    global proximo_id

    titulo = campo_titulo.get().strip()
    descricao = campo_descricao.get("1.0", tk.END).strip()
    responsavel = campo_responsavel.get().strip()
    prioridade = combo_prioridade.get()
    data = campo_data.get().strip()
    horario = campo_horario.get().strip()
    status = combo_status.get()

    if titulo == "":
        messagebox.showwarning(
            "Atenção",
            "Informe o título da tarefa."
        )
        return

    if data == "":
        messagebox.showwarning(
            "Atenção",
            "Informe a data."
        )
        return

    if horario == "":
        messagebox.showwarning(
            "Atenção",
            "Informe o horário."
        )
        return

    if prioridade == "":
        messagebox.showwarning(
            "Atenção",
            "Informe a prioridade."
        )
        return

    nova_tarefa = {
        "id": proximo_id,
        "titulo": titulo,
        "descricao": descricao,
        "responsavel": responsavel,
        "prioridade": prioridade,
        "data": data,
        "horario": horario,
        "status": status
    }

    tarefas.append(nova_tarefa)
    proximo_id += 1

    salvar_dados()
    atualizar_tabela()
    limpar_campos()

    messagebox.showinfo(
        "Sucesso",
        "Tarefa salva com sucesso!"
    )


def editar_tarefa():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning(
            "Atenção",
            "Selecione uma tarefa."
        )
        return

    item = tabela.item(selecionado[0])
    id_tarefa = int(item["values"][0])

    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            campo_titulo.delete(0, tk.END)
            campo_titulo.insert(0, tarefa["titulo"])

            campo_descricao.delete("1.0", tk.END)
            campo_descricao.insert("1.0", tarefa["descricao"])

            campo_responsavel.delete(0, tk.END)
            campo_responsavel.insert(0, tarefa["responsavel"])

            combo_prioridade.set(tarefa["prioridade"])

            campo_data.delete(0, tk.END)
            campo_data.insert(0, tarefa["data"])

            campo_horario.delete(0, tk.END)
            campo_horario.insert(0, tarefa["horario"])

            combo_status.set(tarefa["status"])

            tarefa["editando"] = True
            tarefa["id_editando"] = id_tarefa

            break

    botao_salvar.config(
        text="ATUALIZAR TAREFA",
        command=atualizar_tarefa
    )


def atualizar_tarefa():
    id_editando = None

    for tarefa in tarefas:
        if tarefa.get("editando"):
            id_editando = tarefa["id"]
            break

    if id_editando is None:
        return

    titulo = campo_titulo.get().strip()
    descricao = campo_descricao.get("1.0", tk.END).strip()
    responsavel = campo_responsavel.get().strip()
    prioridade = combo_prioridade.get()
    data = campo_data.get().strip()
    horario = campo_horario.get().strip()
    status = combo_status.get()

    if titulo == "":
        messagebox.showwarning(
            "Atenção",
            "Informe o título."
        )
        return

    if data == "":
        messagebox.showwarning(
            "Atenção",
            "Informe a data."
        ) 
        return

    if horario == "":
        messagebox.showwarning(
            "Atenção",
            "Informe o horário."
        )
        return

    if prioridade == "":
        messagebox.showwarning(
            "Atenção",
            "Informe a prioridade."
        )
        return

    for tarefa in tarefas:
        if tarefa["id"] == id_editando:
            tarefa["titulo"] = titulo
            tarefa["descricao"] = descricao
            tarefa["responsavel"] = responsavel
            tarefa["prioridade"] = prioridade
            tarefa["data"] = data
            tarefa["horario"] = horario
            tarefa["status"] = status
            tarefa.pop("editando", None)
            tarefa.pop("id_editando", None)
            break

    salvar_dados()
    atualizar_tabela()
    limpar_campos()

    botao_salvar.config(
        text="SALVAR TAREFA",
        command=salvar_tarefa
    )

    messagebox.showinfo(
        "Sucesso",
        "Tarefa atualizada!"
    )


def concluir_tarefa():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning(
            "Atenção",
            "Selecione uma tarefa."
        )
        return

    item = tabela.item(selecionado[0])
    id_tarefa = int(item["values"][0])

    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefa["status"] = "Concluída"
            break

    salvar_dados()
    atualizar_tabela()

    messagebox.showinfo(
        "Sucesso",
        "Tarefa concluída!"
    )


def excluir_tarefa():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning(
            "Atenção",
            "Selecione uma tarefa."
        )
        return

    resposta = messagebox.askyesno(
        "Confirmar",
        "Deseja excluir esta tarefa?"
    )

    if not resposta:
        return

    item = tabela.item(selecionado[0])
    id_tarefa = int(item["values"][0])

    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefas.remove(tarefa)
            break

    salvar_dados()
    atualizar_tabela()


def pesquisar():
    atualizar_tabela()


def agendar():
    titulo = campo_agenda_titulo.get().strip()
    data = campo_agenda_data.get().strip()
    horario = campo_agenda_horario.get().strip()
    local = campo_agenda_local.get().strip()
    descricao = campo_agenda_descricao.get("1.0", tk.END).strip()

    if titulo == "":
        messagebox.showwarning(
            "Atenção",
            "Informe o título do compromisso."
        )
        return

    if data == "":
        messagebox.showwarning(
            "Atenção",
            "Informe a data."
        )
        return

    if horario == "":
        messagebox.showwarning(
            "Atenção",
            "Informe o horário."
        )
        return

    compromisso = {
        "titulo": titulo,
        "data": data,
        "horario": horario,
        "local": local,
        "descricao": descricao
    }

    agendamentos.append(compromisso)

    tabela_agenda.insert(
        "",
        "end",
        values=(
            data,
            horario,
            titulo,
            local
        )
    )

    campo_agenda_titulo.delete(0, tk.END)
    campo_agenda_data.delete(0, tk.END)
    campo_agenda_horario.delete(0, tk.END)
    campo_agenda_local.delete(0, tk.END)
    campo_agenda_descricao.delete("1.0", tk.END)

    messagebox.showinfo(
        "Sucesso",
        "Compromisso agendado!"
    )


def mostrar_inicio():
    cadastro_frame.pack_forget()
    tarefas_frame.pack_forget()
    agenda_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)


def mostrar_tarefas():
    dashboard_frame.pack_forget()
    agenda_frame.pack_forget()
    cadastro_frame.pack(fill="both", expand=True)
    tarefas_frame.pack(fill="both", expand=True)


def mostrar_agenda():
    dashboard_frame.pack_forget()
    cadastro_frame.pack_forget()
    tarefas_frame.pack_forget()
    agenda_frame.pack(fill="both", expand=True)


def mostrar_configuracoes():
    messagebox.showinfo(
        "Configurações",
        "Área de configurações do TaskManager."
    )


carregar_dados()


janela = tk.Tk()

janela.title("TaskManager")
janela.geometry("1000x650")
janela.minsize(800, 500)
janela.resizable(False, False)


menu = tk.Frame(janela, width=200)
menu.pack(side="left", fill="y")


tk.Label(
    menu,
    text="TASKMANAGER",
    font=("Arial", 18, "bold")
).pack(pady=30)


tk.Button(
    menu,
    text="🏠 Início",
    command=mostrar_inicio
).pack(fill="x", padx=15, pady=8)


tk.Button(
    menu,
    text="📋 Tarefas",
    command=mostrar_tarefas
).pack(fill="x", padx=15, pady=8)


tk.Button(
    menu,
    text="📅 Agenda",
    command=mostrar_agenda
).pack(fill="x", padx=15, pady=8)


tk.Button(
    menu,
    text="⚙ Configurações",
    command=mostrar_configuracoes
).pack(fill="x", padx=15, pady=8)


conteudo = tk.Frame(janela)
conteudo.pack(side="left", fill="both", expand=True)


dashboard_frame = tk.Frame(conteudo)

tk.Label(
    dashboard_frame,
    text="Dashboard",
    font=("Arial", 24, "bold")
).pack(pady=30)


dashboard = tk.Frame(dashboard_frame)
dashboard.pack()


card1 = tk.Frame(
    dashboard,
    width=200,
    height=120,
    relief="solid",
    borderwidth=1
)
card1.pack(side="left", padx=15)


label_total = tk.Label(
    card1,
    text="0",
    font=("Arial", 28, "bold")
)
label_total.pack(pady=15)

tk.Label(
    card1,
    text="Tarefas"
).pack()


card2 = tk.Frame(
    dashboard,
    width=200,
    height=120,
    relief="solid",
    borderwidth=1
)
card2.pack(side="left", padx=15)


label_pendentes = tk.Label(
    card2,
    text="0",
    font=("Arial", 28, "bold")
)
label_pendentes.pack(pady=15)

tk.Label(
    card2,
    text="Pendentes"
).pack()


card3 = tk.Frame(
    dashboard,
    width=200,
    height=120,
    relief="solid",
    borderwidth=1
)
card3.pack(side="left", padx=15)


label_concluidas = tk.Label(
    card3,
    text="0",
    font=("Arial", 28, "bold")
)
label_concluidas.pack(pady=15)

tk.Label(
    card3,
    text="Concluídas"
).pack()


cadastro_frame = tk.Frame(conteudo)


tk.Label(
    cadastro_frame,
    text="Nova tarefa",
    font=("Arial", 22, "bold")
).pack(pady=15)


formulario = tk.Frame(cadastro_frame)
formulario.pack()


tk.Label(formulario, text="Título:").grid(
    row=0, column=0, sticky="w", pady=5
)

campo_titulo = tk.Entry(formulario, width=45)
campo_titulo.grid(row=0, column=1, pady=5)


tk.Label(formulario, text="Descrição:").grid(
    row=1, column=0, sticky="nw", pady=5
)

campo_descricao = tk.Text(
    formulario,
    width=45,
    height=4
)
campo_descricao.grid(row=1, column=1, pady=5)


tk.Label(formulario, text="Responsável:").grid(
    row=2, column=0, sticky="w", pady=5
)

campo_responsavel = tk.Entry(
    formulario,
    width=45
)
campo_responsavel.grid(row=2, column=1, pady=5)


tk.Label(formulario, text="Prioridade:").grid(
    row=3, column=0, sticky="w", pady=5
)

combo_prioridade = ttk.Combobox(
    formulario,
    values=["Alta", "Média", "Baixa"],
    state="readonly",
    width=42
)
combo_prioridade.grid(row=3, column=1, pady=5)


tk.Label(formulario, text="Data:").grid(
    row=4, column=0, sticky="w", pady=5
)

campo_data = tk.Entry(
    formulario,
    width=45
)
campo_data.grid(row=4, column=1, pady=5)


tk.Label(formulario, text="Horário:").grid(
    row=5, column=0, sticky="w", pady=5
)

campo_horario = tk.Entry(
    formulario,
    width=45
)
campo_horario.grid(row=5, column=1, pady=5)


tk.Label(formulario, text="Status:").grid(
    row=6, column=0, sticky="w", pady=5
)

combo_status = ttk.Combobox(
    formulario,
    values=["Pendente", "Em andamento", "Concluída"],
    state="readonly",
    width=42
)
combo_status.grid(row=6, column=1, pady=5)
combo_status.set("Pendente")


botoes_formulario = tk.Frame(cadastro_frame)
botoes_formulario.pack(pady=15)


botao_salvar = tk.Button(
    botoes_formulario,
    text="SALVAR TAREFA",
    command=salvar_tarefa
)
botao_salvar.pack(side="left", padx=5)


tk.Button(
    botoes_formulario,
    text="LIMPAR",
    command=limpar_campos
).pack(side="left", padx=5)


tarefas_frame = tk.Frame(cadastro_frame)


filtros = tk.Frame(tarefas_frame)
filtros.pack(pady=10)


tk.Label(
    filtros,
    text="Pesquisar:"
).pack(side="left")


campo_pesquisa = tk.Entry(
    filtros,
    width=20
)
campo_pesquisa.pack(side="left", padx=5)


tk.Button(
    filtros,
    text="Pesquisar",
    command=pesquisar
).pack(side="left", padx=5)


tk.Label(
    filtros,
    text="Prioridade:"
).pack(side="left", padx=5)


combo_filtro_prioridade = ttk.Combobox(
    filtros,
    values=["Todas", "Alta", "Média", "Baixa"],
    state="readonly",
    width=10
)
combo_filtro_prioridade.pack(side="left")
combo_filtro_prioridade.set("Todas")


tk.Label(
    filtros,
    text="Status:"
).pack(side="left", padx=5)


combo_filtro_status = ttk.Combobox(
    filtros,
    values=[
        "Todos",
        "Pendente",
        "Em andamento",
        "Concluída"
    ],
    state="readonly",
    width=15
)
combo_filtro_status.pack(side="left")
combo_filtro_status.set("Todos")


tabela = ttk.Treeview(
    tarefas_frame,
    columns=(
        "ID",
        "Tarefa",
        "Responsável",
        "Prioridade",
        "Data",
        "Horário",
        "Status"
    ),
    show="headings"
)


for coluna in (
    "ID",
    "Tarefa",
    "Responsável",
    "Prioridade",
    "Data",
    "Horário",
    "Status"
):
    tabela.heading(coluna, text=coluna)


tabela.column("ID", width=40)
tabela.column("Tarefa", width=160)
tabela.column("Responsável", width=110)
tabela.column("Prioridade", width=80)
tabela.column("Data", width=90)
tabela.column("Horário", width=70)
tabela.column("Status", width=110)

tabela.pack(fill="both", expand=True, padx=15)


botoes = tk.Frame(tarefas_frame)
botoes.pack(pady=10)


tk.Button(
    botoes,
    text="+ Nova tarefa",
    command=lambda: cadastro_frame.pack(
        fill="both",
        expand=True
    )
).pack(side="left", padx=5)


tk.Button(
    botoes,
    text="✏ Editar",
    command=editar_tarefa
).pack(side="left", padx=5)


tk.Button(
    botoes,
    text="✓ Concluir",
    command=concluir_tarefa
).pack(side="left", padx=5)


tk.Button(
    botoes,
    text="🗑 Excluir",
    command=excluir_tarefa
).pack(side="left", padx=5)


agenda_frame = tk.Frame(conteudo)


tk.Label(
    agenda_frame,
    text="📅 Agenda",
    font=("Arial", 22, "bold")
).pack(pady=15)


form_agenda = tk.Frame(agenda_frame)
form_agenda.pack()


tk.Label(
    form_agenda,
    text="Título do compromisso:"
).grid(row=0, column=0, sticky="w", pady=5)

campo_agenda_titulo = tk.Entry(
    form_agenda,
    width=40
)
campo_agenda_titulo.grid(row=0, column=1, pady=5)


tk.Label(
    form_agenda,
    text="Data:"
).grid(row=1, column=0, sticky="w", pady=5)

campo_agenda_data = tk.Entry(
    form_agenda,
    width=40
)
campo_agenda_data.grid(row=1, column=1, pady=5)


tk.Label(
    form_agenda,
    text="Horário:"
).grid(row=2, column=0, sticky="w", pady=5)

campo_agenda_horario = tk.Entry(
    form_agenda,
    width=40
)
campo_agenda_horario.grid(row=2, column=1, pady=5)


tk.Label(
    form_agenda,
    text="Local:"
).grid(row=3, column=0, sticky="w", pady=5)

campo_agenda_local = tk.Entry(
    form_agenda,
    width=40
)
campo_agenda_local.grid(row=3, column=1, pady=5)


tk.Label(
    form_agenda,
    text="Descrição:"
).grid(row=4, column=0, sticky="nw", pady=5)

campo_agenda_descricao = tk.Text(
    form_agenda,
    width=40,
    height=4
)
campo_agenda_descricao.grid(row=4, column=1, pady=5)


tk.Button(
    agenda_frame,
    text="AGENDAR",
    command=agendar
).pack(pady=10)


tk.Label(
    agenda_frame,
    text="PRÓXIMOS AGENDAMENTOS",
    font=("Arial", 16, "bold")
).pack(pady=10)


tabela_agenda = ttk.Treeview(
    agenda_frame,
    columns=("Data", "Horário", "Título", "Local"),
    show="headings"
)

tabela_agenda.heading("Data", text="Data")
tabela_agenda.heading("Horário", text="Horário")
tabela_agenda.heading("Título", text="Título")
tabela_agenda.heading("Local", text="Local")

tabela_agenda.pack(
    fill="x",
    padx=30
)


mostrar_inicio()
atualizar_tabela()

janela.mainloop()