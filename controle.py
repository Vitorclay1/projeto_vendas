from PyQt5 import  uic,QtWidgets
import pyodbc

dados_conexao = (
    "Driver={SQL Server};"
    "Server=VITOR-CLAY;"
    "Database=caritas;"
)
conexao = pyodbc.connect(dados_conexao)

def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_4.text()
    linha3 = formulario.lineEdit_5.text()
    
    categoria = ""

    if formulario.radioButton_3.isChecked() :
        categoria = "Eletronicos"
        print("Categoria Eletronicos selecionada")
        
    elif formulario.radioButton_2.isChecked() :

        categoria = "Informatica"
        print("Categoria Informatica selecionada")

    else :
        categoria = "Alimentos"
        print("Categoria Alimentos selecionada")

    print("Código:",linha1)
    print("Descricao:",linha2)
    print("Preco",linha3)
    
    cursor = conexao.cursor()
    
    cadastrar = f"INSERT INTO Vendas(codigo, descricao, preco, categoria) VALUES ({linha1},'{linha2}','{linha3}','{categoria}')"
    cursor.execute(cadastrar)
    cursor.commit()
    formulario.lineEdit.setText('')
    formulario.lineEdit_4.setText('')
    formulario.lineEdit_5.setText('')

def chama_segunda_tela():
    segunda_tela.show()

    cursor = conexao.cursor()
    comando_SQL = "SELECT * FROM Vendas"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
           segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 
           
def chamar_tela_pesquisa():
    
    tela_pesquisa.show()
    
    pesquisa = tela_pesquisa.lineEdit.text()

    cursor = conexao.cursor()
    if pesquisa.isnumeric():
        consulta_sql = f"SELECT id, codigo, descricao, preco, categoria FROM Vendas WHERE codigo = '{pesquisa}'"
    else:
        consulta_sql = f"SELECT id, codigo, descricao, preco, categoria FROM Vendas WHERE preco = '{pesquisa}'"
    cursor.execute(consulta_sql)
    dados_lidos = cursor.fetchall()
    print(pesquisa)

    tela_pesquisa.tableWidget.setRowCount(len(dados_lidos))
    tela_pesquisa.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
           tela_pesquisa.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 



def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM Vendas")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM Vendas WHERE id="+ str(valor_id))

def editar_dados():
    global numero_id

    linha = segunda_tela.tableWidget.currentRow()
    
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM Vendas")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM VEndas WHERE id="+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
    numero_id = valor_id


def salvar_valor_editado():
    global numero_id

    # ler dados do lineEdit
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    # atualizar os dados no banco
    cursor = conexao.cursor()
    cursor.execute("UPDATE Vendas SET codigo = '{}', descricao = '{}', preco = '{}', categoria ='{}' WHERE id = {}".format(codigo,descricao,preco,categoria,numero_id))
    conexao.commit()
    #atualizar as janelas
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()


app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui")
segunda_tela=uic.loadUi("listar_dados.ui")
tela_pesquisa=uic.loadUi("pesquisa_produto.ui")
tela_editar=uic.loadUi("menu_editar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
formulario.pushButton_3.clicked.connect(chamar_tela_pesquisa)
tela_pesquisa.pushButton_3.clicked.connect(chamar_tela_pesquisa)
segunda_tela.pushButton.clicked.connect(excluir_dados)
segunda_tela.pushButton_2.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_valor_editado)
tela_pesquisa.pushButton.clicked.connect(excluir_dados)
tela_pesquisa.pushButton_2.clicked.connect(editar_dados)



formulario.show()
app.exec()