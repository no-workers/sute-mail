from sutemail.client import (
    MailClient,
    check_driver
)



if __name__ == "__main__":
    driver = check_driver()
    cl = MailClient(driver_path=driver)
    # print(cl.issue_new_random_mail())
    if (mails := cl.fetch_mails()):
        print(mails)
        for mailkey, mailnum in mails.items():
            print(cl.get_mail(mailkey, mailnum))
