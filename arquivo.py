class Arquivo:

    # Atributos de um arquivo regular
    nome = None
    tamanho = None
    tc = None     # Tempo de criacao
    tm = None     # Tempo de modificacao
    ta = None     # Tempo de acesso
    dados = None

    def __init__(self, nome):
        # se o nome não existir no sistema, cria um novo
        return None

    def touch(self):
        #se o arquivo existir
        #tm = tempo atual, ta tbm?

        #se não
        #__init__(nome)

    def cp(self, origem):
        # copia informacoes de um arquivo de origem para um arquivo destino
        # se o arquivo destino nao existir, __init__(destino)
	
    def rm(self):
        # remove do sistema de arquivos e apaga da FAT (não precisa zerar os bits ocupados)
