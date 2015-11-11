class SistemaArquivos:

    raiz = None
    diretorios = []
    espaco = None
    FAT = []

    def __init__(self, nome):
        # se o sistema de arquivos nao existe, criar um novo
