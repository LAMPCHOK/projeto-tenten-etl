import pandas as pd
import re
from pathlib import Path

UPLOADS_DIR = Path("uploads")
PROCESSADOS_DIR = Path("processados")

PROCESSADOS_DIR.mkdir(exist_ok=True)

LOJAS_VALIDAS = {
    "tenten",
    "casasdasmesas",
    "espacomoveis"
}


# =========================================
# VALIDAR NOME DO ARQUIVO
# =========================================

def validar_nome_arquivo(nome_arquivo: str):

    nome = nome_arquivo.replace(".xlsx", "").lower()

    partes = nome.split("_")

    if len(partes) != 3:
        raise ValueError(
            "Use o padrão: relatorio_venda_tenten.xlsx"
        )

    tipo_arquivo, categoria, loja = partes

    if tipo_arquivo != "relatorio":
        raise ValueError(
            "O arquivo deve começar com 'relatorio'."
        )

    if categoria not in {"venda", "compra"}:
        raise ValueError(
            "Categoria inválida."
        )

    if loja not in LOJAS_VALIDAS:
        raise ValueError(
            "Loja inválida."
        )

    return categoria, loja


# =========================================
# LIMPAR COLUNAS
# =========================================

def limpar_colunas(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.replace("_x000D_", " ", regex=False)
        .str.replace("\n", " ", regex=False)
        .str.strip()
        .str.lower()
    )

    df.columns = [
        re.sub(r"[^a-z0-9]+", "_", col).strip("_")
        for col in df.columns
    ]

    return df


# =========================================
# TRATAR VENDAS
# =========================================

def tratar_venda(
    df: pd.DataFrame,
    loja: str
) -> pd.DataFrame:

    colunas = [
        "setor",
        "qtd_total_venda",
        "qtd_total_compra",
        "valor_total_compra",
        "valor_total_venda"
    ]

    df = df[colunas].copy()

    df["loja"] = loja

    return df


# =========================================
# TRATAR COMPRAS
# =========================================

def tratar_compra(
    df: pd.DataFrame,
    loja: str
) -> pd.DataFrame:

    
    colunas = [
        "nome",
        "emiss_o",
        "valor_nota"
    ]

    df = df[colunas].copy()

    df = df.rename(
        columns={
            "nome": "fornecedor",
            "emiss_o": "emissao",
        }
    )

    df["loja"] = loja

    return df


# =========================================
# PROCESSAR ARQUIVO
# =========================================

def processar_arquivo(caminho_arquivo: Path):

    categoria, loja = validar_nome_arquivo(
        caminho_arquivo.name
    )

    df = pd.read_excel(caminho_arquivo)

    df = limpar_colunas(df)

    if categoria == "venda":

        df_saida = tratar_venda(
            df,
            loja
        )

        nome_saida = f"vendas_{loja}.xlsx"

    else:

        df_saida = tratar_compra(
            df,
            loja
        )

        nome_saida = f"compras_{loja}.xlsx"

    print(
        f"Processado {caminho_arquivo.name} com sucesso!"
    )

    return categoria, df_saida


# =========================================
# MAIN
# =========================================

def main():
    lista_vendas = []
    lista_compras = []

    arquivos = list(
        UPLOADS_DIR.glob("*.xlsx")
    )

    if not arquivos:
        print(
            "Nenhum arquivo XLSX encontrado."
        )
        return

    for arquivo in arquivos:

        try:

            categoria, df_saida = processar_arquivo(arquivo)
            if categoria == "venda":
                lista_vendas.append(df_saida)
            else: 
                lista_compras.append(df_saida)

        except Exception as e:

            print(
                f"Erro em {arquivo.name}: {e}"
            )


    # =========================================
    # CONSOLIDAR vendas
    # =========================================

    if lista_vendas:

        df_vendas_final = pd.concat(
            lista_vendas,
            ignore_index=True
        )

        df_vendas_final.to_excel(
            PROCESSADOS_DIR / "todas_vendas.xlsx",
            index=False
        )

        print ("Arquivo consolidado de vendas criado!")
            # =========================================
    # CONSOLIDAR COMPRAS
    # =========================================

    if lista_compras:

        df_compras_final = pd.concat(
            lista_compras,
            ignore_index=True
        )

        df_compras_final.to_excel(
            PROCESSADOS_DIR / "todas_compras.xlsx",
            index=False
        )

        print ("Arquivo consolidado de compras criado!")


# =========================================
# INICIAR
# =========================================

if __name__ == "__main__":
    main()