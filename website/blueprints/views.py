from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from website.models import *
from datetime import datetime, date
from website import db
from sqlalchemy import func

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():

    # total balance
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    total_balance = []
    for account in accounts:
        balance = account.balance
        total_balance.append(balance)

    total_balance = sum(total_balance)

    from_date = datetime(year=datetime.now().year,
                         month=datetime.now().month, day=1)

    # income monthly
    income_transactions = Transaction.query.filter_by(user_id=current_user.id).filter(Transaction.date >= from_date).filter(
        Transaction.date <= func.now()).filter(Transaction.transaction_type == 'in').all()
    total_income_transactions = []
    for income_transaction in income_transactions:
        value = income_transaction.value
        total_income_transactions.append(value)

    total_income_transactions = sum(total_income_transactions)

    # expenses monthly
    expense_transactions = Transaction.query.filter_by(user_id=current_user.id).filter(Transaction.date >= from_date).filter(
        Transaction.date <= func.now()).filter(Transaction.transaction_type == 'ex').all()
    total_expense_transactions = []
    for expense_transaction in expense_transactions:
        value = expense_transaction.value
        total_expense_transactions.append(value)

    total_expense_transactions = sum(total_expense_transactions)

    # month balance
    month_balance = total_income_transactions - total_expense_transactions

    # top 5 accounts
    top_accounts = Account.query.filter_by(
        user_id=current_user.id).order_by(Account.balance.desc()).all()[0:5]

    return render_template(
        'views/dashboard.html',
        user=current_user,
        total_balance=total_balance,
        month_balance=month_balance,
        total_income_transactions=total_income_transactions,
        total_expense_transactions=total_expense_transactions,
        top_accounts=top_accounts
    )


@views.route('/profile')
@login_required
def profile():
    return render_template('views/profile.html', user=current_user)


@views.route('/accounts')
@login_required
def accounts():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    return render_template('views/accounts.html', user=current_user, accounts=accounts)


@views.route('/account/<int:id>')
@login_required
def account(id):
    account = Account.query.filter_by(user_id=current_user.id, id=id).first()
    return render_template('views/account.html', user=current_user, account=account)


@views.route('/add/account', methods=['GET', 'POST'])
@login_required
def add_account():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        balance = request.form.get('balance')

        if len(name) < 2:
            flash('Name must be at least 3 characters long.', category='add_error')
        else:
            new_account = Account(
                name=name, description=description, balance=balance, user_id=current_user.id)
            db.session.add(new_account)
            db.session.commit()
            return redirect(url_for('views.accounts'))

    return render_template('views/add-account.html', user=current_user)


@views.route('/transactions')
@login_required
def transactions():
    transactions = Transaction.query.filter_by(
        user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('views/transactions.html', user=current_user, transactions=transactions)


@views.route('/add/transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():

    income_categories = Category.query.filter_by(
        user_id=current_user.id, transaction='in').all()
    expense_categories = Category.query.filter_by(
        user_id=current_user.id, transaction='ex').all()
    transfer_categories = Category.query.filter_by(
        user_id=current_user.id, transaction='tr').all()
    accounts = Account.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        transaction_type = request.form.get('transaction_type')
        category = request.form.get('category')
        account = request.form.get('account')
        value = request.form.get('value')

        account_filter = Account.query.filter_by(id=int(account)).first()
        category_filter = Category.query.filter_by(id=int(category)).first()

        new_transaction = Transaction(category_id=category_filter.id, user_id=current_user.id,
                                      account_id=account_filter.id, transaction_type=transaction_type, value=value)

        if transaction_type == 'in':
            account_filter.balance += int(value)
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('views.transactions'))
        elif transaction_type == 'ex':
            account_filter.balance -= int(value)
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('views.transactions'))
        else:
            from_account = account_filter
            to_account = request.form.get('to_account')
            fee = request.form.get('fee')
            to_account_filter = Account.query.filter_by(
                id=int(to_account)).first()
            from_account.balance -= int(int(value)+int(fee))
            to_account_filter.balance += int(value)
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('views.transactions'))

    return render_template('views/add-transaction.html', user=current_user, income_categories=income_categories, expense_categories=expense_categories, transfer_categories=transfer_categories, accounts=accounts)


@views.route('/delete/transaction/<int:id>')
@login_required
def delete_transaction(id):
    transaction = Transaction.query.filter_by(id=id).first()
    if transaction.user_id != current_user.id:
        flash('You are not allowed to delete this transaction', category='error')
        return redirect(url_for('views.transactions'))
    else:
        if transaction.transaction_type == 'in':
            transaction.account.balance -= int(transaction.value)
            db.session.delete(transaction)
            db.session.commit()
            return redirect(url_for('views.transactions'))
        else:
            transaction.account.balance += int(transaction.value)
            db.session.delete(transaction)
            db.session.commit()
            return redirect(url_for('views.transactions'))


@views.route('/categories')
@login_required
def categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('views/categories.html', user=current_user, categories=categories)


@views.route('/add/category', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        transaction = request.form.get('transaction')

        category = Category.query.filter_by(
            name=name, user_id=current_user.id, transaction=transaction).first()

        if category:
            flash('Category already exists', category='error')
        else:
            new_category = Category(
                name=name, user_id=current_user.id, transaction=transaction)
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for('views.categories'))
    return render_template('views/add-category.html', user=current_user)


@views.route('/delete/account/<int:id>')
@login_required
def delete_account(id):
    account = Account.query.filter_by(id=id).first()
    if account.user_id != current_user.id:
        flash('You are not allowed to delete this account', category='error')
        return redirect(url_for('views.accounts'))
    else:
        db.session.delete(account)
        db.session.commit()
        return redirect(url_for('views.accounts'))
