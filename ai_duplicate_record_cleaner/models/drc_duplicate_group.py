# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class DrcDuplicateGroup(models.Model):
    _name = 'drc.duplicate.group'
    _description = 'Duplicate Group'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'group_score desc'

    name = fields.Char(
        string='Group Name',
        required=True,
        tracking=True,
    )
    model_name = fields.Char(
        string='Target Model',
        required=True,
    )
    record_ids = fields.Text(
        string='Record IDs',
        help='Comma-separated list of record IDs that belong to this duplicate group.',
    )
    group_score = fields.Float(
        string='Group Score',
        default=0.0,
        help='Overall similarity score for the group (0–100).',
    )
    ai_confidence = fields.Float(
        string='AI Confidence (%)',
        default=0.0,
        help='AI confidence level that these records are true duplicates.',
    )
    merge_state = fields.Selection(
        selection=[
            ('pending', 'Pending'),
            ('merged', 'Merged'),
            ('ignored', 'Ignored'),
        ],
        string='Merge State',
        default='pending',
        required=True,
        tracking=True,
    )
    suggested_master = fields.Integer(
        string='Suggested Master Record ID',
        help='ID of the record recommended as the master to merge others into.',
    )
    record_count = fields.Integer(
        string='Record Count',
        default=0,
        compute='_compute_record_count',
        store=True,
    )
    scan_job_id = fields.Many2one(
        comodel_name='drc.scan.job',
        string='Scan Job',
        ondelete='cascade',
    )

    @api.depends('record_ids')
    def _compute_record_count(self):
        for group in self:
            if group.record_ids:
                ids = [rid.strip() for rid in group.record_ids.split(',') if rid.strip()]
                group.record_count = len(ids)
            else:
                group.record_count = 0

    def action_merge_group(self):
        """Mark the group as merged and log to merge history."""
        for group in self:
            if group.merge_state == 'merged':
                continue
            group.merge_state = 'merged'
            # Create merge history entry
            self.env['drc.merge.history'].create({
                'name': _('Merge of %s') % group.name,
                'model_name': group.model_name,
                'master_record_id': group.suggested_master,
                'merged_record_ids': group.record_ids,
                'fields_merged': group.scan_job_id.match_fields or '',
            })
            _logger.info('Merged duplicate group: %s', group.name)
        return True

    def action_ignore_group(self):
        """Mark the group as ignored."""
        for group in self:
            group.merge_state = 'ignored'
        return True
