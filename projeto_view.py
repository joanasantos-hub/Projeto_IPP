# VIEW -> Interface Gráfica
import PySimpleGUI as sg
import projeto_shell as logic
import projeto_model as model

sg.theme_background_color("#FFC0CB")  # Cor de fundo rosa claro
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

        [sg.Text('Nome Completo:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key= '-REG_NOME-'), sg.Input(key= '-NOME-')],
        [sg.Text('Data de Nascimento: (Y-M-D)', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_DOB-'), sg.Input(key= '-DOB-')],
        [sg.Text('Sexo', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_SEXO-'), sg.Combo(['M', 'F'], key= '-SEXO-')],
        [sg.Text('Condições Prévias:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_COND-'), sg.Input(key= '-COND-')],
        [sg.Text('Medicações:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_MEDS-'), sg.Input(key= '-MEDS-')],
        [sg.Text('Número de Cartão de Cidadão:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_CC-'), sg.Input(key= '-CC-')],
        [sg.Text('NIF:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_NIF-'), sg.Input(key= '-NIF-')],
        [sg.Text('Localidade:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_LOCAL-'), sg.Input(key= '-LOCAL-')],
        [sg.Text('Contacto Pessoal:', font=("Arial Rounded Mt Bold", 12), text_color='white', background_color='#FF69B4', key='-REG_CP-'), sg.Input(key= '-CP-')],
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

            try:
                paciente = logic.Paciente(

                    nome = values['-NOME-'],
                    data_nascimento = (values['-DOB-']),
                    sexo = values['-SEXO-'],
                    cond_prévias = values['-COND-'],
                    medicações = values['-MEDS-'],
                    CC = values['-CC-'],
                    NIF = values['-NIF-'],
                    contacto = values['-CP-'],
                    NOK = values['-NOK-'],
                    NOK_contacto = values['-CNOK-'],
                    localidade = values['-LOCAL-']
                )

                sg.popup('Paciente registado com sucesso!')

            except:
                sg.popup('Erro!  Não foi possível guardar o registo!')

        window.close()

def main():

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

    window.close()

if __name__ == "__main__":
    main()
