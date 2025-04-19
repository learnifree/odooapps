from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _

class Resident(models.Model):
    _name = 'bmis.resident'
    _description = 'Barangay Resident'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'resident_seq desc'

    # Add sequence field
    resident_seq = fields.Char(string='Resident ID', required=True, 
                             readonly=True, default=lambda self: _('New'))

    # Personal Information
    name = fields.Char(string='Full Name', required=True, tracking=True, store=True)
    first_name = fields.Char(string='First Name', required=True)
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name', required=True)
    suffix = fields.Char(string='Suffix')
    birth_date = fields.Date(string='Birth Date', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', required=True)
    civil_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('Annulled', 'Annulled'),
        ('separated', 'Separated')
    ], string='Civil Status', required=True)

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            names = self.name.split()
            if len(names) >= 2:
                self.first_name = names[0]
                self.last_name = names[-1]
                if len(names) > 2:
                    self.middle_name = ' '.join(names[1:-1])
                else:
                    self.middle_name = False
            self.suffix = False

    @api.onchange('first_name', 'middle_name', 'last_name', 'suffix')
    def _onchange_name_fields(self):
        if not self._context.get('skip_name_update'):
            names = [name for name in [self.first_name, self.middle_name, self.last_name, self.suffix] if name]
            self.with_context(skip_name_update=True).name = ' '.join(names)

    # Contact Information
    mobile = fields.Char(string='Mobile Number')
    email = fields.Char(string='Email')
    telephone = fields.Char(string='Telephone')

    # Address Information
    address = fields.Char(string='Address', required=True, tracking=True)
    street = fields.Char(string='Street')
    barangay = fields.Char(string='Barangay')
    city = fields.Char(string='City')
    province = fields.Char(string='Province')
    postal_code = fields.Char(string='Postal Code')

    # Additional Personal Information
    birth_place = fields.Char(string='Place of Birth')
    nationality = fields.Char(string='Nationality', default='Filipino')
    religion = fields.Char(string='Religion')
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ], string='Blood Type')

    # Educational and Professional Information
    educational_attainment = fields.Selection([
        ('none', 'None'),
        ('elementary', 'Elementary'),
        ('high_school', 'High School'),
        ('vocational', 'Vocational'),
        ('college', 'College'),
        ('post_graduate', 'Post Graduate')
    ], string='Educational Attainment')
    occupation = fields.Char(string='Occupation')
    monthly_income = fields.Float(string='Monthly Income')
    skills = fields.Text(string='Skills')

    # Residency Information
    resident_type = fields.Selection([
        ('permanent', 'Permanent'),
        ('temporary', 'Temporary'),
        ('transient', 'Transient')
    ], string='Resident Type', required=True, default='permanent')
    years_of_residency = fields.Integer(string='Years of Residency')
    is_voter = fields.Boolean(string='Registered Voter')
    is_head_of_family = fields.Boolean(string='Head of Family')

    # Family Information
    father_name = fields.Char(string="Father's Name")
    mother_name = fields.Char(string="Mother's Name")
    spouse_name = fields.Char(string="Spouse's Name")
    number_of_children = fields.Integer(string='Number of Children')
    family_member_ids = fields.One2many('bmis.family.member', 'resident_id', string='Family Members')

    # System Fields
    active = fields.Boolean(default=True)
    registration_date = fields.Date(string='Registration Date', default=fields.Date.today)
    image = fields.Binary(string='Photo')

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                record.age = relativedelta(date.today(), record.birth_date).years
            else:
                record.age = 0

    # Add create override for sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('resident_seq', _('New')) == _('New'):
                vals['resident_seq'] = self.env['ir.sequence'].next_by_code('bmis.resident') or _('New')
        return super(Resident, self).create(vals_list)

class FamilyMember(models.Model):
    _name = 'bmis.family.member'
    _description = 'Family Member'

    resident_id = fields.Many2one('bmis.resident', string='Resident', required=True)
    name = fields.Char(string='Name', required=True)
    relationship = fields.Selection([
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('sibling', 'Sibling'),
        ('grandparent', 'Grandparent'),
        ('other', 'Other')
    ], string='Relationship', required=True)
    birth_date = fields.Date(string='Birth Date')
    occupation = fields.Char(string='Occupation')
    remarks = fields.Text(string='Remarks')
