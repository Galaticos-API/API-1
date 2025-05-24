# API - 1° Semestre ADS - FATEC SJC

## Objetivo do Projeto

O objetivo é desenvolver um sistema web para o registro e gestão de atestados médicos de alunos, facilitando a comunicação entre estudantes, professores e a coordenação acadêmica, além de permitir a avaliação contínua de equipes ágeis em projetos de desenvolvimento de software. A plataforma garantirá um armazenamento seguro e organizado dos atestados, possibilitando consultas rápidas e emissão de relatórios sobre afastamentos. Paralelamente, permitirá a avaliação individual dos membros de equipes Scrum, analisando métricas como colaboração, proatividade e entrega de resultados, fornecendo relatórios analíticos para acompanhamento da evolução das equipes ao longo do tempo.

<hr>

### Sprints

| Sprint               | Previsão                | Status    |
| -------------------- | ----------------------- | --------- |
| Kick Off Geral       | 26/08/2024 - 30/08/2024 | Concluído |
| Kick Off 1° Semestre | 02/09/2024 - 06/09/2024 | concluído |
| 01                   | 10/03/2025 - 30/03/2025 | Concluído |
| 02                   | 07/04/2025 - 27/04/2025 | Concluído |
| 03                   | 05/05/2025 - 25/05/2025 | Em curso  |
| Feira de Soluções    | 29/05/2024              | A começar |

<hr>

## MVP

<p align="center">
      <img src="./documents/mvp.jpg" alt="MVP do Projeto" width=550 height=310>
<br>

<ul>
  <li>
    <h6>Wireframe inicial: <a href="https://www.figma.com/proto/usvs8u86jhjHeELI54Wwyn/Untitled?node-id=39-22&t=sZmLWbW5VmAn2YGR-1">FIGMA</a>
    </h6>
  </li>
</ul>

