---
name: writing-style
description: >
  Aplica um estilo de escrita técnica denso, direto e sem fluff para documentos como READMEs,
  tutoriais, changelogs, docstrings, wikis e qualquer documentação técnica. Use sempre que o
  usuário pedir para escrever, revisar ou melhorar um README, tutorial, guia de instalação,
  documentação de API, changelog, ou qualquer texto técnico. Também aplique quando o usuário
  disser "escreve no meu estilo", "sem enrolação", "direto ao ponto" ou pedir para revisar
  um texto que está "genérico demais" ou "cheio de enrolação".
---

# Writing Style — Documentação Técnica

Este skill define o padrão de escrita para READMEs, tutoriais, guias e qualquer documentação técnica.
O objetivo é texto que informa sem encher linguiça — denso em informação, sem fluff, com tamanho proporcional à complexidade real do projeto.

---

## Princípios Fundamentais

### 1. Densidade informacional

Cada frase carrega uma informação. Se você consegue remover uma frase sem perder nada, remove.

**Errado:**
> Este projeto foi desenvolvido com o objetivo de facilitar a vida dos desenvolvedores que precisam de uma solução simples e eficiente para gerenciar suas tarefas do dia a dia.

**Certo:**
> Gerenciador de tarefas via CLI. Sem interface, sem banco de dados, sem dependências.

---

### 2. Voz ativa sempre

Não existe "deve ser instalado", "pode ser configurado", "é recomendado".

**Errado:** A dependência deve ser instalada antes de executar.  
**Certo:** Instale a dependência antes de executar.

---

### 3. Zero adjetivos não-mensuráveis

Banido: simples, fácil, intuitivo, poderoso, robusto, rápido (sem número), moderno, elegante, seamless, eficiente (sem contexto).

Se não dá pra medir ou demonstrar, corta.

**Errado:** Uma ferramenta simples e poderosa para desenvolvedores.  
**Certo:** Ferramenta de linha de comando para X. Faz Y em Z segundos.

---

### 4. Introduções diretas

O primeiro parágrafo de qualquer documento diz **o que é** e **o que faz**. Não o que o documento vai explicar, não a história do projeto, não agradecimentos.

**Errado:**
> Este README explica como instalar e usar o projeto. Antes de começar, certifique-se de ter os requisitos instalados.

**Certo:**
> `nomeprojeto` faz X. Requer Node 18+.

---

### 5. Código inline pra tudo técnico

Qualquer referência a: arquivo, comando, variável, função, path, extensão, flag — vai em backtick.

Escreve `npm install`, não "execute o comando de instalação do npm".  
Escreve `config.json`, não "o arquivo de configuração".

---

### 6. Seções curtas

Máximo de 4-5 linhas de prosa antes de quebrar em lista, código ou nova seção.  
Se passou disso, o parágrafo provavelmente tem gordura ou deveria ser dividido.

---

### 7. Listas só quando fazem sentido estrutural

Lista é pra enumerar itens paralelos sem relação narrativa entre eles.  
Passos sequenciais com dependência entre si = numerados.  
Prosa com "e", "depois", "então" = não vira lista, fica prosa.

**Errado (lista desnecessária):**
>
> - O sistema processa a requisição
> - Em seguida valida os dados
> - Depois retorna a resposta

**Certo:**
> O sistema processa a requisição, valida os dados e retorna a resposta.

---

### 8. Títulos descritivos, não criativos

Título de seção diz o que está na seção. Não é eslogan, não é pergunta retórica.

**Errado:** Por que usar isso? / O Poder do Sistema / Começando sua Jornada  
**Certo:** Instalação / Como funciona / Configuração / Exemplos

---

### 9. Tamanho proporcional à complexidade real

O tamanho do documento é determinado pela complexidade do projeto, não pela preferência do autor nem pela vontade de parecer profissional.

**Projeto simples** (CLI de um comando, lib de uma função, script isolado): README de meia página. Instalação, uso, licença. Qualquer coisa além disso é fluff.

**Projeto médio** (API com 10-20 endpoints, bot com algumas funcionalidades, ferramenta com configurações): README de 1-3 páginas. Visão geral, instalação, configuração, exemplos de uso, referência rápida.

