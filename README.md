# Automacao de Faturamento

Projeto em Python para automatizar parte do processo de faturamento de pedidos. A automacao acessa o portal de pedidos e o sistema de gestao, importa os dados da ordem de compra a partir de uma planilha e consulta o estoque antes de iniciar o lancamento do pedido.

## Tecnologias

- Python
- PyAutoGUI e OCR para interacao com as telas
- Pandas para leitura da planilha
- MySQL para consulta de produtos e contratos

## Configuracao

As configuracoes e credenciais devem ser fornecidas localmente por variaveis de ambiente.

## Andamento do projeto

**Em desenvolvimento; ainda nao concluido.**

O fluxo atual inicia o acesso aos sistemas, baixa e le a planilha da ordem de compra, consulta o estoque e comeca o lancamento do pedido. Ainda falta concluir etapas como o preenchimento completo dos itens, a finalizacao do pedido, o tratamento de diferentes ordens de compra e a impressão da nota fiscal. O processo tambem precisa de mais validacao e testes antes de ser considerado pronto para uso.
