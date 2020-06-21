from sutemail.client import (
    MailClient,
    check_driver
)



if __name__ == "__main__":
    driver = check_driver()
    cl = MailClient(driver_path=driver)
    if (mails := cl.fetch_mails()):
        for mailkey, mailnum in mails.items():
            print(cl.get_mail(mailkey, mailnum))
