from sutemail.client import (
    MailClient,
    check_driver
)


if __name__ == "__main__":
    driver = check_driver()
    cl = MailClient(driver_path=driver)
    print(cl.get_mail_list())
    if (mails := cl.fetch_mails()):
        for mailkey, mailnum in mails.items():
            mail_dic = cl.get_mail(mailkey, mailnum)
            print(mail_dic)
            cl.delete_mail(mail_dic["id"])
