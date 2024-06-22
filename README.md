# Web_crawler

Este é um crawler Python para buscar e analisar informações em páginas web.
Utiliza BeautifulSoup e requests para coletar links, imagens, tecnologias, páginas de login e referências a bancos de dados a partir de uma URL fornecida.

**Atenção:**
```Diff
Este projeto é destinado exclusivamente para fins educacionais e de desenvolvimento. Ao usar este web crawler, é importante estar ciente dos seguintes pontos:
- O autor deste projeto não se responsabiliza pelo uso indevido ou não autorizado do software. É responsabilidade do usuário garantir que o uso do crawler esteja em conformidade com as políticas de uso aceitável dos sites que são acessados.
- O uso excessivo ou inadequado do crawler pode sobrecarregar os servidores de um site, o que pode ser interpretado como um ataque de negação de serviço (DoS). Portanto, utilize-o com moderação e respeite as diretrizes de robots.txt e os termos de serviço dos sites visitados.
- Verifique as leis e regulamentos locais e internacionais antes de usar este software para garantir que não viole nenhuma legislação sobre privacidade, direitos autorais ou proteção de dados.
```
## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/crawler-web.git
```
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
## Como Usar

Execute o script com a URL alvo como argumento da linha de comando:

```bash
python run_crawler.py http://www.exemplo.com
```
## Funcionalidades
°Busca recursiva de até uma certa profundidade.
°Análise de tecnologias usadas como JavaScript, CSS e bancos de dados.
°Identificação de páginas de login.

#### Licença
Este projeto é distribuído sob a [MIT License](LICENSE). Ao usar este software, você concorda com os termos e assume toda a responsabilidade pelo seu uso.
