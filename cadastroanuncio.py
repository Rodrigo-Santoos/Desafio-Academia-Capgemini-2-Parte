from datetime import datetime
import sqlite3

# --------------INICIO-----------------

# Funçao para calcular as visualizaçoes      
def my_views(views): 
    # A cada 100 pessoas que visualizam o anúncio 12 clicam nele.  
    cliq = float(views) / 100 * 12
    # A cada 20 pessoas que clicam no anúncio 3 compartilham nas redes sociais.    
    compart = float(cliq) / 20 * 3 
    # Cada compartilhamento nas redes sociais gera 40 novas visualizações.   
    totViews = float(compart) * 40  
    return totViews 

# Funçao para calcular os cliques
def my_cliq(views):   
    cliq = float(views) / 100 * 12     
    return cliq 

# Funçao para calcular os compartilhamentos
def my_compart(views):   
    cliq = float(views) / 100 * 12    
    compart = float(cliq) / 20 * 3    
    return compart 

v = 1
opc = 0
while v != 0 and opc != 5:
    print('\033[33m=-=' * 20)
    print('\033[31mCadastro de anúncios!')
    print('\033[33m=-=' * 20)
# -------------------------------------
    print('''[ 0 ] Criar tabela.
[ 1 ] Cadastrar anúncio.
[ 2 ] Ver relatório de todos os dados.
[ 3 ] Ver relatório apartir do nome.
[ 4 ] Ver relatório apartir da data inicio e data fim.
[ 5 ] Sair do programa.''')
    print('\033[33m=-=' * 20)
    print('')
    opc = int(input('\033[31mDigite sua opção:\033[m'))
    if opc == 0:
       # conectando...
       conn = sqlite3.connect('clientes.db')
       cursor = conn.cursor()
       
       # deleta se existe
       cursor.execute("""
       DROP TABLE IF EXISTS 'anuncios';
       """)
       
       # criando a tabela caso não existir
       cursor.execute("""
        CREATE TABLE IF NOT EXISTS 'anuncios' 
        (
        'id' INTEGER PRIMARY KEY AUTOINCREMENT, 
        'NomeAnuncio' VARCHAR(255) NOT NULL, 
        'NomeCliente' VARCHAR(255) NOT NULL, 
        'DataInicio' DATETIME NOT NULL, 
        'DataTermino' DATETIME NOT NULL, 
        'InvestimentoDia' DOUBLE PRECISION NOT NULL, 
        'ValorTotalInvestido' DOUBLE PRECISION NOT NULL, 
        'QtdMaxVizualizacao' DOUBLE PRECISION NOT NULL, 
        'QtdMaxClique' DOUBLE PRECISION NOT NULL, 
        'QtdMaxCompartilhamento' DOUBLE PRECISION NOT NULL 
        );
        """)
        # desconectando...


    elif opc == 1:
        # solicitando os dados ao usuário
        p_NomeAnuncio = input('Insira o nome do anúncio: ')
        p_NomeCliente = input('Insira o nome do Cliente: ')
        p_DataInicio = input('Insira a data de início neste formato aaaa-mm-dd: ')
        p_DataTermino = input('Insira a data de término neste formato aaaa-mm-dd: ')
        p_InvestimentoDia = float( input("Favor informar o valor investido em reais (R$): ") ) 

        # Data inicial para calculo de diferença de dias
        d1 = datetime.strptime(p_DataInicio, '%Y-%m-%d')

        # Data final para calculo de diferença de dias
        d2 = datetime.strptime(p_DataTermino, '%Y-%m-%d')

        # Realizamos o calculo da quantidade de dias
        quantidade_dias = abs((d2 - d1).days)

        # Valor Total Investido em dias
        p_ValorTotalInvestido  = float(p_InvestimentoDia * quantidade_dias)

        # 30 pessoas visualizam o anúncio original (não compartilhado) a cada R$ 1,00 investido.
        qtdValor  = float(p_ValorTotalInvestido * 30)

        # Valoriza 0 1ª Ciclo
        result1 = 0
        result2 = 0
        Totalcliq = 0
        Totalcompart = 0
        result = float(qtdValor)
        TotalViews = float(result)

        # repeticao de 4 Ciclo
        # O mesmo anúncio é compartilhado no máximo 4 vezes em sequência.
        for x in range(4):
            result = float(my_views(result))
            result1 = float(my_cliq(result))
            result2 = float(my_compart(result))
            Totalcliq = float(Totalcliq) + float(result1)
            Totalcompart = float(Totalcompart) + float(result2)
            TotalViews = float(TotalViews) + float(result) 

        p_QtdMaxVizualizacao = float(TotalViews)
        p_QtdMaxClique = float(Totalcliq)
        p_QtdMaxCompartilhamento = float(Totalcompart)

        # conectando...
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()

        # inserindo dados na tabela
        cursor.execute("""
        INSERT INTO anuncios ( NomeAnuncio, NomeCliente, DataInicio, DataTermino, InvestimentoDia,ValorTotalInvestido,QtdMaxVizualizacao,QtdMaxClique,QtdMaxCompartilhamento) 
        VALUES (?,?,?,?,?,?,?,?,?)
        """, (p_NomeAnuncio, 
            p_NomeCliente, 
            p_DataInicio, 
            p_DataTermino, 
            p_InvestimentoDia,
            p_ValorTotalInvestido,
            p_QtdMaxVizualizacao,
            p_QtdMaxClique,
            p_QtdMaxCompartilhamento))

        conn.commit()
        print('Dados inseridos com sucesso.')
        v = int(input('\033[31mDigite 1 para voltar ao menu:\033[m'))
        
    elif opc == 2:
        # lendo todos os dados da tabela
        print('*==================== lendo todos os dados da tabela =============================================')
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM anuncios;
        """)

        records = cursor.fetchall()
        linhas = int(len(records))
        if linhas > 0 :
            for row in records:
                print("Id: ", row[0])
                print("NomeAnuncio: ", row[1])
                print("NomeCliente: ", row[2])
                print("DataInicio: ", row[3])
                print("DataTermino: ", row[4])
                print("InvestimentoDia: ", row[5])
                print("ValorTotalInvestido: ", row[6])
                print("QtdMaxVizualizacao: ", row[7])
                print("QtdMaxClique: ", row[8])
                print("QtdMaxCompartilhamento: ", row[9])
                print("\n") 
        else:
            print('\033[31mDados não cadastrado, por favor verifique a pesquisa!\033[m')
            #break

        v = int(input('\033[31mDigite 1 para voltar ao menu:\033[m'))

    elif opc == 3:
        # lendo todos os dados da tabela conforme nome pesquisado
        print('*==================== lendo todos os dados da tabela conforme nome pesquisado ====================')
        cliente = str(input('\033[36mRelatorio por nome:\033[31m'))
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM anuncios
        WHERE NomeCliente = ?;
        """, (cliente,))

        records = cursor.fetchall()
        linhas = int(len(records))
        if linhas > 0 :
            for row in records:
                print("Id: ", row[0])
                print("NomeAnuncio: ", row[1])
                print("NomeCliente: ", row[2])
                print("DataInicio: ", row[3])
                print("DataTermino: ", row[4])
                print("InvestimentoDia: ", row[5])
                print("ValorTotalInvestido: ", row[6])
                print("QtdMaxVizualizacao: ", row[7])
                print("QtdMaxClique: ", row[8])
                print("QtdMaxCompartilhamento: ", row[9])
                print("\n") 
        else:
            print('\033[31mDados não cadastrado, por favor verifique a pesquisa!\033[m')
            #break

        v = int(input('\033[31mDigite 1 para voltar ao menu:\033[m'))

    elif opc == 4:

