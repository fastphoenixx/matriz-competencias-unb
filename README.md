# **InterEPRUnB \- Internacionalização da Engenharia de Produção (UnB)**

Ferramenta de mapeamento, diagnóstico e visualização curricular desenvolvida para apoiar o processo de internacionalização e acreditação (ABET) do curso de Engenharia de Produção da Universidade de Brasília (UnB).  
🔗 **Acesse o Sistema Online:** [https://fastphoenixx.github.io/matriz-competencias-unb/](https://www.google.com/search?q=https://fastphoenixx.github.io/matriz-competencias-unb/)

## **🎯 Objetivo do Projeto**

O **InterEPRUnB** foi desenvolvido no âmbito da disciplina *Projeto em Sistemas de Produção 4* com o objetivo de solucionar a lacuna de rastreabilidade entre as competências declaradas no Projeto Pedagógico do Curso (PPC) e os requisitos internacionais exigidos pela ABET (*Student Outcomes*).  
A ferramenta permite:

1. **Centralizar** o mapeamento de disciplinas em uma base única e auditável.  
2. **Visualizar** graficamente a cobertura curricular (quais SOs são mais ou menos atendidos).  
3. **Evidenciar** a conformidade do curso através de justificativas pedagógicas vinculadas a cada disciplina.

## **📂 Estrutura do Repositório**

Este projeto utiliza uma arquitetura **Serverless / Flat Data** focada na simplicidade de manutenção a longo prazo. Não é necessário instalar Node.js, bancos de dados ou servidores complexos.

| Arquivo | Função |
| :---- | :---- |
| index.html | **O Cérebro do Sistema.** Contém todo o código fonte (HTML, CSS Tailwind, React JS e Lógica). É um arquivo único auto-contido. |
| dados\_oficiais.csv | **O Banco de Dados.** É a fonte da verdade. O site lê este arquivo automaticamente ao abrir para popular os gráficos. |
| README.md | Documentação oficial e manual de uso do projeto. |

## **📊 Funcionalidades**

* **Dashboard Gerencial:** KPIs de cobertura, gráfico de radar (equilíbrio de competências) e evolução temporal dos registros.  
* **Visualizações Avançadas:**  
  * **Diagrama de Sankey:** Fluxo visual que conecta *Disciplina ➝ Competência*.  
  * **Heatmap (Matriz de Densidade):** Identificação rápida de quais disciplinas contribuem mais para o currículo.  
* **Explorador de Análise:** Detalhamento granular. Permite clicar em um *Student Outcome* (ex: SO4 \- Ética) e ver exatamente quais disciplinas o ensinam e qual a evidência registrada.  
* **Integração GitOps:** O sistema lê e escreve dados diretamente no GitHub, funcionando como um CMS.

## **🛠 Manual de Atualização (Para a Equipe)**

O sistema foi desenhado para ser mantido por qualquer pessoa com conhecimentos básicos de Excel, garantindo a continuidade do projeto. Existem duas formas de atualizar os dados:

### **Método 1: Edição via Excel (Recomendado para grandes mudanças)**

1. Acesse a aba **Base de Dados** no site.  
2. Clique em **"Exportar CSV Atual"** para baixar a versão mais recente.  
3. Abra o arquivo no Excel ou Google Sheets.  
4. Adicione novas linhas seguindo o padrão das colunas existentes.  
   * *Nota:* Não altere o nome das colunas (cabeçalho).  
5. Volte aqui no GitHub, clique em **Add file \> Upload files**.  
6. Arraste o seu novo arquivo e certifique-se de que o nome seja **exatamente** dados\_oficiais.csv.  
7. Clique em **Commit changes**. O site atualizará automaticamente em alguns minutos.

### **Método 2: Sincronização via Site (Para ajustes rápidos)**

1. Na aba **Mapeamento**, utilize o formulário para adicionar um novo vínculo.  
2. Clique no botão **"Salvar no GitHub"** (canto superior direito).  
3. Insira suas credenciais do GitHub (Usuário, Repositório e [Personal Access Token](https://github.com/settings/tokens)).  
4. O sistema fará o *commit* da alteração diretamente no repositório.

## **📚 Referências Teóricas**

As bases de dados foram construídas cruzando:

* **PPC Engenharia de Produção UnB:** Competências PPC-EP-01 a PPC-EP-07.  
* **ABET Criteria for Accrediting Engineering Programs:** Student Outcomes (SOs) 1 a 7 (Ciclo 2025-2026).

## **👥 Equipe do Projeto**

Trabalho desenvolvido pela equipe da disciplina PSP4 (2024/2):

| Nome | Matrícula |
| :---- | :---- |
| **Arthur de Ávila Oliveira Trojan Repiso** | 221020950 |
| **Bruno Sérgio do Amaral** | 190052473 |
| **Cristiano Alves Rose** | 222005368 |
| **Vitor Alves F. C. Cavalcante** | 221006647 |
| **Gabriel Brum Tristão de Castro** | 221006520 |

Desenvolvido com React, TailwindCSS e Recharts. *Licença: MIT / Uso Acadêmico UnB.*