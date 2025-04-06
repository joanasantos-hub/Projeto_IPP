# VIEW -> Interface Gráfica
import PySimpleGUI as sg
import projeto_controller as control
import projeto_model as model

sg.theme_background_color("#FFC0E1")  # Cor de fundo rosa claro
sg.theme_button_color(("white", "#FF69B4"))  # Botões rosa escuro

def criar_layout():

    menu_botões = [

        [
            sg.Button('Portal do Utente', size=(20, 2), font=("Arial Rounded Mt Bold", 14), key= '-UTENTE-', ),
            sg.Button('Novo Registo de Utente', size=(20, 2), font=("Arial Rounded Mt Bold", 14), key='-NOVO_REG-')
        ],

        [
            sg.Button('Médicos Especialistas', size=(20, 2), font=("Arial Rounded Mt Bold", 14), key='-MD-'),
            sg.Button('Campanha de Vacinação', size=(20, 2), font=("Arial Rounded Mt Bold", 14), key='-VAC-')
        ]
    ]

    layout = [
        [sg.Column(menu_botões, element_justification='center')]
    ]
    return layout

def Novo_Reg_Layout():

    layout = [

        [sg.Text('Nome Completo *:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key= '-REG_NOME-'), sg.Input(key= '-NOME-')],
        [sg.Text('Data de Nascimento (A-M-D) *:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_DOB-'), sg.Input(key= '-DOB-')],
        [sg.Text('Sexo *:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_SEXO-'), sg.Combo(['M', 'F'], key= '-SEXO-')],
        [sg.Text('Condições Prévias:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_COND-'), sg.Input(key= '-COND-')],
        [sg.Text('Medicações:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_MEDS-'), sg.Input(key= '-MEDS-')],
        [sg.Text('Número de Cartão de Cidadão *:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_CC-'), sg.Input(key= '-CC-')],
        [sg.Text('NIF *:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_NIF-'), sg.Input(key= '-NIF-')],
        [sg.Text('Localidade *:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_LOCAL-'), sg.Input(key= '-LOCAL-')],
        [sg.Text('Contacto Pessoal *:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_CP-'), sg.Input(key= '-CP-')],
        [sg.Text('Parente mais Próximo:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_NOK-'), sg.Input(key= '-NOK-')],
        [sg.Text('Contacto do Parente mais Próximo:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_CNOK-'), sg.Input(key= '-CNOK-')],
        [sg.Button('Registar', font=("Arial Rounded Mt Bold", 12), key='-REGISTAR-'), sg.Button('Cancelar', font=("Arial Rounded Mt Bold", 12), key='-CANCELAR-')]
    ]

    window = sg.Window('Novo Registo de Utente', layout, modal=True) # Utilizamos uma janela modal de modo a que não seja possível a interação com a janela principal durante o processo de registo!

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-REGISTAR-':

            if (not values['-NOME-'] or not values['-DOB-'] or not values['-SEXO-'] or not values['-NIF-'] or not values['-CP-'] or not values['-LOCAL-']):
                sg.popup('Por favor preencha os campos obrigatórios (*)!', font=("Arial Rounded Mt Bold", 14), text_color='white', background_color='#FFC0E1')
                continue

            res = control.processo_registo(values)
            sg.popup(res, font=("Arial Rounded Mt Bold", 14), text_color='white', background_color='#FFC0E1')

        window.close()

def Log_In_Layout():

    layout = [[sg.Text('Número de Cartão de Cidadão:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key= '-LOG_CC-'), sg.Input(key= '-UTENTE_CC-')],
              [sg.Button('Entrar', font=("Arial Rounded Mt Bold", 12), key='-ENTRAR-'), 
               sg.Button('Cancelar', font=("Arial Rounded Mt Bold", 12), key='-CANCELAR-')]]

    window = sg.Window('Log In de Utente', layout, modal=True) # Utilizamos uma janela modal de modo a que não seja possível a interação com a janela principal!

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return
        
        elif event == '-ENTRAR-':

            res = control.check_login(values)

            if res is True:

                window.close()
                #Portal_Utente_Layout()

            elif res is False:
                sg.popup('Registo de utente não encontrado! Por favor, realize a sua inscrição na plataforma.', font=("Arial Rounded Mt Bold", 14), text_color='white', background_color='#FFC0E1')

def Portal_Utente_Layout():

    toggle_up =  '▶'
    toggle_down =  '▼'

    hist_consultas = [

        
    ]

    layout = [[sg.Text('Número de Cartão de Cidadão:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key= '-LOG_CC-'), sg.Input(key= '-UTENTE_CC-')],
              [sg.Button('Entrar', font=("Arial Rounded Mt Bold", 12), key='-ENTRAR-'), 
               sg.Button('Cancelar', font=("Arial Rounded Mt Bold", 12), key='-CANCELAR-')]]

    window = sg.Window('Portal do Utente', layout)

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            
            window.close()
            return

def Médicos_Esp_Layout():
    pass

def Campanha_Vac_Layout():
    pass

def run_interface():

    stop = False

    # JANELA PRINCIPAL
    window = sg.Window("Gestão de Saúde Comunitária", criar_layout(), size=(560, 200), element_justification="center", finalize=True)

    while not stop:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            stop = True
        
        # Novo Registo de Pacientes
        elif event == '-NOVO_REG-':
            Novo_Reg_Layout()
        
        # Verificação de Log In de Pacientes -> Página Portal do Utente
        elif event == '-UTENTE-':
            Log_In_Layout()
        
        # Informações sobre Médicos Especialistas
        elif event == '-MD-':
            Médicos_Esp_Layout()
        
        elif event == '-VAC-':
            Campanha_Vac_Layout()

    window.close()