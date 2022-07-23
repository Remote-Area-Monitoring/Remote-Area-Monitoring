from source.util.settings import Settings


class User:
    def __init__(self):
        self.config = Settings('secret.config')

    def add_user_email(self, new_email: str):
        emails = self.config.get_list_setting('notify', 'emails')
        if new_email.lower() in emails:
            return False
        emails.append(new_email.lower())
        self.config.set_setting('notify', 'emails', self.__list_to_string(emails))
        return True

    def remove_user_email(self, email_to_remove: str):
        emails = self.config.get_list_setting('notify', 'emails')
        print(emails)
        if email_to_remove.lower() not in emails:
            return False
        emails = [email for email in emails if email != email_to_remove.lower()]
        self.config.set_setting('notify', 'emails', self.__list_to_string(emails))
        return True

    def __list_to_string(self, input_list):
        if len(input_list) < 1:
            return '[]'
        string = '['
        for item in input_list:
            if item == input_list[-1]:
                item_string = '\"'
                item_string += str(item)
                item_string += '\"'
                string += item_string
                break
            item_string = '\"'
            item_string += str(item)
            item_string += '\", '
            string += item_string
        string += ']'
        return string


def main():
    user = User()
    # print(user.add_user_email('test@email.com'))
    print(user.remove_user_email('Test@email.com'))


if __name__ == '__main__':
    main()
