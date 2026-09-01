# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class DrcScanJob(models.Model):
    _name = 'drc.scan.job'
    _description = 'Duplicate Scan Job'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'created_date desc'

    name = fields.Char(
        string='Scan Job Name',
        required=True,
        tracking=True,
    )
    model_name = fields.Char(
        string='Target Model',
        required=True,
        help='Technical name of the model to scan for duplicates (e.g. res.partner).',
    )
    scan_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('running', 'Running'),
            ('done', 'Done'),
        ],
        string='State',
        default='draft',
        required=True,
        tracking=True,
    )
    match_fields = fields.Text(
        string='Match Fields',
        help='Comma-separated list of field names used for duplicate detection.',
    )
    fuzzy_matching = fields.Boolean(
        string='Fuzzy Matching',
        default=True,
        help='When enabled, uses fuzzy string comparison instead of exact matching only.',
    )
    similarity_threshold = fields.Float(
        string='Similarity Threshold (%)',
        default=80.0,
        help='Minimum similarity percentage for two records to be considered duplicates.',
    )
    duplicates_found = fields.Integer(
        string='Duplicates Found',
        default=0,
        readonly=True,
    )
    records_scanned = fields.Integer(
        string='Records Scanned',
        default=0,
        readonly=True,
    )
    created_by = fields.Many2one(
        comodel_name='res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
    )
    created_date = fields.Datetime(
        string='Created Date',
        default=fields.Datetime.now,
        readonly=True,
    )
    duplicate_group_ids = fields.One2many(
        comodel_name='drc.duplicate.group',
        inverse_name='scan_job_id',
        string='Duplicate Groups',
    )
    matching_rule_id = fields.Many2one(
        comodel_name='drc.matching.rule',
        string='Matching Rule',
        help='Optional matching rule to use for this scan job.',
    )

    def action_start_scan(self):
        """Start the duplicate scan process."""
        for job in self:
            if not job.match_fields and not job.matching_rule_id:
                raise UserError(_('Please define match fields or select a matching rule before scanning.'))
            job.scan_state = 'running'
            job.records_scanned = 0
            job.duplicates_found = 0
            _logger.info('Starting duplicate scan job: %s on model: %s', job.name, job.model_name)
            # Placeholder for actual scan logic — would iterate records and build groups
            job.scan_state = 'done'
        return True

    def action_reset_scan(self):
        """Reset the scan job to draft state."""
        for job in self:
            job.scan_state = 'draft'
            job.duplicates_found = 0
            job.records_scanned = 0
        return True
