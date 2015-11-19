
from datetime import datetime

class Diretorio:

    # Atributos de um arquivo regular
    nome = None
    tc = None     # Tempo de criacao
    tm = None     # Tempo de modificacao
    ta = None     # Tempo de acesso
    cont = None   # Quantidade de elementos dentro do diretorio
    raiz = None
    
    def __init__(self, nome, raiz):
        self.raiz = raiz

    def mkdir(self, nome):
        # Nunca se tentara criar um diretorio que ja existe
        self.nome = nome
        self.ta = self.tm = self.tc = str(datetime.now())
        self.cont = 0

        end = first = FirstFit()
        if end:
            switchBitmap()
            for i in xrange(3):
                prox = FirstFit()
                if prox:
                    escreveBloco(end, struct.pack("h", prox)+struct.pack("h", self.cont))
                    end = prox
                    
                else:
                    # Nao ha mais blocos disponiveis
                    return
            escreveBloco(end, struct.pack("h", -1)+struct.pack("h", self.cont))
        else:
            # Nao ha mais blocos disponiveis
            return
        
        caminho = self.nome.split('/')

        pai = "/".join(caminho[0:len(caminho)-1])

        atualizaDiretorios(first, self.raiz, [""])


        #Falta concluir

    def atualizaDiretorios(self, first, atual, diratual):
        caminho = self.nome.split("/")
        prox, cont, conteudo = leBloco(atual)


        # Substituir pela funcao que busca o arquivo(find diretorio arquivo)
        """
        
        if diratual == caminho[0:len(caminho)-1] or diratual == "":

        else:
           
            for i in xrange(cont):
                if diratual[len(diratual)-1] == conteudo[4+i*77:16+i*77]:
                    # verifica se os nomes sao iguais
                    # encontra o ponteiro para o proximo diretorio
            atualizaDiretorios(self, first, , diratual)




             diratual = caminho[0:len(diratual)+1]
        """
