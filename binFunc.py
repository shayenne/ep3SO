def escreveDados(arquivo, dados, posicao):
    with open(arquivo, 'wb') as f:
        f.seek(posicao)
        f.write(dados)

        
def copiaArquivo(origem, destino, posicao):
    with open(origem,'rb') as f1:
        with open(destino,'wb') as f2:
            # escrever no sistema de arquivos a partir de uma posicao
            f2.seek(posicao)#f2 sera o nosso sistema de arquivos
            # posicao eh a posicao em que comecam os dados do arquivo
            while True:
                bytes=f1.read(1024)
                if bytes: 
                    for byte in bytes:
                        pass    # process the bytes if this is what you want

                    n=f2.write(bytes)
                else:
                    break

def leDados(arquivo, inicio, fim):
    with open(arquivo, 'rb') as f:
        f.seek(inicio)
        data = f.read(fim-inicio)
    return data


if __name__=="__main__":
    escreveDados("test", "ABCDEFGHSHAYENNE", 0)

    copiaArquivo("test", "me", 10)

    # le dados de um arquivo [inicio, fim)
    print leDados("me", 10, 18)
