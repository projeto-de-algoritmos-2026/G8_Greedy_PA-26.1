import os
import random

from item import Item
from knapsack import knapsack_01


CAPACIDADE_TOTAL = 15
LARGURA_TELA = 76

CATALOGO_MOCHILA = [
    Item("Mapa Rasgado", 2, 1),
    Item("Tocha Gasta", 1, 1),
    Item("Racao de Viagem", 3, 3),
    Item("Corda Curta", 2, 2),
    Item("Livro Umido", 3, 4),
    Item("Adaga Enferrujada", 2, 3),
    Item("Cantimplora", 1, 2),
    Item("Pedra Runica Apagada", 4, 5),
]

CATALOGO_BAU = [
    Item("Espada Antiga", 4, 10),
    Item("Pocao Rara", 2, 6),
    Item("Armadura Pesada", 7, 14),
    Item("Anel Mistico", 1, 5),
    Item("Machado Sombrio", 5, 12),
    Item("Elmo de Ferro", 3, 7),
    Item("Gema Carmesim", 2, 9),
    Item("Cajado de Osso", 4, 11),
    Item("Luvas do Ladino", 1, 4),
    Item("Escudo Lunar", 6, 13),
    Item("Pergaminho Arcano", 2, 8),
    Item("Botas Silenciosas", 3, 6),
]


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\n>> Pressione Enter para continuar...")


def linha(char="="):
    return char * LARGURA_TELA


def titulo(texto, subtitulo=None):
    print(linha("="))
    print(f"|| {texto.center(LARGURA_TELA - 6)} ||")
    print(linha("="))
    if subtitulo:
        print(f">> {subtitulo}")
        print(linha("-"))


def caixa(texto):
    print("+" + "-" * (LARGURA_TELA - 2) + "+")
    for linha_texto in texto.splitlines():
        print("| " + linha_texto[: LARGURA_TELA - 4].ljust(LARGURA_TELA - 4) + " |")
    print("+" + "-" * (LARGURA_TELA - 2) + "+")


def barra_capacidade(usado, total, largura=24):
    preenchido = round((usado / total) * largura) if total else 0
    preenchido = min(preenchido, largura)
    vazio = largura - preenchido
    return f"[{'#' * preenchido}{'.' * vazio}] {usado}/{total}"


def desenhar_mapa(restante):
    print(r"             /\                         __________________")
    print(r"            /  \       HER0I           /                  \ ")
    print(r"           /____\       @             /   BAU DA CRIPTA    \ ")
    print(r"          /|    |\     /|\           /______________________\ ")
    print(r"         /_|____|_\    / \             | [] [] [] [] [] |")
    print(r"            ||                         |________________|")
    print(r"     MOCHILA PARCIALMENTE CHEIA")
    print(f"     espaco restante: {restante}")


def capacidade_restante(mochila):
    return CAPACIDADE_TOTAL - sum(item.peso for item in mochila)


def criar_estado_inicial(seed=None):
    gerador = random.Random(seed)
    catalogo_mochila = list(CATALOGO_MOCHILA)
    catalogo_bau = list(CATALOGO_BAU)
    gerador.shuffle(catalogo_mochila)
    gerador.shuffle(catalogo_bau)

    mochila = []
    peso_alvo = gerador.randint(5, 8)

    for item in catalogo_mochila:
        if sum(i.peso for i in mochila) + item.peso <= peso_alvo:
            mochila.append(item)
        if sum(i.peso for i in mochila) >= peso_alvo:
            break

    if not mochila:
        mochila.append(catalogo_mochila[0])

    quantidade_bau = gerador.randint(5, 7)
    itens_bau = catalogo_bau[:quantidade_bau]

    return mochila, itens_bau


def exibir_introducao():
    limpar_tela()
    titulo("KNAPSACK MUD", "O Bau do Guardiao da Cripta")
    caixa(
        "Você derrotou o Guardião da Cripta. No silêncio da sala final,\n"
        "um baú antigo se abre com armas, reliquias e tesouros. Sua mochila\n"
        "ja esta parcialmente cheia, entao sera preciso escolher com cuidado."
    )
    pausar()


def exibir_menu():
    limpar_tela()
    titulo("SALA DO TESOURO", "Escolha sua proxima acao")
    print(r"        .-.")
    print(r"       (o o)     O bau range. A mochila pesa no ombro.")
    print(r"       | O \     O algoritmo aguarda sua ordem.")
    print("        \\   \\")
    print(r"         `~~~'")
    print()
    print("+----+----------------------------------------------+")
    print("| 1  | Ver mochila                                  |")
    print("| 2  | Ver itens do bau                             |")
    print("| 3  | Recolher melhores itens usando Knapsack      |")
    print("| 4  | Ver explicacao do algoritmo                  |")
    print("| 5  | Ver tabela dinamica gerada pelo algoritmo    |")
    print("| 6  | Sair                                         |")
    print("+----+----------------------------------------------+")
    return input("\n>> Escolha uma opcao: ").strip()


