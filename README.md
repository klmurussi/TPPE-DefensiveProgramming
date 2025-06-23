# TPPE (Trabalho Prático 1): Implementação de B-Tree em Python usando icontract

Este repositório contém a implementação de uma B-Tree (Árvore B) em Python, focando na correta aplicação de suas propriedades e no uso de **Programação por Contrato** (`icontract`) para garantir a robustez e a correção do algoritmo. O projeto inclui testes utilizando `pytest` para validação das operações.

## 📚 Visão Geral

Uma B-Tree é uma estrutura de dados de árvore de busca auto-balanceada que mantém dados classificados e permite pesquisas, acessos sequenciais, inserções e exclusões em tempo logarítmico. É comumente usada em bancos de dados e sistemas de arquivos, onde os blocos de dados são armazenados em disco e o número de acessos ao disco precisa ser minimizado.

Este trabalho implementa as principais operações de uma B-Tree de grau mínimo `t`, incluindo o complexo algoritmo de exclusão com suas regras de rebalanceamento (divisão, redistribuição e fusão).

# 🛡️ Programação Defensiva

Este projeto adota os princípios de Programação Defensiva para antecipar, detectar e mitigar erros. Isso é realizado através de:

- **Programação por Contrato (icontract):** Definição de pré-condições, pós-condições e invariantes nas funções principais.
- **Testes Abrangentes (pytest):** Para validar tanto cenários comuns quanto casos extremos e de falha.
- **Mensagens de Erro Claras:** Erros são tratados com assertivas e mensagens que ajudam na identificação rápida do problema.
  
## ✨ Funcionalidades

  * **Inserção de Chaves:** Implementa o algoritmo de inserção, incluindo a divisão de nós (`split`) que se propagam da folha para a raiz.
  * **Exclusão de Chaves:** Implementa o algoritmo de exclusão complexo, que lida com:
      * Exclusão de chaves em nós folhas.
      * Exclusão de chaves em nós internos (substituição por predecessor/sucessor).
      * **Rebalanceamento:** Redistribuição de chaves entre irmãos (`borrow from left/right`) quando um nó entra em underflow.
      * **Fusão de Nós (`merge`):** Combinação de nós com underflow e uma chave do pai quando a redistribuição não é possível.
      * **Propagação de Rebalanceamento:** Resolução de underflow que se propaga para cima na árvore, podendo diminuir a altura da árvore.
  * **Busca:** Encontra chaves na árvore.
  * **Impressão BFS:** Exibe a árvore nível a nível (Busca em Largura).
  * **Programação por Contrato (`icontract`):** Utiliza decoradores para impor pré-condições, pós-condições e invariantes, garantindo que as propriedades da B-Tree sejam mantidas em todas as operações.

## 🛠️ Configuração do Ambiente

Para configurar o ambiente de desenvolvimento e executar o projeto, siga os passos abaixo:

1.  **Clone o Repositório:**

    ```bash
    git clone https://github.com/klmurussi/TPPE-DefensiveProgramming
    cd TPPE-DefensiveProgramming
    ```

2.  **Crie e Ative o Ambiente Virtual:**
    É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    ```

3. **Instale as Dependências:**

    Você pode instalar as dependências de duas formas:

    **Usando o arquivo `requirements.txt`:**

    ```bash
    pytest>=7.0.0
    icontract>=2.6.1
    ```

    ```bash
    pip install -r requirements.txt
    ```

    **Ou instalando manualmente:**

    ```bash
    pip install pytest icontract
    ```

## 🚀 Como Usar

Você pode interagir com a B-Tree executando o script principal `main.py`.

```bash
    python3 main.py
```

## 🧪 Executando Testes

O projeto utiliza `pytest` para seus testes. É fundamental executar os testes para garantir a correção das operações da B-Tree e a aderência aos contratos.

A partir do diretório raiz do projeto, execute:

```bash
pytest
```

## 📦 Estrutura do Projeto

```
TPPE-DefensiveProgramming/
├── btree/
│   ├── __init__.py         # Pacote Python
│   ├── tree.py             # Implementação da classe BTree e seus métodos
│   └── node.py             # Implementação da classe BTreeNode
├── tests/
│   ├── __init__.py         # Pacote Python para testes
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_delete.py  # Testes para a função delete()
│   │   ├── test_insert.py  # Testes para a função insert()
│   │   └── test_tree.py    # Testes para funcionalidades básicas (como print_bfs)
│   └── mocks/
│       ├── __init__.py
│       └── tree_mocks.py   # Funções para criar árvores mockadas para testes específicos
├── main.py                 # Script principal
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
```

## 👥 Membros

- **[Kathlyn Lara Murussi](https://github.com/klmurussi)** - 180042378
- **[Ingrid Soares](https://github.com/ingrdsoares)** - 160125162
- **[Pedro Henrique C. de Moraes](https://github.com/pedromoraes39)** - 190036427
- **[Pablo S. Costa](https://github.com/pabloheika)** - 180128817
