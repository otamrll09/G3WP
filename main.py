import SendEmailAttach

dicionario = {
    'Software': ['log4J', 'log4J', 'log4J', 'log4J'],
    'CVE': ['CVE-2022-0070', 'CVE-2022-0071', 'CVE-2022-0072', 'CVE-2022-0073'],
    'Current Description': ['A', 'B', 'C', 'D'],
    'Severity': [8.8, 2, 6, 9],
    'References to Advisories, Solutions, and Tools': ['A', 'B', 'C', 'D'],
    'Known Affected Software Configurations': ['A', 'B', 'C', 'D'],
    'NVD Published Date': ['04/19/2022', '04/19/2023', '04/19/2024', '04/19/2025'],
    'Link para o respectivo CVE': ['https://google.com', 'https://google.com', 'https://google.com', 'https://google.com']
}

lista_emails = [
    'gelsinhomusico@gmail.com',
    '2.gelsinhomusico@gmail.com',
    'gelsonfilho.contato@gmail.com',
    'filipe.sousa246@gmail.com',
    'otavio.marques@facens.br'
]

nome_da_planilha = "PlanilhaListaVulnerabilidades"

SendEmailAttach.send_email(lista_emails, dicionario, nome_da_planilha)