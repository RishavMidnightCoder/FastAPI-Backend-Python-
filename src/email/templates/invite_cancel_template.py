def invite_cancel_email(invitee_email: str):
    subject = "Your Nivora invitation was cancelled"

    html = f"""\
<div style="background:#f4f6fb;padding:40px 16px;font-family:Arial,Helvetica,sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:10px;overflow:hidden;box-shadow:0 15px 35px rgba(23,34,56,0.08);">
    <tr>
      <td style="padding:22px 26px;border-bottom:1px solid #edf0f5;">
        <table role="presentation" cellpadding="0" cellspacing="0">
          <tr>
            <td style="width:30px;height:30px;border-radius:8px;background:#5d4de8;color:#ffffff;text-align:center;vertical-align:middle;font-weight:800;font-size:14px;">N</td>
            <td style="padding-left:9px;">
              <div style="font-size:13px;font-weight:700;color:#172238;">Nivora</div>
              <div style="font-size:9px;color:#8a95a6;">Move the work forward</div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td style="padding:40px 36px;">
        <p style="margin:0 0 16px;color:#7d72e9;letter-spacing:1.5px;font-size:9px;font-weight:800;">NIVORA WORKSPACE</p>
        <h2 style="margin:0;font-size:28px;font-weight:500;letter-spacing:-0.04em;color:#172238;">Invitation cancelled.</h2>
        <p style="margin:14px 0 0;color:#657288;font-size:13px;line-height:1.7;">
          The invitation to join the <strong>Nivora</strong> workspace has been cancelled by an administrator.
        </p>

        <div style="margin-top:24px;padding:14px;border:1px solid #f2d9dc;border-radius:8px;background:#fff6f7;color:#b85a66;font-size:11px;line-height:1.5;">
          This invitation link has been revoked and can no longer be used.
        </div>

        <p style="margin:22px 0 0;color:#8a95a6;font-size:10px;line-height:1.6;">
          If you believe this was a mistake, contact your workspace administrator for a new invitation.
        </p>
      </td>
    </tr>
    <tr>
      <td style="padding:16px 26px;border-top:1px solid #edf0f5;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="color:#9aa4b3;font-size:9px;">Subject: {subject}</td>
            <td style="color:#9aa4b3;font-size:9px;text-align:right;">&copy; 2026 Nivora</td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</div>
"""

    text = """The invitation to join the Nivora workspace has been cancelled by an administrator.

This invitation link has been revoked and can no longer be used.

If you believe this was a mistake, contact your workspace administrator for a new invitation.
"""

    return subject, html, text