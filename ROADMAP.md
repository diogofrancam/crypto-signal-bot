# Roadmap do Projeto Crypto Signal Bot

## 1. MVP - Protótipo Inicial
- Backend básico com FastAPI
- Envio manual de mensagens de teste para Telegram (já implementado)
- Estrutura inicial do projeto com ambiente virtual e dependências
- Preparação para integração com Binance Testnet

## 2. Integração Binance Testnet
- Conexão à API Binance Futures Testnet
- Receber dados de mercado em tempo real (candles, ticker, volatilidade)
- Armazenar dados para análise (banco local com SQLAlchemy)

## 3. Desenvolvimento da Lógica de Sinais
- Implementação de análise técnica (RSI, médias móveis, suporte/resistência)
- Definição da estratégia baseada em volatilidade e gráficos
- Cálculo de entradas, stops, alavancagem (10-25x), alvos parciais
- Backtest básico com dados históricos

## 4. Envio Automático de Sinais para Telegram
- Bot envia sinais formatados com detalhes completos (entrada, stop, alvo, alavancagem)
- Notificações para alertar momentos ideais baseados em volatilidade
- Limitação de operações diárias (máximo 10)

## 5. Desenvolvimento do Frontend Web
- Página web com histórico de sinais e resultados
- Dashboard com gráficos interativos (usando bibliotecas como Chart.js ou D3.js)
- Ranking de desempenho e estatísticas de operação
- Interface responsiva e segura

## 6. Deploy e Monitoramento
- Configuração de ambiente na nuvem (AWS, GCP ou similar)
- Uso de Docker e Docker Compose para facilitar deploy
- Logs, alertas e monitoramento contínuo
- Backup automático dos dados e recuperação

## 7. Otimizações e Expansões Futuras
- Ajuste fino da estratégia para aumentar taxa de acerto
- Implementação de múltiplas estratégias e diversificação
- Integração com outras exchanges e mercados
- Suporte multilíngue e opções avançadas para o usuário

---

## Como contribuir

- Fork do repositório  
- Criar branch com feature nova  
- Pull request detalhado  