| Sprint   | Link do Vídeo                                              |
| -------- | ---------------------------------------------------------- |
| Sprint 1 | [Clique aqui](https://www.youtube.com/watch?v=Aag2fdVSDXw) |
| Sprint 2 | [Clique aqui](https://www.youtube.com/watch?v=LrEpRZ4XQmg) |
| Sprint 3 | [Clique aqui](https://www.youtube.com/watch?v=2vUJxWFI6WU) |

<hr>

## Backlog do produto

| Rank | Backlog                                                                             | User Story                                                                                                                                                                                                                             | Prioridade | Sprint |
| ---- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------ |
| 1    | Configurar ambiente Flask (instalação do framework e dependências).                 | Como **desenvolvedor**, quero configurar o ambiente Flask e suas dependências, para que o desenvolvimento ocorra de forma eficiente e organizada.                                                                                      | Alta       | 1      |
| 2    | Criar repositório no GitHub e configurar controle de versão.                        | Como **desenvolvedor**, quero criar um repositório no GitHub e versionar o desenvolvimento do sistema, para que o projeto seja otimizado e esteja disponível para colaboração e backup.                                                | Alta       | 1      |
| 3    | Criar estrutura de diretórios para organizar o código do backend e frontend.        | Como **desenvolvedor**, quero criar uma estrutura de pastas organizada para separar o código do back-end e do front-end, para facilitar a manutenção, o entendimento do projeto e o trabalho em equipe.                                | Alta       | 1      |
| 4    | Criar modelo de usuário no arquivo de controle.                                     | Como **desenvolvedor**, quero criar um modelo de usuário em um arquivo de texto de controle, para que o gerenciamento de dados dos usuários seja estruturado.                                                                          | Alta       | 1      |
| 5    | Registrar usuários por meio de armazenamento em arquivos de texto.                  | Como **desenvolvedor**, quero criar um cadastro por meio de arquivo de texto para armazenar informações de usuários de forma simples, para que eu possa registrar e consultar usuários mesmo sem utilizar banco de dados inicialmente. | Alta       | 1      |
| 6    | Criar endpoint Flask para upload de arquivos PDF.                                   | Como **desenvolvedor**, quero receber arquivos PDF através de um endpoint no meu servidor, para que os atestados possam ser armazenados de forma segura e organizada.                                                                  | Alta       | 1      |
| 7    | Criar lógica para armazenamento dos atestados.                                      | Como **administrador** do sistema, quero garantir que os atestados enviados sejam armazenados usando JSON em arquivos de texto, para manter os dados organizados.                                                                      | Alta       | 1      |
| 8    | Criar interface HTML + CSS para cadastro de alunos e membros da equipe.             | Como **usuário**, quero acessar uma página web intuitiva e bonita para realizar o cadastro de alunos e membros da equipe, para que os dados possam ser coletados de maneira organizada.                                                | Média      | 1      |
| 9    | Criar interface para envio de atestados e visualização dos documentos enviados.     | Como **usuário**, quero uma página web onde eu possa enviar atestados em PDF e visualizar os documentos já enviados, para facilitar a organização, controle e acesso aos arquivos.                                                     | Média      | 1      |
| 10   | Criar filtro de busca por aluno, data e tipo de atestado.                           | Como **administrador** ou **usuário**, quero poder buscar atestados usando o nome do aluno, a data de envio e o tipo de atestado, para encontrar rapidamente o documento que preciso analisar ou baixar.                               | Média      | 1      |
| 11   | Criar interface para listagem dos atestados cadastrados.                            | Como **administrador** ou **usuário**, quero visualizar a lista de atestados cadastrados no sistema, para facilitar o acompanhamento e gerenciamento dos documentos.                                                                   | Média      | 2      |
| 12   | Criar modelo de avaliação no arquivo de controle.                                   | Como **administrador**, quero um modelo de avaliação de equipe ágil registrado no sistema, para avaliar equipes de forma organizada.                                                                                                   | Média      | 2      |
| 13   | Fazer endpoint para cadastrar avaliação de equipe ágil.                             | Como **administrador**, quero cadastrar avaliações de equipes ágeis através de um endpoint, para registrar o desempenho das equipes.                                                                                                   | Média      | 2      |
| 14   | Classificação e organização dos atestados por data e período de afastamento.        | Como **administrador**, quero classificar os atestados por data e período de afastamento, para facilitar consultas e relatórios.                                                                                                       | Média      | 2      |
| 15   | Implementar listagem de equipes na aba de equipes.                                  | Como **administrador**, quero listar todas as equipes registradas no sistema, para poder gerenciá-las de forma eficiente.                                                                                                              | Média      | 2      |
| 16   | Utilizar usuários reais no select do formulário de criação de equipe.               | Como **usuário**, quero selecionar usuários reais cadastrados ao criar uma equipe, para garantir que apenas pessoas válidas sejam adicionadas às equipes.                                                                              | Média      | 2      |
| 17   | Finalizar interface de cadastro de membros da equipe.                               | Como **usuário**, quero completar o cadastro dos membros de uma equipe, para garantir que a composição da equipe esteja completa e salva corretamente.                                                                                 | Média      | 2      |
| 18   | Criar modelo de equipe no arquivo de controle.                                      | Como **desenvolvedor**, quero um modelo de equipes ágil no sistema, para manter a organização das registro das mesmas.                                                                                                                 | Média      | 2      |
| 19   | Criação de interface básica para avaliação de membro da equipe ágil.                | Como **usuário**, quero uma interface simples para realizar avaliações de membros da minha equipe ágil, para facilitar a coleta de feedbacks.                                                                                          | Média      | 2      |
| 20   | Configurar validações no backend para proteger os dados.                            | Como **desenvolvedor**, quero implementar validações no backend para proteger os dados recebidos e armazenados, para garantir a segurança e integridade das informações.                                                               | Alta       | 2      |
| 21   | Criar endpoint Flask para recuperar lista de atestados.                             | Como **desenvolvedor**, quero criar um endpoint para recuperar a lista de atestados, para alimentar a interface de visualização dos documentos.                                                                                        | Alta       | 2      |
| 22   | Implementar cadastro de equipes.                                                    | Como **usuário**, quero cadastrar novas equipes no sistema, para organizar os times de trabalho.                                                                                                                                       | Alta       | 2      |
| 23   | Configurar login administrativo.                                                    | Como **administrador**, quero realizar login no sistema, para acessar funcionalidades restritas apenas aos responsáveis.                                                                                                               | Alta       | 2      |
| 24   | Corrigir bug de login inexistente.                                                  | Como **usuário**, quero receber mensagens claras ao tentar logar com um usuário inexistente, para melhorar a usabilidade e segurança do sistema.                                                                                       | Alta       | 2      |
| 25   | Correção de bugs em validações de campos obrigatórios.                              | Como **desenvolvedor**, quero corrigir as validações de campos obrigatórios, para evitar o cadastro de dados incompletos ou inválidos.                                                                                                 | Baixa      | 2      |
| 26   | Testar acesso em dispositivos móveis.                                               | Como **usuário**, quero testar o acesso ao sistema em dispositivos móveis, para garantir que a interface seja responsiva e funcional em diferentes tamanhos de tela.                                                                   | Alta       | 3      |
| 27   | Implementar tela de relatório sobre os atestados.                                   | Como **administrador**, quero uma tela de relatório sobre os atestados, para visualizar e analisar os documentos cadastrados de forma organizada.                                                                                      | Alta       | 3      |
| 30   | Criar funcionalidade Admin para aprovar/reprovar atestados.                         | Como **administrador**, quero aprovar ou reprovar atestados, para validar as justificativas enviadas e manter o controle sobre os documentos aceitos pelo sistema.                                                                     | Alta       | 3      |
| 35   | Mostrar métricas de avaliação com gráficos.                                         | Como **administrador**, quero visualizar as métricas de avaliação por meio de gráficos, para facilitar a análise de desempenho das equipes e membros.                                                                                  | Alta       | 3      |
| 29   | Implementar responsividade para Mobile e PC.                                        | Como **usuário**, quero que a aplicação seja responsiva, para utilizar o sistema de forma eficiente em diferentes dispositivos, como computadores e celulares.                                                                         | Média      | 3      |
| 31   | Criar API Flask para filtro de equipe ágil.                                         | Como **desenvolvedor**, quero criar uma API Flask para filtrar informações de equipes ágeis, para que as consultas sejam mais eficientes e organizadas conforme as necessidades de avaliação e gestão.                                 | Médio      | 3      |
| 32   | Permitir que Admin edite e remova equipes (atualmente não há como remover equipes). | Como **administrador**, quero editar e remover equipes, para garantir que o sistema reflita a organização atual e permitir ajustes conforme necessário.                                                                                | Média      | 3      |
| 34   | Implementar validação de cadastro relacionados à avaliação e equipes.               | Como **desenvolvedor**, quero validar os cadastros relacionados à avaliação e às equipes, para garantir a integridade dos dados e o correto funcionamento do sistema.                                                                  | Média      | 3      |
| 36   | Exportar métricas de avaliação em documento.                                        | Como **administrador**, quero exportar as métricas de avaliação em documentos, para arquivar relatórios e compartilhar os resultados com outros interessados.                                                                          | Média      | 3      |
| 28   | Exportar relatórios sobre os atestados em documento.                                | Como **administrador**, quero exportar relatórios sobre os atestados em documento, para gerar arquivos que possam ser compartilhados e arquivados.                                                                                     | Baixa      | 3      |
| 33   | Implementar função permitindo usuário sair da equipe.                               | Como **usuário**, quero sair de uma equipe, para que minha participação possa ser encerrada quando necessário, mantendo as informações atualizadas.                                                                                    | Baixa      | 3      |

<hr>

## Tecnologias utilizadas

![My Skills](https://go-skill-icons.vercel.app/api/icons?i=git,github,vscode,html,css,bootstrap,js,python,flask,figma)

<hr>

## Autores

|    Função     | Nome                      |                                                                    GitHub                                                                     |
| :-----------: | :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------: |
| Scrum Master  | Giovanni Moretto          |   [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/Giomoret)    |
| Product Owner | Gustavo Bueno da Silva    |  [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/Darkghostly)  |
|   Dev Team    | Rafael Giordano Matesco   |  [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/RafaMatesco)  |
|   Dev Team    | Gustavo Monteiro Greco    | [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/GustavoMGreco) |
|   Dev Team    | Gabriel dos Santos Lasaro |   [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/Sashxjssx)   |
|   Dev Team    | Alice Azambuja            | [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/AlicePenrose)  |

<hr>

## Instalação

- Dependências:
- - Python > 3.7
- - Flask
- - bcyrpt

### Para Windows:

#### Baixando o repositório

Baixe o repositório e extraia ele no diretório desejado ou clone o repositório caso tenha Git instalado utilizando o comando:

```Bash
git clone https://github.com/NinjaDevs-API/NinjaDevs.git
```

Acesse o repositório criado a partir do terminal:

```ps
cd \caminho\para_o\repositorio\
```

#### Instalando as dependências

Na raiz do repositório é providenciado um arquivo de dependencias para o gerenciador de pacotes incluido no Python. É recomendável que se crie um ambiente virtual, porêm este passo é opcional:

```ps
python -m venv venv
.\venv\Scripts\activate
```

Sobre a política de execução do Windows [^1]

Para instalar as dependências, apenas passe o arquivo requirements.txt com o parâmetro -r para o comando install do pip:

```bash
pip instal -r requirements.txt
```

#### Iniciando a aplicação

Apos instaladas as dependências, a aplicação Flask já está pronta para ser iniciada. Apenas entre este comando para iniciar o servidor com o endereço padrão `http://127.0.0.1:5000`:

```Bash
cd .\src
Flask run
```

[^1]: <https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.5>
