from accounting.models import Account, Document, Record


#TODO: check function input
def create_account(serial):
    """
    Creates an account
    INPUT:
        serial: the serial number of the account
    OUTPUT:
        id: id of the created account
    """
    acc = Account.objects.create(serial=serial, credit=0)
    acc.save()
    return acc.id


#TODO: check for account amounts before moving
#TODO: check if given accounts exist
def move_credit(from_id, to_id, amount, desc, from_desc, to_desc, time, resource_id):
    """
    Moves credit from an account to another account
    INPUT:
        from_id: id of source account
        to_id: id of target account
        amount: how much credit is going to be moved
        desc: description of the whole process
        from_desc: description for the source account
        to_desc: description for the target account
        time: date and time of the process
        resource_id: a resource id so you can lookup another table for this process
    """
    doc = Document.objects.create(time=time, description=desc, resource_id=resource_id)
    doc.save()
    from_acc = Account.objects.get(id=from_id)
    to_acc = Account.objects.get(id=to_id)
    from_record = Record.objects.create(
        account=from_acc,
        document=doc,
        credit=-amount,
        previous_credit=from_acc.credit,
        next_credit=from_acc.credit-amount,
        description=from_desc
    )
    from_acc.credit -= amount
    from_acc.save()
    from_record.save()
    to_record = Record.objects.create(
        account=to_acc,
        document=doc,
        credit=amount,
        previous_credit=to_acc.credit,
        next_credit=to_acc.credit+amount,
        description=to_desc
    )
    to_acc.credit += amount
    to_acc.save()
    to_record.save()


#TODO: check if account exist
def get_credit(acc_id):
    """
    retrieves the credit of given account
    INPUT:
        acc_id: id of the account
    OUTPUT:
        credit: account's credit
    """
    acc = Account.objects.get(id=acc_id)
    return acc.credit

static_accounts = {}


def initialize_static_accounts():
    static_accounts['office'] = create_account(0)


def get_static_account(name):
    return static_accounts[map]