**Projeto complexo** (agente autônomo com múltiplas integrações, framework com arquitetura própria, plataforma com vários módulos): README extenso é justificado e necessário. Documentar menos do que o projeto exige é tão ruim quanto documentar mais.

A pergunta certa não é "está longo demais?" mas sim: **"cada seção existe porque o usuário precisa dela, ou porque eu quis escrever?"**

Sinais de que está longo sem justificativa:

- Seções que repetem o que o título já diz
- Parágrafos de contexto histórico que não afetam o uso
- Exemplos redundantes que cobrem o mesmo caso com variação mínima
- Explicações do que o README vai explicar

Sinais de que o tamanho é justificado:

- Cada seção cobre um aspecto diferente do sistema
- Remover qualquer seção deixaria o usuário sem informação necessária
- O projeto tem múltiplos modos de uso, integrações ou configurações que precisam ser documentados separadamente

---

## Estrutura Padrão de README

### Projeto simples

```
# nome-do-projeto

[1-2 frases: o que é e o que faz. Sem adjetivo.]

## Instalação
[comandos.]

## Uso
[exemplo mais comum primeiro. código antes de explicação.]

## Licença
[uma linha.]
```

### Projeto complexo

```
# nome-do-projeto

[Descrição completa: o que é, o que faz, qual problema resolve, diferenciais concretos.]

## Funcionalidades
[Lista das capacidades principais. Pode ser extensa se o projeto tiver muitas.]

## Instalação
[Todos os métodos de instalação disponíveis, com requisitos por plataforma se necessário.]

## Configuração
[Todas as opções, com tipo, default e descrição. Tabela ou seções por módulo.]

## Uso
[Casos de uso principais com exemplos reais de código. Um exemplo por caso de uso.]

## Arquitetura (se relevante)
[Como o projeto funciona internamente. Diagrama se ajudar.]

## Integrações (se houver)
[Cada integração com instruções específicas.]

## Contribuindo
[Como contribuir, convenções, como rodar localmente.]

## Licença
[uma linha.]
```

---

## Estrutura Padrão de Tutorial

1. **O que você vai construir** — resultado concreto, não objetivo vago
2. **Requisitos** — lista seca, sem "certifique-se de ter"
3. **Passos numerados** — um passo = uma ação = um bloco de código
4. **Verificação** — como o usuário sabe que funcionou
5. **Próximos passos** (opcional) — links diretos, sem frase de encerramento motivacional

---

## Palavras e Frases Banidas

| Banido | Substituto |
|--------|-----------|
| Certifique-se de | — (implícito, ou reformula o passo) |
| Não se esqueça de | — (reformula como passo direto) |
| É importante notar que | — (diz o que é importante direto) |
| Sinta-se livre para | — (remove, o usuário já sabe que pode) |
| Espero que este guia tenha ajudado | — (remove, sempre) |
| Qualquer dúvida, abra uma issue | Dúvidas: abra uma issue. |
| Simples assim! / É isso! | — (remove) |
| Como mencionado anteriormente | — (não menciona de novo ou reformula) |
| A fim de | Para |
| Devido ao fato de que | Porque |
| No sentido de | Para |

---

## Bilinguismo (PT/EN)

Quando escrevendo em inglês, os mesmos princípios se aplicam. Adicionalmente:

- Não traduza expressões técnicas consagradas em inglês para português forçado
- `deploy`, `build`, `commit`, `branch`, `merge` ficam em inglês mesmo em texto PT
- Evite "deployar", "bugar", "commitar" — use a forma direta: "faça o deploy", "o build falhou", "commit as alterações"

---

## Checklist antes de finalizar

- [ ] Primeiro parágrafo diz o que o projeto faz sem adjetivo?
- [ ] Tem alguma frase que começa com "Este documento..."?
- [ ] Tem adjetivo não-mensurável?
- [ ] Tem voz passiva que pode virar ativa?
- [ ] Tem lista que deveria ser prosa ou prosa que deveria ser lista?
- [ ] Tem frase de encerramento motivacional?
- [ ] Todo item técnico está em backtick?
- [ ] O tamanho do documento é proporcional à complexidade do projeto?
- [ ] Tem seção que pode ser removida sem o usuário perder informação necessária?
