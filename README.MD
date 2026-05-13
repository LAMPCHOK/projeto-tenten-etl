# Projeto Tenten ETL

Sistema de padronização e consolidação automática de planilhas ERP para múltiplas lojas.

---

# Objetivo

Automatizar o tratamento de planilhas de:

- vendas
- compras

exportadas do ERP das lojas:

- Tenten
- Casas das Mesas
- Espaço Móveis

O sistema:

- detecta arquivos automaticamente
- valida nomes
- limpa colunas
- padroniza estrutura
- consolida os dados
- gera arquivos finais prontos para dashboard e BI

---

# Estrutura do Projeto

```text
projeto_tente/
├── app.py
├── requirements.txt
├── README.md
├── uploads/
├── processados/
├── venv/