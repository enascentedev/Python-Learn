import time

def fazer_duas_vezes(f):
    def meu_pacote(*args, **kwargs):
        _ = f(*args, **kwargs)
        retorno = f(*args, **kwargs)
        return retorno
    return meu_pacote


def medir_tempo(f):
    def meu_pacote(*args, **kwargs):
        inicio = time.time()
        retorno = f(*args, **kwargs)
        final = time.time()
        print(f'A função {f.__name__} levou {round(final - inicio, 5)} segundos para executar.')
        return retorno
    return meu_pacote
