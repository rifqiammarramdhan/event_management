{
    'name':'Event Visitor Management',
    'version': '1.0',
    'category': 'Service',
    'summary' : 'Aplikasi Management Event',
    'description' : """Aplikasi Untuk me manage pengunjung atau tamu pada sebuah event""",
    'website' : '',
    'author' : 'Rifqi Ammar Ramadhan',
    'depends' : ['base','web','mail','website'],
    'data' : [
        'security/ir.model.access.csv',
        'views/event_management_view.xml',
        'views/event_management_action.xml',
        'views/event_management_menu.xml',
        'views/website/web_form_register_visitor_template.xml',
        # 'views/website/web_form_register_visitor_template.xml'
        # 'templates/email_register_template.xml',
        # 'views/sales_sequence.xml',
        # 'reports/kedai_kopi_report_pdf.xml',
    ],
    'installable' : True,
    'auto_install': False,
    'license' : 'OEEL-1',
}