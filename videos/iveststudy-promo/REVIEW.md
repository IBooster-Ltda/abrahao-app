# REVIEW · iVest promo desktop · modo noturno (97 s, 1920×1080, 30 fps, narrado)

## O que mudou nesta versão
- Voz masculina: ElevenLabs "Brian", grave e calma, mesmas 12 falas.
- Modo noturno de ponta a ponta: regravei todos os fluxos do app com o tema escuro ativado (Modo Estudo com duas respostas 10/10 em História, Quiz de Geografia, Flashcards de Química, Simulado FUVEST, Redação 920/1000 sobre juventude e clima, Mentor, Dashboard, Ranks, Conquistas, Turma, home em EN/ES).
- Imagens novas, geradas por IA no Runway (nano-banana-pro) a pedido: abertura com um estudante estudando à noite à luz do notebook; encerramento com estudantes subindo a escadaria de uma universidade ao amanhecer; e uma textura escura com bokeh sutil como fundo das cenas de janela. As três foram escurecidas em pós (0,8 / 0,62 / 0,9) para o texto ler bem.
- Mais efeitos sonoros, cada um sobre uma ação visível: teclas e digitação (abertura do reveal, digitação da resposta, pergunta ao Mentor), clique em "Avaliar resposta", riser + impacto + brilho no 10/10 e no 920/1000, pops nos cards da home e no "Sabia!", clique e pop no "Correto!" do quiz, clique + ping ao iniciar o simulado, notificação quando o Mentor responde, whooshes nas trocas de janela, whoosh cinematográfico nas duas transições de foto, teclas nos chips de idioma, pop na marca e clique no botão final.
- Look: fundo com a textura gerada, janelas do app escuro com borda azul sutil e sombra forte, títulos Inter 700 68 px, acento #60A5FA. Sem end card branco: o fechamento é sobre a foto do campus.

## Medido e olhado
- `hyperframes check`: ok; um aviso mantido de propósito (o clipe da correção começa em 4,9 s dentro da cena, para o 10/10 cair na fala "corrige na hora").
- `snapshot --review` + 8 quadros intermediários: olhados; corrigidos o início do clipe de Flashcards (mostrava a seleção), o quadro claro no início do Simulado e o enquadramento do Dashboard (agora começa no mapa de atividade, sem a linha de KPIs).
- Áudio medido com `hyperframes audio`; ninguém ouviu.

## Pontos fracos
- Dashboard do cliente ainda tem dados antigos de teste (média 3,5); a câmera evita a linha de números.
- "Ranks" mostra "Sem rank" (menos de 10 respostas no Modo Estudo nesta conta).
- Música continua o loop gerado de 22 s; voz "Brian" é uma voz padrão em inglês falando português. Voz nativa exige plano pago da ElevenLabs.
- As fotos geradas mostram pessoas genéricas criadas por IA, não alunos reais do iVest; se preferir, trocamos por fotos reais do cliente.