# lendo todos os dados da tabela conforme nome data inicial
        print('*==================== lendo todos os dados da tabela em um determinado range de datas ====================')
        dtaIni = str(input('\033[36mDigite uma data inicial para pesquisa em formato aaaa-mm-dd:\033[31m'))
        dtaFim = str(input('\033[36mDigite uma data final para pesquisa em formato aaaa-mm-dd:\033[31m'))
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM anuncios
        WHERE  DataInicio >= ?
        AND  DataTermino <= ?;
        """, (dtaIni,dtaFim,))

        records = cursor.fetchall()
        linhas = int(len(records))
        if linhas > 0 :
            for row in records:
                print("Id: ", row[0])
                print("NomeAnuncio: ", row[1])
                print("NomeCliente: ", row[2])
                print("DataInicio: ", row[3])
                print("DataTermino: ", row[4])
                print("InvestimentoDia: ", row[5])
                print("ValorTotalInvestido: ", row[6])
                print("QtdMaxVizualizacao: ", row[7])
                print("QtdMaxClique: ", row[8])
                print("QtdMaxCompartilhamento: ", row[9])
                print("\n") 
        else:
            print('\033[31mDados não cadastrado, por favor verifique a pesquisa!\033[m')
            #break   
    
        v = int(input('\033[31mDigite 1 para voltar ao menu:\033[m'))
    elif opc == 5:
        print('\033[35mFim do Programa! Obrigado!!\033[m')
        break

    conn.close()