def exibir_itens(titulo, itens):
    print(f"\n{titulo}")
    print("+" + "-" * 54 + "+")

    if not itens:
        print("| Nenhum item.".ljust(55) + "|")
        print("+" + "-" * 54 + "+")
        return

    for indice, item in enumerate(itens, start=1):
        conteudo = f"{indice:02d}. {item.nome:<24} peso {item.peso:>2}  valor {item.valor:>2}"
        print("| " + conteudo[:52].ljust(52) + " |")
    print("+" + "-" * 54 + "+")


def ver_mochila(mochila):
    limpar_tela()
    peso_ocupado = sum(item.peso for item in mochila)
    restante = CAPACIDADE_TOTAL - peso_ocupado

    titulo("MOCHILA DO AVENTUREIRO", "Itens que ja ocupam espaco antes do bau")
    desenhar_mapa(restante)
    exibir_itens("Itens na mochila", mochila)
    print("\nCapacidade")
    print("  Ocupado :", barra_capacidade(peso_ocupado, CAPACIDADE_TOTAL))
    print("  Livre   :", barra_capacidade(restante, CAPACIDADE_TOTAL))
    pausar()


def ver_bau(itens_bau):
    limpar_tela()
    titulo("BAU DA CRIPTA", "Itens candidatos para o 0/1 Knapsack")
    print(r"          ______________________________")
    print(r"         /______________________________\ ")
    print(r"         |  $   ?   !   *   $   ?   !  |")
    print(r"         |______________________________|")
    exibir_itens("Itens no bau", itens_bau)
    pausar()


def recolher_melhores_itens(mochila, itens_bau, estado):
    limpar_tela()
    restante = capacidade_restante(mochila)
    itens_candidatos = list(itens_bau)

    titulo("OTIMIZACAO DO SAQUE", "O Knapsack avalia o bau sem remover itens antigos")
    print(r"        [MOCHILA] ---- capacidade livre ----> [BAU]")
    print(f"        {barra_capacidade(CAPACIDADE_TOTAL - restante, CAPACIDADE_TOTAL)}")
    print(f"\nEspaco disponivel para o algoritmo: {restante}")

    escolhidos, valor_total, peso_total, dp = knapsack_01(itens_candidatos, restante)
    nomes_escolhidos = {item.nome for item in escolhidos}
    deixados = [item for item in itens_bau if item.nome not in nomes_escolhidos]

    mochila.extend(escolhidos)
    itens_bau[:] = deixados
    estado["ultima_execucao"] = {
        "capacidade": restante,
        "itens_candidatos": itens_candidatos,
        "itens_escolhidos": escolhidos,
        "valor_total": valor_total,
        "peso_total": peso_total,
        "dp": dp,
    }

    print("\nResultado")
    print(linha("-"))
    exibir_itens("Coletados", escolhidos)
    exibir_itens("Deixados no bau", deixados)
    print("\nResumo do saque")
    print("+----------------------+------------------------------+")
    print(f"| Peso usado no saque  | {peso_total:>2}/{restante:<25}|")
    print(f"| Valor obtido         | {valor_total:<28}|")
    print(f"| Mochila depois       | {barra_capacidade(sum(item.peso for item in mochila), CAPACIDADE_TOTAL, 18):<28}|")
    print("+----------------------+------------------------------+")

    if escolhidos:
        print(
            "\nA escolha foi feita por otimizacao: o algoritmo comparou combinacoes\n"
            "possiveis, em vez de pegar apenas o item de maior valor individual."
        )
    else:
        print("\nNenhum item coube na capacidade restante.")

    pausar()


def explicar_algoritmo():
    limpar_tela()
    titulo("COMO O FEITICO KNAPSACK PENSA", "Programacao dinamica em linguagem simples")
    caixa(
        "O problema da mochila pergunta quais itens devem ser levados quando\n"
        "existe um limite de peso. Neste MUD, peso e o espaco que um item ocupa,\n"
        "valor e o beneficio do item, e capacidade e o peso maximo que ainda cabe.\n\n"
        "Nem todos os itens podem ser pegos porque a mochila ja tem objetos e o\n"
        "espaco restante e limitado. Como cada item do bau so pode ser escolhido\n"
        "uma vez, este e o problema 0/1 Knapsack.\n\n"
        "A programacao dinamica monta uma tabela dp[i][c], onde i representa os\n"
        "primeiros itens considerados e c representa uma capacidade possivel.\n"
        "Para cada item, a tabela decide entre nao pegar o item ou pegar o item,\n"
        "caso ele caiba. O maior valor entre essas duas escolhas fica gravado.\n\n"
        "Complexidade: O(n * W), onde n e o numero de itens e W e a capacidade."
    )
    print("\nFormula da decisao")
    print("+--------------------------------------------------------------+")
    print("| se o item nao cabe: dp[i][c] = dp[i - 1][c]                  |")
    print("| se cabe: max(nao pegar, valor do item + melhor resto)        |")
    print("+--------------------------------------------------------------+")
    pausar()


