from odoo import api, fields, models, _
import base64


class SendEmailAttachment(models.Model):
    _name = 'send.email.attachment'
    _description = 'Simple Send Email with IR Attachment.'

    @api.multi
    def send(self):
        self.ensure_one()
        rec = self
        mail_tmpl_id = self.env.ref('Send_Email_Attachment.mail_template')
        attachment_id = False
        report_action = self.env.ref('Send_Email_Attachment.action_report_attachment')

        if report_action:
            # Use render_qweb_pdf to render xml template to pdf.
            attachment = report_action.render_qweb_pdf([rec.account_payment_id.id])[0]
            attachment_id = self.env['ir.attachment'].sudo().create({
                'name': 'Send Email With Attachment',
                'datas_fname': 'Attachment Document.pdf',
                'res_model': 'send.email.attachment',
                'res_id': rec.id,
                'type': 'binary',
                'datas': base64.b64encode(attachment),
            })
        values = mail_tmpl_id.generate_email(rec.id, fields=None)
        if attachment_id.id:  # Attachment Record
            attachment_ids = [(4, attachment_id.id)]
            values['attachment_ids'] = attachment_ids
        if rec.partner_id:  # Receiver Partners
            recipient_ids = [(4, rec.account_payment_id.partner_id.id)]
            values['recipient_ids'] = recipient_ids
        try:
            self.env['mail.mail'].create(values)
            self.env['mail.mail'].process_email_queue()
            return True
        except Exception as e:
            return False
