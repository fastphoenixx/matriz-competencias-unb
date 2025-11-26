# Matriz de Competências - Engenharia de Produção UnB

Ferramenta de visualização e mapeamento curricular entre o PPC de Engenharia de Produção e os Student Outcomes da ABET.

🔗 **Acesse o sistema:** [Link do seu GitHub Pages aqui]

## 📂 Como Funciona (Arquitetura)

Este sistema opera no modelo **"Flat Data" (GitOps)**. Não existe banco de dados complexo.
A "verdade" dos dados está no arquivo `dados_oficiais.csv` hospedado neste repositório.

1. O site (`index.html`) carrega automaticamente o arquivo `dados_oficiais.csv` ao abrir.
2. Para atualizar os dados do site, basta atualizar este arquivo no GitHub.

## 🛠 Como Atualizar o Mapeamento (Novas Disciplinas/Vínculos)

### Opção A: Edição Direta no GitHub (Rápido)
1. Clique no arquivo `dados_oficiais.csv` acima.
2. Clique no ícone de lápis (Edit).
3. Adicione uma nova linha seguindo o padrão:
   `CÓDIGO,NOME,EMENTA,PPC_ID,ABET_ID,JUSTIFICATIVA`
4. Clique em "Commit changes".
5. Aguarde 1 minuto e atualize o site.

### Opção B: Usando o Excel (Recomendado para muitas alterações)
1. Abra o site da Matriz.
2. Vá na aba **Mapeamento** e faça as alterações desejadas (adicione novos vínculos).
3. Clique no botão verde **"Baixar Base para Atualizar GitHub"**.
4. Um arquivo `.csv` será baixado no seu computador.
5. Venha aqui neste repositório, clique em **Add file > Upload files**.
6. Arraste o novo arquivo e certifique-se de que o nome seja `dados_oficiais.csv`.
7. Salve as alterações.

## 📊 Estrutura dos Dados
O arquivo CSV deve respeitar estritamente as seguintes colunas:
- `cod_disc`: Código da disciplina (ex: EPR0046)
- `nome_disc`: Nome completo
- `ementa`: Texto da ementa (entre aspas se tiver vírgulas)
- `ppc_comp`: ID da competência PPC (ex: PPC-EP-01)
- `abet_so`: ID do Student Outcome (ex: SO1)
- `justificativa_abet`: Texto da evidência