def imprimir_tabela_dp(estado, mochila, itens_bau):
    limpar_tela()
    execucao = estado.get("ultima_execucao")

    if execucao is None:
        capacidade = capacidade_restante(mochila)
        escolhidos, valor_total, peso_total, dp = knapsack_01(itens_bau, capacidade)
        execucao = {
            "capacidade": capacidade,
            "itens_candidatos": list(itens_bau),
            "itens_escolhidos": escolhidos,
            "valor_total": valor_total,
            "peso_total": peso_total,
            "dp": dp,
        }
        estado["ultima_execucao"] = execucao

    capacidade = execucao["capacidade"]
    itens = execucao["itens_candidatos"]
    dp = execucao["dp"]
    escolhidos = execucao["itens_escolhidos"]
    peso_total = execucao["peso_total"]
    valor_total = execucao["valor_total"]

    titulo("TABELA DINAMICA DP", "Cada linha considera mais um item do bau")
    print("LEITURA GUIADA")
    print("+--------------------------------------------------------------------------+")
    print("| Cada numero responde: qual e o melhor VALOR que consigo carregar aqui?  |")
    print("| Linhas = itens liberados para o algoritmo. Colunas = espaco disponivel. |")
    print("| A matriz cresce da esquerda para a direita e de cima para baixo.         |")
    print("+--------------------------------------------------------------------------+")
    print(f"\nCapacidade usada pelo algoritmo: {capacidade}")
    print("A celula final aparece marcada com < >.\n")

    print("Capacidade ->".ljust(22) + "".join(str(c).rjust(5) for c in range(capacidade + 1)))
    cabecalho = "Itens considerados".ljust(22) + "".join("|".rjust(5) for _ in range(capacidade + 1))
    print(cabecalho)
    print("-" * len(cabecalho))

    for i, valores_linha in enumerate(dp):
        nome = "nenhum item" if i == 0 else f"+ {itens[i - 1].nome}"[:21]
        valores = []
        for c, valor in enumerate(valores_linha):
            if i == len(dp) - 1 and c == capacidade:
                valores.append(f"<{valor}>".rjust(5))
            else:
                valores.append(str(valor).rjust(5))
        print(nome.ljust(22) + "".join(valores))

    print("\n" + linha("-"))
    print("RESUMO DA MATRIZ")
    print(f"Melhor valor final: dp[{len(itens)}][{capacidade}] = {dp[-1][-1]}")
    print(f"Peso usado pela solucao: {peso_total}/{capacidade}")
    print("Itens reconstruidos:", ", ".join(item.nome for item in escolhidos) or "nenhum")
    print("\nCOMO INTERPRETAR A ULTIMA CELULA")
    print(
        f"O algoritmo olhou todos os {len(itens)} itens candidatos e todas as capacidades\n"
        f"de 0 ate {capacidade}. O maior valor possivel sem passar do limite foi {valor_total}."
    )

    if escolhidos:
        print("\nCaminho final escolhido:")
        for item in escolhidos:
            print(f"  -> {item.nome}: ocupa {item.peso}, soma valor {item.valor}")
    else:
        print("\nNenhum item foi escolhido porque nada coube na capacidade disponivel.")

    pausar()


def main():
    mochila, itens_bau = criar_estado_inicial()
    estado = {"ultima_execucao": None}

    exibir_introducao()

    while True:
        opcao = exibir_menu()

        if opcao == "1":
            ver_mochila(mochila)
        elif opcao == "2":
            ver_bau(itens_bau)
        elif opcao == "3":
            recolher_melhores_itens(mochila, itens_bau, estado)
        elif opcao == "4":
            explicar_algoritmo()
        elif opcao == "5":
            imprimir_tabela_dp(estado, mochila, itens_bau)
        elif opcao == "6":
            limpar_tela()
            titulo("FIM DA EXPEDICAO")
            print(r"        __")
            print(r"   ____/ /__  fim")
            print(r"  / __  / _ \ ")
            print(r" / /_/ /  __/")
            print(r" \__,_/\___/ ")
            print("\nVoce deixa a cripta com os itens escolhidos.")
            break
        else:
            limpar_tela()
            titulo("COMANDO DESCONHECIDO")
            print(r"        ???")
            print(r"       (o_o)   A cripta nao entendeu sua ordem.")
            print("\nOpcao invalida.")
            pausar()


if __name__ == "__main__":
    main()
