def otp_email(otp: str, expire_minutes: int):
    subject = f"Your Nivora verification code is {otp}"

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
        <h2 style="margin: 0; font-family: Georgia, serif; font-size: 28px; font-weight: 500; letter-spacing: -0.02em; color: #172238;">Verify your email.</h2>
        <p style="margin: 14px 0 0; color: #657288; font-size: 13px; line-height: 1.7;">Use the verification code below to continue signing in to your Nivora workspace.</p>
        <div style="margin: 24px 0 4px; padding: 16px; border: 1px dashed #c9c5fa; border-radius: 8px; background: #f4f3ff; color: #5d4de8; font-size: 28px; font-weight: 800; letter-spacing: 0.22em; text-align: center;">{otp}</div>
        <p style="margin: 22px 0 0; color: #8a95a6; font-size: 10px; line-height: 1.6;">This code expires in {expire_minutes} minutes. If you did not request this code, you can safely ignore this email.</p>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 16px 26px; border-top: 1px solid #edf0f5; color: #9aa4b3; font-size: 9px;">
        <span>Subject: {subject}</span><span>© 2026 Nivora</span>
      </div>
    </div>
    """

    text = (
        f"Verify your email.\n\n"
        f"Your Nivora verification code is: {otp}\n"
        f"This code expires in {expire_minutes} minutes.\n\n"
        f"If you did not request this code, you can safely ignore this email."
    )
    return subject, html, text