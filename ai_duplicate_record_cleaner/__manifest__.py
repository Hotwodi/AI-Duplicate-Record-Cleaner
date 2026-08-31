# -*- coding: utf-8 -*-
{
    'name': 'AI Duplicate Record Cleaner',
    'version': '18.0.1.0.0',
    'summary': 'Detect, group, and merge duplicate records using AI-powered fuzzy matching.',
    'description': """
AI Duplicate Record Cleaner
===========================
Detect, group, and merge duplicate records across any Odoo model using
AI-powered fuzzy matching, phonetic comparison, and composite rule engines.

Features:
- Create scan jobs for any model with configurable match fields
- Fuzzy matching with adjustable similarity thresholds
- Automatic duplicate grouping with AI confidence scores
- Suggested master record selection
- One-click merge with full history logging
- Customizable matching rules (exact, fuzzy, phonetic, composite)
- Field-weighted composite matching
""",
    'author': 'SoftaiDev',
    'website': 'https://softaidev.pages.dev',
    'category': 'Productivity/AI',
    'license': 'LGPL-3',
    'price': 39.99,
    'currency': 'USD',
    'application': True,
    'installable': True,
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/drc_scan_job_views.xml',
        'views/drc_duplicate_group_views.xml',
        'views/drc_merge_history_views.xml',
        'views/drc_matching_rule_views.xml',
        'views/drc_menu.xml',
    ],
}
