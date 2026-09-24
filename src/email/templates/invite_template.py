def invite_email(inviter_name: str, invitee_email: str, role_name: str, invite_link: str):
    subject = f"{inviter_name} invited you to join Nivora"

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
        <h2 style="margin:0;font-size:28px;font-weight:500;letter-spacing:-0.04em;color:#172238;">You&#39;re invited to Nivora.</h2>
        <p style="margin:14px 0 0;color:#657288;font-size:13px;line-height:1.7;">
          <strong>{inviter_name}</strong> invited you to join the <strong>Nivora</strong> workspace as a <strong>{role_name}</strong>.
        </p>

        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:24px;background:#f7f8fb;border-radius:8px;">
          <tr>
            <td style="padding:15px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="4">
                <tr>
                  <td style="color:#8a95a6;font-size:10px;padding-bottom:6px;">Workspace</td>
                  <td style="color:#172238;font-size:11px;font-weight:700;padding-bottom:6px;">Nivora</td>
                </tr>
                <tr>
                  <td style="color:#8a95a6;font-size:10px;padding-bottom:6px;">Invited by</td>
                  <td style="color:#172238;font-size:11px;font-weight:700;padding-bottom:6px;">{inviter_name}</td>
                </tr>
                <tr>
                  <td style="color:#8a95a6;font-size:10px;">Role</td>
                  <td style="color:#172238;font-size:11px;font-weight:700;">{role_name}</td>
                </tr>
              </table>
            </td>
          </tr>
        </table>

        <div style="margin-top:27px;">
          <a href="{invite_link}" style="display:inline-block;background:#5d4de8;color:#ffffff;text-decoration:none;font-size:11px;font-weight:800;padding:13px 18px;border-radius:7px;">Accept invitation &rarr;</a>
        </div>

        <p style="margin:22px 0 0;color:#8a95a6;font-size:10px;line-height:1.6;">
          Accept this invitation and create your password to get started. This link expires in 7 days.
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

    text = f"""{inviter_name} invited you to join the Nivora workspace as a {role_name}.

Accept your invitation here: {invite_link}

This link expires in 7 days.

If you did not expect this invitation, you can ignore this email.
"""

    return subject, html, text