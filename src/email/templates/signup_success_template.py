def signup_success_email(full_name: str, email: str):
    subject = f"Welcome to Nivora, {full_name}"

    html = f"""
    <div style="font-family: 'DM Sans', Arial, sans-serif; max-width: 480px; margin: 0 auto; background: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 15px 35px rgba(23,34,56,0.08);">
      <div style="display: flex; align-items: center; gap: 9px; padding: 22px 26px; border-bottom: 1px solid #edf0f5;">
        <table cellpadding="0" cellspacing="0"><tr>
          <td style="width: 30px; height: 30px; border-radius: 8px; background: #5d4de8; color: #fff; text-align: center; vertical-align: middle; font-weight: 800; font-size: 14px;">N</td>
          <td style="padding-left: 10px;">
            <div style="font-size: 13px; font-weight: 700; color: #172238;">Nivora</div>
            <div style="font-size: 9px; color: #8a95a6;">Move the work forward</div>
          </td>
        </tr></table>
      </div>
      <div style="padding: 40px 32px;">
        <p style="margin: 0 0 16px; color: #7d72e9; letter-spacing: 0.12em; font-size: 9px; font-weight: 800;">NIVORA WORKSPACE</p>
        <div style="display: grid; width: 44px; height: 44px; margin-bottom: 18px; place-items: center; border-radius: 50%; background: #e7f7ef; color: #299661; text-align: center; line-height: 44px; font-size: 20px;">&#10003;</div>
        <h2 style="margin: 0; font-family: Georgia, serif; font-size: 28px; font-weight: 500; letter-spacing: -0.02em; color: #172238;">Welcome to Nivora.</h2>
        <p style="margin: 14px 0 0; color: #657288; font-size: 13px; line-height: 1.7;">Your account is ready. Start organizing projects, assigning work, and moving your team forward.</p>
        <table cellpadding="0" cellspacing="0" style="width: 100%; margin-top: 24px; padding: 15px; border-radius: 8px; background: #f7f8fb;">
          <tr><td style="color: #8a95a6; font-size: 10px; padding: 4px 0;">Account</td><td style="font-size: 11px; font-weight: 700; padding: 4px 0;">{email}</td></tr>
          <tr><td style="color: #8a95a6; font-size: 10px; padding: 4px 0;">Workspace</td><td style="font-size: 11px; font-weight: 700; padding: 4px 0;">Nivora</td></tr>
          <tr><td style="color: #8a95a6; font-size: 10px; padding: 4px 0;">Status</td><td style="font-size: 11px; font-weight: 700; color: #299661; padding: 4px 0;">Verified and active</td></tr>
        </table>
        <p style="margin: 22px 0 0; color: #8a95a6; font-size: 10px; line-height: 1.6;">You received this email because a Nivora account was created with this address. If this was not you, contact your workspace administrator.</p>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 16px 26px; border-top: 1px solid #edf0f5; color: #9aa4b3; font-size: 9px;">
        <span>Subject: {subject}</span><span>© 2026 Nivora</span>
      </div>
    </div>
    """

    text = (
        f"Welcome to Nivora.\n\n"
        f"Your account is ready. Start organizing projects, assigning work, and moving your team forward.\n\n"
        f"Account: {email}\nWorkspace: Nivora\nStatus: Verified and active"
    )
    return subject, html, text