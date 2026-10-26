# Drones — plataforma Google

Código mestre da aplicação de cadastro, aulas, avaliação e coordenação do curso. Os vídeos permanecem no YouTube. Os registros, documentos pessoais, certificados individuais, gabaritos e configurações de produção ficam na área privada do Google.

## Acessos públicos

- [Painel dos instrutores](https://newtonlicciardijr.github.io/drones/docentes.html)
- [Portal do curso](https://newtonlicciardijr.github.io/drones/)
- [Modelo do certificado de 30 h/a](https://newtonlicciardijr.github.io/drones/certificado.html)
- [Catálogo dos vídeos](./lessons-public.json)

## Manutenção

`Code.gs` contém a interface e as funções de servidor para Google Apps Script. Dados e configurações privados devem permanecer fora deste repositório. O guia operacional com os acessos da conta está na pasta privada do projeto no Drive.

Altere o código no master, valide-o, salve a atualização no projeto Apps Script e publique uma nova versão da implantação existente. Preserve o URL da aplicação. Mudanças feitas diretamente no editor devem ser reconciliadas com o master.

Execute `node test-bootstrap.mjs` para as verificações locais com dados sintéticos. A publicação do código é independente da autorização institucional de emissão dos certificados.

Não publique credenciais, documentos pessoais, resultados individuais, banco de respostas ou backups da base. Os arquivos do Google Drive mantêm permissões próprias; os links do portal não tornam esses arquivos públicos.
