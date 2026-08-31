# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class DrcMatchingRule(models.Model):
    _name = 'drc.matching.rule'
    _description = 'Matching Rule'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(
        string='Rule Name',
        required=True,
        tracking=True,
    )
    model_name = fields.Char(
        string='Target Model',
        required=True,
        help='Technical name of the model this rule applies to.',
    )
    rule_type = fields.Selection(
        selection=[
            ('exact', 'Exact Match'),
            ('fuzzy', 'Fuzzy Match'),
            ('phonetic', 'Phonetic Match'),
            ('composite', 'Composite Match'),
        ],
        string='Rule Type',
        default='fuzzy',
        required=True,
        tracking=True,
    )
    field_weights = fields.Text(
        string='Field Weights',
        help='JSON mapping of field names to weight values, e.g. {"name": 0.5, "email": 0.3, "phone": 0.2}.',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    last_run = fields.Datetime(
        string='Last Run',
        readonly=True,
    )
    duplicates_detected = fields.Integer(
        string='Duplicates Detected',
        default=0,
        readonly=True,
    )

    def action_run_rule(self):
        """Execute the matching rule and update statistics."""
        for rule in self:
            rule.last_run = fields.Datetime.now()
            _logger.info('Running matching rule: %s on model: %s', rule.name, rule.model_name)
            # Placeholder for actual matching logic
        return True

    @api.constrains('rule_type', 'field_weights')
    def _check_field_weights(self):
        for rule in self:
            if rule.rule_type == 'composite' and not rule.field_weights:
                _logger.warning('Composite rule %s has no field weights defined.', rule.name)
