"""Parâmetros declarados da simulação.

Nenhum número aqui é estatística do mundo real (banco-simulado.md, "Procedência").
Tudo que a spec fecha vem com o número da decisão; o que a spec deixa aberto está
marcado ASSUNÇÃO e deve ser ratificado (P12/P13: Davi · P15/P17: Filipe+Davi · P18-P23: Yasmin).
"""
ETYPES = ['LOGIN', 'LOGOUT', 'FILE_ACCESS', 'FILE_DOWNLOAD', 'EXTERNAL_DEVICE',
          'WEB_BROWSING', 'SYSTEM_CONFIG', 'PHISHING_SIM']
E = {n: i for i, n in enumerate(ETYPES)}
RESULTS = ['success', 'failure', 'blocked']
FAIL_REASONS = ['', 'wrong_password', 'user_locked', 'mfa_failed', 'unknown_user']
LOGOUT_REASONS = ['user', 'timeout', 'forced']
ACTIONS = ['view', 'edit']
DESTS = ['local_disk', 'external_storage', 'removable']
DEVTYPES = ['usb_pendrive', 'external_hd', 'phone']
SUBTYPES = ['password_change', 'privilege_escalation', 'mfa_disabled', 'mfa_enabled', 'permission_grant']
SUB = {n: i for i, n in enumerate(SUBTYPES)}
INITIATORS = ['self', 'admin']
OUTCOMES = ['reported', 'ignored', 'clicked', 'submitted_credentials']   # do melhor ao pior (D-25)
SENS = ['public', 'internal', 'confidential', 'restricted']
RANGE_TYPES = ['office', 'vpn', 'home', 'external']
DEVICE_TYPES = ['notebook', 'corporate_phone', 'personal_phone', 'unknown_external']

# domínios: sempre .example (seção 9)
DOMAINS = (
    [(f'{n}.corp.example', 'corporate') for n in ('intranet', 'docs', 'suporte', 'rh', 'wiki', 'agenda')] +
    [(f'{n}.example', 'cloud_storage') for n in ('nuvem-arquivos', 'compartilha-ai')] +
    [(f'{n}.example', 'social_media') for n in ('rede-social', 'video-curto')] +
    [(f'{n}.example', 'webmail') for n in ('correio-web', 'caixa-postal')] +
    [(f'{n}.example', 'uncategorized') for n in ('blog-noticias', 'forum-tech', 'loja-online',
                                                  'portal-esportes', 'receitas', 'tutoriais')])
_CAT_W = {'corporate': .70, 'uncategorized': .17, 'social_media': .07, 'webmail': .03, 'cloud_storage': .03}
_cnt = {c: sum(1 for _, k in DOMAINS if k == c) for c in _CAT_W}
DOMAIN_P = [(_CAT_W[k] / _cnt[k]) for _, k in DOMAINS]
CLOUD_IDX = [i for i, (_, k) in enumerate(DOMAINS) if k == 'cloud_storage']

# D-37 / D-38 / D-40: (departamento, persona, sede, n)
COHORTS = [
    ('operations_support', 'shift_ops', 'SP', 30), ('operations_support', 'shift_ops', 'MAO', 15),
    ('operations_support', 'day_admin', 'MAO', 25),
    ('sales', 'sales_traveler', 'SP', 45),
    ('engineering_product', 'hybrid_eng', 'SP', 30), ('engineering_product', 'day_admin', 'SP', 10),
    ('admin_finance', 'day_admin', 'SP', 35),
    ('it_infra', 'it_privileged', 'SP', 25),
    ('hr', 'day_admin', 'SP', 15), ('legal', 'day_admin', 'SP', 10), ('board', 'management', 'SP', 10),
]
TZ = {'SP': -3, 'MAO': -4}
# faixa de eventos por dia útil (D-38) e horário de referência
PERSONAS = {
    'day_admin':      dict(lo=20, hi=35, start=8.5, span=9.0),
    'shift_ops':      dict(lo=25, hi=40, start=6.0, span=8.0),
    'it_privileged':  dict(lo=45, hi=70, start=9.0, span=9.0),
    'sales_traveler': dict(lo=20, hi=35, start=8.5, span=9.0),
    'hybrid_eng':     dict(lo=30, hi=50, start=9.5, span=8.5),
    'management':     dict(lo=15, hi=30, start=8.5, span=9.5),
}
# ASSUNÇÃO (P15): mistura FILE_ACCESS, FILE_DOWNLOAD, WEB_BROWSING, EXTERNAL_DEVICE, SYSTEM_CONFIG
MIX = {
    'day_admin':      [.64, .09, .255, .005, .010],
    'shift_ops':      [.66, .06, .265, .003, .012],
    'it_privileged':  [.60, .05, .22, .015, .115],
    'sales_traveler': [.58, .10, .30, .006, .014],
    'hybrid_eng':     [.62, .12, .21, .015, .035],
    'management':     [.55, .08, .34, .005, .020],
}
RESIDUAL_P = {'weekend': .03, 'holiday': .03, 'vacation': .02}     # D-27: nunca zero absoluto
RESIDUAL_P_MGMT = .12

# D-39: sistemas -> (nome, sigilo, n_recursos, departamentos | None = todos)
SYSTEMS = {
    'portal':      ('portal_interno', 'public', 3, None),
    'mail':        ('email_agenda', 'internal', 1, None),
    'crm':         ('crm_atendimento', 'internal', 20, {'operations_support', 'sales'}),
    'repo':        ('repositorio_codigo', 'internal', 40, {'engineering_product', 'it_infra'}),
    'fs_conf_fin': ('arquivos_financeiro', 'confidential', 80, {'admin_finance', 'legal', 'board'}),
    'fs_conf_leg': ('arquivos_juridico', 'confidential', 60, {'admin_finance', 'legal', 'board'}),
    'erp':         ('erp_financeiro', 'confidential', 15, {'admin_finance', 'board'}),
    'contracts':   ('contratos_juridicos', 'confidential', 40, {'legal', 'board'}),
    'payroll':     ('folha_pagamento', 'restricted', 6, 'hr5+board'),
    'dossier':     ('dossie_pessoal', 'restricted', 30, {'hr'}),
    'console':     ('console_infra', 'restricted', 12, {'it_infra'}),
}
FS_OWN_N = 60          # arquivos por pasta de departamento (internal)

# D-41
MFA0_BASE, MFA0_PRIV = .85, 1.0
PATCH_MEDIAN = {'it_infra': 3, 'sales': 25, 'default': 12}
CORP_PHONE_FRAC, PERSONAL_PHONE_N = .60, 25

# D-24: primeiros 3 meses = baseline; cenários só depois (janela de avaliação).
# 90 e o numero de dias dos tres primeiros meses a partir de 2026-01-01
# (31+28+31), entao o indice 90 e 1 de abril. O valor anterior era 100, que
# punha o inicio da avaliacao em 11 de abril -- dez dias dentro da janela que a
# D-24 reserva ao baseline. A checagem `baseline cobre exatamente 3 meses`
# confere isto contra a data de inicio, e nao contra esta constante.
EVAL_START_DAY = 90
