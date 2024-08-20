import datetime as dt
import csv
import sys
from erros import operation_does_not_exist
import json

def export():
    """Exporta o arquivo
    """
    file_path = files_paths()
    print('\n=== Exportar Registros ===')

    answer = str(input('Qual formato deseja que o arquivo seja salvo? \n1. CSV\n2. JSON\nOpção: '))
    with open(file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)

    file_name = str(input('\nQual o nome  que deseja salvar o arquivo: '))
    if answer == '1':
        with open(file_name + '.csv', mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(rows)
        print(f'Arquivo salvo como {file_name}.csv')

    elif answer == '2':
        with open(file_name + '.json', mode='w') as json_file:
            json.dump(rows, json_file, indent=4, ensure_ascii=False)
        print(f'Arquivo salvo como {file_name}.json')

def print_csv_filter_value(first_value, last_value):
    file_path = files_paths()

    with open(file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        filtered_lines = [line for line in csv_reader if first_value <= float(line['valor']) <= last_value]

        receita = []
        despesa = []
        investimento = []

        if filtered_lines:
            for line in filtered_lines:
                id_transacao = line['id_transacao']
                dt_criacao = dt.datetime.strptime(line['dt_criacao'], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')
                tipo = line['tipo']
                valor = line['valor']
                taxa = ''
                dt_atualizacao = line['dt_atualizacao'] if line['dt_atualizacao'] != 'Data Atualização: ' else ''
                montante = valor
                dias_desde_criacao = (dt.datetime.now() - dt.datetime.strptime(line['dt_criacao'], '%Y-%m-%d %H:%M:%S.%f')).days
                if tipo == "investimento":  
                    taxa = line['taxa']                
                    montante = f"{float(line['valor']) * (1 + float(line['taxa'])) ** dias_desde_criacao:.2f}"

                if tipo == 'receita':
                    receita.append(float(valor))
                elif tipo == 'despesa':
                    despesa.append(float(valor))
                elif tipo == 'investimento':
                    investimento.append(float(valor))

                print("-" * 130)
                print(f"{'ID Transação':<15}{'Data Criação':<25}{'Tipo':<15}{'Valor':<10}{'Taxa':<10}{'Montante':<15}{'Dias investidos':<20}{'Data Atualização':<25}")
                print("-" * 130)
                print(f"{id_transacao:<15}{dt_criacao:<25}{tipo.capitalize():<15}R${valor:<10}{taxa}{'%':<10}{montante:<15}{dias_desde_criacao}{dt_atualizacao:<25}")
                print("-" * 130) 
        else:
            print("Nenhum resultado encontrado para o tipo selecionado.")

        print("\n===Agrupa e mostra o total de valor por tipo.===")
        print(f"{'Receita':<15}{'Despesa':<25}{'Investimento':<15}")
        print("-" * 135)
        print(f"{sum(receita):<15}{sum(despesa):<25}{sum(investimento):<15}")
        print("-" * 135) 

def print_csv_filter_date(first_date, last_date):
    file_path = files_paths()

    with open(file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        filtered_lines = [line for line in csv_reader if first_date <= dt.datetime.strptime(line['dt_criacao'], '%Y-%m-%d %H:%M:%S.%f').date() <= last_date]

        receita = []
        despesa = []
        investimento = []

        if filtered_lines:
            for line in filtered_lines:
                id_transacao = line['id_transacao']
                dt_criacao = dt.datetime.strptime(line['dt_criacao'], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')
                tipo = line['tipo']
                valor = line['valor']
                taxa = ''
                dt_atualizacao = line['dt_atualizacao'] if line['dt_atualizacao'] != 'Data Atualização: ' else ''
                montante = valor
                dias_desde_criacao = (dt.datetime.now() - dt.datetime.strptime(line['dt_criacao'], '%Y-%m-%d %H:%M:%S.%f')).days
                if tipo == "investimento":  
                    taxa = line['taxa']                
                    montante = f"{float(line['valor']) * (1 + float(line['taxa'])) ** dias_desde_criacao:.2f}"

                if tipo == 'receita':
                    receita.append(float(valor))
                elif tipo == 'despesa':
                    despesa.append(float(valor))
                elif tipo == 'investimento':
                    investimento.append(float(valor))

                print("-" * 130)
                print(f"{'ID Transação':<15}{'Data Criação':<25}{'Tipo':<15}{'Valor':<10}{'Taxa':<10}{'Montante':<15}{'Dias investidos':<20}{'Data Atualização':<25}")
                print("-" * 130)
                print(f"{id_transacao:<15}{dt_criacao:<25}{tipo.capitalize():<15}R${valor:<10}{taxa}{'%':<10}{montante:<15}{dias_desde_criacao}{dt_atualizacao:<25}")
                print("-" * 130) 
        else:
            print("Nenhum resultado encontrado para o tipo selecionado.")


        print("\n===Agrupa e mostra o total de valor por tipo.===")
        print(f"{'Receita':<15}{'Despesa':<25}{'Investimento':<15}")
        print("-" * 135)
        print(f"{sum(receita):<15}{sum(despesa):<25}{sum(investimento):<15}")
        print("-" * 135) 

def print_csv_filter_type(value: str) -> None:
    """
    Printa o arquivo conforme o filtro por tipo.
    Args:
        value (str): Tipo especifico para filtrar.
    """    
    file_path = files_paths()

    with open(file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        filtered_lines = [line for line in csv_reader if line['tipo'] == value]
        
        receita = []
        despesa = []
        investimento = []

        if filtered_lines:
            for line in filtered_lines:
                id_transacao = line['id_transacao']
                dt_criacao = dt.datetime.strptime(line['dt_criacao'], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')
                tipo = line['tipo']
                valor = line['valor']
                taxa = line['taxa']
                dt_atualizacao = line['dt_atualizacao'] if line['dt_atualizacao'] != 'Data Atualização: ' else ''

                if tipo == 'receita':
                    receita.append(float(valor))
                elif tipo == 'despesa':
                    despesa.append(float(valor))
                elif tipo == 'investimento':
                    investimento.append(float(valor))

                if value == "investimento":
                    print("-" * 135)
                    print(f"{'ID Transação':<15}{'Data Criação':<25}{'Tipo':<15}{'Valor':<10}{'Taxa':<10}{'Montante':<15}{'Dias investidos':<20}{'Data Atualização':<25}")
                    print("-" * 135)
                    dias_desde_criacao = (dt.datetime.now() - dt.datetime.strptime(line['dt_criacao'], '%Y-%m-%d %H:%M:%S.%f')).days
                    montante = f"{float(line['valor']) * (1 + float(line['taxa'])) ** dias_desde_criacao:.2f}"
                    print(f"{id_transacao:<15}{dt_criacao:<25}{tipo.capitalize():<15}R${valor:<10}{taxa}{'%':<10}{montante:<15}{dias_desde_criacao}{dt_atualizacao:<25}")
                    print("-" * 135)
                elif value != "investimento":
                    print("-" * 130)
                    print(f"{'ID Transação':<15}{'Data Criação':<25}{'Tipo':<15}{'Valor':<10}{'Data Atualização':<25}")
                    print("-" * 130)
                    print(f"{id_transacao:<15}{dt_criacao:<25}{tipo.capitalize():<15}R${valor:<10}{dt_atualizacao:<25}")
                    print("-" * 130) 
        else:
            print("Nenhum resultado encontrado para o periodo selecionado.")


        print("\n===Agrupa e mostra o total de valor por tipo.===")
        print(f"{'Receita':<15}{'Despesa':<25}{'Investimento':<15}")
        print("-" * 135)
        print(f"{sum(receita):<15}{sum(despesa):<25}{sum(investimento):<15}")
        print("-" * 135) 
        
def print_all_csv(chamado = False):
    file_path = files_paths()

    with open(file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        filtered_lines = [line for line in csv_reader]
        
        receita = []
        despesa = []
        investimento = []

        if filtered_lines:
            for line in filtered_lines:
                id_transacao = line['id_transacao']
                dt_criacao = dt.datetime.strptime(line['dt_criacao'], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')
                tipo = line['tipo']
                valor = line['valor']
                dt_atualizacao = line['dt_atualizacao'] if line['dt_atualizacao'] != 'Data Atualização: ' else ''
                dias_desde_criacao = (dt.datetime.now() - dt.datetime.strptime(line['dt_criacao'], '%Y-%m-%d %H:%M:%S.%f')).days
                try:
                    taxa = line['taxa']
                    montante = f"{float(line['valor']) * (1 + float(line['taxa'])) ** dias_desde_criacao:.2f}"
                except ValueError as e:
                    montante = ''
                    taxa = ''

                if tipo == 'receita':
                    receita.append(float(valor))
                elif tipo == 'despesa':
                    despesa.append(float(valor))
                elif tipo == 'investimento':
                    investimento.append(float(valor))
                    
                print("-" * 135)
                print(f"{'ID Transação':<15}{'Data Criação':<25}{'Tipo':<15}{'Valor':<10}{'Taxa':<10}{'Montante':<15}{'Dias investidos':<20}{'Data Atualização':<25}")
                print("-" * 135)
                print(f"{id_transacao:<15}{dt_criacao:<25}{tipo.capitalize():<15}R${valor:<10}{taxa}{'%':<10}{montante:<15}{dias_desde_criacao:<20}{dt_atualizacao:<25}")
                print("-" * 135)


            if chamado == True:
                print("\n===Agrupa e mostra o total de valor por tipo.===")
                print(f"{'Receita':<15}{'Despesa':<25}{'Investimento':<15}")
                print("-" * 135)
                print(f"{sum(receita):<15}{sum(despesa):<25}{sum(investimento):<15}")
                print("-" * 135)           

def consult_record(errors:int = 0) -> None:
    """
    Consulta registros com base em filtros.
    Args:
        errors (int, optional): Controla a quantidade de erros. Defaults to 0.
    """    
    types_filters = {
        "1": "tipo",
        "2": "data",
        "3": "valor"
    }

    types_of_types = {
        "1": "receita",
        "2": "despesa",
        "3": "investimento"
    }
    type_filter = False
    print('\n=== Consultar Registros ===')

    while True:
        if type_filter == False:
            type_filter = str(input(f"\nFiltros disponíveis:\n1. {types_filters["1"].capitalize()} \n2. {types_filters["2"].capitalize()}\n3. {types_filters["3"].capitalize()}\nDigite o tipo para filtrar (ou deixe em branco para ignorar): ")).strip().lower()
        if errors > 3:
            return
        elif type_filter == '4':
            closure(current_date=dt.datetime.now())
        elif type_filter == '':
            print_all_csv(chamado=True)
            type_filter = str(input(f"\nDeseja realizar um novo filtro?:\n1. {types_filters["1"].capitalize()} \n2. {types_filters["2"].capitalize()}\n3. {types_filters["3"].capitalize()}\n4. Sair \nDigite o tipo para filtrar: ")).strip().lower()
        elif type_filter in types_filters:
            errors = 0
            break
        elif type_filter not in types_filters:
            print("\nOpção inválida. Tente novamente.\nAtente-se, digite somente o numero correspondente a sua opção.")
            errors += 1
    
    if types_filters[type_filter] == types_filters["1"]:
        while True:
            value = str(input(f"\nTipos: \n1. {types_of_types['1'].capitalize()}\n2. {types_of_types['2'].capitalize()}\n3. {types_of_types['3'].capitalize()} \nDigite o tipo que deseja filtrar: ")).strip().lower()
            if errors > 3:
                return
            elif value in types_of_types:
                print_csv_filter_type(types_of_types[value])
                break
            elif value not in types_of_types:
                print("\nOpção inválida. Tente novamente.\nAtente-se, digite somente o numero correspondente a sua opção.")
                errors += 1
    elif types_filters[type_filter] == types_filters["2"]:
        while True:
            try:
                first_date = dt.datetime.strptime(input(f'Informe a data inicial do periodo que deseja filtrar. Formato(dd/mm/aaaa): ').strip(), '%d/%m/%Y').date()
                last_date = dt.datetime.strptime(input(f'Informe a data final do periodo que deseja filtrar. Formato(dd/mm/aaaa): ').strip(), '%d/%m/%Y').date()
                print_csv_filter_date(first_date, last_date)
                return
            except ValueError as e:
                print('Informe um valor valido.')
    elif types_filters[type_filter] == types_filters["3"]:
        while True:
            try:
                first_value = float(input(f'Informe o valor inicial que deseja filtrar: ').strip())
                last_value = float(input(f'Informe o valor final que deseja filtrar: ').strip())
                print_csv_filter_value(first_value, last_value)
                return
            except ValueError as e:
                print('Informe um valor valido.')      

def delete_record():
    """Delete um registro"""
    file_path = files_paths()
    print('\n=== Deletar Registros ===')

    print_all_csv()

    with open(file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        while True:
            target_id = input('Informe o ID da transação que deseja excluir, caso não saiba o id consulte através da função consultar.\nID:')
            confere = [row for row in csv_reader if row['id_transacao'] == target_id]
            try:
                if confere[0]:
                    break
            except IndexError as e:
                print('\nvalor invalido, digito um novo id')
        rows = [row for row in csv_reader if row['id_transacao'] != target_id]
        fieldnames = csv_reader.fieldnames

    with open(file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(rows)

    print(f'Registro de id {target_id} foi excluido')

def update_record(current_date):
    """Atualiza o registro
    """
    file_path = files_paths()
    types_of_types = {
        "1": "receita",
        "2": "despesa",
        "3": "investimento"
    }

    print('\n=== Atualizar Registros ===')

    print_all_csv()
    id = str(input('Qual o ID da transação que deseja atualizar?\nID:'))

    with open(file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        fieldnames = csv_reader.fieldnames
        fixed_columns = ['taxa','id_transacao', 'dt_criacao', 'dt_atualizacao']
        alterable_columns = [coluna for coluna in fieldnames if coluna not in fixed_columns]
        
        for idx, coluna in enumerate(alterable_columns, start=1):
            print(f"{idx}. {coluna}")
        
        target_column_index = int(input("Digite o número da coluna que deseja alterar: ")) - 1
        target_column = alterable_columns[target_column_index]
        
        if target_column_index == 0:
            new_value = input(f"Digite o novo valor para a coluna '{target_column}'\n1. Receita\n2. Despesa\n3. Investimento\nNúmero do tipo: ")
            new_value = types_of_types[new_value]
        elif target_column_index == 1:
            new_value = input(f"Digite o novo valor para a coluna '{target_column}: ")

        lines = []
        
        for line in csv_reader:
            if line['id_transacao'] == id:
                line[target_column] = new_value
                line['dt_atualizacao'] = current_date 
                if new_value == types_of_types['1']:
                    line['taxa'] = ''
                    try:
                        line['valor'] = str(line['valor']).replace('-','')
                    except Exception as e:  # FIXME: Aquela gambiarrinha só para tornar o valor da despesa positivo novamente, vai dar erro caso o valor já esteja positivo. Se o valor já for positivo tá tudo certo.
                        pass
                elif new_value == types_of_types['2']:
                    line['taxa'] = ''
                    line['valor'] = line['valor'] * -1
                elif new_value == types_of_types['3']:
                    taxa = float(input('Informe a taxa: '))
                    line['taxa'] = taxa
                    try:
                        line['valor'] = str(line['valor']).replace('-','') 
                    except Exception as e: # FIXME: Aquela gambiarrinha só para tornar o valor da despesa positivo novamente, vai dar erro caso o valor já esteja positivo. Se o valor já for positivo tá tudo certo.
                        pass
            lines.append(line)

    with open(file_path, mode='w', newline='') as csv_file:
        escritor = csv.DictWriter(csv_file, fieldnames=fieldnames)
        escritor.writeheader()
        escritor.writerows(lines)

    print("Linha atualizada com sucesso.")
    print_all_csv()

def upload() -> dict:
    """Traz o arquivo e guarda dentro de um dicionario.
    """

def closure(current_date: dt.datetime) -> None:
    """
    Função de encerramento do programa.
    Args:
        current_date (dt.datetime): Dia atual.
    """
    while True:
        answer = str(input(f"\nDeseja realizar uma nova operação: \n1. Sim \n2. Não\nDigite o número correspondente: ")).strip().lower()
        if  answer == '1':
            main(current_date)
        elif answer == '2':
            break
        elif answer != '1' and answer != '2':
            print("\nOpção inválida. Tente novamente.\nAtente-se, digite somente o numero correspondente a sua opção.")
            
    print('\nObrigado por utilizar nossos serviços') 
    sys.exit()

def save_file(type_record: str, valor: float, current_date: dt.datetime, dt_atulizacao: dt.datetime | None = None, taxa: float | None = None) -> None:
    """
    Salva o arquivo.

    Args:
        type_record (str): Tipo do registro.
        valor (float): Valor do registro.
        current_date (dt.datetime): Data atual.
        dt_atulizacao (dt.datetime | None, optional): Data de atualização. Defaults to None.
        taxa (float | None, optional): Taxa do investimento. Defaults to None.
    """    
    file_path = files_paths() 
    file_columns = ['id_transacao', 'dt_criacao', 'tipo', 'valor', 'taxa', 'dt_atualizacao']  
    first_id = 1
    
    try:
        with open(file_path, mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            lines = list(csv_reader)
            
            ids = [int(line[0]) for line in lines if line[0].isdigit()]
             
            if ids:
                last_id = max(ids)
                first_id = last_id + 1
    except FileNotFoundError:
        lines = [file_columns]

    new_line = [str(first_id), current_date, type_record,valor, taxa, dt_atulizacao]

    lines.append(new_line)

    with open(file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(lines)

    print(f'Novo registro adicionado com ID {first_id}') 

def new_record(insert_type: dict, current_date: dt.datetime, errors: int = 0) -> None:
    """
    Registra um novo registro e caso o arquivo não exista essa função faz a criação.
    Args:
        insert_type (dict): Tipo de inserções disponiveis.
        current_date (dt.datetime): Dia atual
    """    
    insert_type = insert_type
    current_date = current_date
    print('\n=== Inserir Novo Registro ===')

    while True:
        type_record = str(input(f"Escolha uma opção:\n1. {insert_type['1'].capitalize()}\n2. {insert_type['2'].capitalize()}\n3. {insert_type['3'].capitalize()}\nDigite o número correspondente: ")).strip().lower()
        if errors > 3:
            return
        elif type_record in insert_type:
            try:
                valor = float(input("Digite o valor que deseja inserir: "))
                break
            except ValueError as e:
                print("\nOpção inválida. Tente novamente.\nAtente-se, digite somente o numero correspondente a sua opção.")
        elif type_record not in insert_type:
            print("\nOpção inválida. Tente novamente.\nAtente-se, digite somente o numero correspondente a sua opção.")
            errors += 1

    if insert_type[type_record] == insert_type['1']:
        save_file(insert_type[type_record], valor, current_date)
    elif insert_type[type_record] == insert_type['2']:
        save_file(insert_type[type_record], valor * -1, current_date)
    elif insert_type[type_record] == insert_type['3']:
        taxa = float(str(input(f"Informe a taxa de juros diaria: ")).replace(',','.'))
        save_file(insert_type[type_record], valor, current_date, taxa=taxa)

def user_input(operations: dict, errors: int = 0) -> str:
    """
    Pergunta ao user o tipo de operação que será realizada. 
    Args:
        operations (dict): Tipo de operações disponiveis.
        errors (int, optional): Quantidade de vezes que o usuario escolheu uma opção invalida. Defaults to 0.
    Returns:
        str: Resposta do usuario
    """
    operations = operations
    print('\n=== MENU ===')
    while True:
        user_response = str(input(f"Escolha uma opção:\n1. {operations['1'].capitalize()}\n2. {operations['2'].capitalize()}\n3. {operations['3'].capitalize()}\n4. {operations['4'].capitalize()}\n5. {operations['5'].capitalize()} \nDigite o número correspondente: ")).strip().lower()
        if errors > 3:
            return user_response
        elif user_response in operations:
            return user_response
        elif user_response not in operations and errors <= 3:
            print("\nOpção inválida. Tente novamente.\nAtente-se, digite somente o numero correspondente a sua opção.")
            errors +=1
    
def dicts() -> dict:
    """
    Função que cria/armazena e retorna os dicionarios utilizados.

    Returns:
        dict: Retorna diversos dicionarios de dados.
    """    
    operations = {
        '1': "inserir",
        '2': "consultar",
        '3': "excluir",
        '4': "atualizar",
        '5': 'extrair'
    }

    insert_type = {
        '1': "receita",
        '2': "despesa",
        '3': "investimento",
    }

    return operations, insert_type

def files_paths() -> str:
    """
    Função que armazena o path do arquivo.
    Returns:
        str: Caminho do arquivo
    """    
    file_path = 'base.csv'
    return file_path
    
def main(current_date: dt.datetime) -> None:
    """
    Função principal, organiza o programa e inicia outras funções.
    """
    current_date = current_date
    
    operations, insert_type = dicts()

    user_response = user_input(operations)

    try:
        if operations[user_response] == operations['1']:
            new_record(insert_type, current_date)
        elif operations[user_response] == operations['2']:
            consult_record()
        elif operations[user_response] == operations['3']:
            delete_record()
        elif operations[user_response] == operations['4']:
            update_record(current_date)
        elif operations[user_response] == operations['5']:
            export()
    except KeyError as e:
        print('Você fez várias escolhas incorretas. Reinicie o programa para continuar.')

    closure(current_date)

if __name__ == "__main__":
    current_date = dt.datetime.now()

    print('\nSeja Bem-vindo(a)!')
    main(current_date)