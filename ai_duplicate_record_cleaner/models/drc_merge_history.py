# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class DrcMergeHistory(models.Model):
    _name = 'drc.merge.history'
    _description = 'Merge History'
    _inherit = ['mail.thread']
    _order = 'merge_date desc'

    name = fields.Char(
        string='Merge Name',
        required=True,
        tracking=True,
    )
    model_name = fields.Char(
        string='Target Model',
        required=True,
    )
    master_record_id = fields.Integer(
        string='Master Record ID',
        help='ID of the record that was kept as the master.',
    )
    merged_record_ids = fields.Text(
        string='Merged Record IDs',
        help='Comma-separated list of record IDs that were merged into the master.',
    )
    merged_by = fields.Many2one(
        comodel_name='res.users',
        string='Merged By',
        default=lambda self: self.env.user,
        readonly=True,
    )
    merge_date = fields.Datetime(
        string='Merge Date',
        default=fields.Datetime.now,
        readonly=True,
    )
    fields_merged = fields.Text(
        string='Fields Merged',
        help='Comma-separated list of fields that were combined during the merge.',
    )
