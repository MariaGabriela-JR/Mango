# Indíce
- [Padrões de Branch](#padrôes-de-branch)
- [Mensagens de commit](#mensagens-de-commit)
- [Workflow](#workflow)

--- 

## Padrões de branch
- O padrão de branch a ser seguido é lowercase_snake_case.
- Para nomea-las usar o mesmo padrão de commit “tipo: nome_da_branch”. Exemplo “feat/login-system”
- A branch main é protegida, então somente pull requests para main poderão atualizá-la.
- Teremos três padrões de branches (baseado na estratégia de branches GitHub Flow):
    - Main - origem, código atual
    - Release - branch de integração, onde todas as funcionalidades estão desenvolvidas e finalizadas
    - Features - Para desenvolver as tarefas apenas e após o código ser promovido para Develop essa branch é excluida

---

## Mensagens de commit
Os commits devem seguir o padrão "tipo(origem): mensagem do commit"

- Tipos sugeridos:
    - feat: Implementação de código
    - fix: Correção de bug ou alteração que modifica algo que já foi criado
    - doc: Documentação

---

## Workflow
- Verificar issues disponíveis no Project
- Crie sua branch a partir da master com o nome da issue atribuida a você.
- Ao terminar não esqueça de criar o pull request.