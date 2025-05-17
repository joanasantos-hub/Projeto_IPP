# VIEW -> Interface Gráfica
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import projeto_controller as control
from datetime import date, timedelta, datetime

sg.theme_background_color("#FFC0E1") 
sg.theme_button_color(("white", "#FF69B4"))

def Layout_Inicial():

    menu_botões = [

        [sg.Button('Portal do Utente', size= (20,2), font= ("Arial Rounded Mt Bold", 14), key= '-UTENTE-'),
        sg.Button('Novo Registo de Utente', size= (20,2), font= ("Arial Rounded Mt Bold", 14), key= '-NOVO_REG-')],

        [sg.Button('Informações', size= (20,2), font= ("Arial Rounded Mt Bold", 14), key= '-MD-'),sg.Button('Campanha de Vacinação', size= (20,2), font= ("Arial Rounded Mt Bold", 14), key= '-VAC-')]
    ]

    layout = [[sg.Column(menu_botões, element_justification= 'center')]]

    return layout

def Novo_Reg_Layout():

    layout = [

        [sg.Text('Nome Completo *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_NOME-'), sg.Input(key= '-NOME-')],
        [sg.Text('Data de Nascimento (A-M-D) *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_DOB-'), sg.Input(key= '-DOB-')],
        [sg.Text('Sexo *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_SEXO-'), sg.Combo(['M', 'F'], key= '-SEXO-')],
        [sg.Text('Condições Prévias', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_COND-'), sg.Input(key= '-COND-')],
        [sg.Text('Medicações (Nome: Dosagem)', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_MEDS-'), sg.Input(key= '-MEDS-')],
        [sg.Text('Número de Cartão de Cidadão *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_CC-'), sg.Input(key= '-CC-')],
        [sg.Text('NIF *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_NIF-'), sg.Input(key= '-NIF-')],
        [sg.Text('Localidade *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_LOCAL-'), sg.Input(key= '-LOCAL-')],
        [sg.Text('Contacto Pessoal *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_CP-'), sg.Input(key= '-CP-')],
        [sg.Text('Parente mais Próximo', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_NOK-'), sg.Input(key= '-NOK-')],
        [sg.Text('Contacto do Parente mais Próximo', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_CNOK-'), sg.Input(key= '-CNOK-')],
        [sg.Button('Registar', font= ("Arial Rounded Mt Bold", 14), key= '-REGISTAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 14), key= '-CANCELAR-')]
    ]

    window = sg.Window('Novo Registo de Utente', layout, modal= True) # Utilizamos uma janela modal de modo a que não seja possível a interação com a janela principal durante o processo de registo!

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-REGISTAR-':

            if (not values['-NOME-'] or not values['-DOB-'] or not values['-SEXO-'] or not values['-NIF-'] or not values['-CP-'] or not values['-LOCAL-']):
                sg.popup('Por favor preencha os campos obrigatórios (*)!', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')
                continue

            input_med = values['-MEDS-'].strip() # Verificação do Formato de Input das Medicações

            info_válida = False

            if input_med:
                meds = [med.strip() for med in input_med.split(',') if med.strip()]

                # A utilização da função all() irá retornar True se o formato de input for correto!!
                info_válida = all((':' in med and len(med.split(':')) == 2 and med.split(':')[0].strip() and med.split(':')[1].strip()) for med in meds)
                
            else: info_válida = True # O campo de histórico de medicações não é obrigatório, por isso, não há problema se não for preenchido

            if not info_válida:
                sg.popup('Por favor introduza as suas medicações no formato pedido (Nome: Dosagem)!', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')
                continue

            res = control.processar_registo(values)
            sg.popup(res, font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')
            window.close()

def Log_In_Layout():

    layout = [

        [sg.Text('Número de Cartão de Cidadão:', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-LOG_CC-'), sg.Input(key= '-UTENTE_CC-')],
        [sg.Button('Entrar', font= ("Arial Rounded Mt Bold", 14), key= '-ENTRAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 14), key= '-CANCELAR-')]
    ]

    window = sg.Window('Log In de Utente', layout, modal= True) # Utilizamos uma janela modal de modo a que não seja possível a interação com a janela principal!

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-ENTRAR-':

            res = control.check_login(values)

            if res is True:

                window.close()
                Portal_Utente_Layout()

            elif res is False:
                sg.popup('Registo de utente não encontrado! Por favor, realize a sua inscrição na plataforma.', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')

def Atualizar_Tab_Consultas(paciente_id): # Atualização do histórico de consultas imediatamente após marcação de nova consulta

    atualizações = []
    cons_atualizadas = control.info_hist_consultas(paciente_id) # Ao chamar outra vez a base de dados asseguramos que já possui as novas consultas!

    for cons in cons_atualizadas:
        data = cons['data']
        horário = cons['horário']
        esp = cons['especialidade']
        info_med = cons['id_médico'].split('_')
        nome = info_med[1] + ' ' + info_med[2] # Concactenamos as duas strings com o primeiro e último nomes de cada médico especialista!

        atualizações.append([data, horário, nome, esp])
    
    return atualizações

def Portal_Utente_Layout():

    paciente = control.info_paciente_logged()
    paciente_id = paciente.get('id')
    consultas = control.info_hist_consultas(paciente_id)
    medicações = control.info_hist_medicações(paciente_id)
    certificados = control.info_hist_certificados(paciente_id)

    tab_cons = []
    tab_medicações = []
    tab_certificados = []

    for consulta in consultas:

        data = consulta['data']
        horário = consulta['horário']
        esp = consulta['especialidade']
        info_med = consulta['id_médico'].split('_')
        nome = info_med[1] + ' ' + info_med[2] # Concactenamos as duas strings com o primeiro e último nomes de cada médico especialista!
        
        tab_cons.append([data, horário, nome, esp])

    for medicação in medicações:

        medicamento = medicação[0]
        dosagem = medicação[1]
        
        tab_medicações.append([medicamento, dosagem])
    
    for certificado in certificados:

        vacina = certificado[0]
        dose = certificado[1]
        data_adm = certificado[2]

        tab_certificados.append([vacina, dose, data_adm])

    headers_cons = ['Data', 'Horário', 'Médico Especialista', 'Especialidade']
    headers_medicações = ['Medicação', 'Dosagem']
    headers_certificados = ['Vacina', 'Dose', 'Data']

    certificados = [ # Tabela de certificados de vacinação (vacina, dose, data de administração)
        [sg.Table(values= tab_certificados, headings= headers_certificados, auto_size_columns= False, justification= 'centre', num_rows= 2, max_col_width= 50, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_VAC-' )]
    ]

    hist_consultas = [ # Tabela de todas as consultas (data, horário, médico especialista, especialidade)
        [sg.Table(values= tab_cons, headings= headers_cons, auto_size_columns= True, justification= 'centre', num_rows= 3, max_col_width= 50, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_CONS-')]
    ]

    hist_medicações = [ # Tabela de medicações (nome da prescrição, dosagem)
        [sg.Table(values= tab_medicações, headings= headers_medicações, auto_size_columns= False, justification= 'centre', num_rows= 1, max_col_width= 50, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_MEDICA-' )]
    ]

    layout = [
        
        [sg.Text('★ Histórico de Consultas', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-HIST_CONS-')],
        [hist_consultas],
        [sg.Text('★ Histórico de Prescrições Médicas', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-HIST_PRESC-')],
        [hist_medicações],
        [sg.Text('★ Certificados de Vacinação', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-CERTIF-')],
        [certificados],
        [sg.Button('Marcar Consulta', font= ("Arial Rounded Mt Bold", 14), key= '-MARCAR-'), sg.Button('Cancelar Consulta', font= ("Arial Rounded Mt Bold", 14), key= '-CANC_CONS-'), sg.Button('Sair', font= ("Arial Rounded Mt Bold", 14), key= '-SAIR-')]
    ]

    window = sg.Window('Portal do Utente', layout)

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-SAIR-'):
            
            window.close()
            return
        
        elif event == '-MARCAR-':

            especialidade = Especialidade_Cons_Layout()
            if especialidade:
                Agenda_Cons_Layout(especialidade, paciente_id)
                window['-TAB_CONS-'].update(values= Atualizar_Tab_Consultas(paciente_id))

        elif event == '-CANC_CONS-':
            Cancelar_Cons_Layout(paciente_id)

def Cancelar_Cons_Layout(paciente_id):
    
    consultas_futuras = control.info_consultas_futuras(paciente_id)

    tab_futuras = []
    headers = ['Data', 'Horário', 'Médico Especialista', 'Especialidade']

    for consulta in consultas_futuras:

        data = consulta['data']
        horário = consulta['horário']
        esp = consulta['especialidade']
        info_med = consulta['id_médico'].split('_')
        nome = info_med[1] + ' ' + info_med[2] # Concactenamos as duas strings com o primeiro e último nomes de cada médico especialista!
        
        tab_futuras.append([data, horário, nome, esp])

    layout =[

        [sg.Text('Selecione a consulta que deseja cancelar', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4')],
        [sg.Table(values= tab_futuras, headings= headers, auto_size_columns= True, justification= 'centre', num_rows= 3, max_col_width= 35, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', enable_events= True, select_mode= 'browse', key= '-TAB_FUT-')],
        [sg.Button('Sair', font= ("Arial Rounded Mt Bold", 14), key= '-SAIR-')]
    ]    

    window = sg.Window('Cancelamento de Consultas', layout)

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-SAIR-'):
            
            window.close()
            return
        
        elif event == '-TAB_FUT-' and values['-TAB_FUT-']:

            índice = values['-TAB_FUT-'][0]
            click = consultas_futuras[índice]
            info_med = click['id_médico'].split('_')
            nome = info_med[1] + ' ' + info_med[2]

            cancelada = Confirmar_Cancel_Layout(click, nome)
            
            if cancelada:
                window.close()
                return

def Confirmar_Cancel_Layout(click, nome):

    layout = [

        [sg.Text(f'Cancelar consulta de {click['especialidade']} com Dr. {nome}, dia {click['data']}, {click['horário']}', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4')],
        [sg.Button('Confirmar', font= ("Arial Rounded Mt Bold", 14), key= '-CONFIRMAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 14), key= '-CANCELAR-')]
    ]
    
    window = sg.Window('Confirmação de Cancelamento', layout, modal= True)

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return False
        
        elif event == '-CONFIRMAR-':
            
            res = control.processar_cancelar_consulta(click)
            sg.popup(res, font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')
            window.close()
            return True

def Especialidade_Cons_Layout():
    
    especialidades = list(set(med['especialidade'] for med in control.get_info_médicos())) # Obtemos uma lista SEM REPETIÇÕES das especialidades existentes!

    layout = [

        [sg.Text('Especialidade da Consulta:', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4'), sg.Combo(especialidades, key= '-SEL_ESPEC-', readonly= True)],
        [sg.Text('Código: CARDIOlogia, PNEUMologia, CLÍNICA Geral, ORTOpedia, OB/GIN, Medicina DENTária, PEDIATria', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-CÓDIGO-')],
        [sg.Button('Avançar', font= ("Arial Rounded Mt Bold", 14), key= '-AVANÇAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 14), key= '-CANCELAR-')]
    ]

    window = sg.Window('Seleção de Especialidade', layout, modal= True)
    
    while True:
    
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-AVANÇAR-':

            if values.get('-SEL_ESPEC-'):
                window.close()
                return values['-SEL_ESPEC-']
            
            else:
                sg.popup('Por favor selecione uma especialidade para avançar!', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')

def Agenda_Cons_Layout(especialidade, paciente_id):

    # Construção de slots para a semana atual
    hoje = date.today()
    início_semana = hoje - timedelta(days= hoje.weekday()) # Segunda-feira da semana atual
    início_semana_atual = início_semana
    
    # Organização dos slots de cada semana num calendário de agendamento
    def construção_calendário(início_semana):
        semana, slots, agenda = control.agenda_especialidade(especialidade, início_semana)

        # Cabeçalhos da tabela -> Dias da Semana (Segunda - Sábado)
        header = [sg.Text('Horário', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', size= (12,1), pad= (1,1))]
        for i, dia in enumerate(semana):
            header.append(sg.Text(dia.strftime("%a %d/%m"), key= ('-HEADER-', i), size= (13,1), font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', justification= 'center', pad= (1,1)))

        # Linhas da tabela -> Slots de Tempo (intervalos de 30 minutos)
        colunas = []
        for slot in slots:
            coluna = [sg.Text(slot, font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', size= (12,1), pad= (1,1))]

            for dia_index in range(len(semana)):
                info = agenda.get((dia_index, slot))
                
                if info:
                    bg_color = '#4CBB17' if not info['marcada'] else 'red' # Slots disponíveis -> VERDE, Slots ocupados -> VERMELHO
                    coluna.append(sg.Button(info['médico'], key= ('-SLOT-', dia_index, slot, info['id_médico']), size= (12,1), font= ("Arial Rounded Mt Bold", 14), button_color= (bg_color, 'white'), pad= (1,1)))
                
                else:
                    coluna.append(sg.Text('--', size= (12,1), font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', pad= (1,1)))
            colunas.append(coluna)
        
        # Navegação entre semanas (Semana Anterior, Semana Seguinte)
        layout = [header] + colunas + [

            [sg.Button('Semana Anterior', font= ("Arial Rounded Mt Bold", 14), key= '-ANTERIOR-', pad=(5, 5)), 
            sg.Button('Semana Seguinte', font= ("Arial Rounded Mt Bold", 14), key= '-SEGUINTE-', pad=(5, 5)), 
            sg.Button('Sair', font= ("Arial Rounded Mt Bold", 14), key= '-SAIR-', pad=(5, 5))]
        ]

        w = sg.Window(f'Agendamento de Consultas ({especialidade})', layout, finalize= True)
        return w, semana, slots, agenda
    
    window, semana, slots, agenda = construção_calendário(início_semana_atual)

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-SAIR-'):
            
            window.close()
            return
        
        elif event == '-SEGUINTE-': # Construção da tabela para a semana seguinte

            início_semana_atual = início_semana_atual + timedelta(days= 7) # Avançamos uma semana no calendário
            window.close()
            window, semana, slots, agenda = construção_calendário(início_semana_atual)
            
        elif event == '-ANTERIOR-': # Construção da tabela para a semana anterior

            início_semana_atual = início_semana_atual - timedelta(days= 7) # Retrocedemos uma semana no calendário
            window.close()
            window, semana, slots, agenda = construção_calendário(início_semana_atual)
            
        elif isinstance(event, tuple) and event[0] == '-SLOT-': # Marcação da consulta num slot disponível

            dia_index, slot, med_id = event[1], event[2], event[3]
            info = agenda.get((dia_index, slot))

            if info and not info['marcada']:
                data = semana[dia_index].strftime('%Y-%m-%d')

                if isinstance(info['id_médico'], tuple): # Temos um tuplo quando existe mais do que um médico especialista disponível para o slot desejado!
                    med_selecionado = Med_Disponíveis_Layout(especialidade, restantes_id= info['id_médico'])

                    if not med_selecionado:
                        continue
                    med_id = med_selecionado['id']
                    med_nome = med_selecionado['nome']
                
                else: 
                    med_id = info['id_médico'] 
                    med_nome = info['médico']

                marcada = Marcação_Cons_Layout(data, slot, med_nome, med_id, especialidade, paciente_id)
                
                if marcada:
                    window.close()
                    return

def Med_Disponíveis_Layout(especialidade, restantes_id):

    med_disponíveis = [med for med in control.get_info_médicos() if med['especialidade'] == especialidade and med['id'] in restantes_id]
    if not med_disponíveis:
        sg.popup('Nenhum médico disponível para esta especialidade!')
    
    opções = [f'{med['nome']} - {med['localidade']}' for med in med_disponíveis]

    layout = [

        [sg.Text('Médico Especialista:', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4'), sg.Combo(opções, key= '-MED_ESC-', readonly= True)],
        [sg.Button('Avançar', font= ("Arial Rounded Mt Bold", 14), key= '-AVANÇAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 14), key= '-CANCELAR-')]
    ]

    window = sg.Window('Seleção do Médico Especialista', layout, modal= True)

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-AVANÇAR-':

            escolha = values['-MED_ESC-']
            
            if escolha:
                seleção = next((med for med in med_disponíveis if f'{med['nome']} - {med['localidade']}' == escolha), None)
                window.close()
                return seleção
            
            else: sg.popup('Por favor selecione um médico especialista!', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')

def Marcação_Cons_Layout(data, slot, med_nome, med_id, especialidade, paciente_id):

    layout = [

        [sg.Text(f'Agendar consulta para o dia {data}, {slot}', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4')],
        [sg.Text(f'Médico Especialista: {med_nome}', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4')],
        [sg.Button('Confirmar', font= ("Arial Rounded Mt Bold", 14), key= '-CONFIRMAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 14), key= '-CANCELAR-')]
    ]
    
    window = sg.Window('Confirmação de Agendamento', layout, modal=True)

    while True:
    
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return False
        
        elif event == '-CONFIRMAR-':

            res = control.processar_marcar_consulta(data, slot, especialidade, med_id, paciente_id)
            sg.popup(res, font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')
            window.close()
            return True

def Informações_Layout():
    
    tab_especialidades = []
    headers_especialidades = ['Médico Especialista', 'Especialidade', 'Localidade', 'Horário de Atendimento', 'Contacto']

    médicos = control.get_info_médicos()

    for médico in médicos:

        med_especialista = médico['nome']
        esp = médico['especialidade']
        horário_atend = médico['horas_ativas']
        contacto = médico['contacto']
        localidade = médico['localidade']

        tab_especialidades.append([med_especialista, esp, localidade, horário_atend, contacto])

    # Tabela de médicos especialistas registados na plataforma
    med_especialistas_info = [sg.Table(values= tab_especialidades, headings= headers_especialidades, auto_size_columns= True, justification= 'centre', num_rows= 10, max_col_width= 35, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_MD-' )]

    disp_sma = control.info_disponibilidade_local('São Martinho das Amoreiras')
    disp_valverde = control.info_disponibilidade_local('Valverde')
    disp_svitória = control.info_disponibilidade_local('Santa Vitória')
    disp_albernoa = control.info_disponibilidade_local('Albernoa')
    disp_sbm = control.info_disponibilidade_local('São Bento do Mato')
    disp_nsm = control.info_disponibilidade_local('Nossa Senhora de Machede')

    headers_disponibilidades = ['Especialidade', 'Próxima Disponibilidade']

    # Tabela de disponibilidade de marcação de consultas para São Martinho das Amoreiras
    tab_sma = sg.Table(values= disp_sma, headings= headers_disponibilidades, auto_size_columns= True, justification= 'centre', num_rows= 7, max_col_width= 35, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_SMA-')

    # Tabela de disponibilidade de marcação de consultas para Valverde
    tab_valverde = sg.Table(values= disp_valverde, headings= headers_disponibilidades, auto_size_columns= True, justification= 'centre', num_rows= 7, max_col_width= 35, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_VALVERDE-' )

    # Tabela de disponibilidade de marcação de consultas para Santa Vitória
    tab_svitória = sg.Table(values= disp_svitória, headings= headers_disponibilidades, auto_size_columns= True, justification= 'centre', num_rows= 7, max_col_width= 35, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_SVITÓRIA-' )

    # Tabela de disponibilidade de marcação de consultas para Albernoa
    tab_albernoa = sg.Table(values= disp_albernoa, headings= headers_disponibilidades, auto_size_columns= True, justification= 'centre', num_rows= 7, max_col_width= 35, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_ALBERNOA-' )
    
    # Tabela de disponibilidade de marcação de consultas para São Bento do Mato
    tab_sbm = sg.Table(values= disp_sbm, headings= headers_disponibilidades, auto_size_columns= True, justification= 'centre', num_rows= 7, max_col_width= 35, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_SBM-' )

    # Tabela de disponibilidade de marcação de consultas para Nossa Senhora de Machede
    tab_nsm = sg.Table(values= disp_nsm, headings= headers_disponibilidades, auto_size_columns= True, justification= 'centre', num_rows= 7, max_col_width= 35, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_NSM-' )

    informações = [
        
        [sg.Text('★ Médicos Especialistas de Serviço', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-HIST_CONS-')],
        [sg.Text('Código: CARDIOlogia, PNEUMologia, CLÍNICA Geral, ORTOpedia, OB/GIN, Medicina DENTária, PEDIATria', font= ("Arial Rounded Mt Bold", 12), text_color= 'white', background_color= '#FF69B4', key= '-CÓDIGO-')],
        med_especialistas_info,
        [sg.Text('--------------------------------------------------------------------------------------------------------------------------------', font= ("Arial Rounded Mt Bold", 20), text_color= 'white', background_color= '#FFC0E1', key= '-DIV-')],
        [sg.Text('★ Agendamento de Consulta - São Martinho das Amoreiras, Valverde', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-HIST_CONS-')],
        [tab_sma, tab_valverde],
        [sg.Text('--------------------------------------------------------------------------------------------------------', font= ("Arial Rounded Mt Bold", 20), text_color= 'white', background_color= '#FFC0E1', key= '-DIV-')],
        [sg.Text('★ Agendamento de Consulta - Santa Vitória, Albernoa', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-HIST_CONS-')],
        [tab_svitória, tab_albernoa],
        [sg.Text('--------------------------------------------------------------------------------------------------------', font= ("Arial Rounded Mt Bold", 20), text_color= 'white', background_color= '#FFC0E1', key= '-DIV-')],
        [sg.Text('★ Agendamento de Consulta - São Bento do Mato, Nossa Senhora de Machede', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-HIST_CONS-')],
        [tab_sbm, tab_nsm],
        [sg.Button('Sair', font= ("Arial Rounded Mt Bold", 14), key= '-SAIR-')]
    ]
    
    scroll = sg.Column(informações, size= (875,450), scrollable= True, vertical_scroll_only= True)
    layout = [[scroll]]

    window = sg.Window('Informações', layout)
    
    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-SAIR-'):
            
            window.close()
            return

def Campanha_Vac_Layout():

    tab_localidades = []
    header_loc = ['Localidades Abrangidas', 'Datas']

    tab_plano_vac = []
    header_plano = ['Plano de Vacinação', 'Doses a Administrar']

    localidades = [['Aveleda e Rio de Onor','20/9'],['Castro Laboreiro','21/9'],['Sobradelo da Goma','22/9'],
                   ['Aldeia das Dez','23/9'],['Piódão','24/9'],['Janeiro de Cima','25/9'],
                   ['Monte da Pedra','26/9'],['Barrancos','27/9'],['S. Martinho das Amoreiras','28/9'],
                   ['Alferce','29/9'],['Cachopo','30/9'],['Martim Longo','1/10']]
    
    plano_vac = [['COVID-19','Reforço Sazonal'],['Gripe A','Reforço Sazonal'],['HPV','1ª e 2ª'],['Tétano e Difteria','Reforço']]

    for localidade in localidades:
        local = localidade[0]
        data = localidade[1]

        tab_localidades.append([local,data])
    
    for vacinas in plano_vac:
        tipo = vacinas[0]
        dose = vacinas[1]

        tab_plano_vac.append([tipo,dose])

    layout = [

        [sg.Text('★ Campanha "Saúde Sobre Rodas", 20 de Setembro - 1 de Outubro 2025', font= ("Arial Rounded Mt Bold", 19), text_color= 'white', background_color= '#FF69B4', key= '-T_CAMP-')],
        [sg.Text('Juntos, vamos levar saúde e esperança às comunidades remotas do nosso país!', font= ("Arial Rounded Mt Bold", 17), text_color= 'white', background_color= '#FF69B4', key= '-T_CAMP2-')],
        [sg.Text('Inscrições abertas até 5 de Junho', font= ("Arial Rounded Mt Bold", 15), text_color= 'white', background_color= '#FF69B4', key= '-T_CAMP2-')],
        [sg.Table(values= tab_localidades, headings= header_loc, auto_size_columns= False, justification= 'centre', num_rows= 4, col_widths=[20, 9], font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_LOC-'), 
         sg.Table(values= tab_plano_vac, headings= header_plano, auto_size_columns= True, justification= 'centre', num_rows= 4, max_col_width= 35, font= ("Arial Rounded Mt Bold", 13), text_color= '#FF69B4', background_color= 'white', alternating_row_color= '#FCE5FC', key= '-TAB_PLANO-')],
        [sg.Button('Inscreva-se já!', font= ("Arial Rounded Mt Bold", 14), key= '-NOVA_INSC-'), sg.Button('Estatísticas', font= ("Arial Rounded Mt Bold", 14), key= '-STATS-'), sg.Button('Sair', font= ("Arial Rounded Mt Bold", 14), key= '-SAIR-')]
    ]
    
    window = sg.Window('Campanha de Vacinação', layout)

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-SAIR-'):
            
            window.close()
            return
        
        elif event == '-NOVA_INSC-':
            Nova_Insc_Layout()

        elif event == '-STATS-':
            Estatísticas_Layout()

def Nova_Insc_Layout():

    layout = [

        [sg.Text('Nome Completo *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-INSC_NOME-'), sg.Input(key= '-NOME-')],
        [sg.Text('Data de Nascimento (A-M-D) *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-INSC_DOB-'), sg.Input(key= '-DOB-')],
        [sg.Text('Sexo *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-INSC_SEXO-'), sg.Combo(['M', 'F'], key= '-SEXO-')],
        [sg.Text('Certificados (Vacina: Dose: Data)', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-INSC_CERTIF-'), sg.Input(key= '-CERTIF-')],
        [sg.Text('Vacinação *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-INSC_VACINA-'), sg.Combo(['COVID-19', 'Gripe A', 'HPV', 'Tétano e Difteria'], key= '-VACINA-')],
        [sg.Text('Dose Desejada *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-INSC_DOSE-'), sg.Combo(['1ª (HPV)','2ª (HPV)','Reforço (Tétano, Difteria)','Reforço Sazonal (COVID-19, Gripe A)'], key= '-DOSE-')],
        [sg.Text('Localidade *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-INSC_LOCAL-'), sg.Combo(['Aveleda e Rio de Onor', 'Castro Laboreiro', 'Sobradelo da Goma', 
            'Aldeia das Dez', 'Piódão','Janeiro de Cima', 'Monte da Pedra', 'Barrancos', 'S. Martinho das Amoreiras', 'Alferce', 'Cachopo', 'Martim Longo'], key= '-LOCAL-')],
        [sg.Text('Número de Cartão de Cidadão *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-INSC_CC-'), sg.Input(key= '-CC-')],
        [sg.Text('Contacto Pessoal *', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FF69B4', key= '-REG_CP-'), sg.Input(key= '-CP-')],
        [sg.Button('Registar', font= ("Arial Rounded Mt Bold", 14), key= '-REGISTAR-'), sg.Button('Cancelar', font= ("Arial Rounded Mt Bold", 14), key= '-CANCELAR-')]
    ]

    window = sg.Window('Nova Inscrição para Vacinação', layout, modal= True) # Utilizamos uma janela modal de modo a que não seja possível a interação com a janela principal durante o processo de registo!

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-REGISTAR-':

            if (not values['-NOME-'] or not values['-DOB-'] or not values['-SEXO-'] or not values['-VACINA-'] or not values['-DOSE-'] or not values['-CC-'] or not values['-CP-'] or not values['-LOCAL-']):
                sg.popup('Por favor preencha os campos obrigatórios (*)!', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')
                continue

            # Verificação do Formato de Input dos Certificados
            input_certif = values['-CERTIF-'].strip()

            info_válida = False

            if input_certif:
                certificados = [certif.strip() for certif in input_certif.split(',') if certif.strip()]

                # A utilização da função all() irá retornar True se o formato de input for correto!!
                info_válida = all((':' in certif and len(certif.split(':')) == 3 and certif.split(':')[0].strip() and certif.split(':')[1].strip() and certif.split(':')[2].strip()) for certif in certificados)
                
            else: info_válida = True # O campo de certificados de vacinação não é obrigatório, por isso, não há problema se não for preenchido

            if not info_válida:
                sg.popup('Por favor introduza os seus certificados de vacinação no formato pedido (Vacina: Dose: Data)!', font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')
                continue

            res = control.processar_vacinação(values)
            sg.popup(res, font= ("Arial Rounded Mt Bold", 14), text_color= 'white', background_color= '#FFC0E1')
            window.close()

def Estatísticas_Layout():

    faixas_etárias = control.info_dist_faixa()
    sexo = control.info_dist_sexo()
    localidade = control.info_dist_localidade()
    vacinas = control.info_dist_vacina()

    def gráfico_circ(dist, título, xlabel):

        plt.figure(figsize=(6,4))
        plt.bar(dist.keys(), dist.values(), color= '#FFC0E1', width= 0.4)
        plt.title(título, fontdict= {'fontname': 'Arial Rounded Mt Bold', 'fontsize': 16})
        plt.xlabel(xlabel, fontdict= {'fontname': 'Arial Rounded Mt Bold', 'fontsize': 14})
        plt.ylabel('Inscrições', fontdict= {'fontname': 'Arial Rounded Mt Bold', 'fontsize': 14})
        plt.xticks(fontname= 'Arial Rounded Mt Bold', fontsize= 13)
        plt.tight_layout()
        plt.show(block= False)

    layout = [

        [sg.Button('Distribuição por Faixa Etária', font= ("Arial Rounded Mt Bold", 14), key= '-IDADES-'), sg.Button('Distribuição por Sexo', font= ("Arial Rounded Mt Bold", 14), key= '-SEXO-')],
        [sg.Button('Distribuição por Localidade', font= ("Arial Rounded Mt Bold", 14), key= '-LOCAL-'), sg.Button('Distribuição por Vacina Administrada', font= ("Arial Rounded Mt Bold", 14), key= '-VACINA-')],
        [sg.Button('Sair', font= ("Arial Rounded Mt Bold", 14), key= '-SAIR-')]
    ]
    
    window = sg.Window('Estatísticas', layout)

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-SAIR-'):
            
            window.close()
            return
        
        elif event == '-IDADES-':
            gráfico_circ(faixas_etárias,'Distribuição por Faixa Etárias','Faixas Etárias')

        elif event == '-SEXO-':

            plt.figure(figsize=(5,3))
            plt.bar(sexo.keys(), sexo.values(), color= '#FFC0E1', width= 0.4)
            plt.title('Distribuição por Sexo', fontdict= {'fontname': 'Arial Rounded Mt Bold', 'fontsize': 16})
            plt.xlabel('Sexo', fontdict= {'fontname': 'Arial Rounded Mt Bold', 'fontsize': 14})
            plt.ylabel('Inscrições', fontdict= {'fontname': 'Arial Rounded Mt Bold', 'fontsize': 14})
            plt.xticks(fontname= 'Arial Rounded Mt Bold', fontsize= 13)
            plt.tight_layout()
            plt.show(block= False)

        elif event == '-LOCAL-':
            
            plt.figure(figsize=(7,5))
            plt.bar(localidade.keys(), localidade.values(), color= '#FFC0E1')
            plt.title('Distribuição por Localidade', fontdict= {'fontname': 'Arial Rounded Mt Bold', 'fontsize': 16})
            plt.xlabel('Localidades', fontdict= {'fontname': 'Arial Rounded Mt Bold', 'fontsize': 14})
            plt.ylabel('Inscrições', fontdict= {'fontname': 'Arial Rounded Mt Bold', 'fontsize': 14})
            plt.xticks(rotation= 45, ha= 'right', fontname=' Arial Rounded Mt Bold', fontsize= 13)
            plt.tight_layout()
            plt.show(block= False)

        elif event == '-VACINA-':
            gráfico_circ(vacinas,'Distribuição por Vacina Administrada','Vacinas Administradas')

def run_interface():

    stop = False

    # JANELA PRINCIPAL
    window = sg.Window("Gestão de Saúde Comunitária", Layout_Inicial(), size= (560, 200), element_justification= "center", finalize= True)

    while not stop:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            stop = True
        
        # Novo Registo de Pacientes
        elif event == '-NOVO_REG-':
            Novo_Reg_Layout()
        
        # Verificação de Log In de Pacientes -> Página Portal do Utente -> Marcação e Cancelamento de Consultas, Históricos de Informação do Utente
        elif event == '-UTENTE-':
            Log_In_Layout()
        
        # Informações sobre Médicos Especialistas, Próxima Disponibilidade Para Agendamento de Consultas
        elif event == '-MD-':
            Informações_Layout()
        
        # Informação sobre Campanha de Vacinação -> Nova Inscrição na Campanha, Análise Gráfica de Taxas de Vacinação, Informação sobre Vacinação Disponível
        elif event == '-VAC-':
            Campanha_Vac_Layout()

    window.close()
